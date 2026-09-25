# GMS September 25 release

## Scope and readiness

Includes signup email verification, existing-user Add/Verify Email, Viewer/Editor
password recovery, session invalidation on reset, crop-year delivery assignments,
and crop-year inventory/dashboard updates. Admin accounts cannot request or use
password-reset links. Existing verified addresses and passwords are preserved.

The reviewed source must be committed and pushed to GitLab branch
`codex/gms-updates-2026-09-09` before running the server update. Preparing this
checklist does not publish or deploy the changes. Do not include .env, tmp/,
backups/, generated SQL, or the local deployment Word document in the release.

## Server procedure

Use the lagad-grainms account in
`/var/www/html/lagad-grainms-prod.unl.edu/app`, with `source venv/bin/activate`.
Finish any Raven import first. Take the normal production database backup.

Run each command separately; stop on an error:

```bash
git status --short
git branch --show-current
```

The working tree must be clean, and the deployment branch must be
`codex/gms-updates-2026-09-09`. Preserve and review any server-specific changes
before continuing.

```bash
git branch "backup/production-$(date +%Y%m%d-%H%M%S)"
git pull --ff-only origin codex/gms-updates-2026-09-09
python -m py_compile app.py invitations.py password_reset.py email_verification.py
python -c "from invitations import mail_config; mail_config(); print('Mail configuration present')"
systemctl --user stop gms
python scripts/deploy_account_updates.py --apply --check-mail
systemctl --user start gms
systemctl --user status gms --no-pager
curl --retry 5 --retry-connrefused --retry-delay 2 http://127.0.0.1:5000/health
git log -1 --oneline
```

The migration adds Delivery.Crop_Year and its index if missing, then ensures the
invitation, password-reset, and email-verification tables exist. It does not guess
historical crop years, change memberships/passwords, send messages, or change
.env/Postfix. It is safe to rerun after a partially completed additive migration.
No new Python package is required for these changes.

If migration fails after stopping GMS, do not continue blindly. Capture the error.
To restore the previous code, select the exact backup branch created above using
`git switch backup/production-TIMESTAMP`, then `systemctl --user start gms` and
check health. The prior release tolerates these additive schema changes; do not
delete the new tables or restore a database over newly created user data.

## Verify after deployment

All existing sessions require a fresh sign-in. Check dashboard/inventory and
Delivery → Assign crop years. Historical deliveries remain unassigned until an
Editor/Admin reviews them; year-filtered totals display an incomplete warning.
All-years inventory continues to include unassigned deliveries.

Use an intended UNL test recipient for signup or Add/Verify Email. Sign in to the
same account and confirm the received verification link. Verify that pending
membership still needs Admin approval. Test Forgot password for an approved
Viewer/Editor with verified email, then sign in with the new password. Admin
accounts must receive no reset link. Check the recent service log for errors.
Local Windows tests cannot establish production Postfix delivery.

## Validation performed locally

Automated tests cover invitations, signup, email verification, password recovery,
Admin exclusion at both reset stages, token expiry/replay, rate limits, CSRF,
grower isolation, inventory attribution, and repeatable migration/data preservation.
Email sending is mocked. Updated pages and inventory export were rendered against
the configured local database. All templates and changed Python modules compile.
