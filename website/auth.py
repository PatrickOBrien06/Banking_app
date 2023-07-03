from re import escape, match
from flask import Blueprint, render_template, request, flash, redirect, url_for
from . import db
from .models import Users
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# Create authentication 
auth = Blueprint('auth', __name__)

# Allow GET and POST methods on /signup
@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = escape(request.form.get('email'))
        username = escape(request.form.get('username'))
        password1 = escape(request.form.get('password1'))
        password2 = escape(request.form.get('password2'))

        # Validate and check inputs 
        email_exists = Users.query.filter_by(email=email).first()
        if email_exists:
            flash('Email already exists.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        
        # Submit checked inputs
        else: 
            new_user = Users(email=email, username=username, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Signed Up!')
            return redirect(url_for('views.home'))
    return render_template('signup.html')

# Allow GET and POST methods on /login
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = escape(request.form.get('email'))
        password = escape(request.form.get('password'))

        # Validate and check before submitting
        user = Users.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in!', category='success')
                login_user(user, remember=False)
                return redirect(url_for('views.home'))
        else:
            flash('Email or Password is incorrect.', category='error')
    return render_template('login.html')

# Authenticate for logout() func and redirect to 'login.home'
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))