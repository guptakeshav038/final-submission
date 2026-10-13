# CreatorX

AI-powered creator and brand matching. Next.js (React) frontend, FastAPI backend, MySQL database.

```
creatorx/
  backend/    FastAPI + SQLAlchemy (scoring engine in app/scoring.py)
  frontend/   Next.js 14 app router, plain CSS
  database/   schema.sql (MySQL 8)
```

## 1. Database
Start MySQL with Docker (`docker compose up -d`) or use your own MySQL 8 server.
For your own server, run `database/schema.sql`, or just create an empty `creatorx` database and user. The API creates the tables on startup.

## 2. Backend
```bash
cd backend
python -m venv .venv && source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env                                  # edit DATABASE_URL and JWT_SECRET
python seed.py                                        # optional demo data
uvicorn app.main:app --reload --port 8000
```
API docs: http://localhost:8000/docs

## 3. Frontend
```bash
cd frontend
npm install
cp .env.local.example .env.local
npm run dev
```
Open http://localhost:3000

## Demo accounts (after `python seed.py`, password `password123`)
- Brand: `brand@demo.com` (has one Pune launch campaign, select Find matches)
- Creator: `aanyamoves@demo.com`

## How scoring works
Weights: audience 30%, niche 25%, engagement 20%, location 10%, content quality 10%, past ROI 5%.
The campaign goal re-weights them (for example, Local launch raises location to 25%). Every match stores a per-factor breakdown with a plain-language reason, shown to brands and creators.

## What is simplified in this version
- Niche similarity uses keyword (bag-of-words) cosine similarity. To use the deck's `all-MiniLM-L6-v2` embeddings, replace `niche()` in `backend/app/scoring.py` with sentence-transformers cosine similarity.
- Engagement, audience demographics, content quality and past ROI are stored values (seeded or self-entered). A production version should pull verified numbers from the Instagram/YouTube APIs and compute quality and ROI from real campaign history.
- Not yet built from the roadmap: escrow payouts (Stripe Connect / Razorpay Route), agreement generation, bot-fraud detection, pgvector/Pinecone search.
