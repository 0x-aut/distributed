from app.db.connection import connectToDatabase
from scripts.generatesql import generateSchema, createSQLFile
from typing import LiteralString, cast
import os


def makeSchema():
  if os.path.exists("migrations/001_create_jobs_table.sql"):
    try:
      connect = connectToDatabase()
      with open("migrations/001_create_jobs_table.sql", "r") as f:
        sql_command_text = f.read()
      literal_sql_command_text = cast(LiteralString, sql_command_text)
      connect.execute(literal_sql_command_text)
      connect.commit()
      print("The table has been created successfully")
      connect.close()
    except Exception as e:
      print(f"An exception occurred while making the table a schema: {e}")
  else:
    try:
      createSQLFile()
    except Exception as e:
      print(f"An error occurred while creating the SQL schema file: {e}")

def main():
  try:
    makeSchema()
  except Exception as e:
    print(f"An exception occured {e}")




if __name__ == "__main__":
  main()
 