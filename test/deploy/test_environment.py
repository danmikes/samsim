import pytest
import os
import sys
from pathlib import Path

@pytest.mark.deploy
def test_environment_sanity():
  assert sys.version_info.major == 3

  assert Path('app').exists()
  assert Path('test').exists()

  assert Path('wsgi.py').exists()
  assert Path('requirements.txt').exists()

  from app import create_app
  assert create_app is not None
