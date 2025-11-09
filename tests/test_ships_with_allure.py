import pytest
import allure

from db.engine_service import get_engine_params
from db.hull_service import get_hull_params
from db.ship_service import get_ship_component_name, get_ships_names_with_connection
from db.weapon_service import get_weapon_params


class TestShips:

    @staticmethod
    def compare_related_table(
        orig_cursor, copy_cursor, ship_name, ship_component, table_name
    ):
        with allure.step(f"[{ship_name}] Verify {ship_component} reference in ships"):
            original_component = get_ship_component_name(
                orig_cursor, ship_component, ship_name
            )
            copy_componet = get_ship_component_name(
                copy_cursor, ship_component, ship_name
            )

            assert (
                original_component == copy_componet
            ), f"{ship_name} {copy_componet} expected {original_component}, was {copy_componet}"

        table_dispatch = {
            "weapons": get_weapon_params,
            "hulls": get_hull_params,
            "engines": get_engine_params,
        }

        parser = table_dispatch.get(table_name)
        if not parser:
            raise ValueError(f"Unsupported table: {table_name}")

        with allure.step(
            f"[{ship_name}] Verify {ship_component} parameters in {table_name}"
        ):
            orig_dict = parser(orig_cursor, ship_component, ship_name)
            copy_dict = parser(copy_cursor, ship_component, ship_name)

            for col in orig_dict.keys():
                if orig_dict[col] != copy_dict[col]:
                    allure.attach(
                        name=f"Diff: {table_name}.{col}",
                        body=(
                            f"Ship: {ship_name}\n"
                            f"Part: {ship_component}\n"
                            f"Column: {col}\n"
                            f"Expected: {orig_dict[col]}\n"
                            f"Actual:   {copy_dict[col]}"
                        ),
                        attachment_type=allure.attachment_type.TEXT,
                    )
                    pytest.fail(
                        f"{ship_name}, {original_component} {col}: expected {orig_dict[col]}, was {copy_dict[col]}"
                    )

    @pytest.mark.parametrize(
        "ship_component,table_name",
        [
            ("weapon", "weapons"),
            ("engine", "engines"),
            ("hull", "hulls"),
        ],
        ids=["weapons", "engines", "hulls"],
    )
    @pytest.mark.parametrize("ship_name", get_ships_names_with_connection())
    def test_related_tables_equivalence(
        self, ship_name, ship_component, table_name, orig_cursor, copy_cursor
    ):
        allure.dynamic.parent_suite("Database Integrity")
        allure.dynamic.suite(table_name.capitalize())
        allure.dynamic.sub_suite(f"{table_name.capitalize()} Data Check")
        allure.dynamic.feature(table_name.capitalize())
        allure.dynamic.story(f"Verify {ship_component} linkage for ship {ship_name}")
        allure.dynamic.title(f"Compare {table_name} data for ship '{ship_name}'")

        with allure.step(f"Compare {ship_component} for ship {ship_name}"):
            self.compare_related_table(
                orig_cursor, copy_cursor, ship_name, ship_component, table_name
            )
