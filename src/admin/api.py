import uuid
from flask import Blueprint, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from database import db
from common.models import Product


admin =Blueprint('admin',__name__,template_folder='templates',static_folder='static')

@admin.route('/add_product_admin', methods=['GET', 'POST'])
def auth():
    if current_user.is_admin == True:
        if request.method == 'POST':
            check_password = request.form.get('check_password')
            if check_password == current_user.password:
                return redirect(url_for('admin.product'))
            else:
                errormsg = 'Wrong Password!! Try again...'
                return render_template('authorized.html', errormsg=errormsg)
        return render_template('authorized.html')
    else:
        return jsonify({'message': '401 Unauthorized User....'})


@admin.route("/add_product", methods=['GET', 'POST'])
@login_required
def product():
    if current_user.is_admin == True:
        if request.method == 'POST':
            add = Product(
                          id = str(uuid.uuid4()),
                          pname=request.form.get("pname"),
                          pinfo=request.form.get("pinfo"),
                          pdescription=request.form.get("pdescription"),
                          pprice=request.form.get("pprice"))
            db.session.add(add)
            db.session.commit()
        return render_template('product.html')
    else:
        return jsonify({'message': '401 Unauthorized User....'})