import sqlite3
import sys

DB_NAME = "world_of_warships.db"


def create_database(db_name=DB_NAME):
    """Создаёт SQLite-базу данных с таблицами для тестового задания World of Warships."""
    try:
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
            CREATE TABLE IF NOT EXISTS weapons (
                weapon TEXT PRIMARY KEY,
                reload_speed INTEGER,
                rotation_speed INTEGER,
                diameter INTEGER,
                power_volley INTEGER,
                count INTEGER
            );
            """
            )

            cursor.execute(
                """
            CREATE TABLE IF NOT EXISTS hulls (
                hull TEXT PRIMARY KEY,
                armor INTEGER,
                type INTEGER,
                capacity INTEGER
            );
            """
            )

            cursor.execute(
                """
            CREATE TABLE IF NOT EXISTS engines (
                engine TEXT PRIMARY KEY,
                power INTEGER,
                type INTEGER
            );
            """
            )

            cursor.execute(
                """
            CREATE TABLE IF NOT EXISTS ships (
                ship TEXT PRIMARY KEY,
                weapon TEXT,
                hull TEXT,
                engine TEXT,
                FOREIGN KEY (weapon) REFERENCES weapons(weapon),
                FOREIGN KEY (hull) REFERENCES hulls(hull),
                FOREIGN KEY (engine) REFERENCES engines(engine)
            );
            """
            )

            conn.commit()
            print(f"✅ Database '{db_name}' created successfully.")

    except sqlite3.Error as e:
        print(f"❌ SQLite error while creating database: {e}")
        sys.exit(1)

    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    create_database()
