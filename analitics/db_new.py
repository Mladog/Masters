# %%
import pandas as pd
from exams_to_drop import ExamsToDrop
import sqlite3
from examination import Examination

path = "C:/Users/mlado/Desktop//nowa_matryca.xlsx"
data = pd.read_excel(path, header=0)
data_clean = data[["Wiek kalendarzowy ", "Yo-Yo level [ilość]", "Yo-Yo dystans [m]", "Yo-Yo VO2max [ml/kg/min]", "Yo-Yo training load"]]
data_clean["folder_name"] = [f"{index+1}_{row['Nazwisko']}" for index, row in data.iterrows()]
data_clean=data_clean[~data_clean["folder_name"].isin(ExamsToDrop)]

# %%
def create_db(table_name):
    """
    function to create new database
    """
    conn = sqlite3.connect('yoyo.db')
    c = conn.cursor()

    c.execute(f"DROP TABLE IF EXISTS {table_name};")

    create_string = f'''
    CREATE TABLE IF NOT EXISTS {table_name}
    ([competitor_id] INTEGER PRIMARY KEY AUTOINCREMENT, 
    [competitor_foldername] TEXT,
    [competitor_age] FLOAT,
    [yoyo_level] FLOAT,
    [yoyo_dist] FLOAT,
    [yoyo_vo2max] FLOAT,
    [yoyo_training_load] FLOAT'''    

    RRV_data = ["RRV_mean", "RRV_STD", "RRV_RMSSD"]
    groups = ['supine', 'standing', 'supine_vs_standing', 'yoyo']
    HRV_data = ["HRV_mean", "HRV_SDNN", "HRV_RMSSD", "HRVPNN50", "HRV_TRIANG", "HRV_TINN",
                "HRV_VLF", "HRV_LF", "HRV_LFnu", "HRV_HFnu", "HRV_HF", "HRV_LF_HF", "HRV_SD1", "HRV_SD2"]

    params_vector = RRV_data
    for group in groups:
        for parameter in HRV_data:
            params_vector.append(parameter + '_' + group)

    for param in params_vector:
        create_string += ",\n[" + param + "] FLOAT"

    print(create_string)
    c.execute(f"{create_string})")            
                       
    conn.commit()

def insert_into_db(data_source_path, table_name):
    """
    function to insert all data from file to database
    """
    # database file path
    conn = sqlite3.connect('yoyo.db')  
    # connection to db
    c = conn.cursor()

    # import metadata from local file
    path = data_source_path
    data = pd.read_excel(path, header=0)
    data["Nazwisko"] = data["Nazwisko"].str.replace(" ", "")
    # drop unnecessary info
    data_clean = data[["Wiek kalendarzowy ", "Yo-Yo level [ilość]", "Yo-Yo dystans [m]", "Yo-Yo VO2max [ml/kg/min]", "Yo-Yo training load"]]
    data_clean["folder_name"] = [f"{index+1}_{row['Nazwisko']}" for index, row in data.iterrows()]
    if table_name == 'Teenagers':
        data_clean = data_clean[data_clean["Wiek kalendarzowy "]>=11]
    else:
        data_clean = data_clean[data_clean["Wiek kalendarzowy "]<11]

    data_clean=data_clean[~data_clean["folder_name"].isin(ExamsToDrop)]
    # get table columns
    c.execute(f"PRAGMA table_info({table_name})")
    column_names = c.fetchall()
    column_names = [column[1] for column in column_names]

    RRV_data = ["RRV_mean", "RRV_STD", "RRV_RMSSD"]
    groups = ['supine', 'standing', 'supine_vs_standing' ,'yoyo']
    HRV_data = ["HRV_mean", "HRV_SDNN", "HRV_RMSSD", "HRVPNN50", "HRV_TRIANG", "HRV_TINN",
                "HRV_VLF", "HRV_LF", "HRV_HF", "HRV_LF_HF", "HRV_SD1", "HRV_SD2"]
    HRV_data_nonfreq = ["HRV_mean", "HRV_SDNN", "HRV_RMSSD", "HRVPNN50", "HRV_TRIANG", "HRV_TINN",
                        "HRV_SD1", "HRV_SD2"]

    """for competitor in data_clean["folder_name"]:
        ex = Examination(competitor)
        hrv_yoyo = ex.get_hrv(ex.RR_yoyo)
        hrv_standing = ex.get_hrv(ex.RR_standing)
        hrv_supine = ex.get_hrv(ex.RR_supine)

        hrv_keys = ['competitor_foldername']; hrv_exam_data = [competitor]
        for hrv, name in zip ([hrv_supine, hrv_standing, hrv_yoyo], 
                                ["_supine", "_standing", "_yoyo"]):
            
            if hrv["stationarity"] < 0.05:
                hrv_exam_data.extend(hrv["hrv_time"].values())
                hrv_exam_data.extend(hrv["hrv_freq"].values())
                hrv_exam_data.extend(hrv["hrv_nonlinear"].values())
                for parameter in HRV_data:
                    hrv_keys.append(parameter + name)
            else:
                hrv_exam_data.append(hrv["hrv_time"].values())
                hrv_exam_data.append(hrv["hrv_nonlinear"].values())
                for parameter in HRV_data_nonfreq:
                    hrv_keys.append(parameter + name)"""


    # put all values into table
    """values_list = [row for row in data.values]
    for idx in range(len(values_list)):
        query = f"INSERT INTO Competitors ({', '.join(column_names[1:])}) VALUES {tuple(values_list[idx])}"
        c.execute(query)
        conn.commit()

    # print table
    c.execute("SELECT * FROM Competitors")
    print(c.fetchall())"""

