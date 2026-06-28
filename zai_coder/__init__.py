from __future__ import annotations

import os as _os
import platform as _platform
from types import SimpleNamespace as _SimpleNamespace

__all__ = ["__version__"]
__version__ = "0.1.4"


def _portable_uname():
    return _SimpleNamespace(
        sysname=_platform.system(),
        nodename=_platform.node(),
        release=_platform.release(),
        version=_platform.version(),
        machine=_platform.machine(),
    )


if not hasattr(_os, "uname"):
    _os.uname = _portable_uname
