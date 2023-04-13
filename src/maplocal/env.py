from pydantic import BaseModel, BaseSettings, Field, validator
import pathlib
import importlib.util
import sys
import typing as ty
import os
import logging

logger = logging.getLogger(__name__)


MAPOS = {"windows": pathlib.PureWindowsPath, "linux": pathlib.PurePosixPath}
PLATFORM = sys.platform

def load(path, fn_name: str):
    if isinstance(path, str):
        path = pathlib.Path(path)
    if not path.is_file():
        raise ValueError(f"{str(path)} must be a file")
    try:
        spec = importlib.util.spec_from_file_location("maplocal", path)
        foo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(foo)
        fn = getattr(foo, fn_name)
    except:
        raise ValueError(f"could not find `{fn_name}` from {str(path)}")

    return fn

def get_maplocal_dir():
    if PLATFORM == "linux":
        return pathlib.Path(os.environ['HOME']) / '.maplocal'
    elif PLATFORM == "windows":
        return pathlib.Path(os.environ['USERPROFILE']) / '.maplocal'
    else:
        raise ValueError('platform not windows or linux')

def get_maplocal_path():
    return get_maplocal_dir() / 'maplocal.py'

class MapLocalEnv(BaseSettings):
    MAPLOCAL_OS_FROM: str = "linux"  #  TODO make enum
    MAPLOCAL_OS_TO: str = "windows"
    MAPLOCAL_FROM: ty.Optional[pathlib.PurePath] = None
    MAPLOCAL_TO: ty.Optional[pathlib.PurePath] = None
    MAPLOCAL_SCRIPT_PATH: ty.Optional[pathlib.Path] = None
    openpath: ty.Optional[ty.Callable[[pathlib.Path], bool]] = None
    runcmd: ty.Optional[ty.Callable[[str], None]] = None

    @validator("MAPLOCAL_FROM", always=True, pre=True)
    def _MAPLOCAL_FROM(cls, v, values):
        if v is None:
            return None
        else:
            return MAPOS[values["MAPLOCAL_OS_FROM"]](v)

    @validator("MAPLOCAL_TO", always=True, pre=True)
    def _MAPLOCAL_TO(cls, v, values):
        if v is None:
            return None
        else:
            return MAPOS[values["MAPLOCAL_OS_TO"]](v)
        
    @validator("MAPLOCAL_SCRIPT_PATH", always=True, pre=True)
    def _MAPLOCAL_SCRIPT_PATH(cls, v, values):
        if v is None:
            p = get_maplocal_path()
            if p.is_file():
                return p
            else:
                return None
        else:
            p = pathlib.Path(v)
            if p.is_file():
                return p
            else:
                logger.warning(f"for maplocal to load openpath and runcmd callable, {str(p)} must exist with functions `openpath` and `runcmd`")
                return None
            

    @validator("openpath", always=True)
    def _openpath(cls, v, values):
        if "MAPLOCAL_SCRIPT_PATH" not in values:
            return None
        p = values["MAPLOCAL_SCRIPT_PATH"]
        if p is not None:
            return load(p, "openpath")
        else:
            return None

    @validator("runcmd", always=True)
    def _runcmd(cls, v, values):
        if "MAPLOCAL_SCRIPT_PATH" not in values:
            return None
        p = values["MAPLOCAL_SCRIPT_PATH"]
        if p is not None:
            return load(p, "runcmd")
        else:
            return None

    class Config:
        # env_file = PATH_ENV
        env_file_encoding = "utf-8"
        arbitrary_types_allowed=True


if __name__ == "__main__":

    DIR_REPO = pathlib.Path("/home/jovyan/maplocal")
    PATH_ENV = DIR_REPO / "tests" / ".env"
    PATH_SCRIPT = DIR_REPO / "scripts" / "maplocal_wsl.py"
    assert PATH_ENV.is_file()
    MAPENV = MapLocalEnv(_env_file=PATH_ENV)
    print('done')
    # DIR_REPO = pathlib.Path(__file__).parents[2]
    # PATH_ENV = DIR_REPO /  ".env"
    # PATH_SCRIPT = DIR_REPO / "scripts" / "maplocal_wsl.py"
    # # assert PATH_ENV.is_file()
    # MAPENV = MapLocalEnv(
    #     MAPLOCAL_FROM="/home/jovyan",
    #     MAPLOCAL_TO="\\\\wsl$\\20221021\\home\\jovyan",
    #     MAPLOCAL_SCRIPT_PATH=PATH_SCRIPT,
    # )
