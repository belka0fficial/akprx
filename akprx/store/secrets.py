"""
akprx.store.secrets
Read and write secrets.env from disk.
Values are never returned — only key names are exposed outside this module.
"""

from akprx.config import SECRETS_FILE


def _read_lines() -> list[str]:
    if not SECRETS_FILE.exists():
        return []
    with SECRETS_FILE.open("r") as f:
        return f.readlines()


def _write_lines(lines: list[str]) -> None:
    with SECRETS_FILE.open("w") as f:
        f.writelines(lines)


def list_keys() -> list[str]:
    keys = []
    for line in _read_lines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            keys.append(line.split("=", 1)[0].strip())
    return keys


def exists(key: str) -> bool:
    return key in list_keys()


def add(key: str, value: str) -> None:
    with SECRETS_FILE.open("a") as f:
        f.write(f"{key}={value}\n")


def remove(key: str) -> bool:
    lines = _read_lines()
    new_lines = []
    found = False
    for line in lines:
        k = line.strip().split("=", 1)[0].strip()
        if k == key and not line.strip().startswith("#"):
            found = True
        else:
            new_lines.append(line)
    if found:
        _write_lines(new_lines)
    return found


def rotate(key: str, new_value: str) -> bool:
    if not exists(key):
        return False
    remove(key)
    add(key, new_value)
    return True
