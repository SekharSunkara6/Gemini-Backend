from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine
from app.models import Base

# Import routers
from app.routes import auth, chatroom, message, subscription, webhook, user

app = FastAPI(
    title="Gemini Backend",
    description="API for Gemini Chat Application",
    version="1.0.0"
)

# CORS middleware (adjust allow_origins in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your frontend domain in production!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Auto-create tables on startup (development only)
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Include routers with correct prefixes
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(chatroom.router, prefix="/chatroom", tags=["chatroom"])
app.include_router(message.router, tags=["message"])  # No prefix, endpoints are /chatroom/{id}/message(s)
app.include_router(subscription.router)  # Handles /subscribe/pro, /subscription/status, /subscriptions/my
app.include_router(webhook.router)       # Handles /webhook/stripe
app.include_router(user.router, prefix="/user", tags=["user"])  # Enables /user/me

# Root endpoint for health check
@app.get("/", tags=["health"])
def health_check():
    return {"status": "ok"}
