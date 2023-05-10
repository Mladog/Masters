import sqlite3
import pandas as pd

def create_db():
    """
    function to create new database
    """
    conn = sqlite3.connect('yoyo.db')
    c = conn.cursor()

    c.execute("DROP TABLE IF EXISTS Competitors;")

    c.execute('''
            CREATE TABLE IF NOT EXISTS Competitors
            ([competitor_id] INTEGER PRIMARY KEY AUTOINCREMENT, 
            [competitor_name] TEXT,
            [competitor_surname] TEXT,
            [competitor_birthyear] FLOAT,
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
    """
    function to insert all data from file to database
    """
    # database file path
    conn = sqlite3.connect('yoyo.db')  
    # connection to db
    c = conn.cursor()

    # import metadata from local file
    path = "C:/Users/mlado/Desktop/Nowa magisterka/Matryca danych dla Magdy.xlsx"
    data = pd.read_excel(path, header=0)
    # drop unnecessary info
    data.drop(["Data urodzenia", "Numer paska", "Godzina",
               "Czas trwania Yo-Yo", "Beat rozpoczynający Yo-Yo",
               "Beat kończący Yo-Yo"], axis=1, inplace=True)

    # get table columns
    c.execute("PRAGMA table_info(Competitors)")
    column_names = c.fetchall()
    column_names = [column[1] for column in column_names]

    # put all values into table
    values_list = [row for row in data.values]
    for idx in range(len(values_list)):
        query = f"INSERT INTO Competitors ({', '.join(column_names[1:])}) VALUES {tuple(values_list[idx])}"
        c.execute(query)
        conn.commit()

    # print table
    c.execute("SELECT * FROM Competitors")
    print(c.fetchall())

def select_from_db():
    conn = sqlite3.connect('yoyo.db')  # Specify the correct database file path
    c = conn.cursor()
    c.execute("SELECT * FROM Competitors")
    print(c.fetchall())


if __name__ == "__main__":
    #create_db()
    #insert_into_db()
    select_from_db()