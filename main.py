from app.db.connection import connectToDatabase
from scripts.generatesql import generateSchema, createSQLFile
from typing import LiteralString



def makeSchema(sql_command_text: LiteralString):
  connect = connectToDatabase()
  connect.execute(sql_command_text)
  connect.close()

def main():
  schema = generateSchema()
  createSQLFile() # Bad writing will solve this later
  try:
    makeSchema(schema)
  except Exception as e:
    print(f"An exception occured {e}")
    
  
  
  
  

if __name__ == "__main__":
  main()
 