import os
import sys

# Ensure the repository root is on sys.path so that top-level packages like
# `ai` are importable when running the backend from the `backend` directory.
_here = os.path.abspath(os.path.dirname(__file__))
_repo_root = os.path.abspath(os.path.join(_here, os.pardir, os.pardir))
if _repo_root not in sys.path:
    sys.path.insert(0, _repo_root)


