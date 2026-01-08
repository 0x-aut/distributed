# The model for running tasks or jobs and what those jobs may look like
# Extremely different depending on use case but you get the point

from pydantic import BaseModel, PrivateAttr, Field
from typing import Any, List, Dict, Literal, Annotated, Optional
from datetime import datetime, timedelta
from uuid import uuid4


# Let us define classes for several job types including creating a custom job type
class SendEmailJob(BaseModel):
  sender_email: str # This may be redundant but it will do
  recipient_email: str
  subject: str
  message: str
  _started_sent_at: datetime = PrivateAttr(default_factory=datetime.now)

class GenerateThumbnailJob(BaseModel):
  image_url: str
  _started_generation_at: datetime = PrivateAttr(default_factory=datetime.now)


class RunAnalysisJob(BaseModel):
  analysis_type: Literal["addition", "subtraction", "multiplication", "division", "custom_analysis"] # custom_analysis will be developed to allow custom math functions perhaps
  analysis_data: Dict[str, Any]
  _started_analysis_at: datetime = PrivateAttr(default_factory=datetime.now)
  _analysis_end_time: datetime = PrivateAttr(default_factory=datetime.now)
  _analysis_total_run_time:timedelta = PrivateAttr(default_factory= lambda: RunAnalysisJob._started_analysis_at - RunAnalysisJob._analysis_end_time) # Look at this function a little bit more just to be clear
  

class NotifyUserJob(BaseModel):
  user_to_notify: str
  notification_channel: Literal["mobile", "email", "web_toast"]
  # Email channel is meant to point or tie to sending emails via the email job
  message: str
  _started_notification_at: datetime = PrivateAttr(default_factory=datetime.now)

class CleanOldDataJob(BaseModel):
  data_type: Literal["records", "list"] # Records for dictionaries and lists for normal data in a list of data
  data_payload: Dict[str, Any]|List
  _started_cleanup_at: datetime = PrivateAttr(default_factory=datetime.now)

class BackUpDataJob(BaseModel):
  data_type: Literal["records", "list"]
  data_payload: Dict[str, Any]|Literal["", 1]
  _started_backup_at: datetime = PrivateAttr(default_factory=datetime.now)


class CustomJob(BaseModel):
  """
  This is where use creates a custom job of their choosing using the made template
  """
  custom_job_type: str # User will declare a job type
  payload: Dict[str, Any]
  _created_at: datetime = PrivateAttr(default_factory=datetime.now)

class Job(BaseModel):
  """
  This class is the model for running tasks or jobs and what they may look like.
  """
  _id: str = PrivateAttr(default_factory=lambda: str(uuid4()))
  job_type: Literal["send_email", "generate_thumbnail", "run_analysis", "notify_user", "clean_old_data", "backup_data", "custom_jobs"]
  payload: Annotated[SendEmailJob|GenerateThumbnailJob|RunAnalysisJob|NotifyUserJob|CleanOldDataJob|BackUpDataJob|CustomJob, Field(discriminator="job_type")]
  status: Literal["pending", "processing", "completed", "failed", "retry"]
  # Pending is different from processing as pending is for sending the data to the system
  priority: int = 0
  attempts: int = 0
  max_retries: int = 3
  _created_at: datetime = PrivateAttr(default_factory=datetime.now)
  scheduled_at: Optional[datetime] = None
  updated_at: Optional[datetime] = None
  failed_reason: Optional[str] = None
  failed_at: Optional[datetime] = None
  completed_at: Optional[datetime] = None
  result: Dict[str, Any]
  