from __future__ import print_function
import sys
from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request
from flask_sqlalchemy import sqlalchemy
from config import Config

from app import db
from app.Model.models import User, Professor, Student
from app.Controller.auth_forms import StudentRegistrationForm, FacultyRegistrationForm ,LoginForm
from flask_login import current_user
from flask_login.utils import login_required, login_user, logout_user

bp_auth = Blueprint('auth', __name__)
bp_auth.template_folder = Config.TEMPLATE_FOLDER 

@bp_auth.route('/register', methods=['GET'])
def register():
    return render_template('RegisterLanding.html', title="Register")


@bp_auth.route('/registerfaculty', methods=['GET', 'POST'])
def registerfaculty():
    if current_user.is_authenticated:
        return redirect(url_for('routes.index'))
        
    form = FacultyRegistrationForm()

    if form.validate_on_submit():
        professor = Professor(
            username=form.username.data,
            email=form.email.data,
            name=form.name.data,
            last_name=form.last_name.data,
            wsu_id=form.wsu_id.data,
            phone=form.phone.data,
        )
        professor.set_password(form.password.data)
        db.session.add(professor)
        db.session.commit()
        flash("You've registered!")
        return redirect("/")
    return render_template("register_faculty.html", form=form)


@bp_auth.route('/registerstudent', methods=['GET', 'POST'])
def registerstudent():
    if current_user.is_authenticated:
        return redirect(url_for('routes.index'))
        
    form = StudentRegistrationForm()

    if form.validate_on_submit():
        student = Student(
            username=form.username.data,
            email=form.email.data,
            name=form.name.data,
            last_name=form.last_name.data,
            wsu_id=form.wsu_id.data,
            phone = form.phone.data,
            gpa = form.gpa.data,
            major=form.major.data,
            graduation_year = form.graduation_year.data,
            taken_courses=form.taken_courses.data,
            prior_experience = form.prior_experience.data
        )
        student.set_password(form.password.data)
        db.session.add(student)
        for l in form.languages.data:
            student.languages.append(l)
        for f in form.research_fields.data:
            student.research_fields.append(f)
        db.session.commit()
        flash("You've registered!")
        return redirect("/")
    return render_template("register_student.html", form=form)

@bp_auth.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('routes.index'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("auth.login"))
        login_user(user, remember = form.remember_me.data)
        return redirect(url_for('routes.index'))

    return render_template("login.html", form=form)

@bp_auth.route("/editprofile/<user_id>", methods=['GET', 'POST'])
def editprofile(user_id):
    if (current_user.id != int(user_id)):
        flash("You are not authorized to view this page")
        return redirect(url_for('routes.index'))
    if current_user.is_professor():
        form = FacultyRegistrationForm()
        user = current_user
        if request.method == 'POST':
            
            user.username=form.username.data
            user.email=form.email.data
            user.name=form.name.data
            user.last_name=form.last_name.data
            user.wsu_id=form.wsu_id.data
            user.phone=form.phone.data
            db.session.add(user)
            db.session.commit()
            flash("Your changes have been saved")
            return redirect(url_for('routes.index'))
        elif request.method == 'GET':
            form.username.data = user.username
            form.email.data = user.email
            form.name.data = user.name
            form.last_name.data = user.last_name
            form.wsu_id.data = user.wsu_id
            form.phone.data = user.phone
        else:
            pass
        return render_template('edit_professor_prof.html', title= 'Edit Profile', form=form)
    else:
        form = StudentRegistrationForm()
        user = Student.query.filter_by(id=current_user.id).first()
        if request.method == 'POST':
            user.username=form.username.data
            user.email=form.email.data
            user.name=form.name.data
            user.last_name=form.last_name.data
            user.wsu_id=form.wsu_id.data
            user.phone = form.phone.data
            user.gpa = form.gpa.data
            user.major=form.major.data
            user.graduation_year = form.graduation_year.data
            user.taken_courses=form.taken_courses.data
            user.prior_experience = form.prior_experience.data
            db.session.add(user)
            old_fields = user.research_fields.all()
            for f in old_fields:
                user.research_fields.remove(f)
            new_fields = form.research_fields.data
            for f in new_fields:
                user.research_fields.append(f)
            old_lang = user.languages.all()
            for f in old_lang:
                user.languages.remove(f)
            new_lang = form.languages.data
            for f in new_lang:
                user.languages.append(f)
            db.session.commit()
            flash("Your changes have been saved")
            return redirect(url_for('routes.index'))
        elif request.method == "GET":
            form.username.data = user.username
            form.email.data=user.email
            form.name.data = user.name
            form.last_name.data = user.last_name
            form.wsu_id.data = user.wsu_id
            form.phone.data = user.phone
            form.gpa.data = user.gpa
            form.major.data = user.major
            form.graduation_year.data = user.graduation_year
            form.taken_courses.data = user.taken_courses
            form.prior_experience.data = user.prior_experience
            fields = user.research_fields.all()
            form.research_fields._set_data(fields)
            lang = user.languages.all()
            form.languages._set_data(lang)
        else:
            pass
        return render_template('edit_student_prof.html', title= 'Edit Profile', form=form)
    



@login_required
@bp_auth.route('/logout')
def logout():
    logout_user()
    flash("You've logged out")
    return redirect(url_for('auth.login'))