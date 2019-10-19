import sqlite3

db_path = "data/deid_data.db"


def get_db():
    return sqlite3.connect(db_path)


def execute_sql(cmd):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute(cmd)
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return data

