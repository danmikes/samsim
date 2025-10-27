function initialixeSettingsPage(dataUrl) {
  document.addEventListener('DOMContentLoaded', function() {
    fetch(dataUrl)
      .then(response => response.json())
      .then(data => populateParameterValues(data))
      .catch(handleDataError);
  });
}

function populateParameterValues(data) {
  document.getElementById('T-value').textContent = data.T.toLocaleString();
  document.getElementById('A-value').textContent = data.A.toLocaleString();
  document.getElementById('Tm-value').textContent = data.Tm.toLocaleString();
  document.getElementById('Am-value').textContent = data.Am.toLocaleString();
  document.getElementById('p-value').textContent = data.p;
}

function handleDataError(error) {
  console.error('Error fetching data:', error);
  const elements = ['T-value', 'A-value', 'Tm-value', 'Am-value', 'p-value'];
  elements.forEach(id => {
    document.getElementById(id).textContent = 'Error loading data';
  });
}
