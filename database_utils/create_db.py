import sqlite3
import pandas as pd

def create_db():
    conn = sqlite3.connect('yoyo.db')  # Specify the correct database file path
    c = conn.cursor()

    c.execute("DROP TABLE IF EXISTS Competitors;")

    c.execute('''
            CREATE TABLE IF NOT EXISTS Competitors
            ([competitor_id] INTEGER PRIMARY KEY AUTOINCREMENT, 
            [competitor_name] TEXT,
            [competitor_surname] TEXT,
            [competitor_birthyear] TEXT,
            [competitor_height] FLOAT,
            [competitor_weight] FLOAT,
            [competitor_bmi] FLOAT,
            [competitor_fat] FLOAT,
            [competitor_muscle] FLOAT,
            [competitor_metabolism] FLOAT,
            [training_load] FLOAT,
            [yoyo_resut] FLOAT,
            [speed_5_1] FLOAT,
            [speed_10_1] FLOAT,
            [speed_30_1] FLOAT,
            [speed_5_2] FLOAT,
            [speed_10_2] FLOAT,
            [speed_30_2] FLOAT,
            [speed_5_3] FLOAT,
            [speed_10_3] FLOAT,
            [speed_30_3] FLOAT,
            [speed_5_4] FLOAT,
            [speed_10_4] FLOAT,
            [speed_30_4] FLOAT,
            [speed_5_5] FLOAT,
            [speed_10_5] FLOAT,
            [speed_30_5] FLOAT,
            [speed_5_6] FLOAT,
            [speed_10_6] FLOAT,
            [speed_30_6] FLOAT,
            [speed_5_7] FLOAT,
            [speed_10_7] FLOAT,
            [speed_30_7] FLOAT,
            [jamar_right_1] FLOAT,
            [kforce_right_1] FLOAT,
            [jamar_left_1] FLOAT,
            [kforce_left_1] FLOAT,
            [jamar_right_2] FLOAT,
            [kforce_right_2] FLOAT,
            [jamar_left_2] FLOAT,
            [kforce_left_2] FLOAT,
            [examination_path] TEXT)
            ''')            
                       
    conn.commit()



def insert_into_db():
    conn = sqlite3.connect('yoyo.db')  # Specify the correct database file path
    c = conn.cursor()
    path = "C:/Users/mlado/Desktop/Nowa magisterka/Matryca danych dla Magdy.xlsx"
    data = pd.read_excel(path, header=0)
    data.drop(["Data urodzenia", "Numer paska", "Godzina",
               "Czas trwania Yo-Yo", "Beat rozpoczynający Yo-Yo",
               "Beat kończący Yo-Yo"], axis=1, inplace=True)

    c.execute("PRAGMA table_info(Competitors)")
    column_names = c.fetchall()
    column_names = [column[1] for column in column_names]

    values_list = [row for row in data.values]
    for idx in range(len(values_list)):
        val0 = tuple(values_list[idx])
        val0 = val0 + ('path',)

        query = f"INSERT INTO Competitors ({', '.join(column_names[1:])}) VALUES {val0}"

        c.execute(query)
        conn.commit()

    c.execute("SELECT * FROM Competitors")
    print(c.fetchall())

if __name__ == "__main__":
    #create_db()
    insert_into_db()
