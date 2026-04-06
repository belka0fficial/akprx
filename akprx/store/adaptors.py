"""
akprx.store.adaptors
Read and write adaptor registry from disk.
"""

import json
from typing import Any
from akprx.config import ADAPTORS_FILE


def load() -> dict[str, Any]:
    if not ADAPTORS_FILE.exists():
        return {}
    with ADAPTORS_FILE.open("r") as f:
        return json.load(f)


def save(adaptors: dict[str, Any]) -> None:
    with ADAPTORS_FILE.open("w") as f:
        json.dump(adaptors, f, indent=2)


def get(name: str) -> dict[str, Any] | None:
    return load().get(name)


def exists(name: str) -> bool:
    return name in load()


def put(name: str, cfg: dict[str, Any]) -> None:
    adaptors = load()
    adaptors[name] = cfg
    save(adaptors)


def delete(name: str) -> bool:
    adaptors = load()
    if name not in adaptors:
        return False
    del adaptors[name]
    save(adaptors)
    return True
