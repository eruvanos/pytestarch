from pathlib import Path
import pytest  # noqa: F401 E401

from pytestarch.pytestarch import get_evaluable
import typing, sys  # noqa: F401 E401
import io as io_import  # noqa: F401
from os import path as p, read  # noqa: F401
from ast import *  # noqa: F401 F403
from . import test_dummy_2, test_dummy_3  # noqa: F401


class A:
    pass


ROOT_PATH = Path(__file__).parent.parent.parent.parent.parent.resolve()
ROOT_PATH_STR: typing.Final[str] = str(ROOT_PATH)
MODULE_PATH_STR: typing.Final[str] = str(ROOT_PATH / "tests/resources")


def dummy_test() -> None:
    get_evaluable(ROOT_PATH_STR, MODULE_PATH_STR)
    import itertools  # noqa: F401

    assert True
