# GRAIN_SW

## UNL user invitations

Administrators can invite `@unl.edu` addresses from **Farm Setup → User Access**,
choose Viewer/Editor/Admin access, and resend or revoke invitations. Links expire
after seven days. Resending replaces the old link. Acceptance verifies the email
and activates membership; existing users must provide their current username and
password, and new users choose a username/password. An already-active member's
role is preserved. Existing signup requests still require administrator approval.

Deploy `invitations.py`, the updated templates/app, and
`migrations/007_user_invitations.sql` together. The two new tables are created
idempotently by the existing access-schema initialization at login/startup; the SQL
file can also be applied manually before restart. No existing user data is changed.

On the UNL production server, configure these in the application's `.env`:

```dotenv
GMS_PUBLIC_URL=https://lagad-grainms-prod.unl.edu
GMS_SENDMAIL_PATH=/sbin/sendmail
# Replace this placeholder with the sender address approved by UNL IT:
GMS_MAIL_FROM=APPROVED_SENDER@unl.edu
```

Restart the GMS service after setting the actual approved sender. The application
submits to local Postfix and needs no SMTP password. It does not change Postfix's
relay or TLS settings. The invitation controls show a configuration warning when
the sender, HTTPS URL, or sendmail executable is unavailable (including typical
Windows development environments). Configuration validation does not establish
relay authorization or delivery; verify those with UNL IT and an invitation to
an intended UNL recipient. A successful submission means Postfix accepted the
message, not that it arrived. For failed delivery, ask the server administrator
to inspect the mail queue and mail logs. No test messages are sent automatically.

Invitation tokens are stored only as hashes. The acceptance page has no external
assets and sets no-referrer/no-store headers. Access forms use session CSRF tokens,
and invitation acceptance is transactional and single-use. Ten failed existing
account password attempts disable that invitation until an admin resends it.

Run the integration checks with
`python -m unittest discover -s tests -p test_invitations.py -v`. They create and
remove uniquely prefixed test tables in the configured MySQL database and mock
email submission; application tables and real recipients are not modified.

## Cart load cells

Before deploying this version, back up the database, pause imports, and apply
`migrations/006_cart_load_cell.sql` once. It adds the cart load cell columns and
fills them from each cart's latest linked harvest with a load cell value.
Restart the app and resume imports after applying the migration.

Load Cell is optional under **Farm Setup → Carts** (Add/Edit and the list).
Vehicles no longer display or edit it. Raven imports now update the cart's
load cell, with older dated loads prevented from replacing newer values.
Historical harvest values and legacy vehicle columns are retained. Carts
without linked harvest history can be filled in manually.

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
