import sqlite3
from excel_op import loadData

db_path = "data/deid_data.db"


def get_db():
    return sqlite3.connect(db_path)


def excel_to_db():
    tables, table_names = loadData()
    connection = get_db()

    for name in table_names:
        print("Adding table "+name+" to db.")
        tables[name].to_sql(name, con=connection)
    
    connection.commit()


if __name__ == "__main__":
    excel_to_db()
