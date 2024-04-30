---
title: "CSI3335 Project Documentation"
output: html_document
---

# CSI3335 Project Group No Name Yest

This README will show you have to run our project on your machine

## Getting Started

### Prerequisites

- Python 3.10 or higher
- MariaDB 11.3 or compatible version

### Setup Instructions

1. Start MariaDB Service:
    - Press Windows Key + R, type services.msc, and press Enter.
    - Scroll to find MariaDB, right-click it, and choose "Start".


2. In the project's main folder, modify the `csi3335sp2023.py` file as needed to match the MySQL user information for database connection.


3. Ensure that the necessary Python packages are installed in the project's virtual environment. You can use command prompt in the current directory and do

   ```bash
   pip install -r requirements.txt
   ```

## Running the Project

1. In the project folder terminal, activate the virtual environment.


2. Start the Flask application by running the following command:
   ```bash
   flask run
   ```
   if the project did not boot up correctly or encounters 404 please to try the following command in the terminal:
    ```bash
    mysql -u root -p -e "DROP DATABASE IF EXISTS nonameyet;" 
    mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS nonameyet;"
    mysql -u root -p nonameyet < nonameyet.sql
   ```
   
3. Open a web browser and navigate to [http://localhost:5000](http://localhost:5000) to access the application.


4. You will be directed to the login page and register page where the default admin credentials are:
   - Username: admin
   - Password: admin123


5. Upon successful login, you will have access to search and view stats based on your permissions.


## Other Files

The project have other files included:

- `lahman_1871-2023_csv`: Contains the baseball data in csv format.
- `project_env`: Contains project compile library.
- `python scripts`: Use to update database by reading csv files.



## Extra Credit
1. **Added all stats of all players and teams from years 1930 all the way up to 2023**

2. **Included a link to each player on the team roster page that takes the user to all of the player's stats throughout the years**