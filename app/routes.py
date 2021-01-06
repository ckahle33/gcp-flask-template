from app import app, db
from app.models import User, Project, Organization, Tag
from flask import render_template, url_for, session, redirect

import os

@app.cli.command('seed')

def seed():
    project = Project(name="Test Project", description="Test description.....", image_url="https://source.unsplash.com/random")
    db.session.add(project)
    org = Organization(name="Test Org", description="Test description.....", image_url="https://source.unsplash.com/random")
    db.session.add(org)
    db.session.commit()

@app.route('/')
@app.route('/index')
def index():
    if session.get('user') is not None:
        user = User.query.filter_by(username=session.get('user')).first()
        return render_template('index.html', user=user)
    else:
        return render_template('index.html')


@app.route('/onboarding')
def onboarding():
    return render_template('onboarding.html')

