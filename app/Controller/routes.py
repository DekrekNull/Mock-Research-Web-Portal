from __future__ import print_function
from sqlalchemy import or_

import sys
from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request
from flask_login.utils import login_required
from app.Model.models import Professor, Student, User
from config import Config

from app import db
from app.Model.models import ResearchPost, Application
from app.Controller.forms import PostForm, ApplicationForm, SortForm
from flask_login import current_user
from datetime import date, datetime

bp_routes = Blueprint('routes', __name__)
bp_routes.template_folder = Config.TEMPLATE_FOLDER #'..\\View\\templates'


@bp_routes.route('/', methods=['GET', 'POST'])
@bp_routes.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html', title="Student Research Portal")


@bp_routes.route('/new-post', methods=['GET', 'POST'])
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        newPost = ResearchPost(
            title = form.title.data, description = form.description.data,
            user_id = current_user.id, start_date = form.start_date.data,
            end_date=form.end_date.data, time_commitment=form.time_commitment.data,
            requirements=form.requirements.data
            )
        db.session.add(newPost)
        fields = form.research_field.data
        for f in fields:
            newPost.research_fields.append(f)
        db.session.commit()
        flash('"' + newPost.title + '" has been successfully created and posted!')
        return redirect(url_for('routes.index'))
    return render_template('create.html', form=form, title="New Post")

