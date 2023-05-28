import pandas as pd
from exams_to_drop import ExamsToDrop
import sqlite3
from examination import Examination
from constants import DATA_PATH

path = DATA_PATH

def create_dataframe(path):
    """
    funkcja odpowiedzialna za utworzenie odpowiednio
    przygotowanej ramki danych
    """

    # odczyt danych
    data = pd.read_excel(path, header=0)
    # usuniecie bialych znakow
    data["Nazwisko"] = data["Nazwisko"].str.replace(" ", "")
    # usuniecie z ramki danych o zawodnikach odrzuconych z badania
    data = data[~data_clean["folder_name"].isin(ExamsToDrop)]
    # pobranie jedynie ważnych z punktu widzenia analizy danych
    data_clean = data[["Wiek kalendarzowy ", "Yo-Yo level [ilość]", "Yo-Yo dystans [m]", "Yo-Yo VO2max [ml/kg/min]", "Yo-Yo training load"]]
    # stworzenie kolumny zawierajacej nazwisko oraz indeks kolejnych zawodnikow
    data_clean["folder_name"] = [f"{index+1}_{row['Nazwisko']}" for index, row in data.iterrows()]

    # ustalenie grup kolejnych parametrow
    groups = ['supine', 'standing', 'supine_vs_standing' ,'yoyo']
    # zdefiniowanie nazw kolumn dla parametrow fizjologicznych
    RRV_data = ["RRV_mean", "RRV_STD", "RRV_RMSSD", "RRV_EXP_INSP_RATE", "RRV_BR_REG"]
    HRV_data_time = ["HRV_mean", "HRV_SDNN", "HRV_RMSSD", "HRVPNN50", "HRV_TRIANG", "HRV_TINN"]
    HRV_data_freq = ["HRV_VLF", "HRV_LF", "HRV_HF", "HRV_LFnu", "HRV_HF_nus", "HRV_LF_HF"]
    HRV_data_non = ["HRV_SD1", "HRV_SD2"]

    # utworzenie ramki danych zawierającej dane z pliku lokalnego
    df = pd.DataFrame(data_clean.values.tolist(), columns=["competitor_age",
                                "yoyo_level",
                                "yoyo_dist",
                                "yoyo_vo2max",
                                "yoyo_training_load",
                                "competitor_foldername"], 
                                )

    # petla for wykonujaca sie dla kazdego zawodnika
    for competitor in data_clean["folder_name"]:
        # zaladowanie sygnalu RR i obliczenie parametrow fizjologicznych
        ex = Examination(competitor)
        hrv_yoyo = ex.get_hrv(ex.RR_yoyo)
        hrv_standing = ex.get_hrv(ex.RR_standing)
        hrv_supine = ex.get_hrv(ex.RR_supine)
        rrv_yoyo = ex.respiration_yoyo.RRV_params
        rrv_standing = ex.respiration_standing.RRV_params
        rrv_supine = ex.respiration_supine.RRV_params

        # obliczenie HRV w kazdej z grup
        for hrv, name in zip ([hrv_supine, hrv_standing, hrv_yoyo], 
                                ["_supine", "_standing", "_yoyo"]):
            HRV_time_names = [h + name for h in HRV_data_time]
            HRV_freq_names = [h + name for h in HRV_data_freq]
            HRV_non_names = [h + name for h in HRV_data_non]
            df.loc[df["competitor_foldername"] == competitor, HRV_time_names] = list(hrv["hrv_time"].values())
            if hrv_yoyo["stationarity"] <= 0.05:
                df.loc[df["competitor_foldername"] == competitor, HRV_freq_names] = list(hrv["hrv_freq"].values())
            df.loc[df["competitor_foldername"] == competitor, HRV_non_names] = list(hrv["hrv_nonlinear"].values())

        # obliczenie RRV w kazdej z grup
        for rrv, name in zip ([rrv_supine, rrv_standing, rrv_yoyo], 
                                ["_supine", "_standing", "_yoyo"]):
            RRV_names = [h + name for h in RRV_data]
            df.loc[df["competitor_foldername"] == competitor, RRV_names] = list(rrv.values())

        # obliczenie stosunku wartosci parametrow obliczonych podczas stania i lezenia
        ratio_column_name = '_sup_stand_ratio'
        HRV_time_names = [h + ratio_column_name for h in HRV_data_time]
        HRV_freq_names = [h + ratio_column_name for h in HRV_data_freq]
        HRV_non_names = [h + ratio_column_name for h in HRV_data_non]
        time_ratio = [x1/x2 for x1, x2 in zip(list(hrv_supine["hrv_time"].values()),list(hrv_standing["hrv_time"].values()))]
        freq_ratio = [x1/x2 for x1, x2 in zip(list(hrv_supine["hrv_freq"].values()),list(hrv_standing["hrv_freq"].values()))]
        nonl_ratio = [x1/x2 for x1, x2 in zip(list(hrv_supine["hrv_nonlinear"].values()),list(hrv_standing["hrv_nonlinear"].values()))]
        rrv_ratio = [x1/x2 for x1, x2 in zip(list(rrv_supine.values()),list(rrv_standing.values()))]
        
        # uzupelnienie danych dla danego zawodnika
        df.loc[df["competitor_foldername"] == competitor, HRV_time_names] = time_ratio
        df.loc[df["competitor_foldername"] == competitor, HRV_freq_names] = freq_ratio
        df.loc[df["competitor_foldername"] == competitor, HRV_non_names] = nonl_ratio
        df.loc[df["competitor_foldername"] == competitor, RRV_names] = rrv_ratio

    return df

def create_db_from_dataframe(df):
    """
    funkcja tworzaca nowa baze danych z ramki danych
    """
    conn = sqlite3.connect('yoyo.db')
    df.to_sql('RESULTS', conn, if_exists='replace', index=False)
    conn.close()

def get_data_from_db():
    """
    funkcja pobierajaca dane z bazy
    """
    conn = sqlite3.connect('yoyo.db')
    query = "SELECT * FROM RESULTS"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


