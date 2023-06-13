from flask_login import UserMixin
from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, LargeBinary, String
from database import db 

class Signup(UserMixin, db.Model):
    id = Column(String(50), primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    phone = Column(Integer, nullable=False)
    password = Column(String(250), unique=True, nullable=False)
    is_admin = Column(Boolean, default=False)


class Product(db.Model):
    id = Column(String(50), primary_key=True)
    pname = Column(String(100), nullable=False)
    pinfo = Column(String(200))
    pdescription = Column(String(200))
    pprice = Column(Float, nullable=False)

class Order(db.Model):
    id = Column(String(50),primary_key=True)
    pid = Column(Integer,ForeignKey(Product.id))
    name = Column(String(50),ForeignKey(Product.pname),nullable= False)
    price = Column(Integer,ForeignKey(Product.pprice),nullable=False)
    quantity = Column(Integer,nullable=False)
    user_name= Column(String,ForeignKey(Signup.name))