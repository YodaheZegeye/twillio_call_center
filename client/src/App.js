import React, { useState } from 'react';
import './App.css';
import LoginPage from './components/login_page';
import Dashboard from './components/dashboard';

export default function App() {
  const [formData, setFormData] = useState({
    name: '',
    dob: '',
    creditCard: '',
    zip: ''
  });
  const [loggedIn, setLoggedIn] = useState(false);
  const [status, setStatus] = useState('');
  const [transcripts, setTranscripts] = useState([]);
  const [summary, setSummary] = useState([]);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleLogin = (e) => {
    e.preventDefault();
    setLoggedIn(true);
  };

  const handleCallAgency = async () => {
    setStatus('Dialing...');
    setTranscripts([]);
    setSummary([]);
    try {
      // Initiate call via backend
      await fetch('/api/call', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user: formData })
      });

      // Open WebSocket for streaming events
      const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws';
      const ws = new WebSocket(
        `${protocol}://${window.location.host}/stream?user=${encodeURIComponent(JSON.stringify(formData))}`
      );

      ws.onmessage = (event) => {
        const msg = JSON.parse(event.data);
        switch (msg.type) {
          case 'status':
            setStatus(msg.text);
            break;
          case 'transcript':
            setTranscripts(prev => [...prev, msg.text]);
            break;
          case 'summary':
            setSummary(msg.bullets);
            ws.close();
            break;
          default:
            break;
        }
      };

      ws.onerror = (err) => {
        console.error('WebSocket error', err);
        ws.close();
      };
    } catch (err) {
      console.error('Call initiation failed', err);
      setStatus('Error initiating call');
    }
  };

  return (
    loggedIn
      ? <Dashboard
          formData={formData}
          onCall={handleCallAgency}
          status={status}
          transcripts={transcripts}
          summary={summary}
        />
      : <LoginPage
          formData={formData}
          onChange={handleChange}
          onLogin={handleLogin}
        />
  );
}