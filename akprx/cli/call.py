"""
akprx.cli.call
Fire an authenticated API call through a registered adaptor.
"""

import json
import sys
from akprx.cli import http

USAGE = """\
usage:
  akprx call <adaptor> <path>
  akprx call <adaptor> <path> --method POST --data '{...}'

examples:
  akprx call github /repos/belka0fficial/belka.life
  akprx call github /repos/belka0fficial/belka.life/issues --method POST --data '{"title":"bug"}'
"""


def run(args: list[str]) -> None:
    if not args or args[0] in ("-h", "--help", "help"):
        print(USAGE); sys.exit(0)

    if len(args) < 2:
        print("usage: akprx call <adaptor> <path>", file=sys.stderr); sys.exit(1)

    adaptor = args[0]
    path    = args[1]
    method  = "GET"
    data    = None

    i = 2
    while i < len(args):
        if args[i] == "--method" and i + 1 < len(args):
            method = args[i + 1].upper(); i += 2
        elif args[i] == "--data" and i + 1 < len(args):
            data = args[i + 1]; i += 2
        else:
            i += 1

    body: dict = {"adaptor": adaptor, "method": method, "path": path}

    if data:
        try:
            body["payload"] = json.loads(data)
        except json.JSONDecodeError:
            print("error: --data is not valid JSON", file=sys.stderr); sys.exit(1)

    http.pp(http.post("/call", body))
