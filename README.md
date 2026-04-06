# akprx

**Agent Key Proxy** — credential broker daemon for AI agents on Linux.

Your agent needs to call external APIs. You don't want it holding the keys.  
`akprx` sits in the middle: the agent sends a request, akprx injects the real credential, returns only the result. The agent never sees a token.

```
agent → POST /call → akprx injects key → GitHub API
                  ↑
         key never crosses this boundary
```

---

## Install

```bash
curl -fsSL https://belka0fficial.github.io/akprx/install-unsigned.sh | sudo bash
```

Or manually:

```bash
echo "deb [trusted=yes] https://belka0fficial.github.io/akprx stable main" \
  | sudo tee /etc/apt/sources.list.d/akprx.list
sudo apt update
sudo apt install akprx
```

---

## Quickstart

```bash
akprx status

akprx key add GITHUB_TOKEN

akprx adaptor add

akprx call github /repos/youruser/yourrepo
```

---

## Commands

```
akprx status                      service health, keys, adaptors

akprx adaptor list                list registered adaptors
akprx adaptor add                 register a new adaptor (interactive)
akprx adaptor show <n>            show full config of one adaptor
akprx adaptor remove <n>          remove an adaptor

akprx key list                    list stored key names (no values shown)
akprx key add <n>                 store a new key (value prompted, hidden)
akprx key remove <n>              remove a key
akprx key rotate <n>              replace a key value (prompted, hidden)

akprx call <adaptor> <path>       GET request through adaptor
akprx call <adaptor> <path> --method POST --data '{...}'

akprx version                     print version
```

---

## How it works

`akprx` runs as a systemd service on `127.0.0.1:8080` — only local processes can reach it, nothing from outside the machine.

An **adaptor** is a registered API provider. Register one with `akprx adaptor add` — you give it a name, base URL, and which env var holds the token. After that the agent can call any endpoint on that provider.

**Secrets** are stored in `/var/lib/akprx/secrets/secrets.env` — owned by the `akprx` system user, mode `600`. The agent user cannot read this file. The secret is loaded into the broker process environment at startup, never exposed via the API.

---

## File layout

```
/var/lib/akprx/
├── adaptors.json          registered providers   akprx:akprx 600
└── secrets/
    └── secrets.env        API keys               akprx:akprx 600

/usr/lib/akprx/
└── venv/                  Python runtime

/usr/bin/akprx             CLI
/lib/systemd/system/akprx.service
```

---

## Security model

| What                       | Who can access          |
|----------------------------|-------------------------|
| `secrets.env`              | `akprx` user only       |
| `adaptors.json`            | `akprx` user only       |
| broker HTTP API            | any local process       |
| secret values via HTTP     | nobody — never returned |
| port 8080 from outside VPS | nobody — loopback only  |

---

## Requirements

- Ubuntu 22.04+ or Debian 12+ (systemd-based)
- amd64 architecture
- Internet access during install (to fetch Python deps into venv)

---

## Remove

```bash
sudo apt remove akprx        # removes package, keeps data
sudo apt purge akprx         # removes everything including secrets
```

---

## License

MIT — see [LICENSE](LICENSE)

## Author

[Belka](https://github.com/belka0fficial)
