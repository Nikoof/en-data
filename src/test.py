import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/csv/note_evaluare_nationala.csv", index_col=0)

rd = df["rf"] - df["ri"]
md = df["mf"] - df["mi"]

print(f"Diferenta medie (Lb. Romana): {rd.mean()}")
print(f"Diferenta medie (Matematica): {md.mean()}")