from flask import Blueprint, render_template

help = Blueprint('help', __name__,
                     static_folder='.',
                     static_url_path='/static',
                     template_folder='.')

@help.route('/')
def view():
  return render_template('blueprint/help/view.htm')
