"""
akprx.server.app
FastAPI application factory.
"""

from fastapi import FastAPI
from akprx.server import adaptors, secrets, call

app = FastAPI(
    title="akprx",
    description="Agent Key Proxy — credential broker for AI agents",
    version="0.1.0",
    docs_url=None,
    redoc_url=None,
)

app.include_router(adaptors.router)
app.include_router(secrets.router)
app.include_router(call.router)
