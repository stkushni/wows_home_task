import sqlite3
import random
import os
import sys

DB_NAME = "world_of_warships.db"


def random_int():
    """Возвращает случайное число в диапазоне 1–20."""
    return random.randint(1, 20)


def populate_database(db_name=DB_NAME):
    """Очищает и заполняет SQLite базу случайными данными в соответствии с ТЗ."""

    # Проверяем наличие базы
    if not os.path.exists(db_name):
        print(f"❌ Database file '{db_name}' not found. Run create_db.py first.")
        sys.exit(1)

    try:
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()

            # Очистка таблиц
            cursor.executescript(
                """
                DELETE FROM ships;
                DELETE FROM weapons;
                DELETE FROM hulls;
                DELETE FROM engines;
            """
            )
            print("🧹 Tables cleared.")

            # ---- 1. weapons ----
            for i in range(1, 21):  # 20 записей
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

            # ---- 2. hulls ----
            for i in range(1, 6):  # 5 записей
                cursor.execute(
                    """
                    INSERT INTO hulls (hull, armor, type, capacity)
                    VALUES (?, ?, ?, ?)
                """,
                    (f"Hull-{i}", random_int(), random_int(), random_int()),
                )

            # ---- 3. engines ----
            for i in range(1, 7):  # 6 записей
                cursor.execute(
                    """
                    INSERT INTO engines (engine, power, type)
                    VALUES (?, ?, ?)
                """,
                    (f"Engine-{i}", random_int(), random_int()),
                )

            # ---- 4. ships ----
            weapons = [f"Weapon-{i}" for i in range(1, 21)]
            hulls = [f"Hull-{i}" for i in range(1, 6)]
            engines = [f"Engine-{i}" for i in range(1, 7)]

            for i in range(1, 201):  # 200 записей
                cursor.execute(
                    """
                    INSERT INTO ships (ship, weapon, hull, engine)
                    VALUES (?, ?, ?, ?)
                """,
                    (
                        f"Ship-{i}",
                        random.choice(weapons),
                        random.choice(hulls),
                        random.choice(engines),
                    ),
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
