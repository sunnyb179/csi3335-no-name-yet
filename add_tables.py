import pandas as pd
from sqlalchemy import create_engine

# create a database connection
try:
    engine = create_engine('mysql+mysqlconnector://root:nguyen12@localhost/nonameyet')
    print("Connected to the database successfully.")
except Exception as e:
    print("Error connecting to database:", e)

# load CSV files with specified encoding and handle exceptions
try:
    df_teams = pd.read_csv('lahman_1871-2023_csv\\Teams.csv', encoding='ISO-8859-1')
    df_halloffame = pd.read_csv('lahman_1871-2023_csv\\HallOfFame.csv', encoding='ISO-8859-1')
    df_batting = pd.read_csv('lahman_1871-2023_csv\\Batting.csv', encoding='ISO-8859-1')
    df_pitching = pd.read_csv('lahman_1871-2023_csv\\Pitching.csv', encoding='ISO-8859-1')
    df_people = pd.read_csv('lahman_1871-2023_csv\\People.csv', encoding='ISO-8859-1')
    df_fielding = pd.read_csv('lahman_1871-2023_csv\\Fielding.csv', encoding='ISO-8859-1')
    print("CSV files loaded successfully.")
except FileNotFoundError as e:
    print("File not found:", e)
except Exception as e:
    print("Error loading CSV files:", e)

# import data into database and handle potential SQL errors
try:
    df_teams.to_sql('teams', con=engine, if_exists='append', index=False)
    df_halloffame.to_sql('halloffame', con=engine, if_exists='append', index=False)
    df_batting.to_sql('batting', con=engine, if_exists='append', index=False)
    df_pitching.to_sql('pitching', con=engine, if_exists='append', index=False)
    df_people.to_sql('people', con=engine, if_exists='append', index=False)
    df_fielding.to_sql('fielding', con=engine, if_exists='append', index=False)
    print("Data imported into the database successfully.")
except Exception as e:
    print("Error during data import:", e)
