from maplocal.maplocal import _remove_root, maplocal
import os
import pathlib
import typing as ty
import pytest
from maplocal.maplocal import MAPENV, openlocal, runlocal
from maplocal.env import MapLocalEnv

PATH_TEST = pathlib.Path(__file__)
DIR_REPO = PATH_TEST.parents[1]


class TestMAPENV:
    def test_MAPENV(self):
        assert MAPENV.MAPLOCAL_FROM == pathlib.PurePosixPath("/home")
        assert MAPENV.MAPLOCAL_TO == pathlib.PureWindowsPath('//wsl.localhost/20221021/home')


class TestRemoveRoot:
    def test__remove_root(self):
        rootfound, newpath = _remove_root(PATH_TEST, DIR_REPO)
        assert rootfound == True
        assert newpath == pathlib.Path("tests/test_maplocal.py")


class TestMapLocal:
    def test_map_local(self):
        path = maplocal(PATH_TEST)
        assert (
            str(path)
            == '\\\\wsl.localhost\\20221021\\home\\jovyan\\maplocal\\tests\\test_maplocal.py'
        )
        print(path)
        print("done")


class TestWslExample:
    def test_map_local(self):
        openlocal(PATH_TEST)
        assert isinstance(MAPENV.openpath, ty.Callable)

