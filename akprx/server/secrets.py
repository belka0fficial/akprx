"""
akprx.server.secrets
REST routes for secret key management.
Values are never returned — only key names are exposed.
"""

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from akprx.store import secrets as store

router = APIRouter(prefix="/secrets", tags=["secrets"])


class SecretIn(BaseModel):
    key: str
    value: str


@router.get("")
def list_secrets() -> dict[str, Any]:
    keys = store.list_keys()
    return {"total": len(keys), "keys": keys}


@router.post("")
def add_secret(body: SecretIn) -> dict[str, Any]:
    if not body.key or not body.key.replace("_", "").isalnum():
        raise HTTPException(
            status_code=400,
            detail="Key must be alphanumeric with underscores only.",
        )
    if store.exists(body.key):
        raise HTTPException(
            status_code=409,
            detail=f"Key '{body.key}' already exists. Use rotate to update it.",
        )
    try:
        store.add(body.key, body.value)
    except PermissionError:
        raise HTTPException(
            status_code=500,
            detail="Permission denied writing to secrets file.",
        )
    return {
        "created": body.key,

    }


@router.put("/{key}")
def rotate_secret(key: str, body: SecretIn) -> dict[str, Any]:
    if not store.rotate(key, body.value):
        raise HTTPException(status_code=404, detail=f"Key '{key}' not found.")
    return {
        "rotated": key,

    }


@router.delete("/{key}")
def delete_secret(key: str) -> dict[str, Any]:
    if not store.remove(key):
        raise HTTPException(status_code=404, detail=f"Key '{key}' not found.")
    return {
        "removed": key,

    }
