from flask import Blueprint, jsonify, redirect, render_template, request
from flask_login import current_user, login_required, logout_user
from common.models import Product

user=Blueprint('user',__name__,template_folder='templates',static_folder='static')
@user.route('/profile')
@login_required
def profile():
    if current_user.is_authenticated:
        return render_template('profile.html', sname=current_user.name, semail=current_user.email, sphone=current_user.phone)


@user.route("/menu", methods=['GET', 'POST'])
def menu():
    products = Product.query.all()
    msg=""  
    if request.method == 'POST':
        search = request.form.get('search')
        if search:
            searchproducts = Product.query.filter(Product.pname.like(f'%{search}%')).all()
            if not searchproducts:
                msg = "Product not found"
            return render_template('menu.html', products=products,searchproducts=searchproducts,msg=msg)
        else:
            return render_template('menu.html', products=products)
    return render_template('menu.html', products=products)
    

@user.route('/order')
def order():
    return render_template('order.html')

@user.route("/rewards")
def rewards():
    return render_template('rewards.html')


@user.route("/gift")
def gift():
    return render_template('gift.html')


@user.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('login')
