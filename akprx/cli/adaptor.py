"""
akprx.cli.adaptor
Subcommands for managing adaptors.
"""

import sys
from akprx.cli import http

USAGE = """\
usage:
  akprx adaptor list
  akprx adaptor add
  akprx adaptor show <name>
  akprx adaptor remove <name>
"""


def _list() -> None:
    data = http.get("/adaptors")
    if data["total"] == 0:
        print("no adaptors registered.")
        print("add one: akprx adaptor add")
        return
    for a in data["adaptors"]:
        sym = "✓" if a["status"] == "ok" else "✗"
        name = a["name"].ljust(16)
        url = a["config"]["base_url"].ljust(40)
        state = "ok" if a["config"]["secret_loaded"] else "MISSING SECRET"
        print(f"  {sym} {name} {url} {state}")
        for issue in a.get("issues", []):
            print(f"    ! {issue}")


def _show(name: str) -> None:
    http.pp(http.get(f"/adaptors/{name}"))


def _add() -> None:
    print("register a new adaptor.\n")
    name        = input("  name (e.g. github):              ").strip()
    base_url    = input("  base url:                        ").strip()
    secret_env  = input("  secret env var name:             ").strip()
    auth_header = input("  auth header [Authorization]:     ").strip() or "Authorization"
    auth_prefix = input("  auth prefix [Bearer]:            ").strip() or "Bearer"

    extra: dict[str, str] = {}
    print("  extra headers (blank name to finish):")
    while True:
        k = input("    header name:  ").strip()
        if not k:
            break
        v = input("    header value: ").strip()
        extra[k] = v

    result = http.post("/adaptors", {
        "name": name,
        "base_url": base_url,
        "secret_env": secret_env,
        "auth_header": auth_header,
        "auth_prefix": auth_prefix,
        "extra_headers": extra,
    })
    http.pp(result)


def _remove(name: str) -> None:
    http.pp(http.delete(f"/adaptors/{name}"))


def run(args: list[str]) -> None:
    if not args or args[0] in ("-h", "--help", "help"):
        print(USAGE); sys.exit(0)

    sub = args[0]
    if sub == "list":
        _list()
    elif sub == "add":
        _add()
    elif sub == "show":
        if len(args) < 2:
            print("usage: akprx adaptor show <name>", file=sys.stderr); sys.exit(1)
        _show(args[1])
    elif sub == "remove":
        if len(args) < 2:
            print("usage: akprx adaptor remove <name>", file=sys.stderr); sys.exit(1)
        _remove(args[1])
    else:
        print(f"akprx adaptor: unknown subcommand '{sub}'", file=sys.stderr)
        print(USAGE, file=sys.stderr); sys.exit(1)
