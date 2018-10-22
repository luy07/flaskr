from flask import Blueprint, render_template, request, redirect, url_for, flash,session
from flask import jsonify
import time

html = Blueprint('html', __name__, url_prefix='/')
ws = Blueprint('ws', __name__, url_prefix='/')


@html.route('/')
@html.route('/index')
def hello_world():
    return render_template('home/home.html')


@html.route('login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'default':
            flash('login successful')
            session['logined']=True
            return redirect(url_for('backend.index'))
        else:
            flash('invalid username or password')
            return redirect(url_for('.error_show'))
    else:
        return render_template('home/login.html')


@html.route('error')
def error_show():
    return render_template('error.html')

@html.route('jsontest')
def jsontest():
    return jsonify(msg='ok')

@ws.route("ws_test")
def ws_test(socket):
    rd=socket.receive()
    socket.send('server receive:%s'% rd)
    for i in range(1,1000):
        socket.send('loop %s ' % i)
        if i%5==0:
            socket.close('end')
            time.sleep(3)
        time.sleep(1)