"""AsyncPG connection pool configured through SQLSpec."""

import asyncio
import os
from pydantic_settings import BaseSettings

from sqlspec.adapters.asyncpg import AsyncpgConfig, AsyncpgPoolConfig

__all__ = ("main",)


class DatabaseConfig(BaseSettings):
    host: str = os.getenv("DB_HOST", "db")
    database: str = os.getenv("DB_NAME", "litestardb")
    user: str = os.getenv("DB_USER", "litestar")
    password: str = os.getenv("DB_PASSWORD", "litestar")
    port: str = os.getenv("DB_PORT", "5432")

    def get_dsn(self) -> str:
        return f"postgres://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"


db_conf = DatabaseConfig()

config = AsyncpgConfig(
    bind_key="docs_asyncpg",
    pool_config=AsyncpgPoolConfig(dsn=db_conf.get_dsn(), min_size=1, max_size=5)
)


async def main() -> None:
    """Connect to Postgres and return the server version."""
    async with config.provide_session() as session:
        result = await session.execute("SELECT version() AS version")
        row = result.one_or_none()
        if row:
            print({"adapter": "asyncpg", "version": row["version"]})
        else:
            print({"adapter": "asyncpg", "version": "unknown"})


if __name__ == "__main__":
    asyncio.run(main())
