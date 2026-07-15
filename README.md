# Turnover Dashboard

An employee turnover risk dashboard with explainable scoring and department-level insights.

## Overview

Companies lose money when good employees resign before leadership notices warning signs. Turnover creates costs through hiring, training, lost productivity, and direct impact on team morale.

This dashboard helps managers identify employees with a higher risk of leaving before they resign. It combines salary, tenure, promotions, raises, absences, and warnings to generate a clear, actionable risk score.

## Demo

- Dashboard: https://turnover-dashboard-pi.vercel.app
- API: https://turnover-dashboard-production-2a7a.up.railway.app/docs

## Features

Each employee receives a score from 0 to 100 based on six factors:

- More than two years without a promotion: 20 points
- Salary below the role average: 20 points
- More than three absences in the last 12 months: 15 points
- Less than one year at the company: 15 points
- Warnings in the last 12 months: 15 points
- No raise in the last 12 months: 15 points

Score below 40 = Low Risk. From 40 to 70 = Medium Risk. Above 70 = High Risk.

## Tech Stack

- Backend: Python, FastAPI, SQLAlchemy, PostgreSQL
- Frontend: React, Recharts
- Deployment: Railway (backend), Vercel (frontend)

## Getting Started

### Quick option with Docker

```bash
git clone https://github.com/lucaspwalter/turnover-dashboard.git
cd turnover-dashboard
docker compose up
```

Open `http://localhost:3000`. API: `http://localhost:8000/docs`.

### Manual installation

1. Clone the repository:

```bash
git clone https://github.com/lucaspwalter/turnover-dashboard.git
cd turnover-dashboard
```

2. Create and activate the virtual environment inside `backend`:

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the API:

```bash
python3 main.py
```

5. Open the API documentation:

```text
http://localhost:8000/docs
```

6. Run the frontend in another terminal:

```bash
cd frontend
npm install
npm start
```

## Project Structure

```text
turnover-dashboard/
├── backend/
│   ├── app/
│   │   ├── api/          # FastAPI routes: employees, scores, and dashboard
│   │   ├── db/           # Database configuration
│   │   ├── models/       # SQLAlchemy models
│   │   ├── schemas/      # Pydantic schemas
│   │   └── services/     # Business rules, including the scoring engine
│   ├── main.py           # FastAPI entry point
│   ├── seed.py           # Populates the database with sample data
│   └── requirements.txt  # Backend dependencies
├── frontend/
│   ├── src/
│   │   ├── components/   # Cards, department chart, and ranking table
│   │   ├── api.js        # Axios API client
│   │   └── App.jsx       # Main dashboard page
│   └── package.json      # Frontend dependencies and scripts
└── README.md
```

## License

Licensed under the MIT License. See `LICENSE`.
