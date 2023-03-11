import os
import pathlib

from Path.Path_database import PATH_DATI


class Controller_path:
    @classmethod
    def genera_path(cls, path):
        if not os.path.isdir(PATH_DATI):
            os.makedirs(PATH_DATI, exist_ok=True)
        if not os.path.isdir(pathlib.Path(path).parent):
            os.makedirs(pathlib.Path(path).parent)
        if not os.path.isfile(path):
            open(path, "x").close()
