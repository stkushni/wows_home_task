import sqlite3
import os
import allure
import pytest
import pathlib
import shutil

from config import orig_db

@pytest.fixture(scope="session", autouse=True)
@allure.title("Prepare a copy of the original database with intentional data inconsistencies")
def test_db_path(tmp_path_factory, request):
    with allure.step("Create a copy of the original database."):
        tmp_dir = tmp_path_factory.mktemp("db_copy")
        copy_db = tmp_dir / "world_of_warships_work.db"
        shutil.copyfile(orig_db, copy_db)
        request.config.COPY_DB_PATH = copy_db
        yield str(copy_db)

    with allure.step("Remove copied database"):
        if copy_db.exists():
            os.remove(copy_db)


@pytest.fixture(scope="session", autouse=True)
@allure.title("Start DB connections")
def db_conns(pytestconfig, test_db_path):
    orig_conn = sqlite3.connect(orig_db)
    orig_conn.row_factory = sqlite3.Row
    copy_conn = sqlite3.connect(pytestconfig.COPY_DB_PATH)
    copy_conn.row_factory = sqlite3.Row

    pytestconfig.ORIG_CONN = orig_conn
    pytestconfig.COPY_CONN = copy_conn

    yield
    with allure.step("Close connections"):
        orig_conn.close()
        copy_conn.close()


@pytest.fixture
@allure.title("Get original database connection")
def orig_conn(pytestconfig):
    return pytestconfig.ORIG_CONN


@pytest.fixture
@allure.title("Get copy database connection")
def copy_conn(pytestconfig):
    return pytestconfig.COPY_CONN
