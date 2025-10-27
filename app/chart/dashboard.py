from app.chart import create_insolation_chart, create_simulation_chart, create_logistic_chart

def create_dashboard_chart(insolation, simulation, logistic):
  return {
    'insolation': create_insolation_chart(insolation),
    'simulation': create_simulation_chart(simulation, insolation),
    'logistic': create_logistic_chart(logistic, simulation),
  }
