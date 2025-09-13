# backend/utils.py

from fastapi import Request, HTTPException
from typing import Optional
import datetime
import re

def get_bearer_token(request: Request) -> Optional[str]:
    """
    Extract Bearer token from Authorization header.
    Returns the token string if present, otherwise None.
    """
    auth_header: str = request.headers.get("Authorization")
    if not auth_header:
        return None
    match = re.match(r"Bearer\s+(.+)", auth_header)
    if match:
        return match.group(1)
    return None

def current_utc_timestamp() -> str:
    """
    Return current UTC timestamp in ISO 8601 format as string.
    """
    return datetime.datetime.utcnow().isoformat() + "Z"

def raise_bad_request(detail: str):
    """
    Helper to raise HTTP 400 Bad Request error.
    """
    raise HTTPException(status_code=400, detail=detail)

def raise_unauthorized(detail: str = "Unauthorized"):
    """
    Helper to raise HTTP 401 Unauthorized error.
    """
    raise HTTPException(status_code=401, detail=detail)

def raise_not_found(detail: str = "Not found"):
    """
    Helper to raise HTTP 404 Not Found error.
    """
    raise HTTPException(status_code=404, detail=detail)
