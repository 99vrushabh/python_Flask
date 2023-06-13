import uuid
from flask import Flask
from flask_login import LoginManager
from tkinter import *
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import jwt
from flask import flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_user
from src.admin.api import admin
from src.user.api import user
from database import db
from common.models import Signup


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SECRET_KEY'] = 'thisissecretkey'
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.register_blueprint(admin)
    app.register_blueprint(user)
    return app
app=create_app()

login_manager = LoginManager(app)
login_manager.init_app(app)
@login_manager.user_loader
def loader_user(user_id):
    return Signup.query.get(user_id)


@app.route('/')
def home():
    if current_user.is_authenticated:
        name = current_user.name
    else:
        return render_template('Home.html')
    return render_template('Home.html', name=name)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        user = Signup(
                      id = str(uuid.uuid4()),
                      name=request.form.get("name"),
                      email=request.form.get("email"),
                      phone=request.form.get("phone"),
                      password=request.form.get("password"),
                      )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = Signup.query.filter(Signup.name == request.form.get('name')).first()
        if user:
            if user.password == request.form.get("password"):
                login_user(user)
                flash("you are successfuly logged in")
                return redirect(url_for('home'))
            else:
                msg = "Username or Password is wrong"
                return render_template('Login.html',msg=msg)
        else:
            return render_template('Login.html',msg=msg)
    return render_template('Login.html')




if __name__ == "__main__":
    app.run(debug=True)
