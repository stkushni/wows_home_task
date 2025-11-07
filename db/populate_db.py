import sqlite3
import random
import os
import sys

from db.ship_service import create_ship
from helper import random_int

DB_NAME = "world_of_warships.db"

def populate_database(db_name=DB_NAME):
    if not os.path.exists(db_name):
        print(f"❌ Database file '{db_name}' not found. Run create_db.py first.")
        sys.exit(1)

    try:
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()

            cursor.executescript(
                """
                DELETE FROM ships;
                DELETE FROM weapons;
                DELETE FROM hulls;
                DELETE FROM engines;
            """
            )
            print("🧹 Tables cleared.")

            for i in range(1, 21):
                cursor.execute(
                    """
                    INSERT INTO weapons (weapon, reload_speed, rotation_speed, diameter, power_volley, count)
                    VALUES (?, ?, ?, ?, ?, ?)
                """,
                    (
                        f"Weapon-{i}",
                        random_int(),
                        random_int(),
                        random_int(),
                        random_int(),
                        random_int(),
                    ),
                )

            for i in range(1, 6):
                cursor.execute(
                    """
                    INSERT INTO hulls (hull, armor, type, capacity)
                    VALUES (?, ?, ?, ?)
                """,
                    (f"Hull-{i}", random_int(), random_int(), random_int()),
                )

            for i in range(1, 7):
                cursor.execute(
                    """
                    INSERT INTO engines (engine, power, type)
                    VALUES (?, ?, ?)
                """,
                    (f"Engine-{i}", random_int(), random_int()),
                )

            weapons = [f"Weapon-{i}" for i in range(1, 21)]
            hulls = [f"Hull-{i}" for i in range(1, 6)]
            engines = [f"Engine-{i}" for i in range(1, 7)]

            for i in range(1, 201):
                create_ship(cursor, f"Ship-{i}", random.choice(weapons),
                        random.choice(hulls),
                        random.choice(engines),)
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
