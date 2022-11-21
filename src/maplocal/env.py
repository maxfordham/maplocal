
from pydantic import (
    BaseModel,
    BaseSettings,
    Field, 
    validator
)
import pathlib
import importlib
import typing as ty



class MapLocalEnv(BaseSettings):
    MAPLOCAL_FROM: pathlib.PurePath
    MAPLOCAL_TO: pathlib.PurePath = Field(..., env='my_api_key')
    MAPLOCAL_SCRIPT_PATH: pathlib.Path

    openpath: ty.Callable[pathlib.Path, bool] = None
    runcmd: ty.Callable[str, None] = None

    class Config:
        pass


MAPENV = MapLocalEnv()