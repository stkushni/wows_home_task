import random

from helper import random_int


def create_hull(cursor, hull, armor, type, capacity):
    cursor.execute(
        """
        INSERT INTO hulls (hull, armor, type, capacity)
        VALUES (?, ?, ?, ?)
    """,
        (hull, armor, type, capacity),
    )


def get_hulls_names(cursor):
    hulls_names = [row[0] for row in cursor.execute("SELECT hull FROM hulls")]

    return hulls_names


def change_random_hull_parameter(cursor, hull):
    parameter = random.choice(("armor", "type", "capacity"))
    cursor.execute(
        f"UPDATE hulls SET {parameter} = ? WHERE hull = ?",
        (random_int(), hull),
    )


def delete_all_hulls(cursor):
    cursor.executescript(
        """
        DELETE FROM hulls;
    """
    )
