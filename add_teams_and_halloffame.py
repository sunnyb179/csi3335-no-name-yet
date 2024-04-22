import pandas as pd
from sqlalchemy import create_engine

# create a database connection
try:
    engine = create_engine('mysql+mysqlconnector://root:nguyen12@localhost/nonameyet')
    print("Connected to the database successfully.")
except Exception as e:
    print("Error connecting to database:", e)

# load your CSV file and handle exceptions
try:
    df_teams = pd.read_csv('C:\\Users\\vince\\Downloads\\halloffame\\lahman_1871-2023_csv\\Teams.csv')
    df_halloffame = pd.read_csv('C:\\Users\\vince\\Downloads\\halloffame\\lahman_1871-2023_csv\\HallOfFame.csv')
    print("CSV files loaded successfully.")
except FileNotFoundError as e:
    print("File not found:", e)
except Exception as e:
    print("Error loading CSV files:", e)

# import data into your database and handle potential SQL errors
try:
    df_teams.to_sql('teams', con=engine, if_exists='append', index=False)
    df_halloffame.to_sql('halloffame', con=engine, if_exists='append', index=False)
    print("Data imported into the database successfully.")
except Exception as e:
    print("Error during data import:", e)
