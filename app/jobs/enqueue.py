import os
# from pydantic import BaseModel
from typing import Any, Optional, Dict, List
from ..models.model import (
  SendEmailJob, GenerateThumbnailJob,
  RunAnalysisJob, NotifyUserJob,
  CleanOldDataJob, BackUpDataJob,
  CustomJob, Job
)
from ..utils.parsers import listDictToTupleParser
from datetime import datetime
from ..db.connection import connectToDatabase


# Just realised the enqueue is not a Job Model but inseasd a list of params
# We will edit this to be a job model

def enqueue(job: Job):
  """
  Sends or queues a job to the job table using the insert keyword

  Args:
    job: Job model for how a job looks like
  """

  connection = connectToDatabase()
  cursor = connection.cursor()
  try:
    insert_command = """INSERT INTO JOBS (job_type, payload, priority, scheduled_at, max_retries)
    VALUES (%s, %s, %s, %s, %s)
    """
    inserted_data = (job.job_type, job.payload, job.priority, job.scheduled_at, job.max_retries)

    cursor.execute(insert_command, inserted_data)
    connection.commit()
    print(f"Job has been successfully added to the queue with the job type: {job.job_type}")
  except Exception as e:
    connection.rollback()
    # This will change but for now we can leave it here for now
    print(f"An error occured while adding job to queue {e}")
  finally:
    cursor.close()
    connection.close()


def batchEnqueue(job_details_list: List[Job]):
  connection = connectToDatabase()
  cursor = connection.cursor()
  try:
    insert_command = """INSERT INTO JOBS (job_type, payload, priority, scheduled_at, max_retries)
    VALUES (%s, %s, %s, %s, %s)
    """
    dict_keys = [
      "job_type", "payload", "priority", "scheduled_at", "max_retries"
    ]

    if dict_keys not in job_details_list:
      raise KeyError("The correct keys for the parameter is not found, please check the keys for the paramater passed")

    parsed_list = listDictToTupleParser(job_details_list)

    cursor.executemany(insert_command, parsed_list)
    connection.commit()

    print("Batch jobs added to the table")

  except Exception as e:
    connection.rollback()
    print(f"An error occurred while batch sending jobs to the table: {e}")
  finally:
    cursor.close()
    connection.close()


test_payload = GenerateThumbnailJob(image_url="https://testimagelink.testing")

payload_json = test_payload.model_dump_json()

