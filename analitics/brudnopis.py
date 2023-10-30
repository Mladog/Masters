# %%
import pandas as pd

df = pd.read_excel("C:/Users/mlado/Desktop/artefacts_deletion_results.xlsx")
df.drop("Competitor", axis = 1, inplace = True)
df = df.abs()
#df = df.subtract(1, axis = 1)
df = df.multiply(100, axis = 1)
# %%
df.to_excel("C:/Users/mlado/Desktop/artefacts_deletion_results_abs.xlsx")
# %%
