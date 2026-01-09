import os
# from pydantic import BaseModel
from typing import Any, Optional
from models.model import (
  SendEmailJob, GenerateThumbnailJob, 
  RunAnalysisJob, NotifyUserJob, 
  CleanOldDataJob, BackUpDataJob,
  CustomJob
)
from datetime import datetime
from db.connection import connectToDatabase

def enqueue(
  job_type: str,
  payload: SendEmailJob|GenerateThumbnailJob|
  RunAnalysisJob|NotifyUserJob|CleanOldDataJob|
  BackUpDataJob|CustomJob,
  priority: int = 0,
  scheduled_at: Optional[datetime] = None,
  max_retries: int = 5
):
  """
  Sends or queues a job to the job table
  """
  connection = connectToDatabase()
  connection.execute(
    """
    
    """
  )
  pass