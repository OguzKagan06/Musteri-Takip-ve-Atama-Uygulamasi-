import os
import uuid
from werkzeug.utils import secure_filename
from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, current_user, login_required
from app import db
from app.auth import bp
from app.auth.forms import LoginForm, RegisterForm, UpdateProfileForm
from app.models import User

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(db.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Geçersiz kullanıcı adı veya şifre.', 'danger')
            return redirect(url_for('auth.login'))
        login_user(user)
        flash('Başarıyla giriş yaptınız!', 'success')
        return redirect(url_for('main.index'))
    return render_template('auth/login.html', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Çıkış yapıldı.', 'info')
    return redirect(url_for('main.index'))

@bp.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    if current_user.role not in ['admin', 'super_admin']:
        flash('Sadece yöneticiler yeni kullanıcı oluşturabilir.', 'danger')
        return redirect(url_for('main.index'))
    form = RegisterForm()
    if form.validate_on_submit():
        if form.role.data == 'super_admin':
            flash('Güvenlik ihlali: Kurucu rolünde kullanıcı oluşturulamaz.', 'danger')
            return redirect(url_for('auth.register'))
            
        user = User(username=form.username.data, role=form.role.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Tebrikler, kayıt oldunuz! Şimdi giriş yapabilirsiniz.', 'success')
        return redirect(url_for('auth.login'))
        
    if request.method == 'POST':
        print("FORM HATALARI:", form.errors)
        
    return render_template('auth/register.html', form=form)

@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateProfileForm()
    if form.validate_on_submit():
        if form.avatar.data:
            avatar_file = form.avatar.data
            filename = secure_filename(avatar_file.filename)
            unique_filename = f"{uuid.uuid4().hex}_{filename}"
            avatar_path = os.path.join(current_app.root_path, 'static', 'avatars')
            os.makedirs(avatar_path, exist_ok=True)
            avatar_file.save(os.path.join(avatar_path, unique_filename))
            current_user.avatar_file = unique_filename
            
        if form.new_password.data:
            current_user.set_password(form.new_password.data)
            
        db.session.commit()
        flash('Profiliniz başarıyla güncellendi.', 'success')
        return redirect(url_for('auth.profile'))
        
    return render_template('auth/profile.html', form=form)
