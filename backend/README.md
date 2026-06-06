# Inventory API (FastAPI + Supabase)

## Setup

```bash
cd backend
python -m venv .venv
source .venv/Scripts/activate   # Git Bash
pip install -r requirements.txt
```

Copy `.env.example` to `.env`.

### Supabase connection (important)

1. Open **Supabase Dashboard** → your project → **Connect** → **Session pooler**
2. Copy the URI (looks like `postgresql://postgres.PROJECT_REF:...@aws-0-REGION.pooler.supabase.com:5432/postgres`)
3. In `backend/.env`:
   - Replace `postgresql://` with `postgresql+asyncpg://`
   - URL-encode the password: `#` → `%23`, `@` → `%40`
   - Use the **exact** `aws-0-REGION` from the dashboard (do not guess the region)

**Error `getaddrinfo failed`:** You are using the direct `db.*.supabase.co` host (IPv6-only). Switch to the **Session pooler** URI.

**Error `tenant/user ... not found`:** Wrong pooler region in the URL — copy it again from the dashboard.

Set `DATABASE_SSL_VERIFY=false` if you see SSL certificate errors on your network.

## Database (first time)

**Option A — Supabase SQL Editor**

1. Open Supabase → **SQL Editor**
2. Run `supabase/schema.sql`

**Option B — From your machine**

```bash
python scripts/test_db.py      # verify connection
python scripts/init_db.py      # create tables from models
python scripts/seed_data.py    # roles, locations, categories
```

## Run API

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8001
```

- Docs: http://127.0.0.1:8001/docs
- Health: http://127.0.0.1:8001/health
