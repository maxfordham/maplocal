import pathlib
import typing as ty
from maplocal.env import MapLocalEnv
from maplocal.maplocal import _remove_root, openlocal, maplocal
import os

MAPENV = MapLocalEnv()
PATH_TEST = pathlib.Path(__file__)
DIR_REPO = PATH_TEST.parents[1]

def get_wsl_distro_name():
    return (lambda: None if not "WSL_DISTRO_NAME" in os.environ else os.environ['WSL_DISTRO_NAME'])()

class TestMAPENV:
    def test_MAPENV(self):
        assert MAPENV.MAPLOCAL_FROM == pathlib.PurePosixPath("/home")
        assert MAPENV.MAPLOCAL_TO == pathlib.PureWindowsPath(f'//wsl.localhost/{get_wsl_distro_name()}/home')


class TestRemoveRoot:
    def test__remove_root(self):
        rootfound, newpath = _remove_root(PATH_TEST, DIR_REPO)
        assert rootfound == True
        assert newpath == pathlib.Path("tests/test_maplocal.py")


class TestMapLocal:
    def test_map_local(self):
        path = maplocal(PATH_TEST, oldroot=MAPENV.MAPLOCAL_FROM, newroot=MAPENV.MAPLOCAL_TO)
        assert (
            str(path)
            == f"\\\\wsl.localhost\\{get_wsl_distro_name()}" + str(PATH_TEST).replace("/", "\\")
        )


class TestWslExample:
    def test_map_local(self):
        """This will open the file in windows explorer"""
        openlocal(PATH_TEST, mapenv=MAPENV)
        assert isinstance(MAPENV.openpath, ty.Callable)

