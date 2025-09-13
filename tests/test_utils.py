# tests/test_utils.py

import pytest
from fastapi import Request, HTTPException
from fastapi.testclient import TestClient
from starlette.datastructures import Headers
from starlette.testclient import TestClient as StarletteClient

from backend.utils import get_bearer_token, current_utc_timestamp, raise_bad_request, raise_unauthorized, raise_not_found

class DummyRequest:
    def __init__(self, headers):
        self.headers = headers

def test_get_bearer_token_valid():
    headers = {"Authorization": "Bearer sometoken123"}
    request = DummyRequest(headers)
    token = get_bearer_token(request)
    assert token == "sometoken123"

def test_get_bearer_token_missing():
    request = DummyRequest({})
    token = get_bearer_token(request)
    assert token is None

def test_get_bearer_token_invalid_format():
    headers = {"Authorization": "Token sometoken123"}
    request = DummyRequest(headers)
    token = get_bearer_token(request)
    assert token is None

def test_current_utc_timestamp_format():
    timestamp = current_utc_timestamp()
    assert timestamp.endswith("Z")
    # Basic length check for ISO format
    assert len(timestamp) >= 20

def test_raise_bad_request():
    with pytest.raises(HTTPException) as exc_info:
        raise_bad_request("Invalid input")
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Invalid input"

def test_raise_unauthorized():
    with pytest.raises(HTTPException) as exc_info:
        raise_unauthorized()
    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Unauthorized"

def test_raise_not_found():
    with pytest.raises(HTTPException) as exc_info:
        raise_not_found()
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Not found"
