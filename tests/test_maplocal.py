from maplocal.maplocal import _remove_root
import os
import pathlib

PATH_TEST = pathlib.Path(__file__)
DIR_REPO = PATH_TEST.parents[1]


class TestSwapRoot:
    def test__remove_root(self):
        rootfound, newpath = _remove_root(PATH_TEST, DIR_REPO)
        assert rootfound == True
        assert newpath == pathlib.Path('tests/test_maplocal.py')

        

