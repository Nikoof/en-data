import os
import pandas as pd

if __name__ == "__main__":
    writer = pd.ExcelWriter("data/xlsx/note_evaluare_nationala.xlsx", engine="openpyxl")

    df = pd.read_csv("data/csv/note_evaluare_nationala.csv")
    df.to_excel(writer, "RO", index="False")

    writer.save()