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
        ))
