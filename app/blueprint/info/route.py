from flask import Blueprint, render_template

info = Blueprint('info', __name__,
                     static_folder='.',
                     static_url_path='/info',
                     template_folder='.',
                     url_prefix='/info')

@info.route('/')
def view():
  return render_template(
    'blueprint/info/view.htm',
    page_title="Info"
  )
