# GRAIN_SW

## Grower access setup

Grower is the organization boundary. On an empty installation, opening `/`
redirects to `/setup`, where the first Grower and administrator are created
together.

On an existing single-Grower installation, the access migration runs once when
the app starts. Existing legacy admins become Grower admins, existing users
become Grower editors, and existing operational records are assigned to the
existing Grower. New signups remain pending until approved.

A Grower admin reviews requests under **Insert Data → User Access** and assigns
Viewer, Editor, or Admin. Viewers have read-only reporting access, Editors can
also enter and edit harvest loads, and Admins can manage setup data and users.

The reviewed SQL equivalent is in `migrations/001_grower_access.sql`. Back up the
database before deploying the migration to production.

## Raven imports from the website

The admin Import Raven Data button launches `raven_jobs.py` using the same
Python environment as GMS. It returns immediately and polls for progress;
Raven retries no longer occupy a Gunicorn request. The latest job is visible
when returning to the page, and only one website import runs at a time.

Job status and logs are stored in `data/raven_jobs/` (excluded from Git).
The application account needs write access there. Set `GMS_JOB_DIR` to use
another private writable directory. No database migration or extra package
is required. A service/server restart may interrupt an active import; its
status changes to interrupted after three minutes without a heartbeat.
Completed files may already have committed, so inspect the output before
retrying. Do not run a command-line import concurrently with a website job.
