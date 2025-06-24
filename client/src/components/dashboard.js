import React from 'react';

export default function Dashboard({ formData, onCall, status, transcripts, summary }) {
  return (
    <div className="App dashboard">
      <h1>Welcome, {formData.name}</h1>
      <div className="dashboard-controls">
        <button onClick={onCall}>Call Agency</button>
      </div>

      <div className="status-panel">
        <h2>Status</h2>
        <p>{status}</p>
      </div>

      <div className="transcript-panel">
        <h2>Transcript</h2>
        <ul>
          {transcripts.map((t, idx) => <li key={idx}>{t}</li>)}
        </ul>
      </div>

      <div className="summary-panel">
        <h2>Summary</h2>
        <ul>
          {summary.map((s, idx) => <li key={idx}>{s}</li>)}
        </ul>
      </div>
    </div>
  );
}