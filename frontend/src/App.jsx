import { useState } from 'react';
import './App.css';
import CheckIn from './CheckIn';
import History from './History';

function App() {
  const [isLogin, setIsLogin] = useState(true);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const [loggedIn, setLoggedIn] = useState(false);
  const [view, setView] = useState('checkin'); // 'checkin' or 'history'

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage('');

    const endpoint = isLogin ? 'login' : 'signup';

    try {
      const response = await fetch(`http://localhost:5000/api/auth/${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ username, password }),
      });

      const data = await response.json();

      if (response.ok) {
        if (isLogin) {
          setLoggedIn(true);
        } else {
          setMessage('Account created — you can now log in.');
          setIsLogin(true);
        }
      } else {
        setMessage(data.error || 'Something went wrong.');
      }
    } catch (err) {
      setMessage('Could not connect to the server. Is the backend running?');
    }
  };

  if (loggedIn) {
    return view === 'history' ? (
      <History onBack={() => setView('checkin')} />
    ) : (
      <CheckIn onViewHistory={() => setView('history')} />
    );
  }

  return (
    <div className="app-container">
      <div className="auth-card">
        <h1 className="app-title">Mood Check-In</h1>
        <p className="app-subtitle">
          {isLogin ? 'Welcome back — log in to continue' : 'Create an account to get started'}
        </p>

        <form onSubmit={handleSubmit} className="auth-form">
          <input
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          <button type="submit">{isLogin ? 'Log In' : 'Sign Up'}</button>
        </form>

        {message && <p className="auth-message">{message}</p>}

        <p className="toggle-text">
          {isLogin ? "Don't have an account? " : 'Already have an account? '}
          <span className="toggle-link" onClick={() => { setIsLogin(!isLogin); setMessage(''); }}>
            {isLogin ? 'Sign up' : 'Log in'}
          </span>
        </p>
      </div>
    </div>
  );
}

export default App;