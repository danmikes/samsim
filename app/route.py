from flask import Blueprint, render_template

base = Blueprint('base', __name__, static_folder='.', template_folder='.')

@base.route('/')
def index():
  return render_template('index.htm', page_title='Home')

@base.route('/health')
def health():
  return 'status: healthy'
