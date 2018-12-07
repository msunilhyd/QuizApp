from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

app.config['SECRET_KEY'] = 'MY_SECRET_KEY'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format('demouser', 'kumar', 'localhost', 3306, 'demodb')
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager =  LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from flaskBlog.models import User, Post


db.create_all()
db.session.commit()



from flaskBlog import routes



