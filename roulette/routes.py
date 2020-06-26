from flask import url_for, redirect, render_template, flash
from roulette import app, db, bcrypt
from roulette.forms import RegistrationForm, LoginForm
from roulette.models import User, List, Item
from flask_login import login_user, current_user, login_required, logout_user


@app.route("/", methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    # returns true if there is a PUT/POST request and all of the validators
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created', 'success')  # dummy message
        return redirect(url_for('login'))

    # render template on GET request
    return render_template('register.html', form=form)


@app.route("/login", methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    # returns true if PUT/POST request and all of the validators pass
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', form=form)


@app.route("/home")
def home():
    return render_template('user_home.html')


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('register'))
# TODO: implement logout route
# TODO: watch everything  30:00 in the corey schaffer video
# TODO: implement route for interacting with a list
# TODO: implement route for edititng an account
