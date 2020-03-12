from app import app
from flask import render_template, request, flash, redirect, url_for, current_app
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user
from app.models import User, Role
from werkzeug.urls import url_parse
from app import db
from app.forms import RegistrationForm, ResetPasswordRequestForm, ResetPasswordForm
from app.email import send_password_reset_email

from flask_admin import Admin, BaseView, expose
import flask_admin as admin
from app.decorators import admin_required, permission_required
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView



class MyAdmin(admin.AdminIndexView):
    @expose('/')
    @admin_required
    def index(self):
        print(current_user.get_id())
        return super(MyAdmin, self).index()

admin = Admin(app, name='samaraCTF', template_mode='bootstrap3', index_view=MyAdmin())
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Role, db.session))




@app.route('/',methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/login',methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))

        # Keep the user info in the session using Flask-Login
        login_user(user, remember=form.remember_me.data)


        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html',
                           title='Reset Password', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)




