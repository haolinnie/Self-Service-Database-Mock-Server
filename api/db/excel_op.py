import os
import pandas as pd
from db_op import get_db

DATA_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "../data/deid_data_sample.xlsx"
)


def loadExcel(path):
    excel_file = pd.ExcelFile(path)
    sheet_names = excel_file.sheet_names
    tables = dict()
    for name in sheet_names:
        tables[name] = excel_file.parse(name)
    return tables, sheet_names


def loadData():
    return loadExcel(DATA_PATH)


def excel_to_db():
    tables, table_names = loadData()
    connection = get_db()

    for name in table_names:
        print("Adding table " + name + " to db.")
        tables[name].to_sql(name, con=connection)

    connection.commit()


if __name__ == "__main__":
    excel_to_db()
