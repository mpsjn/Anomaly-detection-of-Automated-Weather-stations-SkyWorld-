const API = 'http://localhost:8000';
const fileInput = document.querySelector('#file');
const label = document.querySelector('#file-label');
const button = document.querySelector('#analyze');
fileInput.addEventListener('change', () => { label.textContent = fileInput.files[0]?.name || 'Choose a CSV file or drag it here'; });
button.addEventListener('click', async () => {
  const file = fileInput.files[0];
  const message = document.querySelector('#message');
  if (!file) { message.textContent = 'Please choose a CSV file first.'; return; }
  button.disabled = true; message.textContent = 'Analyzing readings…';
  try {
    const form = new FormData(); form.append('file', file);
    const response = await fetch(`${API}/api/analyze`, { method:'POST', body:form });
    const data = await response.json(); if (!response.ok) throw new Error(data.detail || 'Analysis failed');
    document.querySelector('#total').textContent = data.total; document.querySelector('#anomalies').textContent = data.anomalies; document.querySelector('#normal').textContent = data.normal;
    document.querySelector('#badge').textContent = data.anomalies ? `${data.anomalies} flagged` : 'All clear';
    document.querySelector('#bar').style.width = `${data.total ? data.anomalies / data.total * 100 : 0}%`;
    document.querySelector('#empty').hidden = true; const table = document.querySelector('#table'); table.hidden = false;
    table.querySelector('tbody').innerHTML = data.results.slice(0,100).map(x => `<tr><td>${x.row}</td><td>${x.anomaly ? '⚠ Anomaly' : '✓ Normal'}</td><td>${x.score}</td><td>${x.values.temperature}</td></tr>`).join(''); message.textContent = 'Analysis complete.';
  } catch (error) { message.textContent = error.message; } finally { button.disabled = false; }
});
