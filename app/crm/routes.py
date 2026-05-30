from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from sqlalchemy import or_
from app import db
from app.crm import bp
from app.crm.forms import CustomerForm, NoteForm
from app.models import Customer, User, Note

@bp.route('/dashboard')
@login_required
def dashboard():
    q = request.args.get('q')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)
    query = db.select(Customer).order_by(Customer.id.desc())
    
    if current_user.role not in ['admin', 'super_admin']:
        query = query.where(Customer.assigned_user_id == current_user.id)
        
    if q:
        search_filter = or_(
            Customer.name.ilike(f'%{q}%'),
            Customer.surname.ilike(f'%{q}%'),
            Customer.reference.ilike(f'%{q}%')
        )
        query = query.where(search_filter)
        
    customers = db.paginate(query, page=page, per_page=per_page, error_out=False)
    return render_template('crm/dashboard.html', customers=customers, q=q)

@bp.route('/customer/new', methods=['GET', 'POST'])
@login_required
def new_customer():
    if current_user.role not in ['admin', 'super_admin']:
        flash('Bu sayfaya erişim yetkiniz yok.', 'danger')
        return redirect(url_for('crm.dashboard'))
        
    form = CustomerForm()
    
    # Populate choices for assigned_user_id
    users = db.session.scalars(db.select(User).where(User.role == 'arayıcı')).all()
    form.assigned_user_id.choices = [(u.id, u.username) for u in users]
    form.assigned_user_id.choices.insert(0, (0, 'Atanmadı'))
    
    if form.validate_on_submit():
        customer = Customer(
            reference=form.reference.data,
            name=form.name.data,
            surname=form.surname.data,
            birth_date=form.birth_date.data,
            district=form.district.data,
            profession=form.profession.data,
            phone=form.phone.data,
            call_status=form.call_status.data,
            last_called_by_id=current_user.id
        )
        
        assigned_id = form.assigned_user_id.data
        if assigned_id != 0:
            customer.assigned_user_id = assigned_id
            
        db.session.add(customer)
        db.session.commit()
        flash('Müşteri başarıyla eklendi.', 'success')
        return redirect(url_for('crm.dashboard'))
        
    return render_template('crm/add_customer.html', form=form)

@bp.route('/customer/<int:id>', methods=['GET', 'POST'])
@login_required
def customer_detail(id):
    customer = db.session.get(Customer, id)
    if customer is None:
        flash('Müşteri bulunamadı.', 'danger')
        return redirect(url_for('crm.dashboard'))
        
    if current_user.role not in ['admin', 'super_admin'] and customer.assigned_user_id != current_user.id:
        flash('Bu müşteriyi görüntüleme yetkiniz yok.', 'danger')
        return redirect(url_for('crm.dashboard'))
        
    form = NoteForm()
    if form.validate_on_submit():
        note = Note(content=form.content.data, customer_id=customer.id, user_id=current_user.id)
        db.session.add(note)
        db.session.commit()
        flash('Not başarıyla eklendi.', 'success')
        return redirect(url_for('crm.customer_detail', id=customer.id))
        
    notes = db.session.scalars(db.select(Note).where(Note.customer_id == customer.id).order_by(Note.created_at.desc())).all()
    return render_template('crm/customer_detail.html', customer=customer, form=form, notes=notes)

@bp.route('/customer/<int:id>/delete', methods=['POST'])
@login_required
def delete_customer(id):
    if current_user.role not in ['admin', 'super_admin']:
        flash('Bu işlemi yapma yetkiniz yok.', 'danger')
        return redirect(url_for('crm.dashboard'))
        
    customer = db.session.get(Customer, id)
    if customer is None:
        flash('Müşteri bulunamadı.', 'danger')
        return redirect(url_for('crm.dashboard'))
        
    db.session.delete(customer)
    db.session.commit()
    flash('Müşteri ve ilgili notlar başarıyla silindi.', 'success')
    return redirect(url_for('crm.dashboard'))

@bp.route('/customer/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_customer(id):
    customer = db.session.get(Customer, id)
    if customer is None:
        flash('Müşteri bulunamadı.', 'danger')
        return redirect(url_for('crm.dashboard'))
        
    if current_user.role not in ['admin', 'super_admin'] and customer.assigned_user_id != current_user.id:
        flash('Bu müşteriyi düzenleme yetkiniz yok.', 'danger')
        return redirect(url_for('crm.dashboard'))
        
    form = CustomerForm(obj=customer)
    
    if current_user.role in ['admin', 'super_admin']:
        users = db.session.scalars(db.select(User).where(User.role == 'arayıcı')).all()
        form.assigned_user_id.choices = [(u.id, u.username) for u in users]
        form.assigned_user_id.choices.insert(0, (0, 'Atanmadı'))
    else:
        form.assigned_user_id.choices = [(current_user.id, current_user.username)]
        
    if form.validate_on_submit():
        customer.reference = form.reference.data
        customer.name = form.name.data
        customer.surname = form.surname.data
        customer.birth_date = form.birth_date.data
        customer.district = form.district.data
        customer.profession = form.profession.data
        customer.phone = form.phone.data
        customer.call_status = form.call_status.data
        customer.last_called_by_id = current_user.id
        
        if current_user.role in ['admin', 'super_admin']:
            assigned_id = form.assigned_user_id.data
            customer.assigned_user_id = assigned_id if assigned_id != 0 else None
            
        db.session.commit()
        flash('Müşteri başarıyla güncellendi.', 'success')
        return redirect(url_for('crm.customer_detail', id=customer.id))
        
    return render_template('crm/add_customer.html', form=form, edit_mode=True)
