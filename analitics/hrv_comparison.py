# %%
from examination import Examination
from exams_to_drop import ExamsToDrop
import pandas as pd

path = "C:/Users/mlado/Desktop/nowa_matryca.xlsx"
data = pd.read_excel(path, header=0)
data_clean = data[["Nazwisko", "Wiek kalendarzowy ", "Yo-Yo level [ilość]", "Yo-Yo dystans [m]", "Yo-Yo VO2max [ml/kg/min]", "Yo-Yo training load"]]
data_clean["Nazwisko"] = data_clean["Nazwisko"].str.replace(" ", "")
data_clean["folder_name"] = [f"{index+1}_{row['Nazwisko']}" for index, row in data.iterrows()]
data_clean["folder_name"]= data_clean["folder_name"].str.replace(" ", "")
data_clean = data_clean[~data_clean["folder_name"].isin(ExamsToDrop)]

difference_percentages_yoyo = pd.DataFrame(columns=["Competitor", "Key", "Difference_Percentage"])
difference_percentages_yoyo_clean = pd.DataFrame(columns=["Competitor", "Key", "Difference_Percentage"])

for competitor in data_clean["folder_name"]:
    print(competitor)
    ex_clean = Examination(competitor)
    ex = Examination(competitor, False)
    hrv_yoyo_clean = ex_clean.get_hrv(ex_clean.RR_yoyo)
    del hrv_yoyo_clean["stationarity"]
    hrv_yoyo = ex.get_hrv(ex.RR_yoyo)
    del hrv_yoyo["stationarity"]

    # Iterate over the keys of hrv_yoyo
    for key in hrv_yoyo:
        nested_dict_yoyo = hrv_yoyo[key]
        nested_dict_yoyo_clean = hrv_yoyo_clean[key]
        
        # Iterate over the keys and values of the nested dictionary
        for nested_key, nested_value in nested_dict_yoyo.items():
            # Create a new row dictionary for the dataframe
            row_dict = {
                "Competitor": competitor,
                "Key": f"{key}_{nested_key}",
                "Difference_Percentage": nested_value
            }
            
            # Append the row dictionary to the dataframe
            difference_percentages_yoyo = pd.concat([difference_percentages_yoyo, pd.DataFrame([row_dict])], ignore_index=True)

        # Iterate over the keys and values of the nested dictionary
        for nested_key, nested_value in nested_dict_yoyo_clean.items():
            # Create a new row dictionary for the dataframe
            row_dict = {
                "Competitor": competitor,
                "Key": f"{key}_{nested_key}",
                "Difference_Percentage": nested_value
            }
            
            # Append the row dictionary to the dataframe
            difference_percentages_yoyo_clean = pd.concat([difference_percentages_yoyo_clean, pd.DataFrame([row_dict])], ignore_index=True)

# %%
pivoted_df_yoyo = difference_percentages_yoyo.pivot(index="Competitor", columns="Key", values="Difference_Percentage")
pivoted_df_yoyo_clean = difference_percentages_yoyo_clean.pivot(index="Competitor", columns="Key", values="Difference_Percentage")

difference = pivoted_df_yoyo.subtract(pivoted_df_yoyo_clean, axis = 1)
difference_percentage = difference.divide(pivoted_df_yoyo)

#difference_percentage.drop("Competitor", axis = 1, inplace = True)
difference_percentage = difference_percentage.abs()
difference_percentage = difference_percentage.multiply(100)
difference_percentage.to_excel("C:/Users/mlado/Desktop/artefacts_deletion_results_good.xlsx")



# %%