# %%
insert_into_db("C:/Users/mlado/Desktop/Mgr_new_data/Matryca_danych2.xlsx", "Teenagers")
#create_db('Teenagers')


# %%
# import metadata from local file
path = "C:/Users/mlado/Desktop/nowa_matryca.xlsx"
data = pd.read_excel(path, header=0)
data["Nazwisko"] = data["Nazwisko"].str.replace(" ", "")
# drop unnecessary info
data_clean = data[["Wiek kalendarzowy ", "Yo-Yo level [ilość]", "Yo-Yo dystans [m]", "Yo-Yo VO2max [ml/kg/min]", "Yo-Yo training load"]]
data_clean["folder_name"] = [f"{index+1}_{row['Nazwisko']}" for index, row in data.iterrows()]
"""if table_name == 'Teenagers':
    data_clean = data_clean[data_clean["Wiek kalendarzowy "]>=11]
else:
    data_clean = data_clean[data_clean["Wiek kalendarzowy "]<11]"""

data_clean=data_clean[~data_clean["folder_name"].isin(ExamsToDrop)]
# get table columns
"""c.execute(f"PRAGMA table_info({table_name})")
column_names = c.fetchall()
column_names = [column[1] for column in column_names]"""

RRV_data = ["RRV_mean", "RRV_STD", "RRV_RMSSD", "EXP_INSP_RATE"]
groups = ['supine', 'standing', 'supine_vs_standing' ,'yoyo']
HRV_data_time = ["HRV_mean", "HRV_SDNN", "HRV_RMSSD", "HRVPNN50", "HRV_TRIANG", "HRV_TINN"]
HRV_data_freq = ["HRV_VLF", "HRV_LF", "HRV_HF", "HRV_LFnu", "HRV_HF_nus", "HRV_LF_HF"]
HRV_data_non = ["HRV_SD1", "HRV_SD2"]


df = pd.DataFrame(data_clean.values.tolist(), columns=["competitor_age",
                            "yoyo_level",
                            "yoyo_dist",
                            "yoyo_vo2max",
                            "yoyo_training_load",
                            "competitor_foldername"], 
                            )

for competitor in data_clean["folder_name"]:
    ex = Examination(competitor)
    hrv_yoyo = ex.get_hrv(ex.RR_yoyo)
    hrv_standing = ex.get_hrv(ex.RR_standing)
    hrv_supine = ex.get_hrv(ex.RR_supine)
    rrv_yoyo = ex.respiration_yoyo.RRV_params
    rrv_standing = ex.respiration_standing.RRV_params
    rrv_supine = ex.respiration_supine.RRV_params

    for hrv, name in zip ([hrv_supine, hrv_standing, hrv_yoyo], 
                            ["_supine", "_standing", "_yoyo"]):
        HRV_time_names = [h + name for h in HRV_data_time]
        HRV_freq_names = [h + name for h in HRV_data_freq]
        HRV_non_names = [h + name for h in HRV_data_non]
        df.loc[df["competitor_foldername"] == competitor, HRV_time_names] = list(hrv["hrv_time"].values())
        if hrv_yoyo["stationarity"] <= 0.05:
            df.loc[df["competitor_foldername"] == competitor, HRV_freq_names] = list(hrv["hrv_freq"].values())
        df.loc[df["competitor_foldername"] == competitor, HRV_non_names] = list(hrv["hrv_nonlinear"].values())

    for rrv, name in zip ([rrv_supine, rrv_standing, rrv_yoyo], 
                            ["_supine", "_standing", "_yoyo"]):
        RRV_names = [h + name for h in RRV_data]
        df.loc[df["competitor_foldername"] == competitor, RRV_names] = list(rrv.values())


    ratio_column_name = '_sup_stand_ratio'
    HRV_time_names = [h + ratio_column_name for h in HRV_data_time]
    HRV_freq_names = [h + ratio_column_name for h in HRV_data_freq]
    HRV_non_names = [h + ratio_column_name for h in HRV_data_non]
    time_ratio = [x1/x2 for x1, x2 in zip(list(hrv_supine["hrv_time"].values()),list(hrv_standing["hrv_time"].values()))]
    freq_ratio = [x1/x2 for x1, x2 in zip(list(hrv_supine["hrv_freq"].values()),list(hrv_standing["hrv_freq"].values()))]
    nonl_ratio = [x1/x2 for x1, x2 in zip(list(hrv_supine["hrv_nonlinear"].values()),list(hrv_standing["hrv_nonlinear"].values()))]
    rrv_ratio = [x1/x2 for x1, x2 in zip(list(rrv_supine.values()),list(rrv_standing.values()))]
    
    df.loc[df["competitor_foldername"] == competitor, HRV_time_names] = time_ratio
    df.loc[df["competitor_foldername"] == competitor, HRV_freq_names] = freq_ratio
    df.loc[df["competitor_foldername"] == competitor, HRV_non_names] = nonl_ratio
    df.loc[df["competitor_foldername"] == competitor, RRV_names] = rrv_ratio


df.to_csv("C:/Users/mlado/Desktop/wyniki_git.csv")

# %%
