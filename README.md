# Mental Health Check-In Chatbot
 
A full-stack mood check-in application that uses probabilistic modeling to gently surface patterns in daily wellbeing — without ever naming or suggesting clinical conditions. Built as a collaborative project with a clear frontend/backend split.
 
## Project Philosophy
 
This app is designed around one core principle: **describe observed patterns only, never diagnose.** No message in this app names a mental health condition or tells a user what they "might have." Instead, it reflects back what a user has reported (sleep, stress, mood, social connection) and gently encourages reaching out to a real person or professional when patterns look concerning.
 
The entire stack runs locally with no external API keys, making it auditable and appropriate for a safety-sensitive prototype.
 
## Team
 
- **Backend:** Nanthika — Python/Flask, database, ML pipeline
- **Frontend:** Akshara — React (Vite)
## Tech Stack
 
**Backend**
- Python 3.12
- Flask, Flask-SQLAlchemy (SQLite), Flask-CORS
- Werkzeug (password hashing, session security)
**NLP / ML**
- spaCy (`en_core_web_sm`)
- HuggingFace Transformers, PyTorch
- scikit-learn
- pgmpy (Bayesian Networks)
- hmmlearn (Hidden Markov Models)
**Frontend**
- React (Vite scaffold)
**Version Control**
- GitHub: `https://github.com/Nanthikashree/mental-health-chatbot.git`
## Project Structure
 
```
mental-health-chatbot/
├── backend/
│   ├── app.py                      # Flask entry point
│   ├── auth.py                     # Signup/login/logout/session routes
│   ├── requirements.txt
│   ├── models/
│   │   ├── user_model.py           # User table (SQLAlchemy)
│   │   ├── checkin_model.py        # CheckIn table
│   │   ├── mood_prediction_model.py # MoodPrediction table
│   │   ├── mood_features.py        # Raw answers -> composite Low/Medium/High features
│   │   ├── bayesian_mood_model.py  # pgmpy Bayesian Network (daily mood prediction)
│   │   └── trend_model.py          # hmmlearn HMM (trend detection across check-ins)
│   ├── routes/
│   │   └── checkin_routes.py       # /submit, /history, /trend
│   └── utils/
│       ├── safety_layer.py         # Distress keyword detection + crisis resources
│       └── response_bank.py        # Non-diagnostic supportive message templates
└── frontend/
    ├── src/
    │   ├── App.jsx                 # Login/signup screen, top-level routing
    │   ├── CheckIn.jsx             # 12-question daily check-in form + result screen
    │   └── History.jsx             # Past check-ins + trend view
    └── ...
```
 
## How It Works
 
1. **User checks in daily** by answering 12 fixed questions (11 scaled/yes-no + 1 optional free text).
2. **Composite features** are computed from the raw answers: Physical Wellbeing, Social Connection, Stress Load, Positive Engagement.
3. **Safety check runs first** on the free-text answer. If distress language is detected, the check-in is saved but the response returns a fixed, non-diagnostic safety message with crisis resources — the mood pipeline is skipped entirely for that check-in.
4. **Bayesian Network (pgmpy)** takes the four composite features and outputs a probability distribution over Negative / Neutral / Positive mood for that day.
5. **HMM (hmmlearn)** looks across a user's full check-in history (minimum 21 check-ins) to detect a longer-term trend: Stable, Low, or Declining. A low-variance shortcut avoids flagging a trend change when mood scores aren't meaningfully moving, and a 3-day smoothing window prevents single-day noise from flipping the result.
6. **Response layer** turns both outputs into short, supportive, non-diagnostic messages shown to the user.
## Setup
 
### Backend
 
```powershell
cd backend
python -m venv venv
venv\Scripts\activate       # Windows
pip install -r requirements.txt
python -m spacy download en_core_web_sm
python app.py
```
 
> **Note:** Python 3.12 is required. `hmmlearn` does not have prebuilt wheels for newer Python versions (e.g. 3.13/3.14) on Windows and will fail to build without Microsoft C++ Build Tools.
 
Backend runs at `http://localhost:5000`.
 
### Frontend
 
```powershell
cd frontend
npm install
npm run dev
```
 
Frontend runs at `http://localhost:5173`.
 
> Both must run simultaneously, and both should be accessed via `localhost` (not `127.0.0.1`) — mismatching the two breaks session cookies due to browser cross-origin rules.
 
## API Reference
 
### Auth (`/api/auth`)
 
| Route | Method | Body | Description |
|---|---|---|---|
| `/signup` | POST | `{ username, password }` | Creates a new user |
| `/login` | POST | `{ username, password }` | Logs in, starts a session |
| `/logout` | POST | — | Clears the session |
| `/me` | GET | — | Returns the currently logged-in username |
 
### Check-ins (`/api/checkin`)
 
| Route | Method | Body | Description |
|---|---|---|---|
| `/submit` | POST | 11 required fields + optional `free_text` | Submits a check-in, returns `mood_prediction` + `daily_message`, or a `safety_alert` if distress is detected |
| `/history` | GET | — | Returns all past check-ins for the logged-in user |
| `/trend` | GET | — | Returns the current trend (`Stable` / `Low` / `Declining` / `Not enough data yet`) + `trend_message` |
 
**Check-in submission fields:**
```json
{
  "sleep_quality": 1-5,
  "energy_level": 1-5,
  "ate_regularly": true/false,
  "physical_activity": true/false,
  "social_interaction": true/false,
  "felt_connected": 1-5,
  "stress_level": 1-5,
  "felt_overwhelmed": true/false,
  "overall_mood": 1-5,
  "felt_motivated": 1-5,
  "enjoyed_something": true/false,
  "free_text": "optional string"
}
```
 
## Known Limitations / Next Steps
 
- `SECRET_KEY` in `app.py` is a placeholder — must be replaced with a real secret before any real deployment.
- The distress keyword list in `safety_layer.py` is a starting point and should be reviewed/expanded with informed input before real-world use.
- HMM trend detection requires 21+ check-ins per user before it activates — by design, to avoid unreliable early guesses.
- No password reset flow yet.
- No production WSGI server configured (Flask's dev server is for local testing only).
## Design Principles
 
- Describe patterns, never name conditions — no diagnostic language anywhere in the app.
- Safety-critical logic (distress detection) is hardcoded and rule-based, not ML-driven, for transparency and predictability.
- All models run locally — no external API calls, no data leaves the machine.
 
