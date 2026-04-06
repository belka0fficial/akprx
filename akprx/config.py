"""
akprx.config
All paths and constants. Nothing else in the codebase hardcodes a path.
"""

from pathlib import Path

# ── Directories ───────────────────────────────────────────────────────────────

DATA_DIR    = Path("/var/lib/akprx")
SECRETS_DIR = DATA_DIR / "secrets"
VENV_DIR    = Path("/usr/lib/akprx/venv")

# ── Files ─────────────────────────────────────────────────────────────────────

ADAPTORS_FILE = DATA_DIR / "adaptors.json"
SECRETS_FILE  = SECRETS_DIR / "secrets.env"

# ── Systemd ───────────────────────────────────────────────────────────────────

SERVICE_NAME = "akprx"
SERVICE_FILE = Path(f"/lib/systemd/system/{SERVICE_NAME}.service")

# ── Runtime ───────────────────────────────────────────────────────────────────

HOST     = "127.0.0.1"
PORT     = 8080
BIND     = f"{HOST}:{PORT}"
BASE_URL = f"http://{BIND}"

# ── System user ───────────────────────────────────────────────────────────────

SERVICE_USER  = "akprx"
SERVICE_GROUP = "akprx"
