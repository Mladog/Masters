# %%
import pandas as pd
df = pd.read_excel("C:/Users/mlado/Desktop/raport_z_poprawek_artefaktow.xlsx")
df.drop("competitor", axis=1, inplace=True)
df.astype(int)
df.to_latex("output.tex")

# %%
