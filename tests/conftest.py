import os
import shutil
import sqlite3
import random
import pytest
import allure

from config import ORIGINAL_DATABASE
from db.engine_service import get_engines_names, change_random_engine_parameter
from db.hull_service import get_hulls_names, change_random_hull_parameter
from db.ship_service import get_ships_names, change_ship_component
from db.weapon_service import get_weapons_names, change_random_weapon_parameter


@pytest.fixture(scope="session")
@allure.title("Create modified copy of the original database")
def test_db_path(tmp_path_factory, request):
    with allure.step("Validate existence of the original database"):
        assert os.path.exists(
            ORIGINAL_DATABASE
        ), f"Original DB not found: {ORIGINAL_DATABASE}"
        assert (
            os.path.getsize(ORIGINAL_DATABASE) > 0
        ), f"Original DB is empty: {ORIGINAL_DATABASE}"

    with allure.step("Create a copy of the original database"):
        tmp_dir = tmp_path_factory.mktemp("db_copy")
        copy_db = tmp_dir / "world_of_warships_work.db"
        shutil.copyfile(ORIGINAL_DATABASE, copy_db)

        request.config.COPY_DB_PATH = copy_db

    with allure.step("Randomise data in the copied database"):
        conn = sqlite3.connect(copy_db)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        weapons = get_weapons_names(cursor)
        hulls = get_hulls_names(cursor)
        engines = get_engines_names(cursor)

        components = {"weapon": weapons, "hull": hulls, "engine": engines}

        for ship in get_ships_names(cursor):
            component = random.choice(list(components.keys()))

            if random.choice([True, False]):
                with allure.step(f"[{ship}] Replace {component}"):
                    change_ship_component(
                        cursor, ship, component, random.choice(components[component])
                    )

        for engine in get_engines_names(cursor):
            change_random_engine_parameter(cursor, engine)

        for hull in get_hulls_names(cursor):
            change_random_hull_parameter(cursor, hull)

        for weapon in get_weapons_names(cursor):
            change_random_weapon_parameter(cursor, weapon)

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
