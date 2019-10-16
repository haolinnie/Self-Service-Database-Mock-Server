import pandas as pd

DATA_PATH = 'data/deid_data_sample.xlsx'


def loadExcel(path):
    excel_file = pd.ExcelFile(path)
    sheet_names = excel_file.sheet_names
    tables = dict()
    for name in sheet_names:
        tables[name] = excel_file.parse(name)
    return tables, sheet_names


def loadData():
    return loadExcel(DATA_PATH)


if __name__ == '__main__':

    tables, table_names= loadExcel(DATA_PATH)
    breakpoint()

