# This is the code to connect to the database for certain tasks
import psycopg
from psycopg.connection import Connection
import os
from dotenv import load_dotenv
from typing import Optional


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_CONNECTION_STRING")

user_connection: Optional[Connection] = None

# Do we gotta use a class for global method use?

def connectToDatabase() -> Connection:
  if not DATABASE_URL:
    raise ValueError("DATABASE URL is not found in environment, please add it to the environment")
  user_connection = psycopg.connect(DATABASE_URL)
  return user_connection
  
def closeConnection():
  if user_connection is not None:
    user_connection.close()
  else:
    return 'User connection is already closed'
