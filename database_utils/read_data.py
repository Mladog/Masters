# %%
import pandas as pd
path = "C:/Users/mlado/Desktop/Nowa magisterka/Matryca danych dla Magdy.xlsx"

data = pd.read_excel(path, header=0)

insert_string = ""
data.drop(["Data urodzenia", "Numer paska", "Godzina",
            "Czas trwania Yo-Yo", "Beat rozpoczynający Yo-Yo",
            "Beat kończący Yo-Yo"], axis=1, inplace=True)
columns_of_interest = list(data.columns)

for column in columns_of_interest:
    insert_string += str("'" + str(data[column][0]) + "', ")


# %%
