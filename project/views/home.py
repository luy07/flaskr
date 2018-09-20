from flask import Blueprint, render_template, request, redirect, url_for, flash

mod = Blueprint('home', __name__, url_prefix='/')


@mod.route('/')
@mod.route('/index')
def hello_world():
    # return 'Hello World!'
    return render_template('home/home.html')


@mod.route('login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'default':
            flash('login successful')
            return redirect(url_for('backend.index'))
        else:
            flash('invalid username or password')
            return redirect(url_for('.error_show'))
    else:
        return render_template('home/login.html')


@mod.route('error')
def error_show():
    return render_template('error.html')
