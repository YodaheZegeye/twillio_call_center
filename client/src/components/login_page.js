import React from 'react';

export default function LoginPage({ formData, onChange, onLogin }) {
  return (
    <div className="App login-page">
      <h1>Login to Iris Bot</h1>
      <form onSubmit={onLogin} className="form-section">
        <input
          type="text"
          name="name"
          placeholder="Name"
          value={formData.name}
          onChange={onChange}
          required
        />
        <input
          type="date"
          name="dob"
          placeholder="Date of Birth"
          value={formData.dob}
          onChange={onChange}
          required
        />
        <input
          type="password"
          name="creditCard"
          placeholder="Credit Card Number"
          value={formData.creditCard}
          onChange={onChange}
          required
        />
        <input
          type="text"
          name="zip"
          placeholder="ZIP Code"
          value={formData.zip}
          onChange={onChange}
          required
        />
        <button type="submit">Login</button>
      </form>
    </div>
  );
}
