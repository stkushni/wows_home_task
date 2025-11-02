import pytest
import sqlite3
from config import orig_db


class TestShips:
    """
    Проверяет эквивалентность данных между оригинальной и копией БД
    для зависимых таблиц ships → (weapons, engines, hulls).
    """

    # -------------------------------------------------------------------------
    # Общий источник параметров ship_id
    # -------------------------------------------------------------------------
    @staticmethod
    def get_ship_ids():
        """Получает список ship_id из оригинальной базы."""
        with sqlite3.connect(orig_db) as conn:
            cursor = conn.execute("SELECT ship FROM ships")
            return [row[0] for row in cursor.fetchall()]

    # -------------------------------------------------------------------------
    # Универсальный метод сравнения зависимой таблицы
    # -------------------------------------------------------------------------
    @staticmethod
    def compare_related_table(orig_conn, copy_conn, ship_id, rel_field, table_name):
        """Сравнивает строки таблицы ships и зависимой таблицы (weapons/engines/hulls)."""

        # 1️⃣ Проверка: ссылка из ships совпадает
        orig_val = orig_conn.execute(
            f"SELECT {rel_field} FROM ships WHERE ship = ?", (ship_id,)
        ).fetchone()[rel_field]
        copy_val = copy_conn.execute(
            f"SELECT {rel_field} FROM ships WHERE ship = ?", (ship_id,)
        ).fetchone()[rel_field]

        assert (
            orig_val == copy_val
        ), f"{ship_id},{copy_val} expected {orig_val}, was {copy_val}"

        # 2️⃣ Проверка: совпадение строк в зависимой таблице
        orig_row = orig_conn.execute(
            f"SELECT * FROM {table_name} WHERE {rel_field} = ?", (orig_val,)
        ).fetchone()
        copy_row = copy_conn.execute(
            f"SELECT * FROM {table_name} WHERE {rel_field} = ?", (copy_val,)
        ).fetchone()

        orig_dict = dict(orig_row)
        copy_dict = dict(copy_row)

        for col in orig_dict.keys():
            if orig_dict[col] != copy_dict[col]:
                pytest.fail(
                    f"{ship_id}, {orig_val} {col}: expected {orig_dict[col]} was {copy_dict[col]}"
                )

    # -------------------------------------------------------------------------
    # Параметризованный тест для всех зависимостей
    # -------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "rel_field,table_name",
        [
            ("weapon", "weapons"),
            ("engine", "engines"),
            ("hull", "hulls"),
        ],
        ids=["weapons", "engines", "hulls"],
    )
    @pytest.mark.parametrize("ship_id", get_ship_ids.__func__())
    def test_related_tables_equivalence(
        self, ship_id, rel_field, table_name, orig_conn, copy_conn
    ):
        """Сравнивает строки из ships и зависимых таблиц (weapons, engines, hulls)."""
        self.compare_related_table(orig_conn, copy_conn, ship_id, rel_field, table_name)
