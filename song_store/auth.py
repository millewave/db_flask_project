import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from song_store.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')
ADD_USER = "INSERT INTO Users (user_name, age, password) VALUES (?, ?, ?)"
@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        user_name = request.form['user_name']
        age_str = request.form['age']
        password = request.form['password']
        db = get_db()
        error = None

        if not user_name:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        else:
            try:
                age = int(age_str)
            except ValueError:
                error = f"Age {age_str} should be an integer."
            else:
                if age < 14 or age > 100:
                    error = f"Invalid age {age}."

        if error is None:
            try:
                db.execute(
                    ADD_USER,
                    (user_name, age, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {user_name} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        user_name = request.form['user_name']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM Users WHERE user_name = ?', (user_name,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_name'] = user['user_name']
            return redirect(url_for('song.list_songs'))

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_name = session.get('user_name')

    if user_name is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM Users WHERE user_name = ?', (user_name,)
        ).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('song.list_songs'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
