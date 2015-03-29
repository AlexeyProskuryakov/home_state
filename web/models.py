import hashlib

__author__ = '4ikist'

from web import db


def password_hash(password):
    return hashlib.sha224(password).hexdigest()


devices_tags = db.Table('devices_tags',
                        db.Column('tag_id', db.Integer, db.ForeignKey('tags.id')),
                        db.Column('page_id', db.Integer, db.ForeignKey('devices.id'))
                        )


class DeviceType(db.Model):
    __tablename__ = 'devices_types'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)


class Device(db.Model):
    __tablename__ = 'devices'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    type_id = db.Column(db.Integer, db.ForeignKey('devices_types.id'))
    tags = db.relationship('tags', secondary=devices_tags, backref=db.backref('tags', lazy='dynamic'))


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column('id', db.Integer, primary_key=True)
    login = db.Column(db.String, unique=True)
    password_hash = db.Column(db.String)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __init__(self, login, password):
        self.login = login
        self.password_hash = password_hash(password)

    @classmethod
    def check_and_return(cls, login, password):
        saved = cls.query.filter(login == login).first()
        if password_hash(password) == saved.password_hash:
            return saved
        return None



class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)

