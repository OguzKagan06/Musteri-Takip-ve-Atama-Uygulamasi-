from flask import render_template
from app.crm import bp

@bp.route('/customers')
def customer_list():
    return render_template('crm/customer_list.html')
