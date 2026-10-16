from pathlib import Path

from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, inspect

from app.core.config import get_settings


def test_initial_migration_creates_schema_in_temporary_database(tmp_path: Path, monkeypatch):
    database_url = f"sqlite:///{(tmp_path / 'migration.sqlite').as_posix()}"
    monkeypatch.setenv("DATABASE_URL", database_url)
    get_settings.cache_clear()
    try:
        config = Config(str(Path(__file__).resolve().parents[2] / "alembic.ini"))
        command.upgrade(config, "head")
        engine = create_engine(database_url)
        with engine.connect() as connection:
            assert set(inspect(connection).get_table_names()) >= {"users", "products", "alembic_version"}
        engine.dispose()
    finally:
        get_settings.cache_clear()
