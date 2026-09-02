"""Minimal local-only account storage for the Streamlit prototype.

This is deliberately not a cloud authentication system.  It provides a small
password gate for a locally run demo while keeping password material out of
session state and source control.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import os
import secrets
import tempfile
from pathlib import Path
from typing import Any


PASSWORD_ITERATIONS = 600_000
MINIMUM_PASSWORD_LENGTH = 6


class LocalAccountError(ValueError):
    """Raised when a local account cannot be created or authenticated."""


def _clean_display_name(value: object) -> str:
    name = str(value or "").strip()
    if not (2 <= len(name) <= 24):
        raise LocalAccountError("训练档案名需要是 2–24 个字符。")
    return name


def _display_name_key(name: str) -> str:
    return " ".join(name.casefold().split())


def _validate_password(password: object) -> str:
    value = str(password or "")
    if len(value) < MINIMUM_PASSWORD_LENGTH:
        raise LocalAccountError(f"密码至少需要 {MINIMUM_PASSWORD_LENGTH} 位。")
    return value


def _password_hash(password: str, salt_hex: str, iterations: int = PASSWORD_ITERATIONS) -> str:
    return hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        bytes.fromhex(salt_hex),
        iterations,
    ).hex()


def _empty_store() -> dict[str, Any]:
    return {"schema_version": 1, "accounts": []}


def _read_store(path: Path) -> dict[str, Any]:
    if not path.exists():
        return _empty_store()
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise LocalAccountError("本机账户数据无法读取，请不要继续覆盖它。") from exc
    if not isinstance(payload, dict) or not isinstance(payload.get("accounts"), list):
        raise LocalAccountError("本机账户数据格式无效，请不要继续覆盖它。")
    return payload


def _write_store(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=".accounts-", suffix=".json", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        os.chmod(temporary_name, 0o600)
        os.replace(temporary_name, path)
        os.chmod(path, 0o600)
    finally:
        if os.path.exists(temporary_name):
            os.unlink(temporary_name)


def _public_account(record: dict[str, Any]) -> dict[str, str]:
    return {
        "account_id": str(record["account_id"]),
        "display_name": str(record["display_name"]),
        "storage": "local_account",
    }


def create_local_account(store_path: str | Path, display_name: object, password: object) -> dict[str, str]:
    """Create a local account and return only safe session metadata."""

    path = Path(store_path)
    name = _clean_display_name(display_name)
    password_value = _validate_password(password)
    name_key = _display_name_key(name)
    store = _read_store(path)
    accounts = store["accounts"]
    if any(str(item.get("display_name_key", "")) == name_key for item in accounts if isinstance(item, dict)):
        raise LocalAccountError("这个训练档案名已经存在，请直接登录或换一个名称。")

    salt = secrets.token_hex(16)
    record = {
        "account_id": secrets.token_hex(16),
        "display_name": name,
        "display_name_key": name_key,
        "password_salt": salt,
        "password_hash": _password_hash(password_value, salt),
        "password_iterations": PASSWORD_ITERATIONS,
    }
    accounts.append(record)
    _write_store(path, store)
    return _public_account(record)


def authenticate_local_account(store_path: str | Path, display_name: object, password: object) -> dict[str, str]:
    """Authenticate against the local hash store without returning credentials."""

    path = Path(store_path)
    name = _clean_display_name(display_name)
    password_value = _validate_password(password)
    name_key = _display_name_key(name)
    store = _read_store(path)
    matching = next(
        (
            item
            for item in store["accounts"]
            if isinstance(item, dict) and str(item.get("display_name_key", "")) == name_key
        ),
        None,
    )
    if not matching:
        raise LocalAccountError("训练档案名或密码不正确。")

    try:
        expected_hash = str(matching["password_hash"])
        actual_hash = _password_hash(
            password_value,
            str(matching["password_salt"]),
            int(matching.get("password_iterations", PASSWORD_ITERATIONS)),
        )
    except (KeyError, TypeError, ValueError) as exc:
        raise LocalAccountError("本机账户数据格式无效，请不要继续覆盖它。") from exc
    if not hmac.compare_digest(expected_hash, actual_hash):
        raise LocalAccountError("训练档案名或密码不正确。")
    return _public_account(matching)
