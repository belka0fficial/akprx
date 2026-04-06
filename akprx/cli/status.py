"""
akprx.cli.status
Shows service health, loaded keys, and registered adaptors.
"""

import subprocess
import sys

from akprx import __version__
from akprx.cli import http
from akprx.config import SERVICE_NAME, HOST, PORT


def _service_state() -> tuple[str, str]:
    try:
        r = subprocess.run(
            ["systemctl", "is-active", SERVICE_NAME],
            capture_output=True, text=True
        )
        state = r.stdout.strip()
        if state == "active":
            r2 = subprocess.run(
                ["systemctl", "show", SERVICE_NAME,
                 "--property=ActiveEnterTimestamp"],
                capture_output=True, text=True
            )
            since = r2.stdout.strip().replace("ActiveEnterTimestamp=", "")
            return "running", since
        return state, ""
    except FileNotFoundError:
        return "unknown", ""


def run() -> None:
    state, since = _service_state()
    sym = "●" if state == "running" else "○"

    print(f"\nakprx {__version__}\n")
    print(f"  service     {sym} {state}", end="")
    if since:
        print(f"   (since {since})", end="")
    print(f"\n  listen      {HOST}:{PORT}")

    if state != "running":
        print(f"\n  not running.")
        print(f"  start:   sudo systemctl start {SERVICE_NAME}")
        print(f"  install: sudo apt install akprx\n")
        sys.exit(1)

    try:
        secrets = http.get("/secrets")
        keys = secrets.get("keys", [])
        print(f"  keys        {secrets.get('total', 0)} stored")
        for k in keys:
            print(f"              {k}")
    except SystemExit:
        print("  keys        unavailable")

    try:
        data = http.get("/adaptors")
        adaptors = data.get("adaptors", [])
        print(f"  adaptors    {data.get('total', 0)} registered")
        for a in adaptors:
            sym = "✓" if a["status"] == "ok" else "✗"
            name = a["name"].ljust(16)
            url = a["config"]["base_url"].ljust(36)
            state_str = "ok" if a["config"]["secret_loaded"] else "MISSING SECRET"
            print(f"              {sym} {name} {url} {state_str}")
            for issue in a.get("issues", []):
                print(f"                ! {issue}")
    except SystemExit:
        print("  adaptors    unavailable")

    print()
