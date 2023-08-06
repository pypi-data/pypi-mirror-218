import asyncio
import logging

from cherre_types import get_env, File
from cherre_domain import get_project_id
from cherre_singer_ingest.value_items.run_singer_command import (
    RunSingerPythonTargetCommand,
    RunSingerPythonTapCommand,
)
from cherre_singer_ingest.services.run_command import run_tap_and_target


def run_custom_image_tap(
    tap_cmd: RunSingerPythonTapCommand,
    store_bookmarks: bool = True,
    pipeline_name: str = "",
    include_stream_name: bool = False,
):
    logging.basicConfig(level=get_env("LOGLEVEL", "INFO"))
    loop = asyncio.get_event_loop()

    loop.set_exception_handler(exception_handler)

    project_id = get_project_id()

    if not pipeline_name:
        pipeline_name = get_env("PIPELINE_NAME", "")

    dataset_name = get_env("DATASET_NAME", "")
    destination_dataset = f"{dataset_name}_raw" if dataset_name else "raw"

    target_cmd = RunSingerPythonTargetCommand(
        file=File("cherre_big_query_external_data_target.py"),
        config={
            "project_id": project_id,
            "store_bookmarks": store_bookmarks,
            "destination_dataset": destination_dataset,
            "include_stream_name": include_stream_name,
        },
    )

    loop.run_until_complete(
        run_tap_and_target(tap=tap_cmd, target=target_cmd, pipeline_name=pipeline_name)
    )
    loop.close()

    if len(errors) > 0:
        raise RuntimeError(f"Error in async task {','.join(str(e) for e in errors)}")
    print("Completed All Tasks")


errors = []


def exception_handler(self, context):
    logging.error(f"Exception Handler: {context}")
    errors.append(context)


def get_required_env(key: str) -> str:
    val = get_env(key)
    if not val:
        raise ValueError(f"Env variable {key} was not set")
    return val
