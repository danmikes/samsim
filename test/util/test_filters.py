import pytest
from app import create_app

class TestTemplateFilters:

  @pytest.fixture
  def app_with_filters(self):
    app = create_app()
    return app

  def test_last_filter(self, app_with_filters):
    with app_with_filters.app_context():
      filters = app_with_filters.jinja_env.filters
      assert filters['last']([1, 2, 3]) == 3
      assert filters['last']([]) is None
      assert filters['last']('hello') == 'o'

  def test_first_filter(self, app_with_filters):
    with app_with_filters.app_context():
      filters = app_with_filters.jinja_env.filters
      assert filters['first']([1, 2, 3]) == 1
      assert filters['first']([]) is None
      assert filters['first']('hello') == 'h'

  def test_format_number_filter(self, app_with_filters):
    with app_with_filters.app_context():
      filters = app_with_filters.jinja_env.filters
      assert filters['format_number'](1234.567) == '1_234'
      assert filters['format_number'](1000000) == '1_000_000'
      assert filters['format_number']('invalid') == 'invalid'
      assert filters['format_number'](0) == '0'

  def test_safe_subtract_filter(self, app_with_filters):
    with app_with_filters.app_context():
      filters = app_with_filters.jinja_env.filters
      assert filters['safe_subtract']([10, 5]) == -5
      assert filters['safe_subtract']([1, 2, 3, 4]) == 3
      assert filters['safe_subtract']([10]) == 0
      assert filters['safe_subtract']([]) == 0
      assert filters['safe_subtract'](['invalid', 'values']) == 0
