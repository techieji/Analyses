import xlwings as xw
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path

df = pd.read_csv(Path(__file__).parent / 'all.csv')

def main():
    wb = xw.Book.caller()
    sheet = wb.sheets[0]
    if sheet["A1"].value == "Hello xlwings!":
        sheet["A1"].value = "Bye xlwings!"
    else:
        sheet["A1"].value = "Hello xlwings!"

@xw.func
def hello(name):
    return f"Hello {name}!"

@xw.func
def get_from_all(data, title):
    ret = []
    df_dict = df.set_index('name')[title]
    for x in data:
        try:
            ret.append([df_dict[x]])
        except KeyError:
            ret.append([0])
        except AttributeError:
            if x is None:
                break
    return ret

@xw.func
def get_pass_rate(data):
    # ret = []
    # df_dict = df.set_index('name')['Pass Rate']
    return get_from_all(data, 'Pass Rate')

@xw.func
def adjust(col):
    ret = []
    for x in col:
        try:
            ret.append([" ".join(x.split(' ')[:2]).title()])
        except AttributeError:
            if x is None:
                break
    return ret

@xw.func
def correct(col1, col2):
    return [[x if x else (y if y else 0)] for x, y in zip(col1, col2)]

@xw.func
def divide(col1, col2):
    return [[int(x) / int(y)] for x, y in zip(col1, col2)]

if __name__ == "__main__":
    # xw.Book("education.xlsm").set_mock_caller()
    # main()
    print(df_dict)
