# coding:utf-8
import hashlib
from flask import render_template, request, jsonify, send_from_directory, session, url_for, flash

from werkzeug.utils import redirect
from web import app

from web.forms import RegistrationForm, LoginForm
from web.models import User


__author__ = '4ikist'


# forms

# views
@app.route('/user/register', methods=['GET', 'POST'])
def user_register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        form = RegistrationForm(request.form)
        if not form.validate():
            return jsonify({'error': 'bad form: %s' % form})
            # return render_template('error.html', details='bad form: e-mail is %s' % user_credentials.get('email'))

        new_user = User(login=form.email.data, password=form.password.data)
        new_user.save()

        flash('Thanks for registering')
        return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        form = LoginForm(request.form)
        if not form.validate():
            return jsonify({'error': 'bad form %s' % form})

        username = form.email.data
        password = form.password.data
        user = User.check_and_return(username, password)
        if user is None:
            return redirect('/login')

        session['current_user_id'] = user.id
        session['current_user'] = user
        return redirect('/user')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('current_user', None)
    session.pop('current_user_id', None)
    return redirect(url_for('/'))


@app.route('/')
def index():
    params = {}
    if session['current_user']:
        params['current_user'] = '%s %s' % ()
    return render_template('index.html', **{})


@app.route('/transducer/register', methods=["POST"])
def transducer_register():
    transducer_data = request.form


@app.route('/user/register', methods=['POST'])
def user_register():
    pass


@app.route('/add_transducer', methods=['POST'])
def add_transducer():
    pass


@app.route('/<path:resource>')
def serveStaticResource(resource):
    return send_from_directory('static/', resource)


@app.route('/user/receptors/<int:receptor_id>', methods=['POST'])
def accept_receptor_data(receptor_id):
    pass