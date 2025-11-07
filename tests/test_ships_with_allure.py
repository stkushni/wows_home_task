import pytest
import sqlite3
import allure
from config import ORIGINAL_DATABASE


class TestShips:

    @staticmethod
    def get_ship_ids():
        with sqlite3.connect(ORIGINAL_DATABASE) as conn:
            cursor = conn.execute("SELECT ship FROM ships")
            return [row[0] for row in cursor.fetchall()]

    @staticmethod
    def compare_related_table(orig_conn, copy_conn, ship_id, ship_part, table_name):
        with allure.step(f"[{ship_id}] Verify {ship_part} reference in ships"):
            orig_val = orig_conn.execute(
                f"SELECT {ship_part} FROM ships WHERE ship = ?", (ship_id,)
            ).fetchone()[0]
            copy_val = copy_conn.execute(
                f"SELECT {ship_part} FROM ships WHERE ship = ?", (ship_id,)
            ).fetchone()[0]

            assert (
                orig_val == copy_val
            ), f"{ship_id} {copy_val} expected {orig_val}, was {copy_val}"

        with allure.step(f"[{ship_id}] Verify {ship_part} parameters in {table_name}"):
            orig_row = orig_conn.execute(
                f"SELECT * FROM {table_name} WHERE {ship_part} IN "
                f"(SELECT {ship_part} FROM ships WHERE ship = ?)",
                (ship_id,),
            ).fetchone()

            copy_row = copy_conn.execute(
                f"SELECT * FROM {table_name} WHERE {ship_part} IN "
                f"(SELECT {ship_part} FROM ships WHERE ship = ?)",
                (ship_id,),
            ).fetchone()

            orig_dict = dict(orig_row)
            copy_dict = dict(copy_row)

            for col in orig_dict.keys():
                if orig_dict[col] != copy_dict[col]:
                    allure.attach(
                        name=f"Diff: {table_name}.{col}",
                        body=(
                            f"Ship: {ship_id}\n"
                            f"Part: {ship_part}\n"
                            f"Column: {col}\n"
                            f"Expected: {orig_dict[col]}\n"
                            f"Actual:   {copy_dict[col]}"
                        ),
                        attachment_type=allure.attachment_type.TEXT,
                    )
                    pytest.fail(
                        f"{ship_id}, {ship_part}.{col}: expected {orig_dict[col]} was {copy_dict[col]}"
                    )

    @pytest.mark.parametrize(
        "ship_part,table_name",
        [
            ("weapon", "weapons"),
            ("engine", "engines"),
            ("hull", "hulls"),
        ],
        ids=["weapons", "engines", "hulls"],
    )
    @pytest.mark.parametrize("ship_id", get_ship_ids.__func__())
    def test_related_tables_equivalence(
        self, ship_id, ship_part, table_name, orig_conn, copy_conn
    ):
        allure.dynamic.parent_suite("Database Integrity")
        allure.dynamic.suite(table_name.capitalize())
        allure.dynamic.sub_suite(f"{table_name.capitalize()} Data Check")
        allure.dynamic.feature(table_name.capitalize())
        allure.dynamic.story(f"Verify {ship_part} linkage for ship {ship_id}")
        allure.dynamic.title(f"Compare {table_name} data for ship '{ship_id}'")

        with allure.step(f"Compare {ship_part} for ship {ship_id}"):
            self.compare_related_table(
                orig_conn, copy_conn, ship_id, ship_part, table_name
            )
