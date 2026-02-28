from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from .models import User
from . import _db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('main.index'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('auth/login.html')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists', 'error')
            return redirect(url_for('auth.register'))
        
        new_user = User(username=username)
        new_user.set_password(password)
        _db.session.add(new_user)
        _db.session.commit()
        
        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html')

@bp.route('/forgot-password', methods=('GET', 'POST'))
def forgot_password():
    if request.method == 'POST':
        username = request.form['username']
        user = User.query.filter_by(username=username).first()

        if user:
            token = user.generate_reset_token()
            reset_link = url_for('auth.reset_password', token=token)
            flash(f'Use this link to reset your password: {reset_link}', 'success')
        else:
            flash('If an account exists, a password reset link has been generated.', 'success')

        return redirect(url_for('auth.login'))

    return render_template('auth/forgot_password.html')

@bp.route('/reset-password/<token>', methods=('GET', 'POST'))
def reset_password(token):
    user = User.verify_reset_token(token)
    if not user:
        flash('Invalid or expired password reset link', 'error')
        return redirect(url_for('auth.forgot_password'))

    if request.method == 'POST':
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('auth/reset_password.html', token=token)

        user.set_password(password)
        _db.session.commit()
        flash('Password has been reset successfully. Please log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/reset_password.html', token=token)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
