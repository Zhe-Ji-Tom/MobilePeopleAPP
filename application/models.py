from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)

    def __repr__(self):
        return '<Roles {}>'.format(self.name)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=True)
    email = db.Column(db.String(50), nullable=True)
    status = db.Column(db.Integer, nullable=False)
    role_id = db.Column(db.Integer, unique=True, nullable=False)

    def __repr__(self):
        return '<Name {}>'.format(self.name)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Video(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key= True)
    location = db.Column(db.String(200), nullable=False)

class History(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    count = db.Column(db.Integer, nullable=False)
    video_id = db.Column(db.Integer, nullable=False)
    submit_time = db.Column(db.DATETIME, nullable=True)
    status = db.Column(db.Integer, nullable=False)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))