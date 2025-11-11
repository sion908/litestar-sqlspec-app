from pathlib import Path

from sqlspec import SQLSpec
from sqlspec.adapters.aiosqlite import AiosqliteConfig
from sqlspec.extensions.litestar import SQLSpecPlugin

__all__ = ["config", "sqlspec_plugin"]

BIND_KEY = "docs_aiosqlite"
MIGRATIONS_PATH = Path(__file__).with_name("migrations")
registry = SQLSpec()
registry.add_config(
    AiosqliteConfig(
        bind_key=BIND_KEY,
        pool_config={"database": "database/docs_aiosqlite.db"},
        migration_config={
            "enabled": True,
            "script_location": MIGRATIONS_PATH,
        },
        extension_config={"litestar": {"commit_mode": "autocommit"}},
    )
)

config = registry.get_config(AiosqliteConfig)

sqlspec_plugin = SQLSpecPlugin(sqlspec=registry)
