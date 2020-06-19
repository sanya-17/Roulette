from flask import Flask, url_for, redirect, render_template, request, flash
from forms import RegistrationForm, LoginForm
app = Flask(__name__)
app.config['SECRET_KEY'] = '4197c06cb65a641d37a7c1c096782b3c'


@app.route("/", methods=['POST', 'GET'])
def register():
    form = RegistrationForm()
    # returns true if there is a PUT/POST request and all of the validators pass
    if form.validate_on_submit():
        # dummy message
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))

    # render template on GET request
    return render_template('register.html', form=form)


@app.route("/login", methods=['POST', 'GET'])
def login():
    form = LoginForm()
    # returns true if there is a PUT/POST request and all of the validators pass
    if form.validate_on_submit():
        flash(f'Logged in {form.email.data}!', 'success')  # dummy message
        return redirect(url_for('home'))

    # render template on get request
    return render_template('login.html', form=form)


@app.route("/home")
def home():
    return render_template('user_home.html')


if __name__ == '__main__':
    app.run(debug=True)
