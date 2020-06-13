from flask import Flask, url_for, redirect, render_template
from forms import RegistrationForm, LoginForm
app = Flask(__name__)
app.config['SECRET_KEY'] = '4197c06cb65a641d37a7c1c096782b3c'


@app.route("/", methods=['POST', 'GET'])
def home():
    return render_template('base.html', text="<h1>toodles to you..</h1>")


@app.route("/register", methods=['POST', 'GET'])
def register():
    form = RegistrationForm()
    return render_template('register.html', title='Register', form=form)


@app.route("/login")
def login():
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)


if __name__ == '__main__':
    app.run(debug=True)
