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
