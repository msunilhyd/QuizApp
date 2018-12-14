
from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flaskBlog import db, bcrypt	
from flaskBlog.models import User
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
from flaskBlog.users.utils import save_profile_picture, send_reset_email
from flaskBlog.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
								  RequestResetForm, ResetPasswordForm)
users = Blueprint('users', __name__)

@users.route("/register", methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username = form.username.data, email = form.email.data, password = hashed_password)
		db.session.add(user)
		db.session.commit()
		flash('Your Account has been created ! You should be able to Login', 'success')
		return redirect(url_for('users.login'))
	return render_template('register.html', title='Register', form=form)



@users.route("/login", methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('main.home'))
		else:
			flash('Login Unsuccessful, Check email and password', 'danger')

	return render_template('login.html', title='Login', form=form)


@users.route("/logout")
def logout():
	logout_user()
	return render_template('index.html')


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
	form = UpdateAccountForm()
	if form.validate_on_submit():
		if form.picture.data:
			picture_file = save_profile_picture(form.picture.data)
			current_user.image_file = picture_file
		current_user.username = form.username.data
		current_user.email = form.email.data
		db.session.commit()	
		flash('Your Account has been Updated !', 'success')
		return redirect(url_for('users.account'))		
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email	
	image_file = url_for('static', filename = 'profile_pics/' + current_user.image_file)
	return render_template('account.html', title="Account", image_file=image_file, form=form)




@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = RequestResetForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		send_reset_email(user)
		flash('An email has been sent with instructions to reset your password.', 'info')
		return redirect(url_for('users.login'))
	return render_template('reset_request.html', title="Reset Password", form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_password_with_token(token):
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	user = User.verify_reset_token(token)
	if user is None:
		flash('That is an invalid or expired token', 'warning')
		return redirect(url_for('users.reset_request'))
	form = ResetPasswordForm()
	if form.validate_on_submit():
		print("ResetPasswordForm has been validated")
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user.password = hashed_password
		db.session.commit()
		flash('Your Account has been updated ! You should be able to Login', 'success')
		return redirect(url_for('users.login'))
	print("ResetPasswordForm has NOT been validated")
	return render_template('reset_token.html', title="Reset Password", form=form) 