from datetime import datetime
import enum

from sqlalchemy import Enum, Date, DateTime
from sqlalchemy.orm import backref
from sqlalchemy.sql.schema import ForeignKey
from app import db
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from app import login

postFields = db.Table('postfields',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
    db.Column('field_id', db.Integer, db.ForeignKey('field.id'))
    )

studentFields = db.Table('studentfields',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('field_id', db.Integer, db.ForeignKey('field.id'))
    )

studentLanguages = db.Table('languages',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('language_id', db.Integer, db.ForeignKey('language.id'))
    )

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    wsu_id = db.Column(db.String(30), unique=True)
    email = db.Column(db.String(120), unique=True)
    phone = db.Column(db.String(15))
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20))
    __mapper_args__ = {
        'polymorphic_identity':'user',
        'polymorphic_on':role
    }
    def __repr__(self) -> str:
        return f"<User {self.id}, name={self.username}>"
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def is_professor(self):
        return self.role == 'professor'

class Student(User):
    id = db.Column(db.Integer, ForeignKey('user.id'), primary_key=True)
    gpa = db.Column(db.Numeric(3,2))
    major = db.Column(db.String(30))
    graduation_year = db.Column(db.Integer)
    taken_courses = db.Column(db.String(300))
    prior_experience = db.Column(db.String(1500))

    research_fields = db.relationship(
        'ResearchField', secondary=studentFields,
        primaryjoin=(studentFields.c.user_id == id),
        backref=db.backref('studentFields', lazy='dynamic'),
        lazy='dynamic'
    )

    languages = db.relationship(
        'ProgrammingLanguage', secondary=studentLanguages,
        primaryjoin=(studentLanguages.c.user_id == id),
        backref=db.backref('studentLanguages', lazy='dynamic'),
        lazy='dynamic'
    )
    __mapper_args__ = {
        'polymorphic_identity':'student',
    }

    def get_fields(self):
        return self.research_fields

class Professor(User):
    id = db.Column(db.Integer, ForeignKey('user.id'), primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity':'professor',
    }

@login.user_loader
def user_loader(id):

    return User.query.get(int(id))

class ResearchPost(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('user.id'))
    title = db.Column(db.String(150))
    description = db.Column(db.String(1500))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    time_commitment = db.Column(db.String(150))
    requirements = db.Column(db.String(700))
    # status = db.Column()
    applications = db.relationship('Application',
        lazy='dynamic')

    research_fields = db.relationship(
        'ResearchField', secondary=postFields,
        primaryjoin=(postFields.c.post_id == id),
        backref=db.backref('postFields', lazy='dynamic'),
        lazy='dynamic'
    )

    def get_fields(self):
        return self.research_fields
    def get_start(self):
        return self.start_date.strftime('%m/%d/%Y')
    def get_end(self):
        return self.end_date.strftime('%m/%d/%Y')

class ResearchField(db.Model):
    __tablename__ = 'field'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    def __repr__(self):
        return '<{},{} >'.format(self.id,self.name)

class ProgrammingLanguage(db.Model):
    __tablename__ = 'language'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    def __repr__(self):
        return '<{},{} >'.format(self.id,self.name)

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('user.id'))
    post_id = db.Column(db.Integer, ForeignKey('post.id'))
    statement = db.Column(db.String(200))
    reference_name = db.Column(db.String(30))
    reference_email = db.Column(db.String(120))
    status = db.Column(db.String(20))

    applicant = db.relationship('User')
