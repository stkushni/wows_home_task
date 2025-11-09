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
    weapon_names = [row[0] for row in cursor.execute("SELECT weapon FROM weapons")]

    return weapon_names


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
