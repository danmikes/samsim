import os

class Config:
  SECRET_KEY = os.environ.get('SECRET_KEY') or'top-secret'

  SIMULATION_CONFIG = {
    'DUR': int(1e6),
    'SIG': int(1e3),
    'SAM': int(1e2),
    'REP': int(1e1),
  }
