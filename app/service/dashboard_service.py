from app.config import Config
from app.service.insolation_service import InsolationService
from app.service.simulation_service import SimulationService
from app.service.logistic_service import LogisticService
from app.chart.dashboard import create_dashboard_chart

class DashboardService:
  def __init__(self):
    self.insolation = InsolationService()
    self.simulation = SimulationService()
    self.logistic = LogisticService()

  def run_dashboard(self):
    insolation = self.insolation.run_insolation()
    simulation = self.simulation.run_simulation()
    logistics = self.simulation.run_many_simulations()
    logistic = self.logistic.run_logistic()

    chart = create_dashboard_chart(insolation, simulation, logistic)
    return chart
