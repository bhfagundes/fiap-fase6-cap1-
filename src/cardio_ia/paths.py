from __future__ import annotations

import os
from pathlib import Path


def project_root() -> Path:
    """Resolve a raiz do projeto (artefatos e data/) em dev e após instalação."""
    env = os.environ.get("CARDIO_PROJECT_ROOT")
    if env:
        return Path(env).resolve()
    cwd = Path.cwd()
    if (cwd / "artifacts").is_dir() and (cwd / "data").is_dir():
        return cwd
    here = Path(__file__).resolve()
    candidate = here.parents[2]
    if (candidate / "artifacts").is_dir():
        return candidate
    return cwd
