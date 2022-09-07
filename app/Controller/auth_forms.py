from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField
from wtforms_sqlalchemy.fields import QuerySelectMultipleField
from wtforms.fields.core import DecimalField, IntegerField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import  ValidationError, DataRequired, EqualTo, Length, Email
from wtforms.widgets import CheckboxInput, ListWidget, TextArea

from app.Model.models import User, ResearchField, ProgrammingLanguage

def get_field():
    return ResearchField.query.all()

def get_fieldlabel(theField):
    return theField.name

def get_language():
    return ProgrammingLanguage.query.all()

def get_languagelabel(theLanguage):
    return theLanguage.name

class FacultyRegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Email()])
    name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    wsu_id = StringField('WSU ID', validators=[DataRequired()])
    email = StringField('Secondary Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number')
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Submit')

    def validate_wsu_id(self, wsu_id):
        id = wsu_id.data
        id_length = len(id)
        user = User.query.filter_by(wsu_id=id).first()
        if user is not None:
            raise ValidationError(f"The WSU ID {id} is already associated with an account.")
        if id_length < 6 or id_length > 10 or not id.isnumeric():
            raise ValidationError(f"This is not a valid WSU ID.")
        

    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user is not None:
            raise ValidationError(f"The wsu email {username.data} already has an account.")
        usernamed = username.data
        if usernamed.__contains__('@'):
            split_email = usernamed.split('@')
            if split_email[1] != 'wsu.edu':
                raise ValidationError(f"That is not a wsu email.")

    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()

        if user is not None:
            raise ValidationError(f"The email {email.data} is already in use.")
    
    def validate_phone(self, phone):
        n = ''.join(filter(str.isdigit, phone.data))
        if len(n) < 7:
            raise ValidationError("Please enter a 7 digit or greater phone number")

class StudentRegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Email()])
    name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    wsu_id = StringField('WSU ID', validators=[DataRequired()])
    email = StringField('Secondary Email', validators=[Email()])
    phone = StringField('Phone Number')
    gpa = StringField('GPA')
    major = StringField('Major')
    graduation_year = StringField('Graduation Year')
    taken_courses = TextAreaField('Courses Taken')
    prior_experience = TextAreaField('Prior Experience')
    research_fields = QuerySelectMultipleField('Research fields', query_factory= get_field, get_label= get_fieldlabel,
                    widget=ListWidget(prefix_label=False), option_widget=CheckboxInput())
    languages = QuerySelectMultipleField('Programming Languages', query_factory= get_language, get_label= get_languagelabel,
                    widget=ListWidget(prefix_label=False), option_widget=CheckboxInput())
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Submit')

    def validate_wsu_id(self, wsu_id):
        id = wsu_id.data
        id_length = len(id)
        user = User.query.filter_by(wsu_id=id).first()
        if user is not None:
            raise ValidationError(f"The WSU ID {id} is already associated with an account.")
        if id_length < 6 or id_length > 10 or not id.isnumeric():
            raise ValidationError(f"This is not a valid WSU ID.")

    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user is not None:
            raise ValidationError(f"The wsu email {username.data} already has an account.")
        usernamed = username.data

        if usernamed.__contains__('@'):
            split_email = usernamed.split('@')
            if split_email[1] != "wsu.edu":
                raise ValidationError(f"This is not a wsu email.")

    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()

        if user is not None:
            raise ValidationError(f"The email {email.data} is already in use.")
    
    def validate_phone(self, phone):
        n = ''.join(filter(str.isdigit, phone.data))
        if len(n) < 7:
            raise ValidationError("Please enter a 7 digit or greater phone number")
    
    def validate_gpa(self, gpa):
        gpad = gpa.data
        gpad = float(gpad)
        if gpad < 0 or gpad > 4:
            raise ValidationError("GPA range is 0 to 4.0")
    
    

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
