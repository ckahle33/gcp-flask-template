from app import db, oauth
from app.models import User
from app.auth import blueprint
from flask import render_template, url_for, session, redirect
import os

oauth.register(
    name='github',
    authorize_url='https://github.com/login/oauth/authorize',
    access_token_url='https://github.com/login/oauth/access_token',
    client_id=os.getenv('GITHUB_CLIENT_ID'),
    client_secret=os.getenv('GITHUB_CLIENT_SECRET'),
    api_base_url='https://api.github.com'
)

oauth.register(
    name='google',
    client_id=os.getenv('GOOGLE_CLIENT_ID'),
    client_secret=os.getenv('GOOGLE_CLIENT_SECRECT'),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)

@blueprint.route('/login/<name>')
def login(name):

    client = oauth.create_client(name)
    if not client:
        abort(404)

    redirect_uri = url_for('auth.auth', name=name, _external=True)
    return client.authorize_redirect(redirect_uri)

@blueprint.route('/auth/<name>')
def auth(name):
    client = oauth.create_client(name)
    if not client:
        abort(404)

    token = client.authorize_access_token()
    if 'id_token' in token:
        profile = client.parse_id_token(token)
        build_user_and_login(profile)
    else:
        resp = client.get('user', token=token)
        json = resp.json()
        profile = normalize_github_user(json)
        build_user_and_login(profile)
    return redirect('/')

@blueprint.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

# Helpers

def build_user_and_login(profile):
    if User.query.filter_by(username=profile['name']) != None:
        session['user'] = profile['name']
    else:
        user = User(username=profile['name'],
                    email=profile['email'],
                    auth_token=profile['at_hash'],
                    avatar_url=profile['picture'],
                    location=profile['locale'])
        db.session.add(user)
        db.session.commit()
        session['user'] = profile['name']

def normalize_github_user(data):
    # make github account data into UserInfo format
    params = {
        'sub': data.get('node_id'),
        'name': data.get('login'),
        'email': data.get('email'),
        'at_hash': data.get('access_token'),
        'locale': data.get('location'),
        'picture': data.get('avatar_url'),
        'preferred_username': data.get('login'),
    }
    return params
