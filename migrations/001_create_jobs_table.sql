-- Generated on 2026-01-08 17:47:16
-- 001_create_jobs_table.sql
-- DO NOT EDIT MANUALLY - Regenerate with generatesql.py

CREATE TABLE IF NOT EXISTS Jobs (
   _id BIGSERIAL PRIMARY KEY,
   job_type TEXT NOT NULL,
   payload JSONB NOT NULL,
   status TEXT NOT NULL DEFAULT 'pending',
   priority INTEGER NOT NULL DEFAULT 0,
   attempts INTEGER NOT NULL DEFAULT 0,
   max_retries INTEGER NOT NULL DEFAULT 3,
   _created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
   scheduled_at TIMESTAMPTZ,
   updated_at TIMESTAMPTZ,
   failed_reason TEXT,
   failed_at TIMESTAMPTZ,
   completed_at TIMESTAMPTZ,
   result JSONB,
   CHECK (status IN ('pending', 'processing', 'completed', 'failed', 'retry'))
);

CREATE INDEX IF NOT EXISTS idx_jobs_ready ON Jobs
  (priority DESC, _created_at ASC)
  WHERE status IN ('pending', 'retry');

COMMENT ON TABLE Jobs IS 'Durable persistent task queue table using Postgres-native patterns';
COMMENT ON COLUMN Jobs.payload IS 'JSONB payload, validated and structured by Pydantic models at runtime';
COMMENT ON COLUMN Jobs.status IS 'Current job state (pending → processing → completed/failed/retry)';
COMMENT ON COLUMN Jobs.attempts IS 'Number of processing attempts (used for retries)';
COMMENT ON COLUMN Jobs.scheduled_at IS 'For delayed/scheduled jobs (NULL = run immediately)';
COMMENT ON COLUMN Jobs.failed_reason IS 'Last error message when job failed';
COMMENT ON COLUMN Jobs.result IS 'Optional success output/data returned by the job handler';