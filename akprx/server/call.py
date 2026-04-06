"""
akprx.server.call
The core proxy route.
Agent sends adaptor + path + method + payload.
akprx loads the secret, injects it, fires the request, returns the result.
The agent never sees the credential.
"""

import os
from typing import Any

import httpx
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from akprx.store import adaptors as store

router = APIRouter(tags=["call"])


class CallIn(BaseModel):
    adaptor: str
    method: str = "GET"
    path: str
    payload: dict[str, Any] = {}
    params: dict[str, Any] = {}


@router.post("/call")
async def proxy_call(body: CallIn) -> Any:
    cfg = store.get(body.adaptor)
    if not cfg:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown adaptor '{body.adaptor}'. Register it: akprx adaptor add",
        )

    token = os.getenv(cfg["secret_env"])
    if not token:
        raise HTTPException(
            status_code=500,
            detail=(
                f"Secret '{cfg['secret_env']}' not loaded. "
                f"Run: akprx key add {cfg['secret_env']} && sudo systemctl restart akprx"
            ),
        )

    method = body.method.upper()
    url = cfg["base_url"] + "/" + body.path.lstrip("/")

    headers = {
        cfg.get("auth_header", "Authorization"): (
            f"{cfg.get('auth_prefix', 'Bearer')} {token}".strip()
        ),
        "Content-Type": "application/json",
    }
    headers.update(cfg.get("extra_headers", {}))

    try:
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.request(
                method=method,
                url=url,
                headers=headers,
                json=body.payload if body.payload else None,
                params=body.params if body.params else None,
            )
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail=f"Upstream request failed: {exc}")

    if response.status_code >= 400:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    content_type = response.headers.get("content-type", "")
    if "application/json" in content_type:
        return response.json()

    return {"status": response.status_code, "text": response.text}
