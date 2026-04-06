"""
akprx.cli.http
Shared HTTP client for all CLI commands.
"""

import json
import sys
import urllib.error
import urllib.request

from akprx.config import BASE_URL


def request(method: str, path: str, body: dict | None = None) -> dict:
    url = BASE_URL + path
    data = json.dumps(body).encode() if body is not None else None
    headers = {"Content-Type": "application/json"} if data else {}
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        raw = e.read().decode()
        try:
            detail = json.loads(raw).get("detail", raw)
        except Exception:
            detail = raw
        print(f"error {e.code}: {detail}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError:
        print(
            f"error: cannot reach akprx at {BASE_URL}\n"
            "       is the service running?  sudo systemctl status akprx",
            file=sys.stderr,
        )
        sys.exit(1)


def get(path: str) -> dict:
    return request("GET", path)


def post(path: str, body: dict) -> dict:
    return request("POST", path, body)


def put(path: str, body: dict) -> dict:
    return request("PUT", path, body)


def delete(path: str) -> dict:
    return request("DELETE", path)


def pp(data: dict) -> None:
    print(json.dumps(data, indent=2))
