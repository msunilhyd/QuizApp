from flaskBlog import db, login_manager, app
from datetime import datetime
from flask_login import UserMixin
from sqlalchemy.sql import func
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer



@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))


class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(20), unique=True, nullable=False)	
	image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
	password = db.Column(db.String(60), nullable=False)
	

	def get_reset_token(self, expires_sec=1800):
		s = Serializer(app.config['SECRET_KEY'], expires_sec)
		return s.dumps({'user_id': self.id}).decode('utf-8')

	def verify_reset_token(token):
		s = Serializer(app.config['SECRET_KEY'])
		print("Entered verify_reset_token() Method")
		try:
			user_id = s.loads(token)['user_id']
			print(user_id)
		except:
			print("Exception occured")
			return None
		return User.query.get(user_id)

	def __repr__(self):
		return "User('{}', '{}', '{}')".format(self.username, self.email, self.image_file)

	