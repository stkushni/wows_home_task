import random

from helper import random_int


def create_weapon(
    cursor, weapon, reload_speed, rotation_speed, diameter, power_volley, count
):
    cursor.execute(
        """
        INSERT INTO weapons (weapon, reload_speed, rotation_speed, diameter, power_volley, count)
        VALUES (?, ?, ?, ?, ?, ?)
    """,
        (
            weapon,
            reload_speed,
            rotation_speed,
            diameter,
            power_volley,
            count,
        ),
    )


def get_weapons_names(cursor):
    return [row[0] for row in cursor.execute("SELECT weapon FROM weapons")]


def get_weapon_params(cursor, weapon_name, ship_name):
    return cursor.execute(
        f"SELECT * FROM weapons WHERE {weapon_name} IN "
        f"(SELECT {weapon_name} FROM ships WHERE ship = ?)",
        (ship_name,),
    ).fetchone()


def change_random_weapon_parameter(cursor, weapon):
    parameter = random.choice(
        ("reload_speed", "rotation_speed", "diameter", "power_volley", "count")
    )
    cursor.execute(
        f"UPDATE weapons SET {parameter} = ? WHERE weapon = ?",
        (random_int(), weapon),
    )


def delete_all_weapons(cursor):
    cursor.executescript(
        """
        DELETE FROM weapons;
    """
    )
