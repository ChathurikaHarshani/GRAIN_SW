"""Dismiss intentional missing-data warnings without changing harvest values."""
from flask import Blueprint, abort, flash, redirect, request, url_for
from flask_login import current_user, login_required
from db import get_conn
from invitations import check_csrf

bp = Blueprint('harvest_attention', __name__)

# The calling queries use h for Harvest and d for its owning Department.
ATTENTION_SQL = """(h.Gross_Weight IS NULL OR h.MC IS NULL OR h.StorLoc_ID IS NULL)
    AND NOT EXISTS (SELECT 1 FROM Harvest_Attention a
        WHERE a.Harvest_ID=h.Harvest_ID AND a.Grower_ID=d.Grower_ID AND a.Dismissed=1)"""


@bp.route('/harvest/<int:harvest_id>/attention', methods=['POST'])
@login_required
def update(harvest_id):
    if not current_user.can_edit or current_user.membership_status != 'active':
        abort(403)
    check_csrf()
    action = request.form.get('action')
    reason = request.form.get('reason', '').strip()
    if action not in ('dismiss', 'restore') or len(reason) > 500:
        abort(400, description='Choose dismiss or restore and a reason of at most 500 characters.')
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    try:
        cur.execute('''SELECT h.Harvest_ID FROM Harvest h
            JOIN Field f ON f.Field_ID=h.Field_ID JOIN Department d ON d.Dpt_ID=f.Dpt_ID
            WHERE h.Harvest_ID=%s AND d.Grower_ID=%s FOR UPDATE''',
                    (harvest_id, current_user.grower_id))
        if not cur.fetchone():
            abort(404)
        cur.execute('''INSERT INTO Harvest_Attention
            (Harvest_ID, Grower_ID, Dismissed, Reason, User_ID)
            VALUES (%s,%s,%s,%s,%s)
            ON DUPLICATE KEY UPDATE Dismissed=VALUES(Dismissed), Reason=VALUES(Reason),
                User_ID=VALUES(User_ID), Updated_At=CURRENT_TIMESTAMP''',
                    (harvest_id, current_user.grower_id, int(action == 'dismiss'), reason or None, int(current_user.id)))
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()
    flash('Load warning dismissed.' if action == 'dismiss' else 'Load warning restored.', 'success')
    # Preserve filters, but never accept a caller-controlled redirect destination.
    allowed = ('crop_year', 'field_id', 'field_name', 'storloc_id', 'truck_id',
               'crop_id', 'date_from', 'date_to', 'needs_attention')
    filters = {key: request.args[key] for key in allowed if key in request.args}
    return redirect(url_for('harvest_query', **filters))
