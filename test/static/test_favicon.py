import pytest
import os

@pytest.mark.frontend
def test_favicon_exists_on_disk():
  favicon_path = 'app/static/favicon.ico'
  assert os.path.exists(favicon_path), f'Favicon not found at {favicon_path}'
