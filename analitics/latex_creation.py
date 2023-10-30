# %%
import pandas as pd
from exams_to_drop import ExamsToDrop
df = pd.read_excel("C:/Users/mlado/Desktop/raport_z_poprawek_artefaktow.xlsx")
# %%
df = df[~df["competitor"].isin(ExamsToDrop)]
df.drop("competitor", axis=1, inplace=True)
df.astype(int)
df.to_latex("output.tex")

# %%
