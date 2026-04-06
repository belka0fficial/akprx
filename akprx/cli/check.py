"""
akprx.cli.check
Validates that everything is configured correctly.
Checks service health, adaptor/key pairing, and port reachability.
"""

import subprocess
import sys
import urllib.request
import urllib.error

from akprx.config import SERVICE_NAME, BASE_URL
from akprx.cli import http


def _check_service() -> bool:
    try:
        r = subprocess.run(
            ["systemctl", "is-active", SERVICE_NAME],
            capture_output=True, text=True
        )
        running = r.stdout.strip() == "active"
        sym = "✓" if running else "✗"
        print(f"  {sym} service        {'running' if running else 'NOT running'}")
        if not running:
            print(f"    fix: sudo systemctl start {SERVICE_NAME}")
        return running
    except FileNotFoundError:
        print("  ✗ service        systemctl not found")
        return False


def _check_port() -> bool:
    try:
        urllib.request.urlopen(BASE_URL + "/secrets", timeout=3)
        print(f"  ✓ port           reachable at {BASE_URL}")
        return True
    except urllib.error.HTTPError:
        # any HTTP response means the port is up
        print(f"  ✓ port           reachable at {BASE_URL}")
        return True
    except Exception:
        print(f"  ✗ port           cannot reach {BASE_URL}")
        print(f"    fix: sudo systemctl restart {SERVICE_NAME}")
        return False


def _check_keys_and_adaptors() -> bool:
    ok = True

    try:
        secrets_data = http.get("/secrets")
        stored_keys = set(secrets_data.get("keys", []))
    except SystemExit:
        print("  ✗ keys           could not fetch key list")
        return False

    try:
        adaptors_data = http.get("/adaptors")
        adaptors = adaptors_data.get("adaptors", [])
    except SystemExit:
        print("  ✗ adaptors       could not fetch adaptor list")
        return False

    if not adaptors:
        print("  ✓ adaptors       none registered (nothing to check)")
        return True

    for a in adaptors:
        name = a["name"]
        secret_env = a["config"]["secret_env"]
        secret_in_storage = secret_env in stored_keys
        secret_loaded = a["config"]["secret_loaded"]

        if secret_loaded:
            print(f"  ✓ adaptor        {name}")
            print(f"    key loaded:    {secret_env}")
        elif secret_in_storage and not secret_loaded:
            print(f"  ✗ adaptor        {name}")
            print(f"    key stored but not loaded: {secret_env}")
            print(f"    fix: sudo systemctl restart {SERVICE_NAME}")
            ok = False
        elif not secret_in_storage:
            print(f"  ✗ adaptor        {name}")
            print(f"    key missing:   {secret_env}")
            print(f"    fix: akprx key add {secret_env}")
            ok = False

    return ok


def run() -> None:
    print(f"\nakprx check\n")

    service_ok = _check_service()

    if not service_ok:
        print("\n  service is not running — fix that first.\n")
        sys.exit(1)

    port_ok = _check_port()
    adaptors_ok = _check_keys_and_adaptors()

    print()
    if service_ok and port_ok and adaptors_ok:
        print("  all checks passed.\n")
    else:
        print("  some checks failed — see above.\n")
        sys.exit(1)
