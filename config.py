import os

def get_config():
  return {
    'SECRET_KEY': os.environ.get('SECRET_KEY', 'dev-key' + os.urandom(16).hex()),

    'MAIL_SERVER': 'smtp.post.cz',
    'MAIL_PORT': 587,
    'MAIL_USE_TLS': True,
    'MAIL_USE_SSL': False,
    'MAIL_USER': os.environ.get('MAIL_USER'),
    'MAIL_PASS': os.environ.get('MAIL_PASS'),
    'MAIL_DEFAULT_SENDER': os.environ.get('MAIL_USER'),

    'MAIL_DEBUG': True,
  }
