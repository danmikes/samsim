from app.chart import create_insolation_chart, create_simulation_chart, create_logistic_chart

def create_dashboard_chart(insolation, simulation, logistic):
  return {
    'insolation_chart': create_insolation_chart(insolation),
    'simulation_chart': create_simulation_chart(simulation, insolation),
    'logistic_chart': create_logistic_chart(logistic, simulation),
  }
