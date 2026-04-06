"""
akprx.cli.main
Entry point for the akprx CLI.
"""

import sys
from akprx import __version__

USAGE = f"""\
akprx {__version__} — agent key proxy

usage:
  akprx <command> [arguments]

commands:
  status                    service health, loaded keys, registered adaptors
  adaptor list              list all adaptors
  adaptor add               register a new adaptor (interactive)
  adaptor show <n>          show full config of one adaptor
  adaptor remove <n>        remove an adaptor
  key list                  list stored key names (no values)
  key add <n>               store a new key (value prompted, hidden)
  key remove <n>            remove a key
  key rotate <n>            replace a key value (prompted, hidden)
  call <adaptor> <path>     GET request through an adaptor
  call <adaptor> <path> --method POST --data '{{...}}'
  check                     validate service, adaptors, and keys
  version                   print version

run 'akprx <command> --help' for details on any command.
"""


def main() -> None:
    args = sys.argv[1:]

    if not args or args[0] in ("-h", "--help", "help"):
        print(USAGE); sys.exit(0)

    cmd = args[0]

    if cmd == "version":
        print(f"akprx {__version__}"); sys.exit(0)

    if cmd == "status":
        from akprx.cli.status import run
        run(); sys.exit(0)

    if cmd == "adaptor":
        from akprx.cli.adaptor import run
        run(args[1:]); sys.exit(0)

    if cmd == "key":
        from akprx.cli.key import run
        run(args[1:]); sys.exit(0)

    if cmd == "call":
        from akprx.cli.call import run
        run(args[1:]); sys.exit(0)

    print(f"akprx: unknown command '{cmd}'", file=sys.stderr)
    print("run 'akprx --help' to see available commands.", file=sys.stderr)
    sys.exit(1)
