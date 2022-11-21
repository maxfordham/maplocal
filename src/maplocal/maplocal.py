import pathlib
import typing as ty
import logging
#from maplocal.env import MAPENV

def _remove_root(path: pathlib.PurePath, root: pathlib.PurePath) -> ty.Tuple[bool, pathlib.PurePath]:
    """removes root from path
    Args:
        path (pathlib.PurePath): path
        pathlib (pathlib.PurePath): root to remove from path
    Returns:
        bool, path: 
            bool-> if root successfully removed: True, else: False
            path-> if bool: newpath, else: oldpath
    """
    assert isinstance(path, pathlib.PurePath), f"path ({path}) passed to _remove_root fn not a valid pathlib.PurePath"
    assert isinstance(root, pathlib.PurePath), f"root ({root}) passed to _remove_root fn not a valid pathlib.PurePath"
    if root in path.parents:
        rootfound = True
        parts = pathlib.Path(path).parts
        n = len(root.parts)
        newpath = pathlib.PurePath(*parts[n:])
    else:
        rootfound = False
        newpath = path
    return rootfound, newpath

def maplocal(path: pathlib.Path, oldroot=None, newroot=None):
    pass
