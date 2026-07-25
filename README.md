# HomePilot AI

## v0.3.0 - Advanced Expense Analysis

This release brings a more refined household finance experience with:

- duplicate transaction detection and review guidance
- monthly comparison and spending trend insights
- AI-style recommendations and budget alerts
- a more polished premium dashboard experience
- improved import workflow and analytics support

## v0.2 Expense Engine

This release expands the product into a working household expense experience with:

- CSV and Excel import support
- transaction storage and categorization
- monthly spending summaries and trend charts
- category breakdowns and top-spending insights
- budget tracking and budget status monitoring
- a more polished dashboard experience

## v0.1 Foundation

This milestone delivers a runnable local foundation with:

- a FastAPI backend
- a Streamlit frontend
- a Docker Compose setup
- basic health endpoints and tests

## Run locally

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
pip install -r requirements.txt
streamlit run app.py
```

### Docker Compose

```bash
docker compose up --build
```

## Testing

```bash
cd backend
pytest
```
