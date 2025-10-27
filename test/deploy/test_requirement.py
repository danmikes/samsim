import re
from pathlib import Path


def test_requirements_exists():
  path = Path("requirements.txt")
  assert path.exists(), "requirements.txt missing"
  assert path.stat().st_size > 0, "requirements.txt is empty"


def test_requirements_format():
  with open("requirements.txt", "r") as f:
    for line_num, line in enumerate(f, 1):
      line = line.strip()
      if line and not line.startswith("#"):
        assert " " not in line, f"Line {line_num}: Remove spaces in '{line}'"
        assert re.match(r'^[a-zA-Z0-9_\-\.]+', line), f"Line {line_num}: Invalid format '{line}'"


def test_critical_dependencies():
  with open("requirements.txt", "r") as f:
    content = f.read().lower()
  assert "flask" in content, "Flask not found in requirements"
