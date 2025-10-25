import pytest
import numpy as np
from app.util import SimulationManager, Par

class TestSimulationManager:
  def setup_method(self):
    self.sim = SimulationManager()

  def test_initialization(self):
    assert hasattr(self.sim, 'default_pars')
    assert hasattr(self.sim, 'config')
    assert len(self.sim.default_pars) == 3
    assert all(isinstance(p, Par) for p in self.sim.default_pars)

  def test_default_parameters(self):
    pars = self.sim._get_default_parameters()
    assert len(pars) == 3
    assert all(isinstance(p, Par) for p in pars)

    for par in pars:
      assert par.T > 0
      assert par.A >= 0
      assert par.Tm > 0
      assert par.Am >= 0
      assert isinstance(par.p, (int, float))

  def test_run_insolation_default(self):
    t, signals, total = self.sim.run_insolation()

    assert isinstance(t, np.ndarray)
    assert isinstance(signals, list)
    assert isinstance(total, np.ndarray)

    assert len(t) == 1000
    assert len(signals) == 3
    assert len(total) == 1000
    assert all(len(s) == 1000 for s in signals)

  def test_run_insolation_custom_parameters(self):
    custom_pars = (
      Par(100000, 10, 500000, 5, 0),
      Par(50000, 20, 250000, 10, 0),
      Par(25000, 15, 125000, 7, 0)
    )

    t, signals, total = self.sim.run_insolation(custom_pars)

    assert len(signals) == 3
    assert len(total) == 1000

  def test_sine_function(self):
    t = np.linspace(0, 100, 10)
    result = self.sim.sine(A=1, T=10, t=t)

    assert isinstance(result, np.ndarray)
    assert len(result) == 10
    assert all(-1 <= x <= 1 for x in result)

  def test_cosine_function(self):
    t = np.linspace(0, 100, 10)
    result = self.sim.cosine(Am=1, Tm=10, t=t)

    assert isinstance(result, np.ndarray)
    assert len(result) == 10
    assert all(-1 <= x <= 1 for x in result)

  def test_signal_sum_correctness(self):
    t = np.linspace(0, 100, 10)

    signal1 = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    signal2 = np.array([10, 9, 8, 7, 6, 5, 4, 3, 2, 1])

    signals = [signal1, signal2]
    total = np.sum(signals, axis=0)

    expected = np.array([11, 11, 11, 11, 11, 11, 11, 11, 11, 11])
    np.testing.assert_array_equal(total, expected)

  def test_config_values(self):
    assert 'DUR' in self.sim.config
    assert 'SIG' in self.sim.config
    assert 'SAM' in self.sim.config
    assert 'REP' in self.sim.config

    assert self.sim.config['DUR'] == 1000000
    assert self.sim.config['SIG'] == 1000
