from flask import url_for, redirect, render_template, flash, request
import random
from roulette import app, db, bcrypt
from roulette.forms import RegistrationForm, LoginForm, ListForm, ItemForm
from roulette.models import User, List, Item
from flask_login import login_user, current_user, login_required, logout_user

# TODO: add a popupwindow for deleteing an item from the list
# TODO: implement route for edititng an account
# demo@testing.com, pass

# landing page and account registration


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

# login page


@app.route("/login", methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    # returns true if PUT/POST request and all of the validators pass
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # validate password
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        # redirect to login page if password fails
        else:
            flash('Login unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', form=form)

# user home page


@app.route("/home")
def home():
    lists = current_user.lists
    return render_template('user_home.html', lists=lists)

# handles logging out


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('register'))

# account page, users can reset password and change username


@app.route("/account")
@login_required
def account():
    return render_template('account.html')

# route for creating a new list


@app.route("/list/new", methods=['POST', 'GET'])
@login_required
def new_list():
    form = ListForm()
    if form.validate_on_submit():
        current_list = List(title=form.name.data, user_id=current_user.id)
        db.session.add(current_list)
        db.session.commit()
        flash('List created', 'success')
        return redirect(url_for('home'))
    return render_template('create_list.html', form=form)


# route for interacting with the list and performing CRUD operations
@app.route("/list/<int:list_id>", methods=['POST', 'GET'])
@login_required
def list(list_id):
    roulette = ""
    form = ItemForm()
    current_list = List.query.filter_by(
        user_id=current_user.id,  id=list_id).first_or_404()
    # handles roulette button press
    if request.method == 'POST':
        if request.form.get('roulette_btn'):
            roulette = random.choice(current_list.items).title
            return render_template('list.html', list=current_list, form=form, roulette=roulette)

    # handles item entry
    if form.validate_on_submit():
        # split user entry
        item_list = form.item_list.data.split(',')
        # add item to db after verifying that the item does not already exist
        for item in item_list:
            test = Item.query.filter_by(
                title=item.strip(), list_id=current_list.id).first()
            if not test:
                item_db = Item(title=item.strip(), list_id=current_list.id)
                db.session.add(item_db)
                db.session.commit()
    return render_template('list.html', list=current_list, form=form, roulette=roulette)


# route for deleting a list
@app.route("/delete/<int:list_id>", methods=['POST', 'GET'])
@login_required
def delete_list(list_id):
    current_list = List.query.get(list_id)
    title = current_list.title
    # delete items in list
    for item in current_list.items:
        db.session.delete(item)
        db.session.commit()
    # delete list
    db.session.delete(current_list)
    db.session.commit()
    flash(f"Deleted {title} List", 'success')
    return redirect(url_for('home'))
