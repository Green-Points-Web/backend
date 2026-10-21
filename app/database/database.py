from pathlib import Path

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    Float,
    Integer,
    Numeric,
    String,
    create_engine,
    event,
    inspect,
    text,
)
from sqlalchemy.orm import DeclarativeBase, sessionmaker

BASE_DIR = Path(__file__).resolve().parent
DATABASE_URL = f"sqlite:///{BASE_DIR / 'greenpoints.db'}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}, 
)


@event.listens_for(engine, "connect")
def enable_sqlite_foreign_keys(dbapi_connection, _connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def _fallback_default(column) -> str:
    """Return a SQL literal usable as default when altering an existing table."""
    if isinstance(column.type, Boolean):
        return "0"
    if isinstance(column.type, (Integer, Float, Numeric)):
        return "0"
    if isinstance(column.type, (Date, DateTime)):
        return "'1970-01-01'"
    if isinstance(column.type, String):
        return "''"
    return "''"



_BACKFILL_STATEMENTS = (
    
    """
    UPDATE action_logs
    SET category = (
        SELECT action_types.category
        FROM action_types
        WHERE action_types.id = action_logs.action_type_id
    )
    WHERE category = ''
      AND EXISTS (
          SELECT 1 FROM action_types
          WHERE action_types.id = action_logs.action_type_id
      )
    """,
)


def _sync_missing_columns() -> None:
    """Add model columns that are missing from already existing tables.

    ``create_all`` only creates absent tables and never alters existing ones, so
    columns added to a model after the database file was generated have to be
    applied manually, otherwise every query selecting them fails with
    ``sqlite3.OperationalError: no such column``.
    """
    inspector = inspect(engine)
    existing_tables = set(inspector.get_table_names())
    added_column = False

    for table in Base.metadata.sorted_tables:
        if table.name not in existing_tables:
            continue

        existing_columns = {
            column["name"] for column in inspector.get_columns(table.name)
        }
        missing_columns = [
            column for column in table.columns if column.name not in existing_columns
        ]
        if not missing_columns:
            continue

        with engine.begin() as connection:
            for column in missing_columns:
                column_type = column.type.compile(engine.dialect)
                if column.nullable:
                    definition = f"{column.name} {column_type}"
                else:
                    definition = (
                        f"{column.name} {column_type} NOT NULL "
                        f"DEFAULT {_fallback_default(column)}"
                    )
                connection.execute(
                    text(f"ALTER TABLE {table.name} ADD COLUMN {definition}")
                )
                added_column = True

    if added_column:
        with engine.begin() as connection:
            for statement in _BACKFILL_STATEMENTS:
                connection.execute(text(statement))


def init_db():
    from .. import models 

    Base.metadata.create_all(bind=engine)
    _sync_missing_columns()