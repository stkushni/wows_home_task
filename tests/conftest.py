import sqlite3
import os
import pytest
import pathlib
import shutil

from config import orig_db


@pytest.fixture(scope="session", autouse=True)
def work_db_path(tmp_path_factory, request):
    """Создаёт копию базы."""
    tmp_dir = tmp_path_factory.mktemp("db_copy")
    copy_db = tmp_dir / "world_of_warships_work.db"
    shutil.copyfile(orig_db, copy_db)

    request.config.COPY_DB_PATH = copy_db
    print(f"[Fixture] COPY_DB_PATH = {copy_db}")

    yield str(copy_db)

    if copy_db.exists():
        os.remove(copy_db)
        print(f"[Fixture] Копия базы удалена: {copy_db}")


@pytest.fixture(scope="session", autouse=True)
def db_conns(pytestconfig, work_db_path):
    """Создаёт сессионные соединения (зависит от work_db_path)."""
    orig_conn = sqlite3.connect(orig_db)
    orig_conn.row_factory = sqlite3.Row
    copy_conn = sqlite3.connect(pytestconfig.COPY_DB_PATH)
    copy_conn.row_factory = sqlite3.Row

    pytestconfig.ORIG_CONN = orig_conn
    pytestconfig.COPY_CONN = copy_conn

    print("[Fixture] Соединения открыты.")

    yield  # тесты работают

    orig_conn.close()
    copy_conn.close()
    print("[Fixture] Соединения закрыты.")


@pytest.fixture
def orig_conn(pytestconfig):
    """Отдаёт соединение с оригинальной базой."""
    return pytestconfig.ORIG_CONN


@pytest.fixture
def copy_conn(pytestconfig):
    """Отдаёт соединение с копией базы."""
    return pytestconfig.COPY_CONN
