from abc import ABC, abstractmethod
from typing import Dict, Any
import pathlib

from cherre_types import File, FilePath, FolderPath


class RunSingerCommand(ABC):
    """
    Basic command object for running a singer tap or target with a config file
    """

    def __init__(self, cmd: str, config: Dict[str, Any]):
        self.cmd = cmd
        self.config = config

    @property
    def name(self):
        return self.cmd

    def get_config_folder(self) -> FolderPath:
        # determine if we're in a venv or not!
        path_here = pathlib.Path(__file__).parent.absolute()
        if ".venv" in str(path_here):
            return FolderPath("./services")

        # we're in container, go to the .temp directory!
        return FolderPath("/usr/src/app/ingest/ingest/services/", is_root=True)


class RunSingerPythonCommand(RunSingerCommand, ABC):
    """
    Command which takes a python file that we should run
    """

    def __init__(self, file: File, config: Dict[str, Any]):
        self.file = file
        tap_folder = self.get_scripts_folder()
        full_file = FilePath.from_file_in_folder(tap_folder, file)
        cmd = f"python {str(full_file)}"
        super().__init__(cmd, config)

    @staticmethod
    def _get_base_folder() -> FolderPath:
        # since this is a library, we need to get this relative to this file
        value_items_folder = pathlib.Path(__file__).parent.absolute()
        main_folder = value_items_folder.parent
        main_folder_path = FolderPath("/" + str(main_folder), is_root=True)
        return main_folder_path.add_sub_folder("services")

    @abstractmethod
    def get_scripts_folder(self):
        raise NotImplementedError()

    @property
    def name(self):
        return str(self.file)


class RunSingerPythonTapCommand(RunSingerPythonCommand):
    def get_scripts_folder(self) -> FolderPath:
        return super()._get_base_folder().add_sub_folder("taps")

    def get_config_folder(self) -> FolderPath:
        return super().get_config_folder().add_sub_folder("taps/configs")


class RunSingerPythonTargetCommand(RunSingerPythonCommand):
    def get_scripts_folder(self) -> FolderPath:
        return super()._get_base_folder().add_sub_folder("targets")

    def get_config_folder(self) -> FolderPath:
        return super().get_config_folder().add_sub_folder("targets/configs")


class RunSingerCustomImageTapCommand(RunSingerPythonTapCommand):
    """
    Represents a tap which exists in our standard project layout under bin/ingest
    Assumes our tap was written under bin/ingest/<project>/services/taps
    If the file is not specified, assumes the tap is in <project>_tap.py
    """

    def __init__(self, project_name: str, config: Dict[str, Any], file: File = None):
        if not project_name:
            raise ValueError("Project name is required!")
        self.project_name = project_name
        if not file:
            file = File(f"{self.project_name}_tap.py")
        super().__init__(file, config)

    def get_scripts_folder(self) -> FolderPath:
        return FolderPath(f"./{self.project_name}/services/taps")

    def get_config_folder(self) -> FolderPath:
        return self.get_scripts_folder().add_sub_folder("configs")