@bp_routes.route('/edit_post/<post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    form = PostForm()
    id = post_id
    post = ResearchPost.query.filter_by(id = post_id).first()

    if current_user.id != post.user_id:
        flash("You are not authorized to view this page!")
        return redirect(url_for('routes.index'))

    if request.method == 'POST':
        if form.validate_on_submit():
            post.title = form.title.data
            post.description = form.description.data
            post.start_date = form.start_date.data
            post.end_date = form.end_date.data
            post.requirements = form.requirements.data
            post.time_commitment = form.time_commitment.data
            db.session.add(post)
            old_fields = post.get_fields()
            for f in old_fields:
                post.research_fields.remove(f)
            new_fields = form.research_field.data
            for f in new_fields:
                post.research_fields.append(f)
            db.session.commit()
            flash("Your changes have been saved!")
            return redirect(url_for('routes.index'))
    elif request.method == 'GET':
        form.title.data = post.title
        form.description.data = post.description
        form.start_date.data = post.start_date
        form.end_date.data = post.end_date
        form.requirements.data = post.requirements
        form.time_commitment.data = post.time_commitment
        fields = post.get_fields()
        form.research_field._set_data(fields)
    else:
        pass
    return render_template('edit_post.html', title= 'Edit Profile', form=form, id=id)

def is_recommended(post):
    preferences = current_user.get_fields()
    i = 0
    for p in preferences:
        post_fields = post.get_fields()
        if p in post_fields:
            i = i + 1
    if i >= 2: return True

@bp_routes.route('/open_posts', methods=['GET', 'POST'])
def open_posts():
    sort_form = SortForm()
    recommendations = []
    if current_user.is_authenticated and isinstance(current_user, Student):
        sort_form = SortForm(research_field=current_user.research_fields)
        all_posts = ResearchPost.query.all()
        for p in all_posts:
            if is_recommended(p):
                recommendations.append(p)
    
    sort = ResearchPost.start_date.desc()

    if sort_form.validate_on_submit():
        if sort_form.sort_by.data == 'start_date':
            sort = ResearchPost.start_date.desc()
        elif sort_form.sort_by.data == 'end_date':
            sort = ResearchPost.end_date.desc()
        elif sort_form.sort_by.data == 'time_commitment':
            sort = ResearchPost.time_commitment.desc()
        elif sort_form.sort_by.data == 'title':
            sort = ResearchPost.title.desc()
        else:
            sort = ResearchPost.start_date.desc()
        
        if len(sort_form.research_field.data):
            #posts = ResearchPost.query.filter(ResearchPost.research_fields.any(name=sort_form.research_field.data)).order_by(sort).all()
            fields = [t.id for t in sort_form.research_field.data]
            print('fields', fields)
            posts = ResearchPost.query.filter(or_(*[ResearchPost.research_fields.any(id=f) for f in fields])).order_by(sort).all()
            #posts = ResearchPost.query.filter(ResearchPost.research_fields.any(fields)).order_by(sort).all()
            #posts = ResearchPost.query.order_by(sort).all()
        else:
            posts = ResearchPost.query.order_by(sort).all()

        if sort_form.start_date.data:
            posts = [p for p in posts if p.start_date >= sort_form.start_date.data]
        if sort_form.end_date.data:
            posts = [p for p in posts if p.end_date <= sort_form.end_date.data]
    else:
        posts = ResearchPost.query.order_by(sort).all()
    return render_template('open_posts.html', title="Available Student Research Positions", posts=posts, sort_form=sort_form, recommendations=recommendations, is_professor=False)

@bp_routes.route('/my_posts', methods=['GET'])
def my_posts():
    posts = ResearchPost.query.filter_by(user_id=current_user.id).all()
    sort_form = SortForm()

    return render_template('open_posts.html', title="My Posted Research Positions", posts=posts, sort_form=sort_form, is_professor=True)

@bp_routes.route('/post_details/<post_id>', methods=['GET'])
def post_details(post_id):
    post = ResearchPost.query.filter_by(id=post_id).first()
    return render_template('_post.html', title="Post Details", post=post)

@bp_routes.route('/post_detals/<post_id>/applicants', methods=['GET'])
def post_applicants(post_id):
    post = ResearchPost.query.filter_by(id=post_id).first()
    if current_user.id != post.user_id:
        flash("You are not authorized to view this page!")
        return redirect(url_for('routes.index'))
    return render_template('applicants.html', title="Post Applicants", post=post)

@bp_routes.route('/my_applications', methods=['GET'])
def my_applications():
    apps = Application.query.filter_by(user_id=current_user.id).all()
    post = ResearchPost
    if current_user.is_professor():
        flash("You are not authorized to view this page!")
        return redirect(url_for('routes.index'))
    return render_template('appstatus.html', title="My Applications", post = post, app=apps)



@bp_routes.route('/new-application/<post_id>', methods=['GET', 'POST'])
def new_application(post_id):
    user_applications = Application.query.filter_by(post_id=post_id).all()
    for app in user_applications:
        if app.user_id == current_user.id:
            flash('You cannot apply for the same position again!')
            return redirect(url_for('routes.post_details', post_id=post_id))
    form = ApplicationForm()
    post = ResearchPost.query.filter_by(id=post_id).first()
    if request.method == 'POST':
        if form.validate_on_submit():
            newApplication = Application(
                user_id = current_user.id,
                post_id = post_id,
                statement = form.statement.data,
                reference_name = form.reference_name.data,
                reference_email = form.reference_email.data,
                status = 'Pending'
                )
            db.session.add(newApplication)
            db.session.commit()
            flash('Successfully submitted your applicaiton to the position!')
            return redirect(url_for('routes.index'))
    return render_template('application.html', form=form, post=post, title="Application")

@bp_routes.route('/view_applicant/<applicant_id>/<application_id>', methods=['GET'])
def view_applicant(applicant_id, application_id):
    applicant = Student.query.filter_by(id=applicant_id).first()
    application = Application.query.filter_by(id=application_id).first()
    return render_template('applicant_profile.html', title="Applicant Details", applicant=applicant, application=application)

@bp_routes.route('/update_status/<application_id>/<applicant_id>/<new_status>', methods=['GET'])
def update_status(application_id,applicant_id,new_status):
    app = Application.query.filter_by(id=application_id).first()
    app.status = new_status
    db.session.commit()
    if not current_user.is_professor():
            return redirect(url_for('routes.my_applications'))
    return redirect(url_for('routes.view_applicant', application_id=application_id,applicant_id=applicant_id))

@bp_routes.route('/delete/<post_id>', methods=['GET','POST', 'DELETE'])
def delete_posts(post_id):
    post = ResearchPost.query.filter_by(id = post_id).first()
    for x in post.applications:
        app = Application.query.filter_by(id = x.id).first()
        app.status = "Not Hired"
        db.session.commit()
        post.applications.remove(x)
    for i in post.research_fields:
        post.research_fields.remove(i)
    db.session.commit()
    db.session.delete(post)
    db.session.commit()
    flash("Post Deleted")
    return redirect(url_for('routes.index'))

@bp_routes.route('/viewprofile/<user_id>', methods=['GET'])
def view_prof(user_id):
    user = User.query.filter_by(id = user_id).first()
    if(user.is_professor()):
        user = Professor.query.filter_by(id = user_id).first()
        prof = True
    else:
        user = Student.query.filter_by(id = user_id).first()
        prof = False
    return render_template('viewprofile.html', title = 'Profile', user = user, prof=prof)