from flask import render_template, redirect, url_for, request
from flask_login import current_user, login_required
from app.main import bp
from app import db
from app.models import Notification

@bp.app_context_processor
def inject_notifications():
    if current_user.is_authenticated:
        unread_count = db.session.scalar(db.select(db.func.count(Notification.id)).where(Notification.user_id == current_user.id, Notification.is_read == False))
        latest = db.session.scalars(db.select(Notification).where(Notification.user_id == current_user.id).order_by(Notification.timestamp.desc()).limit(5)).all()
        return dict(unread_notifications_count=unread_count, latest_notifications=latest)
    return dict(unread_notifications_count=0, latest_notifications=[])

@bp.route('/notifications/read/<int:id>')
@login_required
def read_notification(id):
    notification = db.session.get(Notification, id)
    if notification and notification.user_id == current_user.id:
        notification.is_read = True
        db.session.commit()
    return redirect(request.referrer or url_for('main.index'))

@bp.route('/')
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    return render_template('main/index.html')

@bp.app_errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500
