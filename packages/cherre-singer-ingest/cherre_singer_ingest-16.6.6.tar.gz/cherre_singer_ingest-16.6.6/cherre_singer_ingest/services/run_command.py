from typing import Iterable, Callable, Tuple, Optional
import logging
import subprocess
import random
import string
from datetime import datetime, timezone
import json
from os import path, makedirs
import os
import asyncio

from cherre_types import FolderPath, FilePath, File

from cherre_singer_ingest.value_items import (
    TapError,
    TargetError,
    TapOrTargetError,
    RunSingerCommand,
)
from cherre_singer_ingest.repositories import CloudSQLIngestStateRepository


def write_values_to_config_file(**kwargs) -> str:
    """
    Given a dictionary of values for a tap or target, turn it into a JSON file that can be passed
    to other processes
    :param kwargs:
    :return:
    """
    if "location" not in kwargs:
        raise ValueError("Must have a location parameter!")
    if not isinstance(kwargs["location"], FolderPath):
        raise ValueError("Location must be a FolderPath!")

    location = kwargs["location"]

    if not path.exists(str(location)):
        logging.debug(f"Creating config location at {str(location)}")
        makedirs(str(location))

    if "start_date" not in kwargs:
        kwargs["start_date"] = datetime(
            year=1917, month=11, day=11, tzinfo=timezone.utc
        ).isoformat()

    str_kwargs = {}
    for key in kwargs.keys():
        if not key == "location":
            str_kwargs[key] = str(kwargs[key])
    text = json.dumps(str_kwargs)

    file_name = random_word(16)
    # note we don't use file path here, that can mess with roots in Docker!
    file = f"{location}/{file_name}.json"

    logging.debug(f"Writing config values to {file}")
    with open(file, "w+") as file_obj:
        file_obj.write(text)

    return file


def random_word(length):
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(length))


def do_nothing_to_discover_results(
    tap_config: FilePath, discovery_output: FilePath
) -> FilePath:
    """
    Null operation to return the discovery output unchanged
    """
    return discovery_output


async def run_tap_and_target(
    tap: RunSingerCommand,
    target: RunSingerCommand,
    is_discover_sync: bool = False,
    discovery_filter_function: Callable[[FilePath, FilePath], FilePath] = None,
    pipeline_name: str = "",
    ingest_state_repository: CloudSQLIngestStateRepository = None,
):
    if discovery_filter_function and not is_discover_sync:
        raise ValueError(
            "Discovery filter function can only be called if is_discover_sync is true"
        )
    if not discovery_filter_function:
        discovery_filter_function = do_nothing_to_discover_results

    if not ingest_state_repository:
        ingest_state_repository = CloudSQLIngestStateRepository()

    location = tap.get_config_folder()
    tap.config["location"] = location
    tap_config = write_values_to_config_file(**tap.config)
    tap_cmd = f"{tap.cmd} --config {tap_config}"

    states = list(
        ingest_state_repository.get_latest_states(pipeline_name=pipeline_name)
    )
    if len(states) > 0:
        output_file = FilePath(path=location, file=File.parse("state.json"))
        ingest_state_repository.write_states_to_file(
            output_file=output_file, states=states
        )

        tap_cmd += f" --state {str(output_file)}"

    if is_discover_sync:
        property_json_file = f"{random_word(5)}_properties.json"

        # we have to run the discover
        discover_cmd = (
            f"{tap.cmd} --config {tap_config} --discover > {property_json_file}"
        )

        _run_cmd(discover_cmd)

        # let the override do its thing
        updated_property_file = discovery_filter_function(
            FilePath.parse(tap_config), FilePath.parse(property_json_file)
        )
        tap_cmd += f" --properties {updated_property_file}"

    target.config["location"] = target.get_config_folder()
    target_config = write_values_to_config_file(**target.config)
    target_cmd = f"{target.cmd} --config {target_config}"

    try:
        tap_return_code, target_return_code = await _run_tap_and_target(
            tap_cmd, target_cmd
        )
        if tap_return_code and tap_return_code != 0:
            raise TapError(f"Tap exited with a non zero code {tap_return_code}")
        if target_return_code and target_return_code != 0:
            raise TargetError(
                f"Target exited with a non zero code {target_return_code}"
            )
    except TapOrTargetError:
        raise
    except Exception as e:
        raise TapOrTargetError(str(e))


def _run_cmd(cmd: str) -> Iterable[str]:
    start = datetime.now()
    logging.debug(f"Starting command {cmd} at {start.isoformat()}")
    process = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)

    while process.poll() is None:
        if process and process.stderr:
            output = process.stderr.readline()
            for error in output.decode().strip().split("\n"):
                logging.info(error)
                yield error
        else:
            raise TapError("Unable to connect with subprocess")

    finish = datetime.now()
    logging.debug(f"Finished command {cmd} at {finish.isoformat()}")
    logging.info(
        f"Command {cmd} finished in {(finish - start).total_seconds()} seconds"
    )


async def _run_tap_and_target(tap_cmd: str, target_cmd: str) -> Tuple[int, int]:
    start = datetime.now()
    logging.info(f"Starting command {tap_cmd} and {target_cmd}")

    read, write = os.pipe()
    tap = await asyncio.subprocess.create_subprocess_shell(
        tap_cmd, stdout=write, stderr=asyncio.subprocess.PIPE
    )
    os.close(write)
    target = await asyncio.subprocess.create_subprocess_shell(
        target_cmd, stdin=read, stderr=asyncio.subprocess.PIPE
    )
    os.close(read)

    await asyncio.wait([_log_stderr_msg(tap.stderr), _log_stderr_msg(target.stderr)])
    tap_return_code = await tap.wait()
    target_return_code = await target.wait()

    finish = datetime.now()
    logging.debug(
        f"Finished command {tap_cmd} and {target_cmd} at {finish.isoformat()}"
    )
    logging.info(
        f"Command {tap_cmd} and {target_cmd} finished in {(finish - start).total_seconds()} seconds"
    )
    return tap_return_code, target_return_code


async def _log_stderr_msg(stream: Optional[asyncio.StreamReader]):
    if isinstance(stream, asyncio.StreamReader):
        while True:
            line = await stream.readline()
            if line:
                msg = line.decode().strip()
                if "level=CRITICAL" in msg:
                    logging.critical(msg)
                elif "level=ERROR" in msg:
                    logging.error(msg)
                elif "level=WARNING" in msg:
                    logging.warning(msg)
                elif "level=DEBUG" in msg:
                    logging.debug(msg)
                else:
                    logging.info(msg)
            else:
                break
