"""
akprx.cli.key
Subcommands for managing secret keys.
Values are never shown — hidden input only.
"""

import getpass
import subprocess
import sys
from akprx.cli import http

def _restart_service() -> None:
    try:
        result = subprocess.run(
            ["sudo", "systemctl", "restart", "akprx"],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            print("  service restarted — key is now active.")
        else:
            print("  warning: could not restart service automatically.")
            print("  run manually: sudo systemctl restart akprx")
    except FileNotFoundError:
        print("  warning: systemctl not found — restart akprx manually.")


USAGE = """\
usage:
  akprx key list
  akprx key add <n>
  akprx key remove <n>
  akprx key rotate <n>
"""


def _list() -> None:
    data = http.get("/secrets")
    if data["total"] == 0:
        print("no keys stored.")
        print("add one: akprx key add <KEY_NAME>")
        return
    for k in data["keys"]:
        print(f"  {k}")


def _add(name: str) -> None:
    value = getpass.getpass(f"  value for '{name}' (hidden): ").strip()
    if not value:
        print("error: value cannot be empty.", file=sys.stderr); sys.exit(1)
    http.pp(http.post("/secrets", {"key": name, "value": value}))
    _restart_service()


def _remove(name: str) -> None:
    http.pp(http.delete(f"/secrets/{name}"))
    _restart_service()


def _rotate(name: str) -> None:
    value = getpass.getpass(f"  new value for '{name}' (hidden): ").strip()
    if not value:
        print("error: value cannot be empty.", file=sys.stderr); sys.exit(1)
    http.pp(http.put(f"/secrets/{name}", {"key": name, "value": value}))
    _restart_service()


def run(args: list[str]) -> None:
    if not args or args[0] in ("-h", "--help", "help"):
        print(USAGE); sys.exit(0)

    sub = args[0]
    if sub == "list":
        _list()
    elif sub == "add":
        if len(args) < 2:
            print("usage: akprx key add <n>", file=sys.stderr); sys.exit(1)
        _add(args[1])
    elif sub == "remove":
        if len(args) < 2:
            print("usage: akprx key remove <n>", file=sys.stderr); sys.exit(1)
        _remove(args[1])
    elif sub == "rotate":
        if len(args) < 2:
            print("usage: akprx key rotate <n>", file=sys.stderr); sys.exit(1)
        _rotate(args[1])
    else:
        print(f"akprx key: unknown subcommand '{sub}'", file=sys.stderr)
        print(USAGE, file=sys.stderr); sys.exit(1)
