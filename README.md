---
title: "CSI3335 Project Documentation"
output: html_document
---

# CSI3335 Project Group "No Name Yet"

This README will show you how to run our project on your machine.

## Getting Started

### Prerequisites

- Python 3.10 or higher
- MariaDB 11.3 or a compatible version

### Setup Instructions

1. Start MariaDB Service:
    - Press Windows Key + R, type services. msc, and press Enter.
    - Scroll to find MariaDB, right-click it, and choose "Start".


2. In the project's main folder, modify the `csi3335sp2023.py` file as needed to match the MySQL user information for database connection.


3. Ensure the necessary Python packages are installed in the project's virtual environment. You can use the command prompt in the current directory and do

   ```bash
   pip install -r requirements.txt
   ```

## Running the Project

1. In the project folder terminal, activate the virtual environment.


2. Start the Flask application by running the following command:
   ```bash
   flask run
   ```
   If the project did not boot up correctly or encounters 404, please try the following commands in the terminal:
    ```bash
    mysql -u root -p -e "DROP DATABASE IF EXISTS nonameyet;" 
    mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS nonameyet;"
    mysql -u root -p nonameyet < nonameyet.sql
   ```
   
3. Open a web browser and navigate to [http://localhost:5000](http://localhost:5000) to access the application.


4. At home page, you will be directed to the login page and register page, where the default admin credentials are:
   - Username: admin
   - Password: admin123

![img.png](readMe%20image/img.png)


5. Upon successful login, you can search and view stats based on your permissions.
   
*Please notice you might get no result for 2023 since some teams' stats still need to be updated for 2023 in the database. For 2023, only the team's table and the Hall of Fame table are fully updated.*

![img2.png](readMe%image/img2.png)

## Other Files

The project has other files included:

- `lahman_1871-2023_csv`: Contains the baseball data in CSV format.
- `project_env`: Contains project compile library.
- `Python scripts`: Update the database by reading CSV files.



## Extra Credit
1. **Added all stats of all players and teams from years 1930 up to 2022( Some stats of 2023)**

2. **Included a link to each player on the team roster page that takes the user to all of the player's stats throughout the years**
