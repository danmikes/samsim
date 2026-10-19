Chart.defaults.color = '#000000';
Chart.defaults.font.size = 12;
Chart.defaults.font.family = "'Helvetica Neue', 'Helvetica', 'Arial', sans-serif";

Chart.defaults.plugins.legend.position = 'right';
Chart.defaults.plugins.legend.labels.boxWidth = 6;
Chart.defaults.plugins.legend.labels.boxHeight = 6;

Chart.defaults.datasets.line = {
  ...Chart.defaults.datasets.line,
  borderCapStyle: 'round',
  borderJoinStyle: 'round',
};

Chart.defaults.clip = false;

function initialiseChartSizes() {
  document.querySelectorAll('.chart-container canvas').forEach(canvas => {
    const container = canvas.parentElement;
    canvas.width = container.clientWidth;
    canvas.height = container.clientHeight;
  });
}

function setupCanvas(canvasId) {
  const canvas = document.getElementById(canvasId);
  if (!canvas) {
    console.error(`${canvasId} canvas not found!`);
    return null;
  }

  const ctx = canvas.getContext('2d');
  const container = canvas.parentElement;
  canvas.width = container.clientWidth;
  canvas.height = container.clientHeight;

  return { canvas, ctx, container };
}

function calculateYAxisRange(datasets) {
  const allYValues = datasets.flatMap(dataset =>
    dataset.data.map(point => point.y)
  );
  const maxAmplitude = Math.max(
    Math.abs(Math.min(...allYValues)),
    Math.abs(Math.max(...allYValues))
  );
  const tickStep = Math.ceil(maxAmplitude / 20) * 10;
  return {
    min: -2 * tickStep,
    max: 2 * tickStep,
    stepSize: tickStep
  };
}

function renderInsolationChart(jsonData) {
  const setup = setupCanvas('insolationChart');
  if (!setup) return;

  const { ctx } = setup;

  const datasets = jsonData.datasets.map(dataset => ({
    ...dataset,
    data: jsonData.time.map((time, index) => ({
      x: time,
      y: dataset.data[index]
    }))
  })).reverse();

  const yAxis = calculateYAxisRange(datasets);

  new Chart(ctx, {
    type: 'line',
    data: { datasets: datasets },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        title: { display: true, text: 'Insolation', font: { size: 16 } },
        legend: { labels: { usePointStyle: true, pointStyle: 'line' } }
      },
      scales: {
        x: {
          type: 'linear',
          title: { display: true, text: 'Time [Ma]', font: { size: 12 } },
          ticks: { font: { size: 10 } },
          grid: { color: 'rgba(0,0,0,0.5)', drawTicks: false }
        },
        y: {
          title: { display: true, text: 'Amplitude [m]', font: { size: 12 } },
          min: yAxis.min,
          max: yAxis.max,
          ticks: {
            font: { size: 10 },
            stepSize: yAxis.stepSize
          },
          grid: { color: 'rgba(0,0,0,0.5)', drawTicks: false }
        }
      }
    }
  });
}

function renderSimulationChart(jsonData) {
  const setup = setupCanvas('simulationChart');
  if (!setup) return;

  const { ctx } = setup;

  const datasets = jsonData.datasets.map(dataset => {
    const timeArray = dataset.time || jsonData.time;

    return {
      ...dataset,
      data: timeArray.map((time, index) => ({
        x: time,
        y: dataset.data[index]
      }))
    };
  }).reverse();

  const yAxis = calculateYAxisRange(datasets);

  new Chart(ctx, {
    type: 'line',
    data: { datasets: datasets },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        title: { display: true, text: 'Simulation', font: { size: 16 } },
        legend: { labels: { usePointStyle: true, pointStyle: 'line' } }
      },
      scales: {
        x: {
          type: 'linear',
          title: { display: true, text: 'Time [Ma]', font: { size: 12 } },
          min: 0,
          max: 1,
          ticks: { font: { size: 10 } },
          grid: { color: 'rgba(0,0,0,0.5)', drawTicks: false }
        },
        y: {
          type: 'linear',
          title: { display: true, text: 'Amplitude [m]', font: { size: 12 } },
          min: yAxis.min,
          max: yAxis.max,
          ticks: {
            font: { size: 10 },
            stepSize: yAxis.stepSize
          },
          grid: { color: 'rgba(0,0,0,0.5)', drawTicks: false }
        }
      }
    }
  });
}

