# MediVision AI

### AI-Powered Heart Disease Detection & Medical Image Analysis Platform

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![Next.js 14](https://img.shields.io/badge/Next.js-14-black.svg)](https://nextjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-blue.svg)](https://www.typescriptlang.org/)
[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A production-grade healthcare SaaS platform that uses AI to analyze medical images (ECG, MRI, CT Scan, X-Ray) for heart disease prediction, provide AI-powered medical consultations via chatbot, generate PDF reports, and manage patient-doctor workflows.

> ⚠️ **Medical Disclaimer**: This AI system provides preliminary screening results and should not be considered a medical diagnosis. Please consult a licensed healthcare professional for clinical decisions.

---

## Architecture

```
medivision-ai/
├── backend/                  # FastAPI Backend
│   ├── app/
│   │   ├── api/             # API Routes
│   │   │   ├── v1/
│   │   │   │   ├── auth.py
│   │   │   │   ├── users.py
│   │   │   │   ├── patients.py
│   │   │   │   ├── doctors.py
│   │   │   │   ├── admin.py
│   │   │   │   ├── analysis.py
│   │   │   │   ├── chatbot.py
│   │   │   │   ├── reports.py
│   │   │   │   ├── appointments.py
│   │   │   │   ├── notifications.py
│   │   │   │   └── analytics.py
│   │   │   └── websocket/
│   │   │       └── notifications.py
│   │   ├── core/            # Config, Security, Events
│   │   ├── models/          # Database Models
│   │   ├── schemas/         # Pydantic Schemas
│   │   ├── services/        # Business Logic
│   │   ├── ai/              # AI/ML Modules
│   │   │   ├── image_processor.py
│   │   │   ├── prediction_engine.py
│   │   │   ├── models/
│   │   │   └── chatbot.py
│   │   ├── utils/           # Utilities
│   │   └── main.py
│   ├── tests/
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/                 # Next.js Frontend
│   ├── src/
│   │   ├── app/             # App Router Pages
│   │   ├── components/      # React Components
│   │   ├── hooks/           # Custom Hooks
│   │   ├── lib/             # Utilities
│   │   ├── store/           # State Management
│   │   ├── types/           # TypeScript Types
│   │   └── styles/          # Global Styles
│   ├── public/
│   ├── Dockerfile
│   └── package.json
├── docker-compose.yml
├── .env.example
└── .github/workflows/
```

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 14, TypeScript, Tailwind CSS, Framer Motion |
| Backend | FastAPI, Python 3.11+ |
| Database | MongoDB |
| Cache | Redis |
| AI/ML | PyTorch, Hugging Face, OpenCV |
| Auth | JWT, OAuth2 |
| Storage | Cloudinary / AWS S3 |
| Real-time | WebSocket |
| Deployment | Docker, AWS, Render |

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- MongoDB
- Redis

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```

### Frontend Setup
```bash
cd frontend
npm install
cp .env.example .env.local
npm run dev
```

### Docker
```bash
docker-compose up --build
```

## API Documentation

- Swagger UI: `http://localhost:8000/api/v1/docs`
- ReDoc: `http://localhost:8000/api/v1/redoc`

## License

MIT License - see [LICENSE](LICENSE) for details.
