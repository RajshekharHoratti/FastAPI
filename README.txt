Fast API Boilerplate

This is just a simple code which performs CRUD Operations Using FASTAPI.
Database used is PostgreSQL

Steps to Run The Code:

Step 1: Create a new Virtual Environment.
        "python3 -m venv venv"

Step 2: Activate the Virtual Environment.
        ". venv/bin/activate" (or) "source venv/bin/activate"

Step 3: Install all the dependency from the requirements.txt file.
        "pip install -r requirements.txt"

Step 4: Run the code.
        "python main.py"


Detailed Information:

Files Used:
1) .env
2) config.py
3) main.py
4) model.py


1) .env: This file consist the credentials for the database
2) config.py: This file consist of all the required configuration, Such as CROS, LOGGER, ENV VARIABLES, DATABASE CONNECTION
3) main.py: This is the file where we write the API's
4) model.py: This is where we have specified the Schemas

NOTE:
All the logs are written in the logs file inside the logs folder.
It is configured such that every day a new log file gets created if the code is running in the background


