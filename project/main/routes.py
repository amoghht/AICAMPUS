from flask import Blueprint
from flask import render_template



main=Blueprint('main',__name__)

@main.route('/')
@main.route('/home')      #2 routes for same web page. Also know as decorators
def home_page():
    return render_template("home.html")

@main.route('/about_developers', methods=["GET", "POST"])
def about_developers():
    return render_template('about_developers.html')