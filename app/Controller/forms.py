from inspect import _empty
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, DateField
from wtforms import validators
from wtforms.fields.core import BooleanField
from wtforms.fields.simple import PasswordField, TextAreaField
from wtforms.validators import  DataRequired, Length, EqualTo, Email, ValidationError
from wtforms_sqlalchemy.fields import QuerySelectMultipleField
from wtforms.widgets import CheckboxInput, ListWidget
from app.Model.models import ResearchField
from datetime import date


def get_field():
    return ResearchField.query.all()

def get_fieldlabel(theField):
    return theField.name

class PostForm(FlaskForm):
    title = StringField('Research project title', validators=[DataRequired()])
    description = TextAreaField('Goals and objectives', [Length(min=1,max=1500)])
    start_date = DateField('Starting Date', format='%m/%d/%Y', default=date.today)
    end_date = DateField('End Date', format='%m/%d/%Y', default=date.today)
    time_commitment = TextAreaField('Required time commitment', [Length(min=1,max=150)])
    research_field = QuerySelectMultipleField('Research fields', query_factory= get_field, get_label= get_fieldlabel,
                    widget=ListWidget(prefix_label=False), option_widget=CheckboxInput())
    requirements = TextAreaField('Applicant requirements', [Length(min=1,max=700)])
    submit = SubmitField('Post')

    def validate_end_date(self, end_date):
        start = self.start_date.data
        if start > end_date.data :
            raise ValidationError('End date must not be before start date')


# class EditPostForm(FlaskForm):
#     title = StringField('Research project title', validators=[DataRequired()])
#     description = TextAreaField('Goals and objectives', [Length(min=1,max=1500)])
#     start_date = DateField('Starting Date', format='%m/%d/%Y')
#     end_date = DateField('End Date', format='%m/%d/%Y')
#     time_commitment = TextAreaField('Required time commitment', [Length(min=1,max=150)])
#     research_field = QuerySelectMultipleField('Research fields', query_factory= get_field, get_label= get_fieldlabel,
#                     widget=ListWidget(prefix_label=False), option_widget=CheckboxInput())
#     requirements = TextAreaField('Applicant requirements', [Length(min=1,max=700)])
#     submit = SubmitField('Confirm Changes')

#     def validate_end_date(self, end_date):
#         start = self.start_date.data
#         if start > end_date.data :
#             raise ValidationError('End date must not be before start date')

class ApplicationForm(FlaskForm):
    statement = TextAreaField('Personal Statement', [Length(min=1,max=1500)])
    reference_name = StringField('First and last name',[Length(min=1,max=30)])
    reference_email = StringField('WSU Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Apply')

class SortForm(FlaskForm):
    sort_by = SelectField('Sort by', choices=[('start_date', 'Start Date'), ('end_date', 'End Date'), ('title', 'Title')])
    start_date = DateField('Starting Date', validators=(validators.Optional(),))
    end_date = DateField('End Date', validators=(validators.Optional(),))
    research_field = QuerySelectMultipleField('Research fields', query_factory= get_field, get_label= get_fieldlabel,
                    widget=ListWidget(prefix_label=False), option_widget=CheckboxInput())
    submit = SubmitField('Sort')