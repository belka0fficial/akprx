"""
akprx.server.adaptors
REST routes for adaptor management.
"""

import os
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from akprx.store import adaptors as store

router = APIRouter(prefix="/adaptors", tags=["adaptors"])


class AdaptorIn(BaseModel):
    name: str
    base_url: str
    secret_env: str
    auth_header: str = "Authorization"
    auth_prefix: str = "Bearer"
    extra_headers: dict[str, str] = {}


@router.get("")
def list_adaptors() -> dict[str, Any]:
    all_adaptors = store.load()
    if not all_adaptors:
        return {"total": 0, "adaptors": []}
    result = []
    for name, cfg in all_adaptors.items():
        secret_loaded = bool(os.getenv(cfg["secret_env"]))
        result.append({
            "name": name,
            "status": "ok" if secret_loaded else "missing_secret",
            "config": {
                "base_url": cfg["base_url"],
                "auth_header": cfg.get("auth_header", "Authorization"),
                "auth_prefix": cfg.get("auth_prefix", "Bearer"),
                "secret_env": cfg["secret_env"],
                "secret_loaded": secret_loaded,
                "extra_headers": cfg.get("extra_headers", {}),
            },
            "issues": [] if secret_loaded else [
                f"Env var '{cfg['secret_env']}' not set — calls will fail."
            ],
        })
    return {"total": len(result), "adaptors": result}


@router.post("")
def create_adaptor(body: AdaptorIn) -> dict[str, Any]:
    if store.exists(body.name):
        raise HTTPException(
            status_code=409,
            detail=f"Adaptor '{body.name}' already exists. Remove it first.",
        )
    secret_present = bool(os.getenv(body.secret_env))
    store.put(body.name, {
        "base_url": body.base_url.rstrip("/"),
        "secret_env": body.secret_env,
        "auth_header": body.auth_header,
        "auth_prefix": body.auth_prefix,
        "extra_headers": body.extra_headers,
    })
    return {
        "created": body.name,
        "secret_loaded": secret_present,
        "warning": None if secret_present else (
            f"Env var '{body.secret_env}' not set. "
            f"Run: akprx key add {body.secret_env}"
        ),
    }


@router.get("/{name}")
def get_adaptor(name: str) -> dict[str, Any]:
    cfg = store.get(name)
    if not cfg:
        raise HTTPException(status_code=404, detail=f"Adaptor '{name}' not found.")
    secret_loaded = bool(os.getenv(cfg["secret_env"]))
    return {
        "name": name,
        "status": "ok" if secret_loaded else "missing_secret",
        "config": cfg,
        "issues": [] if secret_loaded else [
            f"Env var '{cfg['secret_env']}' not set."
        ],
    }


@router.delete("/{name}")
def delete_adaptor(name: str) -> dict[str, Any]:
    if not store.delete(name):
        raise HTTPException(status_code=404, detail=f"Adaptor '{name}' not found.")
    return {"removed": name}
