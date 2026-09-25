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
# Delivery crop years and inventory

Apply `migrations/008_delivery_crop_year.sql` once before deploying this version.
Delivery crop year means the original harvest year, independent of delivery date.
Existing deliveries are left unassigned rather than guessed. An editor can open
Delivery → Assign crop years to review and save each original crop year.
Crop-year inventory excludes unassigned deliveries and displays an incomplete-total
warning until assignments are complete. All-years inventory still includes them.
The dashboard shows harvest minus assigned deliveries separately by crop for its
displayed crop year. The delivery import generator records the selected workbook
crop year; other importers must populate `Delivery.Crop_Year` explicitly.
Carryover transfers are not implemented; do not enter them as new harvest.

## Viewer and Editor password reset

The login page has a Forgot password link. Recovery requires an active Viewer or
Editor membership and a verified @unl.edu email (recorded when an invitation is
accepted). Accounts marked admin globally or in any grower membership cannot
request or redeem reset links. Admin status is checked again at redemption.
Legacy users can sign in and use Add/Verify Email before requesting recovery. Users who cannot sign in and have no verified email need administrator assistance.

Deploy password_reset.py, templates/password_reset.html, the login template,
app.py, and migrations/009_password_resets.sql together. Migration 008 belongs to
separate delivery work; password recovery does not depend on it. The new reset
table is created by access schema initialization, including on recovery pages.
The existing GMS_MAIL_FROM, GMS_PUBLIC_URL and GMS_SENDMAIL_PATH settings are reused.

Links expire after 30 minutes and are single-use; a newer request replaces the
older link. Requests are limited to one per minute and five per hour per eligible
account. Responses do not reveal whether an email exists or is an Admin account.
Password changes invalidate other login sessions. Deploying this version also
requires already-signed-in users to sign in again to establish session binding.
No reset email is sent automatically during deployment or testing.

## Signup and existing-account email verification

Signup now requires an @unl.edu address. After creating an account, GMS sends a
24-hour verification link and opens Add/Verify Email. The new grower membership
remains pending until an administrator approves it; verification never grants or
changes membership roles. Admin accounts remain excluded from password recovery.

Existing users can open **Add/Verify Email** from the account menu (or from Access
pending), enter their current password and UNL address, then confirm the emailed
link while signed in to that same account. If signed out, sign in first and reopen
the email link. Already-verified addresses are displayed but cannot be replaced
through this form. Users who cannot sign in and never verified an email still
need administrator assistance.

Deploy email_verification.py, templates/account_email.html, templates/verify_email.html,
the updated signup/base/access_pending templates and app.py, and
migrations/010_email_verification.sql alongside the password-reset changes.
Access-schema initialization creates the new pending-verification table.
Existing user_emails records are preserved. Unverified email addresses are kept
separately and cannot be used for password recovery. No new email settings are
needed; the existing local sendmail configuration is reused.

Requests are limited to one per minute and five per hour per account. Resending
replaces the prior single-use link. Email submission failures leave the account
pending verification and allow a later retry from Add/Verify Email. Email links
require explicit confirmation, so automated email-link scanners cannot verify an
account. Tests mock email delivery and use isolated MySQL test tables.

## September 25 release deployment

See DEPLOYMENT_2026_09_25.md for the reviewed release procedure. Use
`python scripts/deploy_account_updates.py --apply --check-mail` on production to
apply migrations 008–010 idempotently before restarting the app. This command
preserves existing data, adds only missing schema, validates the existing mail
configuration, and sends no messages. Do not rerun the older vehicle cleanup.

The local delivery SQL generator now requires an explicit grower:
`python generate_delivery_import_sql.py 2025 --grower-id YOUR_GROWER_ID`.
It uses the Linux table names and scopes location lookups to that grower.
Generated SQL remains a manual import, not part of release deployment.
