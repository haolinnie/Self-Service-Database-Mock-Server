import sqlite3

db_path = "data/deid_data.db"


def get_db():
    return sqlite3.connect(db_path)

