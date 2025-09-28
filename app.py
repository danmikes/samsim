import os
from flask import flash, Flask, render_template, request, jsonify
from flask_mail import Mail, Message
from config import get_config

app = Flask(__name__)
app.config.update(get_config())
mail = Mail(app)

@app.route('/')
def index():
  return render_template('index.htm')

@app.route('/service')
def service():
  return render_template('service.htm')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
  if request.method == 'POST':
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    try:
      msg = Message(
        subject=f"Message from {name}",
        recipients=['max8@post.cz'],
        reply_to=email
      )
      msg.body = f"""
Name: {name}
Email: {email}
Message: {message}
      """
      mail.send(msg)
      flash(f'Thank you {name}! Your message was sent.', 'success')
    except Exception as e:
      flash('Your message was not sent', 'error')
      print(f"Email error: {e}")

  return render_template('contact.htm')

@app.route('/health')
def health_check():
  return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)
