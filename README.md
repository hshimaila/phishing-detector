# ⬡ PhishGuard — AI-Powered Phishing Detection

<div align="center">

![PhishGuard Banner](https://img.shields.io/badge/PhishGuard-AI%20Threat%20Detection-00e5ff?style=for-the-badge&logo=shield&logoColor=black)

[![Live Demo](https://img.shields.io/badge/🌐%20Live%20Demo-sublime--ambition--production--176f.up.railway.app-00e5ff?style=for-the-badge)](https://sublime-ambition-production-176f.up.railway.app)
[![Backend API](https://img.shields.io/badge/🔌%20Backend%20API-phishing--detector--production--e5dc.up.railway.app-9f7aea?style=for-the-badge)](https://phishing-detector-production-e5dc.up.railway.app/api/health)
[![Railway](https://img.shields.io/badge/Deployed%20on-Railway-0B0D0E?style=for-the-badge&logo=railway)](https://railway.app)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge&logo=docker)](https://docker.com)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python)](https://python.org)
[![React](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react)](https://react.dev)

**An intelligent, real-time phishing detection system powered by NLP, Machine Learning, and live threat intelligence APIs.**

[🌐 Live Demo](https://sublime-ambition-production-176f.up.railway.app) • [🔌 API Health](https://phishing-detector-production-e5dc.up.railway.app/api/health) • [📖 API Docs](#api-reference) • [🚀 Quick Start](#quick-start)

</div>

---

## 📸 Preview

> **Scan Page** — Paste any email or URL and get an instant AI-powered verdict with risk score, signal breakdown, and plain-English explanation.

> **History Page** — View all past scans with live stats, filter by type, and delete individual records.

---

## 🧠 How It Works

PhishGuard uses a **multi-layer detection pipeline** — combining machine learning, NLP, and real-time threat intelligence into a single weighted risk score.

```
┌─────────────────────────────────────────────────────────┐
│                    INPUT (Email / URL)                   │
└───────────────────────┬─────────────────────────────────┘
                        │
          ┌─────────────┴──────────────┐
          ▼                            ▼
   ┌─────────────┐             ┌─────────────┐
   │  NLP Layer  │             │  URL Parser │
   │  (SpaCy +   │             │  (18 struct │
   │   TF-IDF)   │             │   features) │
   └──────┬──────┘             └──────┬──────┘
          │                           │
          ▼                           ▼
   ┌─────────────┐             ┌─────────────┐
   │   Random    │             │   Random    │
   │   Forest    │             │   Forest    │
   │ (Email ML)  │             │  (URL ML)   │
   └──────┬──────┘             └──────┬──────┘
          │                           │
          │              ┌────────────┘
          │              │
          │    ┌─────────▼──────────┐
          │    │   Threat Intel     │
          │    │ Google Safe Browse │
          │    │ PhishTank API      │
          │    └─────────┬──────────┘
          │              │
          └──────┬───────┘
                 ▼
        ┌─────────────────┐
        │   Risk Scorer   │
        │  ML:       50%  │
        │  Threat:   35%  │
        │  Rules:    15%  │
        └────────┬────────┘
                 ▼
        ┌─────────────────┐
        │  VERDICT +      │
        │  RISK SCORE     │
        │  + SIGNALS      │
        └─────────────────┘
```

### Detection Layers

| Layer | Technology | What it detects |
|---|---|---|
| **NLP Analysis** | SpaCy + TF-IDF | Urgency language, threats, credential harvesting, impersonation |
| **ML Classification** | Random Forest | Statistical patterns across 500+ text features |
| **URL Structural Analysis** | Custom feature extractor | Suspicious TLDs, IP addresses, lookalike domains, redirects |
| **Threat Intelligence** | Google Safe Browsing + PhishTank | Known phishing URLs from live databases |
| **Risk Scorer** | Weighted ensemble | Combines all layers into a single 0–100% confidence score |

---

## ✨ Features

- 🔍 **Email Scanner** — NLP analysis of email body text with signal detection
- 🔗 **URL Scanner** — 18-feature structural analysis + live threat intel lookup
- 📊 **Risk Meter** — Animated 0–100% risk score with color-coded verdict
- 🔎 **Score Breakdown** — See exactly how much ML, threat intel, and rules each contributed
- ⚠️ **Plain-English Alerts** — No technical jargon, just clear warnings
- 📜 **Scan History** — Full SQLite-backed history with filter and delete
- 📈 **Live Stats** — Detection rate, phishing count, safe/suspicious breakdown
- 🐳 **Fully Dockerized** — Runs anywhere with one command
- 🚀 **Auto-Deploy** — Pushes to GitHub trigger automatic Railway redeploys

---

## 🛠️ Tech Stack

### Frontend
| Technology | Purpose |
|---|---|
| **React 18** | UI framework |
| **React Router v6** | Client-side routing |
| **Axios** | HTTP client for API calls |
| **Vite** | Build tool and dev server |
| **CSS Modules** | Scoped component styling |
| **Nginx** | Production static file serving + API proxy |

### Backend
| Technology | Purpose |
|---|---|
| **Flask 3** | REST API framework |
| **Flask-SQLAlchemy** | ORM for database access |
| **Flask-CORS** | Cross-origin request handling |
| **SQLite** | Local scan history storage |

### ML / NLP
| Technology | Purpose |
|---|---|
| **Scikit-learn** | Random Forest classifier |
| **SpaCy 3** | Text preprocessing and tokenization |
| **TF-IDF Vectorizer** | Word importance feature extraction |
| **NLTK** | Stopword removal |
| **Joblib** | Model serialization |
| **NumPy / Pandas** | Data manipulation |

### Threat Intelligence
| API | Purpose |
|---|---|
| **Google Safe Browsing** | Real-time URL reputation check |
| **PhishTank** | Community-verified phishing database |
| **OpenPhish** | Live phishing feed |

### DevOps
| Technology | Purpose |
|---|---|
| **Docker** | Containerization |
| **Docker Compose** | Local multi-container orchestration |
| **Railway** | Cloud deployment platform |
| **GitHub** | Source control + auto-deploy trigger |

---

## 📁 Project Structure

```
phishing-detector/
│
├── 📄 docker-compose.yml          # frontend + backend
├── 📄 railway.json                # Railway deployment config
├── 📄 .gitignore                  # Git ignore rules
├── 📄 README.md                   # You are here
│
├── 🐍 backend/
│   ├── 📄 run.py                  # Flask entry point
│   ├── 📄 requirements.txt        # Python dependencies
│   ├── 📄 Dockerfile              # Backend container definition
│   ├── 📄 .dockerignore
│   │
│   ├── app/
│   │   ├── 📄 __init__.py         # Flask app factory
│   │   ├── 📄 config.py           # Environment configuration
│   │   │
│   │   ├── api/                   # REST API routes
│   │   │   ├── 📄 email_routes.py # POST /api/scan/email
│   │   │   ├── 📄 url_routes.py   # POST /api/scan/url
│   │   │   └── 📄 history_routes.py # GET /api/history
│   │   │
│   │   ├── ml/                    # Machine learning inference
│   │   │   ├── 📄 model_loader.py # Singleton model cache
│   │   │   ├── 📄 email_classifier.py # Email NLP pipeline
│   │   │   ├── 📄 url_classifier.py   # URL feature pipeline
│   │   │   └── 📄 risk_scorer.py  # Weighted ensemble scorer
│   │   │
│   │   ├── models/                # Database models
│   │   │   └── 📄 scan_result.py  # SQLAlchemy scan record
│   │   │
│   │   ├── threat_intel/          # External API integrations
│   │   │   ├── 📄 google_safebrowsing.py
│   │   │   └── 📄 phishtank.py
│   │   │
│   │   └── utils/                 # Shared utilities
│   │       ├── 📄 text_cleaner.py # SpaCy preprocessing
│   │       └── 📄 url_parser.py   # URL feature extraction
│   │
│   ├── ml_training/               # Offline model training
│   │   ├── 📄 download_datasets.py
│   │   ├── 📄 train_email_model.py
│   │   ├── 📄 train_url_model.py
│   │   └── datasets/              # Training data (CSV)
│   │
│   └── saved_models/              # Serialized trained models
│       ├── 📄 email_model.pkl
│       ├── 📄 email_tfidf.pkl
│       ├── 📄 url_model.pkl
│       └── 📄 url_feature_names.pkl
│
└── ⚛️  frontend/
    ├── 📄 index.html              # HTML entry point
    ├── 📄 package.json            # Node dependencies
    ├── 📄 vite.config.js          # Vite + API proxy config
    ├── 📄 nginx.conf              # Production nginx config
    ├── 📄 Dockerfile              # Frontend container definition
    ├── 📄 .dockerignore
    │
    └── src/
        ├── 📄 main.jsx            # React entry point
        ├── 📄 App.jsx             # Router + navbar + layout
        ├── 📄 index.css           # Global CSS variables + animations
        │
        ├── components/
        │   ├── 📄 ScanInput.jsx   # Email/URL input panel
        │   ├── 📄 ResultCard.jsx  # Verdict + risk meter + signals
        │   ├── 📄 AlertBanner.jsx # Error/warning banners
        │   └── 📄 ScanHistory.jsx # Past scans table
        │
        ├── pages/
        │   ├── 📄 Dashboard.jsx   # Main scan page
        │   └── 📄 History.jsx     # Scan history page
        │
        └── services/
            └── 📄 api.js          # Axios API client
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 20+
- Docker Desktop

### Option 1 — Docker (Recommended)

```bash
# Clone the repo
git clone https://github.com/hshimaila/phishing-detector.git
cd phishing-detector

# Start both services
docker-compose up --build
```

Open **http://localhost:3000** 🎉

### Option 2 — Manual (Development)

**Backend:**
```bash
cd backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Install SpaCy model
pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.1/en_core_web_sm-3.7.1-py3-none-any.whl

# Train ML models
python ml_training/download_datasets.py
python ml_training/train_email_model.py
python ml_training/train_url_model.py

# Start Flask
python run.py
```

**Frontend** (new terminal):
```bash
cd frontend
npm install
npm run dev
```

Open **http://localhost:3000** 🎉

---

## 🔌 API Reference

### Health Check
```http
GET /api/health
```
```json
{
  "status": "ok",
  "models": {
    "email_model_loaded": true,
    "url_model_loaded": true
  }
}
```

### Scan Email
```http
POST /api/scan/email
Content-Type: application/json

{
  "text": "URGENT! Your account has been suspended. Click here NOW!"
}
```

**Response:**
```json
{
  "verdict": "phishing",
  "risk_score": 0.823,
  "confidence": "high",
  "explanation": "⚠️ This looks like a phishing attempt!",
  "signals": [
    "⚡ Urgency language detected",
    "⚠️ Threatening language detected",
    "🔑 Credential harvesting attempt"
  ],
  "ml_score": 0.791,
  "threat_intel_flagged": false,
  "score_breakdown": {
    "ml_contribution": 0.395,
    "threat_intel_contribution": 0.0,
    "rules_contribution": 0.12
  },
  "scan_id": 1,
  "scan_type": "email"
}
```

### Scan URL
```http
POST /api/scan/url
Content-Type: application/json

{
  "url": "http://paypa1.verify-login.tk/secure/account"
}
```

**Response:**
```json
{
  "verdict": "phishing",
  "risk_score": 0.912,
  "confidence": "high",
  "explanation": "⚠️ This looks like a phishing attempt!",
  "signals": [
    "🌐 Suspicious top-level domain (.tk)",
    "🎭 Trusted brand name in subdomain",
    "🔑 Login/verify keyword in URL",
    "🔓 No HTTPS"
  ],
  "scan_id": 2,
  "scan_type": "url"
}
```

### Get Scan History
```http
GET /api/history
GET /api/history?type=email
GET /api/history?type=url&limit=20
```

### Delete Scan
```http
DELETE /api/history/:id
```

---

## ⚙️ Environment Variables

Create a `.env` file in the root directory:

```env
SECRET_KEY=your-super-secret-key-here
GOOGLE_SAFE_BROWSING_API_KEY=your-gsb-key    # Optional
PHISHTANK_API_KEY=your-phishtank-key         # Optional
```

| Variable | Required | Description |
|---|---|---|
| `SECRET_KEY` | Yes | Flask session secret |
| `GOOGLE_SAFE_BROWSING_API_KEY` | No | Enables GSB threat intel checks |
| `PHISHTANK_API_KEY` | No | Enables PhishTank lookups |

> Without API keys, the app still works fully — ML model handles all detection.

---

## 🧪 Test Cases

**Phishing emails to test:**
```
URGENT: Your PayPal account has been suspended! Click here immediately 
to verify your identity or your account will be permanently deleted.
```

**Phishing URLs to test:**
```
http://paypa1.verify-login.tk/secure/account
http://192.168.1.1/bank/login/verify
http://amazon-security-alert.xyz/update-payment
```

**Legitimate content to test:**
```
Hi Sarah, following up on the meeting notes from Tuesday. 
Can you send the Q3 report when you get a chance? Thanks!
```

---

## 🤝 Contributing

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License.

---

## 🙏 Acknowledgements

- [PhishTank](https://phishtank.com) — Community phishing database
- [Google Safe Browsing](https://developers.google.com/safe-browsing) — URL threat intelligence
- [SpaCy](https://spacy.io) — Industrial-strength NLP
- [Scikit-learn](https://scikit-learn.org) — Machine learning library
- [Railway](https://railway.app) — Deployment platform

---

Built by **Shimaila Hanif**

