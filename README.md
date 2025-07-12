# Gemini Backend

A robust, production-ready backend for a Gemini-style chat application.  
Features user authentication via OTP, user-specific chatrooms, AI-powered conversations with Google Gemini, and subscription management with Stripe.

## 🚀 Features

- **OTP-based login** (mobile number only, no SMS needed)
- **JWT authentication** for secure API access
- **User chatrooms** (create, list, view)
- **AI chat**: Messages processed via Google Gemini API (async with Celery & Redis)
- **Stripe subscriptions**: Basic (free, limited) & Pro (paid, higher limits)
- **Rate limiting** for Basic users (daily prompt cap)
- **Caching** for chatroom list (per user)
- **Consistent JSON responses and error handling**

## 🏗️ Tech Stack

- **Language:** Python 3.10+ (FastAPI)
- **Database:** PostgreSQL
- **Queue & Caching:** Celery + Redis
- **Payments:** Stripe (sandbox)
- **AI:** Google Gemini API
- **Deployment:** Render.com / Railway.app (recommended)

## 📂 Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── ... (other modules)
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
git clone https://github.com/yourusername/gemini-backend.git
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

```
DATABASE_URL=
SECRET_KEY=
ALGORITHM=
ACCESS_TOKEN_EXPIRE_MINUTES=
REDIS_URL=
STRIPE_SECRET_KEY=
GEMINI_API_KEY=
STRIPE_WEBHOOK_SECRET=
```

### 4. **Database Setup**

- Ensure PostgreSQL is running.
- Create a database named (e.g.) `gemini_db`.
- Update `DATABASE_URL` in `.env` accordingly.
- Run migrations (if using Alembic) or create tables manually.

### 5. **Start Redis**

- Make sure Redis is running (for Celery and caching).
  - On Windows, you can use Memurai or Redis for Windows[2].

### 6. **Run the FastAPI Server**

```bash
uvicorn app.main:app --host 0.0.0.0 --port 9002
```

### 7. **Start Celery Worker**

```bash
celery -A queue.worker.celery_app worker --loglevel=info --pool=solo
```

## 🧪 API Testing

- **Swagger UI:** [http://localhost:9002/docs](http://localhost:9002/docs)
- **Postman Collection:**  
  Import `Gemini_Backend.postman_collection.json` into Postman for ready-to-use API requests.
- **JWT Token:**  
  Obtain from `/auth/verify-otp` and use as `Bearer ` for protected endpoints.

## 💳 Subscriptions

- **Basic:** Free, 5 prompts/day (rate-limited).
- **Pro:** Paid via Stripe, higher/unlimited prompts.
- Use `/subscribe/pro` to start payment, `/webhook/stripe` for Stripe events.

## ⚙️ Caching & Rate Limiting

- **Chatroom list** (`GET /chatroom`) is cached per user for 5 minutes.
- **Basic users** are rate-limited by daily prompt count.

## 🤖 Gemini API Integration

- Chat messages are sent to Google Gemini API asynchronously via Celery.
- Ensures non-blocking, scalable AI conversations.

## 🌐 Deployment

### **Recommended: Render.com or Railway.app**
1. Push your code to GitHub.
2. Create a new Web Service on [Render](https://render.com) or [Railway](https://railway.app).
3. Connect your GitHub repo.
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
6. Add all environment variables from `.env.example`.
7. Deploy and get your public URL.

## 📝 Notes

- **OTP is returned in API response** (no SMS provider needed).
- **All protected endpoints require JWT in Authorization header.**
- **Stripe is in sandbox mode** for safe testing.
- **For local testing:**  
  Use default `.env.example` values and run PostgreSQL/Redis locally.

## 📬 Contact

For questions or help, open an issue on GitHub or email [sekharsunkara2002@gmail.com](mailto:your.sekharsunkara2002@gmail.com).
