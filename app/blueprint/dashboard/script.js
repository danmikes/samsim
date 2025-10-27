Chart.defaults.color = '#000000';
Chart.defaults.font.size = 12;
Chart.defaults.font.family = "'Helvetica Neue', 'Helvetica', 'Arial', sans-serif";

Chart.defaults.datasets.line.clip = false;
Chart.defaults.datasets.scatter.clip = false;

Chart.defaults.plugins.legend.position = 'right';
Chart.defaults.plugins.legend.labels.boxWidth = 6;
Chart.defaults.plugins.legend.labels.boxHeight = 6;

function initialiseChartSizes() {
  document.querySelectorAll('.chart-container canvas').forEach(canvas => {
    const container = canvas.parentElement;
    canvas.width = container.clientWidth;
    canvas.height = container.clientHeight;
  });
}

function renderInsolationChart(jsonData) {
  const canvas = document.getElementById('insolationChart');
  const ctx = canvas.getContext('2d');
  const container = canvas.parentElement;
  canvas.width = container.clientWidth;
  canvas.height = container.clientHeight;

  const datasets = jsonData.datasets.map(dataset => {
    return {
      ...dataset,
      data: jsonData.time.map((time, index) => ({
        x: time,
        y: dataset.data[index]
      }))
    };
  }).reverse();

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
          grid: { drawTicks: false }
        },
        y: {
          title: { display: true, text: 'Amplitude [m]', font: { size: 12 } },
          min: -60,
          max: +60,
          ticks: { font: { size: 10 }, stepSize: 30 },
          grid: { drawTicks: false }
        }
      }
    }
  });
}

function renderSimulationChart(jsonData) {
  const canvas = document.getElementById('simulationChart');
  const ctx = canvas.getContext('2d');
  const container = canvas.parentElement;
  canvas.width = container.clientWidth;
  canvas.height = container.clientHeight;

  const datasets = [];

  const addDataset = (signal, label, borderWidth = 2) => {
    if (signal && signal.data) {
      const timeArray = signal.time || jsonData.time;

      datasets.push({
        label: label || signal.name,
        data: timeArray.map((t, i) => ({
          x: t,
          y: signal.data[i]
        })),
        borderColor: signal.color,
        backgroundColor: signal.color + '40',
        borderWidth: borderWidth,
        pointRadius: 0,
        tension: 0.1
      });
    }
  };

  addDataset(jsonData.samples?.simulated_signal, null, 3);
  addDataset(jsonData.samples?.sampled_signal);
  addDataset(jsonData.signals?.total_signal);

  new Chart(ctx, {
    type: 'line',
    data: { datasets: datasets },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        title: { display: true, text: 'Simulation', font: { size: 16 } },
        legend: { labels: { usePointStyle: true, pointStyle: 'line' } },
        tooltip: {
          callbacks: {
            label: context => `${context.dataset.label}: ${context.parsed.y.toFixed(2)}`
          }
        }
      },
      scales: {
        x: {
          type: 'linear',
          title: { display: true, text: 'Time [Ma]', font: { size: 12 } },
          min: 0,
          max: 1,
          ticks: { font: { size: 10 } },
          grid: { drawTicks: false }
        },
        y: {
          type: 'linear',
          title: { display: true, text: 'Amplitude [m]', font: { size: 12 } },
          min: -60,
          max: +60,
          ticks: { font: { size: 10 }, stepSize: 30 },
          grid: { color: 'rgba(0,0,0,0.3)', drawTicks: false }
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
      pointRadius: 4,
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
          grid: { color: 'rgba(0,0,0,0.3)', drawTicks: false }
        },
        y: {
          title: { display: true, text: 'Fit [-]', font: { size: 12 } },
          min: 0,
          max: 1,
          ticks: { font: { size: 10 }, stepSize: 0.1 },
          grid: { color: 'rgba(0,0,0,0.3)', drawTicks: false }
        }
      }
    }
  });
}

document.addEventListener('DOMContentLoaded', () => {
  initialiseChartSizes();

  fetch('/dashboard/chart-data')
    .then(response => response.json())
    .then(data => {
      if (data.insolation) renderInsolationChart(data.insolation);
      if (data.simulation) renderSimulationChart(data.simulation);
      if (data.logistic) renderLogisticChart(data.logistic);

      document.getElementById('loadingSpinner').style.display = 'none';
    })
    .catch(error => {
      console.error('Error loading charts:', error);
      document.getElementById('loadingSpinner').style.display = 'none';
    });
});

window.addEventListener('resize', initialiseChartSizes);
