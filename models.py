# Imports
import base64
from datetime import datetime
from Crypto.Protocol.KDF import scrypt
from Crypto.Random import get_random_bytes
from cryptography.fernet import Fernet
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from app import db


# Encrypt Function
def encrypt(data, postkey):
    return Fernet(postkey).encrypt(bytes(data, 'utf-8'))


# Decrypt Function
def decrypt(data, postkey):
    return Fernet(postkey).decrypt(data).decode("utf-8")


# Users Class
class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)

    # crypto key for user's posts
    postkey = db.Column(db.BLOB)

    carbons = db.relationship('Carbon')

    def __init__(self, username, firstname, lastname, email, password, role):
        self.username = username
        self.password = generate_password_hash(password)
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.role = role
        self.postkey = base64.urlsafe_b64encode(scrypt(password, str(get_random_bytes(32)), 32, N=2 ** 14, r=8, p=1))
        self.registered_on = datetime.now()


# Posts Class
class Carbon(db.Model):
    __tablename__ = 'carbons'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, db.ForeignKey(User.username), nullable=True)
    created = db.Column(db.DateTime, nullable=False)
    title = db.Column(db.Text, nullable=False, default=False)
    body = db.Column(db.Text, nullable=False, default=False)

    def __init__(self, username, title, body, postkey):
        self.username = username
        self.created = datetime.now()
        self.title = encrypt(title, postkey)
        self.body = encrypt(body, postkey)

    def update_post(self, title, body, postkey):
        self.title = encrypt(title, postkey)
        self.body = encrypt(body, postkey)
        db.session.commit()


# Database Initialization
def init_db():
    db.drop_all()
    db.create_all()
    user0 = User(username='admin',
                 firstname='Dimitris',
                 lastname='Poulimenos',
                 password='Admin1!',
                 email='admin@email.com',
                 role='admin')

    user1 = User(username='jdoe',
                 firstname='John',
                 lastname='Doe',
                 password='Jdoe1',
                 email='johndoe@email.com',
                 role='user')

    db.session.add(user0)
    db.session.add(user1)

    db.session.commit()
