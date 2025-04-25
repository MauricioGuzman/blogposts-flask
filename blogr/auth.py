import functools

from flask import  Blueprint, render_template, request, url_for, redirect, flash, session, g
from sqlalchemy.testing.suite.test_reflection import users
from sqlalchemy.util import methods_equivalent
#auth son las vistas

from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from blogr import  db

bp = Blueprint('auth', __name__, url_prefix= '/auth')


@bp.route('/register', methods = ('GET', 'POST'))
def register():

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        user = User(username, email, generate_password_hash(password))

        #validacion de datos
        error = None
        #comparando nombre de usaurio con los existentes
        user_email = User.query.filter_by(email = email).first()
        if user_email == None:
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('auth.login'))
        else:
            error = f'El correo {email} ya esta registrado'
        flash(error)
    return render_template('auth/register.html')

@bp.route('/login',  methods = ('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        #validando datos
        error = None
        user = User.query.filter_by(email = email).first()

        if user == None or not check_password_hash(user.password, password): #compureba pass y usuario
            error = 'Correo o contraseña incorrecta'

        #inciando sesion, borra sesion iniciada y crea una nueva con el usuario
        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('post.posts'))
        flash(error)
    return render_template('auth/login.html')

#mantiene sesion
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get_or_404(user_id)

 #CERRAR SESION y redirecciona ala pag principal
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home.index'))

import functools

#se requiere iniciar sesion
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view()

#editar perfil
from werkzeug.utils import secure_filename
def get_photo(id):
    user = User.query.get_or_404(id)
    photo = None
    if photo != None:
        photo = user.photo
    return photo

@bp.route('/profile/<int:id>', methods=('GET','POST'))
#@login_required
def profile(id):
    user = User.query.get_or_404(id)
    photo = get_photo(id)
    if request.method == 'POST':
        user.username = request.form.get('username')
        password = request.form.get('password')

        error = None
        if len(password) !=0:
            user.password = generate_password_hash(password)
        elif len(password) > 0 and len(password) < 6:
            error = 'La contraseña debe tener mas de 5 caracteres'
        #con lo siguiente, guarda el nombre de la foto en la ruta indicada
        if request.files['photo']: #el id dentro de profile html se llama photo
            photo = request.files['photo']
            photo.save(f'blogr/static/media/{secure_filename(photo.filename)}')
            user.photo = f'media/{secure_filename(photo.filename)}'

        if error is not None:
            flash(error)
        else:
            db.session.commit()
            return redirect(url_for('auth.profile', id = user.id))

        flash(error)

    return render_template('auth/profile.html', user = user)



