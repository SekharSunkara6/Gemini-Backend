# Gemini Backend

A robust, scalable backend for a Gemini-style chat application.  
Features OTP-based login, user-specific chatrooms, AI-powered conversations via Google Gemini, and Stripe-powered subscriptions.

## 🚀 Features

- **OTP-based login** (mobile number, OTP returned via API)
- **JWT authentication** for secure API access
- **User chatrooms** (create, list, view)
- **AI chat**: Messages processed via Google Gemini API (async with Celery & Redis)
- **Stripe subscriptions**: Basic (free, limited) & Pro (paid, higher limits)
- **Rate limiting** for Basic users (daily prompt cap)
- **Caching** for chatroom lists (per user)
- **Consistent JSON responses and robust error handling**

## 🏗️ Tech Stack

- **Language:** Python 3.10+ (FastAPI)
- **Database:** PostgreSQL
- **Queue & Caching:** Celery + Redis (Docker recommended on Windows)
- **Payments:** Stripe (sandbox)
- **AI:** Google Gemini API
- **Deployment:** Render.com / Railway.app (recommended)
- **API Docs:** Swagger UI & ReDoc (auto-generated)

## 📂 Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── main.py
│   └── ... (other modules)
├── routes/
│   ├── __init__.py
│   └── ...
├── queue/
│   ├── __init__.py
│   └── worker.py
├── requirements.txt
├── .env.example
├── Gemini_Backend.postman_collection.json
├── README.md
└── ...
```

## ⚡ Getting Started

### 1. **Clone the Repository**

```bash
git clone https://github.com/SekharSunkara6/Gemini-Backend.git
cd gemini-backend
```

### 2. **Set Up Virtual Environment & Install Dependencies**

```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### 3. **Environment Variables**

- Copy `.env.example` to `.env` and fill in your values:

  ```env
  DATABASE_URL=
  SECRET_KEY=
  ALGORITHM=
  ACCESS_TOKEN_EXPIRE_MINUTES=
  REDIS_URL=
  STRIPE_SECRET_KEY=
  GEMINI_API_KEY=
  STRIPE_WEBHOOK_SECRET=
  ```

## 🗄️ Database Setup

- Ensure PostgreSQL is running.
- Create a database (e.g., `gemini_db`).
- Update `DATABASE_URL` in `.env` accordingly.

## 🗄️ Database Migrations with Alembic

This project uses **Alembic** for managing database schema migrations.

### **How to Use Alembic**

#### 1. **Initialize Alembic (first time only)**
```bash
alembic init alembic
```
- This creates an `alembic/` directory and an `alembic.ini` file.
- Edit `alembic.ini` to set your database URL (or configure it to read from your `.env`).

#### 2. **Create a New Migration**
Whenever you change your models, generate a new migration script:
```bash
alembic revision --autogenerate -m "Describe your change"
```
- This creates a migration script in `alembic/versions/`.

#### 3. **Apply Migrations**
To apply all pending migrations and update your database schema:
```bash
alembic upgrade head
```

## 🛠️ Start Redis

**If you are on Windows and cannot install Redis natively, use Docker:**

```bash
docker run --name redis -d -p 6379:6379 redis
```
- Make sure Docker Desktop is running before executing the command.
- This starts a Redis container accessible at `localhost:6379`.

**For Mac/Linux:**  
Install Redis using your package manager (`brew install redis` or `sudo apt-get install redis-server`).

## 🚦 Run the FastAPI Server

```bash
uvicorn app.main:app --host 0.0.0.0 --port 9002
```
- The API will be available at [http://localhost:9002](http://localhost:9002).

## ⚡ Start Celery Worker

```bash
celery -A queue.worker.celery_app worker --loglevel=info --pool=solo
```

## 🧪 Running Tests

If you have automated tests:

```bash
pip install pytest
pytest
```
- Tests should be in the `tests/` directory and require a test database and environment variables.

## 🌍 Deployment (Render.com Example)

### **Live Demo**

- **Base URL:**  
  [https://gemini-backend-lwow.onrender.com](https://gemini-backend-lwow.onrender.com)

- **Health Check:**  
  [https://gemini-backend-lwow.onrender.com/](https://gemini-backend-lwow.onrender.com/)  
  Returns:  
  ```json
  {"status":"ok"}
  ```

- **Interactive API Docs (Swagger UI):**  
  [https://gemini-backend-lwow.onrender.com/docs](https://gemini-backend-lwow.onrender.com/docs)

- **ReDoc Documentation:**  
  [https://gemini-backend-lwow.onrender.com/redoc](https://gemini-backend-lwow.onrender.com/redoc)

### **How to Test the Deployed API**

- **With Postman or browser:**  
  - `GET https://gemini-backend-lwow.onrender.com/` → should return `{"status":"ok"}`
  - Open [https://gemini-backend-lwow.onrender.com/docs](https://gemini-backend-lwow.onrender.com/docs) for interactive API docs.
- **Share these URLs** with anyone (instructor, teammates) for live testing.

### **How to Deploy on Render**

1. Push your code to GitHub.
2. Create a new Web Service on [Render](https://render.com).
3. Connect your GitHub repo.
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
6. Add all environment variables from `.env.example` in the Render dashboard.
7. (Recommended) Add a PostgreSQL database via Render and update the `DATABASE_URL` accordingly (use the `+asyncpg` driver for async SQLAlchemy).
8. Deploy and get your public URL.

**Note:** On the free Render plan, the API may take up to 50 seconds to respond after inactivity due to server spin-down. This is normal.

## 🧪 API Documentation & Testing

- **Swagger UI:** [http://localhost:9002/docs](http://localhost:9002/docs) (interactive API docs)
- **ReDoc:** [http://localhost:9002/redoc](http://localhost:9002/redoc) (alternative docs)
- **OpenAPI schema:** [http://localhost:9002/openapi.json](http://localhost:9002/openapi.json) (raw JSON)
- **Postman Collection:**  
  Import `Gemini_Backend.postman_collection.json` into Postman for ready-to-use API requests.

**Authentication:**  
- Obtain JWT from `/auth/verify-otp` and use as `Bearer ` for protected endpoints.

## 💳 Subscriptions

- **Basic:** Free, 5 prompts/day (rate-limited).
- **Pro:** Paid via Stripe, higher/unlimited prompts.
- Use `/subscribe/pro` to start payment, `/webhook/stripe` for Stripe events.

## ⚙️ Caching & Rate Limiting

- **Chatroom list** (`GET /chatroom`) is cached per user for 5 minutes.
- **Basic users** are rate-limited by daily prompt count.

## 🤖 Gemini API Integration

- Chat messages are sent to Google Gemini API asynchronously via Celery.

## 📝 Notes

- OTP is returned in API response (no SMS provider needed).
- All protected endpoints require JWT in Authorization header.
- Stripe is in sandbox mode for safe testing.
- For local testing:  
  Use default `.env.example` values and run PostgreSQL/Redis locally (see Docker note above for Redis on Windows).

## 📬 Contact

For questions or help, open an issue on GitHub or email [sekharsunkara2002@gmail.com](mailto:sekharsunkara2002@gmail.com)

**Happy Building! 🚀**

Let me know if you want any further customizations or additions!
