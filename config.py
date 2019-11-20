import os
import logging
import psycopg2
from fastapi import FastAPI
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from logging.handlers import TimedRotatingFileHandler
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = FastAPI(
    title="Fast API Boilerplate",
    description="This is a very simple boilerplate for the FastAPI Framework",
    version="1.0.0", )

# CROS
origins = [
    "http:localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Loading Environment Variables
dotenv_path = BASE_DIR + '/.env'
load_dotenv(dotenv_path)

# Logger Setup
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler = TimedRotatingFileHandler(BASE_DIR + '/logs/logs.log', when='midnight', interval=1)
handler.setFormatter(formatter)
handler.suffix = "%Y%m%d"
logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

# Database Setup
try:
    db_connection = psycopg2.connect(database=os.environ.get("DATABASE_NAME"),
                                     user=os.environ.get("DATABASE_USER"),
                                     password=os.environ.get("DATABASE_PASSWORD"),
                                     host=os.environ.get("DATABASE_HOST"),
                                     port=os.environ.get("DATABASE_PORT"))
    db_connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur_connection = db_connection.cursor()
    print("SUCCESS: Database Connection Successful..!!")
except:
    print("ERROR: Database Connection Failed..!!")
