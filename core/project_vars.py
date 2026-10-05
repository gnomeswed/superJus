# helper shim se importado via scripts.*
import pathlib
import sys as _sys
_sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from core.config import *  # noqa: F401,F403
