import { useState, useEffect } from 'react';
import './History.css';

function History({ onBack }) {
  const [checkins, setCheckins] = useState([]);
  const [trend, setTrend] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [historyRes, trendRes] = await Promise.all([
          fetch('http://localhost:5000/api/checkin/history', {
            credentials: 'include',
          }),
          fetch('http://localhost:5000/api/checkin/trend', {
            credentials: 'include',
          }),
        ]);

        const historyData = await historyRes.json();
        const trendData = await trendRes.json();

        if (historyRes.ok) setCheckins(historyData);
        if (trendRes.ok) setTrend(trendData);

        if (!historyRes.ok || !trendRes.ok) {
          setError('Could not load your history.');
        }
      } catch (err) {
        setError('Could not connect to the server.');
      }
    };

    fetchData();
  }, []);

  return (
    <div className="history-container">
      <div className="history-card">
        <h2>Your Journey</h2>

        {trend && (
          <div className="trend-box">
            <p className="trend-label">Current trend</p>
            <p className="trend-value">{trend.trend}</p>
            {trend.trend_message && <p className="trend-message">{trend.trend_message}</p>}
          </div>
        )}

        {error && <p className="error-message">{error}</p>}

        <div className="checkin-list">
          {checkins.length === 0 && !error && <p className="empty-message">No check-ins yet.</p>}
          {checkins.map((c) => (
            <div key={c.id} className="checkin-item">
              <div className="checkin-date">
                {new Date(c.timestamp).toLocaleDateString(undefined, {
                  weekday: 'short', month: 'short', day: 'numeric'
                })}
              </div>
              <div className="checkin-details">
                <span>Mood: {c.overall_mood}/5</span>
                <span>Sleep: {c.sleep_quality}/5</span>
                <span>Stress: {c.stress_level}/5</span>
              </div>
              {c.free_text && <div className="checkin-note">"{c.free_text}"</div>}
            </div>
          ))}
        </div>

        <button className="back-btn" onClick={onBack}>Back to Check-In</button>
      </div>
    </div>
  );
}

export default History;