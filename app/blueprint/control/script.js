function saveConfig() {
  const updateData = {};

  document.querySelectorAll('input[data-category]').forEach(input => {
    const category = input.dataset.category;
    const param = input.dataset.param;
    const signalName = input.dataset.signal;
    const value = input.type === 'number' ? parseFloat(input.value) : input.value;

    if (!updateData[category]) {
      updateData[category] = {};
    }

    if (category === 'signal' && signalName) {
      if (!updateData.signal[signalName]) {
        updateData.signal[signalName] = {};
      }
      updateData.signal[signalName][param] = value;
    } else {
      updateData[category][param] = value;
    }
  });

  fetch('/control/update', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(updateData)
  })
  .then(response => response.json())
  .then(data => {
    if (data.status === 'success') {
      alert('Config saved successfully!');
      location.reload();
    } else {
      alert('Error saving config: ' + data.message);
    }
  })
  .catch(error => {
    console.error('Error:', error);
    alert('Error saving config');
  });
}

function resetConfig() {
  if (confirm('Are you sure you want to reset all settings to default?')) {
    fetch('/control/reset', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({})
    })
    .then(response => response.json())
    .then(data => {
      if (data.status === 'success') {
        alert('Config reset to defaults!');
        location.reload();
      } else {
        alert('Error resetting config: ' + data.message);
      }
    })
    .catch(error => {
      console.error('Error:', error);
      alert('Error resetting config');
    });
  }
}

document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('input[data-category]').forEach(input => {
  input.addEventListener('keydown', (event) => {
      if (event.key === 'Enter') {
          event.preventDefault();
          saveConfig();
      }
  });
});
});
