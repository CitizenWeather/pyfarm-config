"""Centralized settings for the pyfarm ecosystem.

All pyfarm services (auth, api, dashboard, …) read their configuration through
:func:`get_settings`, which returns a cached :class:`PyfarmSettings` instance.
Values are sourced from environment variables (optionally via a ``.env`` file)
with the ``PYFARM_`` prefix, falling back to development-friendly defaults so
the stack runs out of the box in tests and local development.

Example::

    from pyfarm.config import get_settings

    settings = get_settings()
    secret = settings.auth_secret_key.get_secret_value()
"""

from __future__ import annotations

from functools import lru_cache

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class PyfarmSettings(BaseSettings):
    """Runtime configuration shared across pyfarm services.

    Override any field via an environment variable, e.g.
    ``PYFARM_AUTH_SECRET_KEY``, ``PYFARM_CONTROL_URL`` or ``PYFARM_PORT``.
    """

    model_config = SettingsConfigDict(
        env_prefix="PYFARM_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # --- Service URLs ---------------------------------------------------
    auth_url: str = "http://localhost:8001"
    control_url: str = "http://localhost:8002"
    pyfarm_api_url: str = "http://localhost:8000"

    # --- Dashboard / serving -------------------------------------------
    port: int = 3000

    # --- Auth / security ------------------------------------------------
    # NOTE: the default is a development secret only. Always override
    # PYFARM_AUTH_SECRET_KEY in production.
    auth_secret_key: SecretStr = SecretStr(
        "dev-insecure-secret-change-me-in-production-0123456789"
    )
    access_token_expire_minutes: int = 30

    # --- Storage --------------------------------------------------------
    storage_backend: str = "sqlite"


@lru_cache(maxsize=1)
def get_settings() -> PyfarmSettings:
    """Return the process-wide cached :class:`PyfarmSettings` instance."""
    return PyfarmSettings()


def reset_settings_cache() -> None:
    """Clear the cached settings (useful in tests after changing env vars)."""
    get_settings.cache_clear()
