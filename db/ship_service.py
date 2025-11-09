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
    ship_names = [row[0] for row in cursor.execute("SELECT ship FROM ships")]

    return ship_names


def change_ship_component(cursor, ship, component, component_name):
    cursor.execute(
        f"UPDATE ships SET {component} = ? WHERE ship = ?",
        (component_name, ship),
    )

def get_ship_ids():
    with sqlite3.connect(ORIGINAL_DATABASE) as conn:
        cursor = conn.execute("SELECT ship FROM ships")
        return [row[0] for row in cursor.fetchall()]


def delete_all_ships(cursor):
    cursor.executescript(
        """
        DELETE FROM ships;
    """
    )
