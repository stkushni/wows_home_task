import sqlite3
import random
import os
import sys
from db.engine_service import delete_all_engines, create_engine, get_engines_names
from db.hull_service import delete_all_hulls, create_hull, get_hulls_names
from db.ship_service import create_ship, delete_all_ships
from db.weapon_service import delete_all_weapons, create_weapon, get_weapons_names
from helper import random_int

DB_NAME = "world_of_warships.db"


def populate_database(db_name=DB_NAME):
    if not os.path.exists(db_name):
        print(f"❌ Database file '{db_name}' not found. Run create_db.py first.")
        sys.exit(1)

    try:
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            conn.row_factory = sqlite3.Row
            delete_all_ships(cursor)
            delete_all_weapons(cursor)
            delete_all_hulls(cursor)
            delete_all_engines(cursor)
            print("🧹 Tables cleared.")

            for i in range(1, 21):
                create_weapon(
                    cursor,
                    f"Weapon-{i}",
                    random_int(),
                    random_int(),
                    random_int(),
                    random_int(),
                    random_int(),
                )

            for i in range(1, 6):
                create_hull(
                    cursor, f"Hull-{i}", random_int(), random_int(), random_int()
                )

            for i in range(1, 7):
                create_engine(cursor, f"Engine-{i}", random_int(), random_int())

            weapons = get_weapons_names(cursor)
            hulls = get_hulls_names(cursor)
            engines = get_engines_names(cursor)

            for i in range(1, 201):
                create_ship(
                    cursor,
                    f"Ship-{i}",
                    random.choice(weapons),
                    random.choice(hulls),
                    random.choice(engines),
                )
            conn.commit()
            print(f"✅ Database '{db_name}' successfully populated with random data!")

    except sqlite3.OperationalError as e:
        print(f"❌ SQLite operational error: {e}")
        sys.exit(1)

    except sqlite3.IntegrityError as e:
        print(f"❌ Integrity constraint failed: {e}")
        sys.exit(1)

    except sqlite3.Error as e:
        print(f"❌ General SQLite error: {e}")
        sys.exit(1)

    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    populate_database()
