import pathlib
import typing as ty
import logging

from maplocal.env import MapLocalEnv

MAPENV = MapLocalEnv()

def _remove_root(
    path: pathlib.PurePath, root: ty.Optional[pathlib.PurePath]
) -> ty.Tuple[bool, pathlib.PurePath]:
    """removes root from path
    Args:
        path (pathlib.PurePath): path
        pathlib (pathlib.PurePath): root to remove from path
    Returns:
        bool, path:
            bool-> if root successfully removed: True, else: False
            path-> if bool: newpath, else: oldpath
    """
    assert isinstance(
        path, pathlib.PurePath
    ), f"path ({path}) passed to _remove_root fn not a valid pathlib.PurePath"
    assert isinstance(
        root, pathlib.PurePath
    ), f"root ({root}) passed to _remove_root fn not a valid pathlib.PurePath"
    if root in path.parents:
        rootfound = True
        parts = pathlib.Path(path).parts
        n = len(root.parts)
        newpath = pathlib.PurePath(*parts[n:])
    else:
        rootfound = False
        newpath = path
    return rootfound, newpath


def maplocal(
    path: pathlib.PurePath,
    oldroot: ty.Optional[pathlib.PurePath] = None,
    newroot: ty.Optional[pathlib.PurePath] = None,
):
    if oldroot is None:
        oldroot = MAPENV.MAPLOCAL_FROM
    if newroot is None:
        newroot = MAPENV.MAPLOCAL_TO
    path = pathlib.PurePath(path)
    rootfound, newpath = _remove_root(path, oldroot)
    if not rootfound:
        raise ValueError(f"root: {str(oldroot)}. not found in path: {str(path)}")
    return newroot / newpath


def mapremote(path: pathlib.PurePath,
    oldroot: ty.Optional[pathlib.PurePath] = None,
    newroot: ty.Optional[pathlib.PurePath] = None,
):
    if oldroot is None:
        oldroot = MAPENV.MAPLOCAL_TO
    if newroot is None:
        newroot = MAPENV.MAPLOCAL_FROM
    path = pathlib.PurePath(path)
    rootfound, newpath = _remove_root(path, oldroot)
    if not rootfound:
        raise ValueError(f"root: {str(oldroot)}. not found in path: {str(path)}")
    return newroot / newpath


def openlocal(path, mapenv=MAPENV):
    path = maplocal(path, oldroot=mapenv.MAPLOCAL_FROM, newroot=mapenv.MAPLOCAL_TO)

    return mapenv.openpath(path)


def runlocal(cmd, mapenv=MAPENV):
    return mapenv.runcmd(cmd)

def maplocal_openlocal_exists():
    if isinstance(MAPENV.openpath, ty.Callable):
        return True
    else:
        return False
    
def maplocal_runlocal_exists():
    if isinstance(MAPENV.runcmd, ty.Callable):
        return True
    else:
        return False
    
