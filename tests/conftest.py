import os
import shutil
import sqlite3
import random
import pytest
import allure

from config import ORIGINAL_DATABASE
from helper import random_int


@pytest.fixture(scope="session")
@allure.title("Create modified copy of the original database")
def test_db_path(tmp_path_factory, request):
    with allure.step("Validate existence of the original database"):
        assert os.path.exists(ORIGINAL_DATABASE), f"Original DB not found: {ORIGINAL_DATABASE}"
        assert os.path.getsize(ORIGINAL_DATABASE) > 0, f"Original DB is empty: {ORIGINAL_DATABASE}"

    with allure.step("Create a copy of the original database"):
        tmp_dir = tmp_path_factory.mktemp("db_copy")
        copy_db = tmp_dir / "world_of_warships_work.db"
        shutil.copyfile(ORIGINAL_DATABASE, copy_db)

        request.config.COPY_DB_PATH = copy_db

    with allure.step("Randomise data in the copied database"):
        conn = sqlite3.connect(copy_db)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        weapons = [f"Weapon-{i}" for i in range(1, 21)]
        hulls = [f"Hull-{i}" for i in range(1, 6)]
        engines = [f"Engine-{i}" for i in range(1, 7)]

        components = {"weapon": weapons, "hull": hulls, "engine": engines}
        ship_ids = [
            r["ship"] for r in cursor.execute("SELECT ship FROM ships").fetchall()
        ]

        for ship_id in ship_ids:
            component = random.choice(list(components.keys()))

            if random.choice([True, False]):
                with allure.step(f"[{ship_id}] Replace {component}"):
                    new_val = random.choice(components[component])
                    cursor.execute(
                        f"UPDATE ships SET {component} = ? WHERE ship = ?",
                        (new_val, ship_id),
                    )

        components = {
            "weapons": [
                "reload_speed",
                "rotation_speed",
                "diameter",
                "power_volley",
                "count",
            ],
            "hulls": ["armor", "type", "capacity"],
            "engines": ["power", "type"],
        }

        for table, columns in components.items():
            cursor.execute(f"SELECT * FROM {table}")
            rows = cursor.fetchall()

            col_names = [desc[0] for desc in cursor.description]
            id_col = col_names[0]

            for row in rows:
                row_id = row[0]
                mutable_cols = columns
                target_col = random.choice(mutable_cols)
                new_value = random_int()

                cursor.execute(
                    f"UPDATE {table} SET {target_col} = ? WHERE {id_col} = ?",
                    (new_value, row_id),
                )

        conn.commit()
        conn.close()

    yield str(copy_db)

    with allure.step("Remove copied database"):
        if copy_db.exists():
            os.remove(copy_db)


@pytest.fixture(scope="session", autouse=True)
@allure.title("Start DB connections")
def db_conns(pytestconfig, test_db_path):
    orig_conn = sqlite3.connect(ORIGINAL_DATABASE)
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
