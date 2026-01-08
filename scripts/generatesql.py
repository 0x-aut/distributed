# To create the sql migration schema file in the migrations folder

import os
from datetime import datetime
from typing import LiteralString, Optional




TABLE_NAME = "Jobs"

COLUMNS = [
  ("_id", "BIGSERIAL PRIMARY KEY"),
  ("job_type", "TEXT NOT NULL"),
  ("payload", "JSONB NOT NULL"),
  ("status", "TEXT NOT NULL DEFAULT 'pending'"),
  ("priority", "INTEGER NOT NULL DEFAULT 0"),
  ("attempts", "INTEGER NOT NULL DEFAULT 0"),
  ("max_retries", "INTEGER NOT NULL DEFAULT 3"),
  ("_created_at", "TIMESTAMPTZ NOT NULL DEFAULT NOW()"),
  ("scheduled_at", "TIMESTAMPTZ"),
  ("updated_at", "TIMESTAMPTZ"),
  ("failed_reason", "TEXT"),
  ("failed_at", "TIMESTAMPTZ"),
  ("completed_at", "TIMESTAMPTZ"),
  ("result", "JSONB")
]

STATUS_CHECK = """   CHECK (status IN ('pending', 'processing', 'completed', 'failed', 'retry'))"""

INDEXES = [
  {
    "name": "idx_jobs_ready",
    "definition": """  (priority DESC, _created_at ASC)
  WHERE status IN ('pending', 'retry')"""
  }
]

COMMENTS = {
  "table": "Durable persistent task queue table using Postgres-native patterns",
  "payload": "JSONB payload, validated and structured by Pydantic models at runtime",
  "status": "Current job state (pending → processing → completed/failed/retry)",
  "attempts": "Number of processing attempts (used for retries)",
  "scheduled_at": "For delayed/scheduled jobs (NULL = run immediately)",
  "failed_reason": "Last error message when job failed",
  "result": "Optional success output/data returned by the job handler",
}



# Generation logic

def generateSchema() -> LiteralString:
  lines = []
  
  timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  lines.append(f"-- Generated on {timestamp}")
  lines.append("-- 001_create_jobs_table.sql")
  lines.append("-- DO NOT EDIT MANUALLY - Regenerate with generatesql.py")
  lines.append("")
  
  # CREATE TABLE
  lines.append(f"CREATE TABLE IF NOT EXISTS {TABLE_NAME} (")
  for i, (col_name, col_def) in enumerate(COLUMNS):
    comma = "," #if i < len(COLUMNS) - 1 else ""
    lines.append(f"   {col_name} {col_def}{comma}")
    
  # Add status check constraint
  lines.append(f"{STATUS_CHECK}\n);")
  lines.append("")
  
  # Indexes
  for idx in INDEXES:
    lines.append(f"CREATE INDEX IF NOT EXISTS {idx['name']} ON {TABLE_NAME}")
    lines.append(f"{idx['definition']};")
    lines.append("")
    
  # Comments
  lines.append(f"COMMENT ON TABLE {TABLE_NAME} IS '{COMMENTS['table']}';")
  for col_name, comment in COMMENTS.items():
    if col_name != "table":
      lines.append(f"COMMENT ON COLUMN {TABLE_NAME}.{col_name} IS '{comment}';")
      
  # print(lines)
  return "\n".join(lines)
 


def createSQLFile():
  sql_content = generateSchema()
  if os.path.lexists("migrations"):
    print("Migrations folder already exist")
  else:
    os.makedirs("migrations", exist_ok=True)
    print("Created Migrations folder")
  
  output_path = "migrations/001_create_jobs_table.sql"
  with open(output_path, "w", encoding="utf-8") as f:
    f.write(sql_content)
    
  print(f"Successfully generated migration file: {output_path}")
  
  
  
  # print("2. Apply it: psql -d your_db_name -f migrations/001_create_jobs_table.sql")
  # print("3. Verify: \\d jobs  and  \\di  in psql")
  
