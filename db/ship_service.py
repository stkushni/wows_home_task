import sqlite3

from config import ORIGINAL_DATABASE


def create_ship(cursor, ship, weapon, hull, engine):
    cursor.execute(
        """
        INSERT INTO ships (ship, weapon, hull, engine)
        VALUES (?, ?, ?, ?)
    """,
        (
            ship,
            weapon,
            hull,
            engine,
        ),
    )


def get_ships_names(cursor):
    return [row[0] for row in cursor.execute("SELECT ship FROM ships")]


def get_ships_names_with_connection():
    with sqlite3.connect(ORIGINAL_DATABASE) as conn:
        cursor = conn.cursor()
        return get_ships_names(cursor)


def get_ship_component_name(cursor, ship_part, ship_name):
    return cursor.execute(
        f"SELECT {ship_part} FROM ships WHERE ship = ?", (ship_name,)
    ).fetchone()[0]


def change_ship_component(cursor, ship, component, component_name):
    cursor.execute(
        f"UPDATE ships SET {component} = ? WHERE ship = ?",
        (component_name, ship),
    )


def delete_all_ships(cursor):
    cursor.executescript(
        """
        DELETE FROM ships;
    """
    )
