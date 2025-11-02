# import pathlib
# import pytest
# import sqlite3
# from config import orig_db
#
#
# class TestDummy:
#     """
#     Smoke-тест.
#     Проверяет:
#       1. pytest запускает тесты в классе;
#       2. фикстура work_db_path создала копию БД;
#       3. путь к этой базе валиден и файл существует;
#       4. строки из таблиц ships и зависимых таблиц совпадают по оригиналу и копии.
#     """
#
#     def test_hello_world(self, pytestconfig):
#         copy_db_path = pytestconfig.COPY_DB_PATH
#
#         print(f"\nHello World from TestDummy! Using DB copy: {copy_db_path}")
#         assert isinstance(copy_db_path, pathlib.Path), "Путь должен быть pathlib.Path"
#         assert copy_db_path.exists(), f"Файл не найден: {copy_db_path}"
#
#         print("[TestDummy] Копия БД доступна и путь получен из pytestconfig.")
#
#     # -------------------------------------------------------------------------
#     # Общий источник параметров
#     # -------------------------------------------------------------------------
#     @staticmethod
#     def get_ship_ids():
#         """Получает список ship_id из оригинальной базы."""
#         with sqlite3.connect(orig_db) as conn:
#             cursor = conn.execute("SELECT ship FROM ships")
#             return [row[0] for row in cursor.fetchall()]
#
#     # -------------------------------------------------------------------------
#     # Проверка таблицы weapons
#     # -------------------------------------------------------------------------
#     @pytest.mark.parametrize("ship_id", get_ship_ids.__func__())
#     def test_weapon_row_equivalence(self, ship_id, orig_conn, copy_conn):
#         """Сравнивает строки из таблиц ships и weapons."""
#         # ships
#         orig_row = orig_conn.execute(
#             "SELECT weapon FROM ships WHERE ship = ?", (ship_id,)
#         ).fetchone()
#         copy_row = copy_conn.execute(
#             "SELECT weapon FROM ships WHERE ship = ?", (ship_id,)
#         ).fetchone()
#
#         orig_weapon = (orig_row["weapon"])
#         copy_weapon = (copy_row["weapon"])
#
#         assert orig_weapon == copy_weapon, f"{ship_id},{copy_weapon} expected {orig_weapon}, was {copy_weapon}"
#
#         # weapons
#         orig_row = orig_conn.execute(
#             "SELECT * FROM weapons WHERE weapon IN (SELECT weapon FROM ships WHERE ship = ?)",
#             (ship_id,),
#         ).fetchone()
#         copy_row = copy_conn.execute(
#             "SELECT * FROM weapons WHERE weapon IN (SELECT weapon FROM ships WHERE ship = ?)",
#             (ship_id,),
#         ).fetchone()
#
#         orig_weapon_dict = dict(orig_row)
#         copy_weapon_dict = dict(copy_row)
#
#         for col in orig_weapon_dict.keys():
#             if orig_weapon_dict[col] != copy_weapon_dict[col]:
#                 pytest.fail(
#                     f"{ship_id}, {orig_weapon} {col}: expected {orig_weapon_dict[col]} was {copy_weapon_dict[col]}"
#                 )
#
#     # -------------------------------------------------------------------------
#     # Проверка таблицы engines
#     # -------------------------------------------------------------------------
#     @pytest.mark.parametrize("ship_id", get_ship_ids.__func__())
#     def test_engine_row_equivalence(self, ship_id, orig_conn, copy_conn):
#         """Сравнивает строки из таблиц ships и engines."""
#         # ships
#         orig_row = orig_conn.execute(
#             "SELECT engine FROM ships WHERE ship = ?", (ship_id,)
#         ).fetchone()
#         copy_row = copy_conn.execute(
#             "SELECT engine FROM ships WHERE ship = ?", (ship_id,)
#         ).fetchone()
#
#         orig_engine = (orig_row["engine"])
#         copy_engine = (copy_row["engine"])
#
#         assert orig_engine == copy_engine, f"{ship_id},{copy_engine} expected {orig_engine}, was {copy_engine}"
#
#         # engines
#         orig_row = orig_conn.execute(
#             "SELECT * FROM engines WHERE engine IN (SELECT engine FROM ships WHERE ship = ?)",
#             (ship_id,),
#         ).fetchone()
#         copy_row = copy_conn.execute(
#             "SELECT * FROM engines WHERE engine IN (SELECT engine FROM ships WHERE ship = ?)",
#             (ship_id,),
#         ).fetchone()
#
#         orig_engine_dict = dict(orig_row)
#         copy_engine_dict = dict(copy_row)
#
#         for col in orig_engine_dict.keys():
#             if orig_engine_dict[col] != copy_engine_dict[col]:
#                 pytest.fail(
#                     f"{ship_id}, {orig_engine} {col}: expected {orig_engine_dict[col]} was {copy_engine_dict[col]}"
#                 )
#
#     # -------------------------------------------------------------------------
#     # Проверка таблицы hulls
#     # -------------------------------------------------------------------------
#     @pytest.mark.parametrize("ship_id", get_ship_ids.__func__())
#     def test_hull_row_equivalence(self, ship_id, orig_conn, copy_conn):
#         """Сравнивает строки из таблиц ships и hulls."""
#         # ships
#         orig_row = orig_conn.execute(
#             "SELECT hull FROM ships WHERE ship = ?", (ship_id,)
#         ).fetchone()
#         copy_row = copy_conn.execute(
#             "SELECT hull FROM ships WHERE ship = ?", (ship_id,)
#         ).fetchone()
#
#         orig_hull = (orig_row["hull"])
#         copy_hull = (copy_row["hull"])
#
#         assert orig_hull == copy_hull, f"{ship_id},{copy_hull} expected {orig_hull}, was {copy_hull}"
#
#         # hulls
#         orig_row = orig_conn.execute(
#             "SELECT * FROM hulls WHERE hull IN (SELECT hull FROM ships WHERE ship = ?)",
#             (ship_id,),
#         ).fetchone()
#         copy_row = copy_conn.execute(
#             "SELECT * FROM hulls WHERE hull IN (SELECT hull FROM ships WHERE ship = ?)",
#             (ship_id,),
#         ).fetchone()
#
#
#         orig_hull_dict = dict(orig_row)
#         copy_hull_dict = dict(copy_row)
#
#         for col in orig_hull_dict.keys():
#             if orig_hull_dict[col] != copy_hull_dict[col]:
#                 pytest.fail(
#                     f"{ship_id}, {orig_hull} {col}: expected {orig_hull_dict[col]} was {copy_hull_dict[col]}"
#                 )
