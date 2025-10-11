import os
from flask import flash, Flask, render_template, request, jsonify
from flask_mail import Mail, Message
from config import get_config
from datetime import datetime

app = Flask(__name__)
app.config.update(get_config())
mail = Mail(app)

@app.route('/')
def index():
  return render_template('index.htm', build=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

@app.route('/service')
def service():
  return render_template('service.htm')

@app.route('/health')
def health_check():
  return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)
