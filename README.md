# SkyGuard Web Application

## 🚀 Quick Start

### What I created:

Your anomaly detection project is now a **complete web application** with:

1. **Frontend** (website) - Beautiful, modern interface
2. **Backend API** - Python/FastAPI server that processes weather data
3. **Docker setup** - Deploy anywhere with one command

---

## 📁 File Organization Explained (SIMPLE)

### Original Files (unchanged):
- **`SkyGuard_Final_Integrated.zip`** - Your trained model & original code lives here

### New Web Structure:
```
📦 Project
├── 📁 frontend/          ← Website files (what users see)
│   ├── index.html        (HTML page)
│   ├── styles.css        (Colors & design)
│   └── app.js            (Button clicks & upload logic)
│
├── 📁 backend/           ← Server code (processes data)
│   ├── app.py            (Main API with detect function)
│   └── requirements.txt   (Python libraries needed)
│
├── docker-compose.yml    ← Run everything at once
├── Dockerfile            ← Package for deployment
└── README.md             ← This file
```

---

## 🔧 How It Works (SIMPLE EXPLANATION)

### Step 1: User uploads CSV
1. User opens website → clicks "Choose CSV"
2. Selects weather data file with: `temperature, humidity, pressure, wind_speed`

### Step 2: Website sends data to server
- JavaScript in `app.js` reads the file
- Sends to backend API at `http://localhost:8000/api/analyze`

### Step 3: Server analyzes
- `backend/app.py` receives CSV
- `detect()` function:
  - Calculates average for each measurement
  - Finds readings that are **far from average** (anomalies)
  - Returns results with scores

### Step 4: Results show on website
- Table displays each row + anomaly status
- Progress bar shows % of anomalies
- Metrics show: Total / Anomalies / Normal

---

## ▶️ Run Locally

### Option 1: Direct Python
```bash
# Install Python 3.11+
# Open terminal/command prompt

cd backend
python -m venv .venv

# Windows:
.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate

pip install -r requirements.txt
uvicorn app:app --reload
```

Then:
1. Open `frontend/index.html` in your browser
2. API docs at: http://localhost:8000/docs

### Option 2: Docker (Recommended)
```bash
docker-compose up
```

Then:
- Website: http://localhost:3000
- API: http://localhost:8000
- API docs: http://localhost:8000/docs

---

## 📊 Test CSV Format

Create `test.csv`:
```
temperature,humidity,pressure,wind_speed
25.5,65.2,1013.25,5.2
26.1,64.8,1013.22,5.1
45.0,70.0,1020.00,15.0
25.9,65.5,1013.20,5.3
```

Row 3 will be flagged as anomaly (unusual temperature).

---

## 🔌 Using Your Original Model

The current `detect()` uses a simple z-score baseline.

To use your trained `anomaly_model.pkl` from the ZIP:

1. Extract `SkyGuard_Final_Integrated.zip`
2. Copy `anomaly_model.pkl` to `backend/models/`
3. In `backend/app.py`, replace the `detect()` function:

```python
import pickle

with open('models/anomaly_model.pkl', 'rb') as f:
    model = pickle.load(f)

def detect(rows):
    # Use model.predict() instead
    predictions = model.predict(data)
    return results
```

---

## 📈 Next Steps

✅ **Deploy online:**
- Heroku: `git push heroku main`
- AWS: Upload Docker image
- Vercel: Host frontend, keep backend on cloud

✅ **Add features:**
- Real-time monitoring with WebSocket
- Historical data charts
- Email alerts for anomalies
- Database to store results

✅ **Improve code:**
- Add unit tests
- Better error messages
- Input validation
- Performance optimization

---

## 🌐 Deployment Links

**When deployed, share these links:**

- **Website:** `https://your-domain.com` ← Users upload data here
- **API:** `https://your-domain.com/docs` ← Interactive API documentation

---

## 📞 Support

- Docs: http://localhost:8000/docs (interactive Swagger UI)
- Health check: http://localhost:8000/health
- API endpoint: POST /api/analyze
