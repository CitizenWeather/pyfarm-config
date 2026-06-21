"""Tests for pyfarm-config settings."""

import pyfarm.config
from pyfarm.config import PyfarmSettings, get_settings, reset_settings_cache


def test_defaults():
    s = PyfarmSettings()
    assert s.auth_url.startswith("http")
    assert s.control_url.startswith("http")
    assert s.pyfarm_api_url.startswith("http")
    assert s.port == 3000
    assert s.access_token_expire_minutes == 30
    assert s.storage_backend == "sqlite"
    # Secret is wrapped so it doesn't leak in reprs.
    assert s.auth_secret_key.get_secret_value()
    assert "dev-insecure" not in repr(s)


def test_get_settings_is_cached():
    reset_settings_cache()
    assert get_settings() is get_settings()


def test_env_override(monkeypatch):
    monkeypatch.setenv("PYFARM_PORT", "9999")
    monkeypatch.setenv("PYFARM_CONTROL_URL", "http://control:1234")
    reset_settings_cache()
    s = get_settings()
    assert s.port == 9999
    assert s.control_url == "http://control:1234"
    reset_settings_cache()


def test_namespace_package_coexists():
    # pyfarm.config must not shadow sibling pyfarm.* packages.
    assert hasattr(pyfarm.config, "get_settings")
