import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)

app.config['SECRET_KEY'] = 'MY_SECRET_KEY'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format('quizuser', 'kumar', 'localhost', 3306, 'quizdb')
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager =  LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from flaskBlog.models import User


db.create_all()
db.session.commit()


app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
mail = Mail(app)

print (app.config['MAIL_USERNAME'])
print (app.config['MAIL_PASSWORD'])

print (app.config['MAIL_SERVER'])
print (app.config['MAIL_PORT'])
print (app.config['MAIL_USE_TLS'])


print(os.environ.get('EMAIL_USER'))
print(os.environ.get('EMAIL_PASS'))

from flaskBlog.users.routes import users

from flaskBlog.main.routes import main

app.register_blueprint(users)

app.register_blueprint(main)


