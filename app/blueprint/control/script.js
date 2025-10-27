document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('input[type="number"]').forEach(input => {
    input.addEventListener('keypress', function(e) {
      if (e.key === 'Enter') {
        saveConfig();
      }
    });
  });

  document.querySelectorAll('input[type="number"]').forEach(input => {
    input.addEventListener('input', function() {
      this.dataset.changed = 'true';
    });
  });
});

function collectConfig() {
  const config = { signal: {}, sim: {}, sample: {} }
  document.querySelectorAll('input[data-category]').forEach(input => {
    const { category, signal, param } = input.dataset
    const value = parseFloat(input.value)
    if (category === 'signal') {
      config.signal[signal] = { ...config.signal[signal], [param]: value }
    } else {
      config[category] = { ...config[category], [param]: value }
    }
  })
  return config
}

async function saveConfig() {
  try {
    const response = await fetch('/control/update', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(collectConfig())
    })
    const result = await response.json()
    if (result.status === 'success') {
      alert('Configuration saved');
      document.querySelectorAll('[data-changed').forEach(el => {
        delete el.changed;
      });
    } else {
      alert('Error: ' + result.message);
    }
  } catch (error) {
    alert('Network error: ' + error.message)
  }
}

async function resetConfig() {
  try {
    const response = await fetch('/control/reset', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({})
    })
    const result = await response.json()
    if (result.status === 'success') {
      alert('Configuration reset!')
      location.reload()
    } else {
      alert('Reset failed: ' + result.message)
    }
  } catch (error) {
    alert('Reset error: ' + error.message)
  }
}
