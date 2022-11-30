from flask import Blueprint, render_template, request, flash, redirect, url_for
from . import db
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('password doesn\'t match', category='error')
        else:    
            flash('The email you\'ve specified does\' match any account', category='error')
    return render_template("signin.html", user=current_user)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter_by(email=email).first()
        if(user != None):
            flash('email already exists', category='error')
        elif password1 != password2:
            flash('passwords don\'t match!', category='error')
        elif "@" not in email:
            flash('this is not an email bud', category='error')
        elif " " not in firstName or len(firstName) ==0:
            flash('fix your danm name', category='error')
        else:
            new_user = User(email=email, firstName=firstName, password=generate_password_hash(password1, method = 'sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('account created', category='success')
            return redirect(url_for('views.home'))
            
    return render_template("signup.html", user=current_user)