function renderLogisticChart(jsonData) {
  const canvas = document.getElementById('logisticChart');
  const ctx = canvas.getContext('2d');
  const container = canvas.parentElement;
  canvas.width = container.clientWidth;
  canvas.height = container.clientHeight;

  const datasets = [
    {
      label: 'Simulation',
      data: jsonData.simulation.sample_rates.map((rate, i) => ({
        x: rate,
        y: jsonData.simulation.fits[i]
      })),
      backgroundColor: '#001964',
      borderColor: '#001964',
      pointRadius: 3,
      pointHoverRadius: 6,
      showLine: false,
      pointStyle: 'circle',
    }
  ];

  if (jsonData.fit) {
    datasets.push({
      label: 'Fit',
      data: jsonData.fit.x.map((x, i) => ({ x: x, y: jsonData.fit.y[i] })),
      backgroundColor: '#00196480',
      borderColor: '#001964',
      borderWidth: 2,
      fill: false,
      pointRadius: 0,
      showLine: true,
      pointStyle: 'line'
    });
  }

  const addReferenceLine = (data, label, color) => {
    datasets.push({
      label: label,
      data: [
        { x: data.sample_rate, y: 0 },
        { x: data.sample_rate, y: data.fit },
        { x: 0.1, y: data.fit }
      ],
      clip: true,
      backgroundColor: color + '80',
      borderColor: color,
      borderWidth: 2,
      pointRadius: 0,
      showLine: true,
      borderDash: [5, 5],
      pointStyle: 'line'
    });
  };

  if (jsonData.target.sample_rate) {
    addReferenceLine(jsonData.target, `Target (${jsonData.target.sample_rate.toFixed(0)} ${jsonData.target.fit.toFixed(1)})`, '#64C800');
  }

  addReferenceLine(jsonData.current, `Current (${jsonData.current.sample_rate.toFixed(0)} ${jsonData.current.fit.toFixed(1)})`, '#FFC800');

  new Chart(ctx, {
    type: 'scatter',
    data: { datasets: datasets },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        title: { display: true, text: 'Fit', font: { size: 16 } },
        legend: { labels: { usePointStyle: true } },
        tooltip: {
          callbacks: {
            label: context => `Samples: ${context.parsed.x.toFixed(0)}, Fit: ${context.parsed.y.toFixed(2)}`
          }
        }
      },
      scales: {
        x: {
          type: 'logarithmic',
          title: { display: true, text: 'Samples [-]', font: { size: 12 } },
          min: 1,
          max: 1000,
          ticks: {
            font: { size: 10 },
            callback: function(value) {
              const logValue = Math.log10(value);
              if (Math.abs(logValue - Math.round(logValue)) < 0.001) {
                return value.toString();
              }
            }
          },
          grid: { color: 'rgba(0,0,0,0.5)', drawTicks: false }
        },
        y: {
          title: { display: true, text: 'Fit [-]', font: { size: 12 } },
          min: 0,
          max: 1,
          ticks: { font: { size: 10 }, stepSize: 0.1 },
          grid: { color: 'rgba(0,0,0,0.5)', drawTicks: false }
        }
      }
    }
  });
}

document.addEventListener('DOMContentLoaded', () => {
  initialiseChartSizes();

  fetch('/dashboard/chart-data')
    .then(response => {
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response.json();
    })
    .then(data => {
      if (data.insolation) {
        renderInsolationChart(data.insolation);
      } else {
        console.warn('No insolation data received');
      }

      if (data.simulation) {
        renderSimulationChart(data.simulation);
      } else {
        console.warn('No simulation data received');
      }

      if (data.logistic) {
        renderLogisticChart(data.logistic);
      } else {
        console.warn('No logistic data received');
      }

      document.getElementById('loadingSpinner').style.display = 'none';
    })
    .catch(error => {
      console.error('Error loading charts:', error);
      document.getElementById('loadingSpinner').style.display = 'none';
    });
});

function handleResize() {
  initialiseChartSizes();
  document.querySelectorAll('canvas').forEach(canvas => {
    const chart = Chart.getChart(canvas);
    if (chart) {
      chart.resize();
      chart.update('none');
    }
  });
}

// Replace all your event listeners with these two lines:
window.addEventListener('resize', handleResize);
window.addEventListener('orientationchange', handleResize);
