from flask import Blueprint, jsonify, render_template
from app import service

setting = Blueprint('setting', __name__,
                     static_folder='.',
                     static_url_path='/static',
                     template_folder='.')

@setting.route('/')
def view():
  data = service.get_settings()

  return render_template('blueprint/setting/view.htm', **data)
