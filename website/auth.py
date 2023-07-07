from flask import Blueprint, render_template, request, flash, redirect, url_for
from . import db
from .models import Users, History
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# Create authentication 
auth = Blueprint('auth', __name__)

# Allow GET and POST methods on /signup
@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        init_balance = request.form.get('init_balance')

        # Validate and check inputs 
        email_exists = Users.query.filter_by(email=email).first()
        if email_exists:
            flash('Email already exists.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        
        # Submit checked inputs
        else: 
            new_user = Users(email=email, username=username, password=generate_password_hash(password1, method='sha256'), balance=init_balance)
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
        email = request.form.get('email')
        password = request.form.get('password')

        # Validate and check before submitting
        user = Users.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in!', category='success')
                login_user(user, remember=False)
                return redirect(url_for('views.home'))
            else:
                flash('Email or Password is incorrect.', category='error')
        else:
            flash('Email or Password is incorrect.', category='error')
    return render_template('login.html')

# Authenticate for logout() func and redirect to 'login.home'
@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

# Page for trans
@auth.route('/transactions', methods=['GET', 'POST'])
@login_required
def transactions():
    if request.method == 'POST':
        amount = float(request.form.get('amount'))
        receiver_email = request.form.get('receiver_email')
        sender_email = request.form.get('sender_email')
        sender_password = request.form.get('sender_password')

        user = Users.query.filter_by(email=sender_email).first()
        receiver = Users.query.filter_by(email=receiver_email).first()

        if not amount or not receiver_email or not sender_email or not sender_password:
            flash('Please fill in all information', category='error')

        elif not user or not check_password_hash(user.password, sender_password):
            flash('Email or Password invalid.', category='error')
        
        elif not receiver:
            flash('Receiver Email doesn\'t exist.', category='error')
        
        elif user.balance < amount:
            flash('You have insufficient funds to perform the transaction.', category='error')

        else:
            user.balance -= amount
            receiver.balance += amount
            round(user.balance, 2)
            round(receiver.balance, 2)
            new_transaction = History(sender_id=current_user.id, receiver_id=receiver.id, amount_sent=amount, transaction_type='fund_transfer')
            current_user.sent_history.append(new_transaction)
            receiver.received_history.append(new_transaction)
            db.session.add(new_transaction)
            db.session.commit()
            flash('Transfer Successful!', category='success')

    return render_template('transactions.html')
    