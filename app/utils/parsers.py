# Straight up helper functions for parsing certain things
# Like converting a list with a dictionary to a list with a tuple

from typing import Dict, List, Annotated, Optional, Any
from ..models.model import Job
from datetime import datetime

# Here we can use Any since we
def listDictToTupleParser(
  original_list: List[Job]
) -> List[tuple]:
  parsed_list = []
  
  """
  job_type, payload, priority, scheduled_at, max_retries
  """

  for i in original_list:
    job_model_list = [i.job_type, i.payload, i.priority, i.scheduled_at, i.max_retries]
    job_model = tuple()
    parsed_list.append(job_model)


  return parsed_list
