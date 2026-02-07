# Ensure stdlib is found before project root so "code" (stdlib) is not shadowed by repo's src/
import os
import sys

_stdlib_dir = os.path.dirname(os.__file__)
if _stdlib_dir not in sys.path:
    sys.path.insert(0, _stdlib_dir)

# Project source directory for imports like "from backtest import Backtest"
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_SRC = os.path.join(_ROOT, "src")
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)
