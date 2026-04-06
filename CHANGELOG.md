# Changelog

## [1.0.0] — 2026-04-06

### Added
- FastAPI broker daemon on `127.0.0.1:8080` — localhost only, zero external attack surface
- Adaptor registry — register, list, show, remove API providers
- Secret management — add, list, remove, rotate keys (values never exposed via API)
- Generic `/call` proxy — works with any REST API using bearer token or API key auth
- `akprx check` — validates service health, adaptor/key pairing, reports exact fix commands
- `akprx status` — service health, loaded keys, registered adaptors at a glance
- Auto-restart service after key add, rotate, remove — no manual restart needed
- Locked system user (`akprx`) — secrets unreadable by agent user, enforced by Linux permissions
- Debian package with automated `postinst` — creates user, dirs, permissions, systemd service on install
- `ProtectSystem=full` — systemd hardening, `/var/lib` writable, `/usr` and `/boot` protected
- MIT license
