from flask import Blueprint, current_app, render_template
from app.service.app_service import service

setting = Blueprint('setting', __name__,
                     static_folder='.',
                     static_url_path='/static',
                     template_folder='.',
                     url_prefix='/setting')

@setting.route('/')
def view():
  data = service.get_settings()

  return render_template('blueprint/setting/view.htm', data=data)
