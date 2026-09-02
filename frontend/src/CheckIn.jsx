import { useState } from 'react';
import './CheckIn.css';

function CheckIn({ onViewHistory }) {
  const [answers, setAnswers] = useState({
    sleep_quality: 3,
    energy_level: 3,
    ate_regularly: true,
    physical_activity: true,
    social_interaction: true,
    felt_connected: 3,
    stress_level: 3,
    felt_overwhelmed: false,
    overall_mood: 3,
    felt_motivated: 3,
    enjoyed_something: true,
    free_text: '',
  });

  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const handleScaleChange = (field, value) => {
    setAnswers({ ...answers, [field]: Number(value) });
  };

  const handleBoolChange = (field, value) => {
    setAnswers({ ...answers, [field]: value });
  };

  const handleTextChange = (e) => {
    setAnswers({ ...answers, free_text: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setResult(null);

    try {
      const response = await fetch('http://localhost:5000/api/checkin/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify(answers),
      });

      const data = await response.json();

      if (response.ok) {
        setResult(data);
      } else {
        setError(data.error || 'Something went wrong.');
      }
    } catch (err) {
      setError('Could not connect to the server.');
    }
  };

  const ScaleQuestion = ({ label, field }) => (
    <div className="question">
      <label>{label}</label>
      <div className="scale-options">
        {[1, 2, 3, 4, 5].map((n) => (
          <button
            type="button"
            key={n}
            className={answers[field] === n ? 'scale-btn active' : 'scale-btn'}
            onClick={() => handleScaleChange(field, n)}
          >
            {n}
          </button>
        ))}
      </div>
    </div>
  );

  const BoolQuestion = ({ label, field }) => (
    <div className="question">
      <label>{label}</label>
      <div className="bool-options">
        <button
          type="button"
          className={answers[field] === true ? 'bool-btn active' : 'bool-btn'}
          onClick={() => handleBoolChange(field, true)}
        >
          Yes
        </button>
        <button
          type="button"
          className={answers[field] === false ? 'bool-btn active' : 'bool-btn'}
          onClick={() => handleBoolChange(field, false)}
        >
          No
        </button>
      </div>
    </div>
  );

  if (result) {
    return (
      <div className="checkin-container">
        <div className="result-card">
          {result.safety_alert ? (
            <>
              <h2>We're here for you</h2>
              <p className="result-message">{result.safety_alert.message}</p>
              <div className="resources">
                {result.safety_alert.resources.map((r, i) => (
                  <div key={i} className="resource-item">
                    <strong>{r.name}</strong>: {r.contact} ({r.available})
                  </div>
                ))}
              </div>
            </>
          ) : (
            <>
              <h2>Check-in complete</h2>
              <p className="result-message">{result.daily_message}</p>
              <div className="mood-bars">
                <div className="mood-bar-row">
                  <span>Positive</span>
                  <div className="bar-track">
                    <div className="bar-fill positive" style={{ width: `${result.mood_prediction.Positive * 100}%` }} />
                  </div>
                </div>
                <div className="mood-bar-row">
                  <span>Neutral</span>
                  <div className="bar-track">
                    <div className="bar-fill neutral" style={{ width: `${result.mood_prediction.Neutral * 100}%` }} />
                  </div>
                </div>
                <div className="mood-bar-row">
                  <span>Negative</span>
                  <div className="bar-track">
                    <div className="bar-fill negative" style={{ width: `${result.mood_prediction.Negative * 100}%` }} />
                  </div>
                </div>
              </div>
            </>
          )}
          <button className="new-checkin-btn" onClick={() => { setResult(null); setError(''); }}>
            Done
          </button>
          <button
            className="new-checkin-btn"
            style={{ marginTop: '10px', background: '#6b8494' }}
            onClick={onViewHistory}
          >
            View History
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="checkin-container">
      <form onSubmit={handleSubmit} className="checkin-form">
        <h2>Daily Check-In</h2>

        <ScaleQuestion label="How did you sleep last night?" field="sleep_quality" />
        <ScaleQuestion label="How would you rate your energy today?" field="energy_level" />
        <BoolQuestion label="Did you eat regularly today?" field="ate_regularly" />
        <BoolQuestion label="Did you get any physical activity today?" field="physical_activity" />
        <BoolQuestion label="Did you interact with other people today?" field="social_interaction" />
        <ScaleQuestion label="Did you feel connected to those around you?" field="felt_connected" />
        <ScaleQuestion label="How would you rate your stress level today?" field="stress_level" />
        <BoolQuestion label="Did anything specific feel overwhelming today?" field="felt_overwhelmed" />
        <ScaleQuestion label="How would you describe your overall mood today?" field="overall_mood" />
        <ScaleQuestion label="Did you feel motivated to do things today?" field="felt_motivated" />
        <BoolQuestion label="Did you enjoy anything today, even briefly?" field="enjoyed_something" />

        <div className="question">
          <label>Anything on your mind you'd like to share? (optional)</label>
          <textarea
            value={answers.free_text}
            onChange={handleTextChange}
            rows={3}
            placeholder="Write as much or as little as you like..."
          />
        </div>

        {error && <p className="error-message">{error}</p>}

        <button type="submit" className="submit-btn">Submit Check-In</button>

        <button
          type="button"
          className="new-checkin-btn"
          style={{ marginTop: '10px', background: '#6b8494' }}
          onClick={onViewHistory}
        >
          View History
        </button>
      </form>
    </div>
  );
}

export default CheckIn;