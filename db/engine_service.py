import random
from helper import random_int


def create_engine(cursor, engine, power, type):
    cursor.execute(
        """
        INSERT INTO engines (engine, power, type)
        VALUES (?, ?, ?)
    """,
        (engine, power, type),
    )


def get_engines_names(cursor):
    engines_names = [row[0] for row in cursor.execute("SELECT engine FROM engines")]

    return engines_names


def change_random_engine_parameter(cursor, engine):
    parameter = random.choice(("power", "type"))
    cursor.execute(
        f"UPDATE engines SET {parameter} = ? WHERE engine = ?",
        (random_int(), engine),
    )


def delete_all_engines(cursor):
    cursor.executescript(
        """
        DELETE FROM engines;
    """
    )
