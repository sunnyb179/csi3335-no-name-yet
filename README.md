---
title: "CSI3335 Project Documentation"
output: html_document
---

# CSI3335 Project Documentation

This README provides comprehensive setup instructions for running the web application developed for the CSI3335 course using Flask and MariaDB.

## Getting Started

### Prerequisites

- Python 3.10 or higher
- MariaDB 11.3 or compatible version

### Setup Instructions

1. **Extract the ZIP File:**
   Unzip the provided ZIP file into a directory of your choice. This directory will contain all the necessary files including the Python scripts, SQL dump, and configuration files.

2. **Create and Activate a Virtual Environment:**

   Navigate to the extracted directory, cd into csi3335-no-name-yet, and create a virtual environment:

   **For Windows:**
   ```bash
   python -m venv project_env
   .\project_env\Scripts\activate
   ```
   **For Linux/MacOS:**   
   ```bash
   python3 -m venv project_env
   source project_env/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   
### Database Setup
1. **Start MariaDB Service:**
    - Press Windows Key + R, type services.msc, and press Enter.
    - Scroll to find MariaDB, right-click it, and choose "Start".
   
2. **Import the Database:**
    - Open a command prompt or terminal in the MariaDB bin directory and run:
    ```bash
    mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS nonameyet;"
    mysql -u root -p nonameyet < nonameyet.sql
   ```
   - The password is: nguyen12

### Running the Flask Application
1. **Launch the Application:**
    - Ensure you are in the root directory of the extracted project where the user_login.py file is located. Start the Flask application by running:
   ```bash
    python user_login.py
   ```
   - Access the web application through a browser at http://127.0.0.1:5000.

### Closing the Application
- To stop the Flask server, press CTRL+C in your command prompt or terminal. Deactivate the virtual environment with:
   ```bash
   deactivate
   ```
  
### Note
- Please make sure to update the database credentials in the `csi3335sp2023.py` if necessary. This project using the following configuration:
```bash
mysql_dict = {
    'host': 'localhost',
    'user': 'root',
    'password': 'nguyen12',
    'database': 'nonameyet'
}
```
- The login information for the admin is:
```bash
user: admin
pass: admin123
```
### Extra Credit
1. **Added all stats of all players and teams from years 1930 all the way up to 2023**
2. **Included a link to each player on the team roster page that takes the user to all of the player's stats throughout the years**