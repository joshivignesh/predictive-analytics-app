# 📊 Predictive Analytics App

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React%2018-61DAFB?style=flat-square&logo=react&logoColor=black)](https://react.dev)
[![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white)](https://typescriptlang.org)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=flat-square&logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![MLflow](https://img.shields.io/badge/MLflow-0194E2?style=flat-square&logo=mlflow&logoColor=white)](https://mlflow.org)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)](https://docker.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white)](https://postgresql.org)

A full-stack **machine learning–powered analytics platform** that ingests datasets, trains predictive models, tracks experiments with MLflow, and exposes predictions through a FastAPI REST API consumed by a React + TypeScript dashboard.

> 🚧 **Active development** — commits land daily. Follow along!

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────┐
│               React 18 + TypeScript Dashboard            │
│   Charts · Prediction form · Model comparison · Alerts   │
└──────────────────────┬───────────────────────────────────┘
                       │ REST / JSON
                       ▼
┌──────────────────────────────────────────────────────────┐
│              FastAPI  (Python 3.11)                      │
│  /predict · /train · /models · /metrics · /datasets      │
└─────────┬──────────────────────┬────────────────────────┘
          │                      │
          ▼                      ▼
   ┌─────────────┐       ┌──────────────┐
   │  ML Engine  │       │  PostgreSQL  │
   │ scikit-learn│       │  (metadata,  │
   │  + MLflow   │       │  predictions │
   │  tracking   │       │  + datasets) │
   └─────────────┘       └──────────────┘
```

## 📁 Repository Structure

```
predictive-analytics-app/
├── backend/                  # Python FastAPI + ML engine
│   ├── app/
│   │   ├── api/              # Route handlers
│   │   ├── core/             # Config, DB, logging
│   │   ├── models/           # Pydantic schemas
│   │   ├── ml/               # Training, inference, feature engineering
│   │   └── main.py
│   ├── tests/
│   ├── notebooks/            # Exploratory analysis
│   ├── requirements.txt
│   └── Dockerfile
├── frontend-react/           # React 18 + TypeScript dashboard
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── hooks/
│   │   ├── services/         # API client
│   │   └── types/
│   └── Dockerfile
├── docker-compose.yml
├── Makefile
└── README.md
```

## 🚀 Quick Start

```bash
git clone https://github.com/joshivignesh/predictive-analytics-app.git
cd predictive-analytics-app
make up
```

| Service | URL |
|---------|-----|
| React Dashboard | http://localhost:3000 |
| FastAPI (Swagger) | http://localhost:8000/docs |
| MLflow UI | http://localhost:5001 |

## 🛠️ Local Development (without Docker)

```bash
# Backend
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend
cd frontend-react
npm install && npm start
```

## 🧪 Running Tests

```bash
make test-backend    # pytest + coverage
make test-frontend   # React Testing Library
```

## 🗺️ Roadmap

- [x] Project scaffold & Docker Compose
- [ ] Backend: FastAPI skeleton + health check
- [ ] Backend: Database models + Alembic migrations
- [ ] Backend: Dataset upload and preprocessing pipeline
- [ ] Backend: ML training endpoint (scikit-learn)
- [ ] Backend: MLflow experiment tracking integration
- [ ] Backend: Prediction endpoint with confidence scores
- [ ] Frontend: React scaffold + API client
- [ ] Frontend: Dataset upload UI
- [ ] Frontend: Live prediction dashboard with charts
- [ ] CI/CD: GitHub Actions pipeline

## 👤 Author

**Vignesh Joshi** — Senior Full Stack Engineer  
[![LinkedIn](https://img.shields.io/badge/LinkedIn-joshivignesh-0077B5?style=flat-square&logo=linkedin)](https://linkedin.com/in/joshivignesh)
[![GitHub](https://img.shields.io/badge/GitHub-joshivignesh-181717?style=flat-square&logo=github)](https://github.com/joshivignesh)
