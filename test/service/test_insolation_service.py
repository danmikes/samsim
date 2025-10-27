import pytest
import math
from app.service.insolation_service import InsolationService
from app.config import Config

class TestInsolationService:
  @pytest.fixture
  def insolation_service(self):
    return InsolationService()

  def test_run_insolation_returns_dict(self, insolation_service):
    result = insolation_service.run_insolation()
    assert isinstance(result, dict)
    assert 'time' in result
    assert 'total_signal' in result
    assert len(result['time']) == int(1e3)

  def test_run_insolation_has_correct_signal_columns(self, insolation_service):
    result = insolation_service.run_insolation()
    expected_signal_count = len(Config.signal.signals)
    signal_columns = [key for key in result.keys() if key.startswith('signal_')]
    assert len(signal_columns) == expected_signal_count
    for i in range(expected_signal_count):
      assert f'signal_{i}' in result

  def test_total_signal_calculation(self, insolation_service):
    result = insolation_service.run_insolation()
    signal_cols = [key for key in result.keys() if key.startswith('signal_')]
    calculated_total = []
    for i in range(len(result['time'])):
      total = sum(result[col][i] for col in signal_cols)
      calculated_total.append(total)
    assert result['total_signal'] == calculated_total

  def test_sine_function_scalar(self, insolation_service):
    t = 1.0
    result = insolation_service.sine(A=1, T=1, t=t)
    expected = 1 * math.sin(2 * math.pi * 1/1 * t + 0)
    assert result == expected

  def test_sine_function_list(self, insolation_service):
    t = [0, 1, 2]
    result = insolation_service.sine(A=1, T=1, t=t)
    expected = [1 * math.sin(2 * math.pi * 1/1 * x + 0) for x in t]
    assert result == expected

  def test_cosine_function_scalar(self, insolation_service):
    t = 1.0
    result = insolation_service.cosine(Am=1, Tm=1, t=t)
    expected = 1 * math.cos(2 * math.pi * 1/1 * t + 0)
    assert result == expected

  def test_cosine_function_list(self, insolation_service):
    t = [0, 1, 2]
    result = insolation_service.cosine(Am=1, Tm=1, t=t)
    expected = [1 * math.cos(2 * math.pi * 1/1 * x + 0) for x in t]
    assert result == expected

  def test_clear_cache(self, insolation_service):
    result1 = insolation_service.run_insolation()
    result2 = insolation_service.run_insolation()

    assert result1 is result2

    insolation_service.clear_cache()
    result3 = insolation_service.run_insolation()

    assert result1 is not result3
    assert result1['time'] == result3['time']
    assert result1['total_signal'] == result3['total_signal']
