from .db_op import *


def get_table_names():
    # Load all table names
    with get_db() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        table_names = list(map(lambda x: x[0], cursor.fetchall()))
        cursor.close()
    return table_names


def get_table_columns(table_name):
    with get_db() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM {}".format(table_name))
        col_names = list(map(lambda x: x[0], cursor.description))
        cursor.close()
    return col_names

