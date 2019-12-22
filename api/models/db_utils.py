from .base import db


def get_table_names():
    """ Get table names in the connected database """
    table_names = db.session.execute("SHOW TABLES").fetchall()
    return [v[0] for v in table_names]


def get_table_columns(table_name):
    """ Get the column names of a table """
    col_names = db.session.execute("SHOW COLUMNS FROM {}".format(table_name)).fetchall()
    return [v[0] for v in col_names]
