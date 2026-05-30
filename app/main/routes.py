from flask import render_template, redirect, url_for, request, flash
from flask_login import current_user, login_required, logout_user
from app.main import bp
from app import db
from app.models import Notification, User, Customer
from app.main.forms import SendNotificationForm

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
    if not notification or notification.user_id != current_user.id:
        flash('Bildirim bulunamadı veya erişim yetkiniz yok.', 'danger')
        return redirect(url_for('main.index'))
        
    if not notification.is_read:
        notification.is_read = True
        db.session.commit()
        
    return render_template('main/notification_detail.html', notification=notification)

@bp.route('/admin/send-notification', methods=['GET', 'POST'])
@login_required
def send_notification():
    if current_user.role not in ['admin', 'super_admin']:
        flash('Bu sayfaya erişim yetkiniz yok.', 'danger')
        return redirect(url_for('main.index'))
    
    form = SendNotificationForm()
    users = db.session.scalars(db.select(User).where(User.id != current_user.id)).all()
    
    choices = [('all', 'Tüm Arayıcılar (Toplu Duyuru)')]
    choices.extend([(str(user.id), f"{user.username} ({user.role})") for user in users])
    form.user_id.choices = choices
    
    if form.validate_on_submit():
        if form.user_id.data == 'all':
            for user in users:
                notification = Notification(user_id=user.id, message=form.message.data)
                db.session.add(notification)
            db.session.commit()
            flash('Toplu duyuru başarıyla gönderildi.', 'success')
        else:
            notification = Notification(user_id=int(form.user_id.data), message=form.message.data)
            db.session.add(notification)
            db.session.commit()
            flash('Kişisel bildirim başarıyla gönderildi.', 'success')
            
        return redirect(url_for('main.send_notification'))
        
    return render_template('main/send_notification.html', form=form)
@bp.route('/admin/users', methods=['GET'])
@login_required
def admin_users():
    if current_user.role not in ['admin', 'super_admin']:
        flash('Bu sayfaya erişim yetkiniz yok.', 'danger')
        return redirect(url_for('main.index'))
    
    users = db.session.scalars(db.select(User).order_by(User.role.asc(), User.id.asc())).all()
    from app.main.forms import AdminDeleteUserForm
    form = AdminDeleteUserForm()
    return render_template('main/admin_users.html', users=users, form=form)

@bp.route('/admin/users/delete/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if current_user.role not in ['admin', 'super_admin']:
        flash('Bu işlemi yapma yetkiniz yok.', 'danger')
        return redirect(url_for('main.index'))
        
    from app.main.forms import AdminDeleteUserForm
    form = AdminDeleteUserForm()
    
    if form.validate_on_submit():
        if not current_user.check_password(form.admin_password.data):
            flash('Admin şifresi hatalı! İşlem iptal edildi.', 'danger')
            return redirect(url_for('main.admin_users'))
            
        user_to_delete = db.session.get(User, user_id)
        if not user_to_delete:
            flash('Kullanıcı bulunamadı.', 'danger')
            return redirect(url_for('main.admin_users'))
            
        if user_to_delete.role == 'super_admin':
            flash('Kurucu hesabı silinemez!', 'danger')
            return redirect(url_for('main.admin_users'))
            
        if current_user.role == 'admin' and user_to_delete.role in ['admin', 'super_admin'] and current_user.id != user_to_delete.id:
            flash('Yetkisiz işlem: Sadece Kurucu diğer yöneticileri silebilir.', 'danger')
            return redirect(url_for('main.admin_users'))
            
        # Update customers to avoid foreign key constraints / orphaned data loss
        db.session.execute(db.update(Customer).where(Customer.assigned_user_id == user_id).values(assigned_user_id=None))
        db.session.execute(db.update(Customer).where(Customer.last_called_by_id == user_id).values(last_called_by_id=None))
        
        is_self_delete = (user_to_delete.id == current_user.id)
        
        db.session.delete(user_to_delete)
        db.session.commit()
        
        if is_self_delete:
            logout_user()
            flash('Kendi hesabınızı başarıyla sildiniz. Oturumunuz kapatıldı.', 'success')
            return redirect(url_for('auth.login'))
            
        flash(f'Kullanıcı ({user_to_delete.username}) başarıyla silindi.', 'success')
        
    return redirect(url_for('main.admin_users'))


@bp.route('/')
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
        
    total_customers = db.session.scalar(db.select(db.func.count(Customer.id)))
    return render_template('main/index.html', total_customers=total_customers)

@bp.app_errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500
