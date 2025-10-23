from flask import Blueprint, render_template

home = Blueprint('home', __name__, static_folder='.', template_folder='.')

@home.route('/')
def index():
  return render_template('index.htm')
