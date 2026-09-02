from __future__ import annotations

import json

import pytest

from sportrx.local_accounts import LocalAccountError, authenticate_local_account, create_local_account


def test_local_account_stores_only_a_password_hash(tmp_path):
    store = tmp_path / "accounts.json"

    account = create_local_account(store, "Lena", "practice-123")

    assert account["display_name"] == "Lena"
    payload = json.loads(store.read_text(encoding="utf-8"))
    stored = payload["accounts"][0]
    assert stored["password_hash"] != "practice-123"
    assert "password" not in account
    assert authenticate_local_account(store, "lena", "practice-123") == account


def test_local_account_rejects_duplicate_names_and_wrong_passwords(tmp_path):
    store = tmp_path / "accounts.json"
    create_local_account(store, "Lena", "practice-123")

    with pytest.raises(LocalAccountError, match="已经存在"):
        create_local_account(store, " lena ", "another-123")
    with pytest.raises(LocalAccountError, match="不正确"):
        authenticate_local_account(store, "Lena", "not-the-password")


def test_local_account_requires_a_usable_name_and_password(tmp_path):
    store = tmp_path / "accounts.json"

    with pytest.raises(LocalAccountError, match="2–24"):
        create_local_account(store, "A", "practice-123")
    with pytest.raises(LocalAccountError, match="至少"):
        create_local_account(store, "Lena", "short")
