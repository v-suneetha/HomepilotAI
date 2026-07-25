# HomePilot AI

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
