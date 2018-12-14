from flask import render_template, Blueprint

main = Blueprint('main', __name__)


@main.route("/")
def main():
	return render_template('index.html')


@main.route("/home")
def home_main():	
	return render_template('home.html')