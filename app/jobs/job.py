from typing import Optional, Tuple
from ..db.connection import connectToDatabase
import json

connection = connectToDatabase()
cursor = connection.cursor()

def pickJobs() -> Optional[Tuple]:
  """
  A function to pick open jobs from the table and run them
  """
  try:
    cursor.execute(
      """
      UPDATE Jobs
      SET status = 'processing',
      updated_at = NOW(),
      attempts = attempts + 1
      WHERE _id = (
        SELECT _id FROM Jobs
        WHERE status IN ('pending', 'retry')
        AND (scheduled_at IS NULL OR scheduled_at <= NOW())
        ORDER BY priority DESC, _created_at ASC
        LIMIT 1
        FOR UPDATE SKIP LOCKED
      )
      RETURNING _id, job_type, payload, attempts, max_retries
      """
    )
    
    result = cursor.fetchone()
    connection.commit()
    
    if result:
      job_id, job_type, payload_json, attempts, max_retries = result    # Destructuring results basically
      payload = json.loads(payload_json)
      return (job_id, job_type, payload, attempts, max_retries)

  except Exception as e:
    print(f"An error occurred while getting a job from the table: {e}")
    return None
  finally:
    cursor.close()
    connection.close()
    
    
def changeJobStatus(job_status: str, job_id: int):
  try:
    if job_status == "completed":
      query = """
      UPDATE Jobs
      SET status = 'completed',
        completed_at = NOW(),
        updated_at = NOW(),
        result = 'job completed'
      WHERE _id = %s
      """
      inserted_data = (job_id,)
      cursor.execute(query, inserted_data)
      connection.commit()
      print(f"The job with the job_id: {job_id} has been completed")
    elif job_status == 'failed':
      query = """
      UPDATE Jobs
      SET status = 'completed',
        failed_at = NOW(),
        updated_at = NOW(),
        failed_reason = 'Just failed after all attempts'
      WHERE _id = %s
      """
      inserted_data = (job_id,)
      cursor.execute(query, inserted_data)
      connection.commit()
      print(f"✗ Job {job_id} permanently failed after the total number of attempts")
    elif job_status == "retry":
      query = """
      UPDATE Jobs
      SET status = 'retry',
        updated_at = NOW(),
        failed_reason = 'Just failed, retry soon'
      WHERE _id = %s
      """
      inserted_data = (job_id,)
      cursor.execute(query, inserted_data)
      connection.commit()
      print("Failed, will retry job soon")
  except Exception as e:
    print(f"An error occured while changing status: {e}")
  finally:
    cursor.close()
    connection.close()