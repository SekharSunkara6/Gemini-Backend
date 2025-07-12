from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from datetime import datetime, timedelta

from app.database import get_db
from app.models import Message, Chatroom, User
from app.schemas import MessageCreate, MessageOut
from app.dependencies import get_current_user
from app.tasks import gemini_task  # Celery task

router = APIRouter()

DAILY_LIMIT = 5  # Basic plan daily message limit

# 1. Send a message to a chatroom (and receive Gemini response via Celery)
@router.post("/chatroom/{chatroom_id}/message", response_model=MessageOut)
async def send_message(
    chatroom_id: int,
    message: MessageCreate,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user)
):
    """
    Sends a message and receives a Gemini response (via queue/async call).
    """
    # Check if user owns the chatroom
    chatroom_result = await db.execute(
        select(Chatroom).where(Chatroom.id == chatroom_id, Chatroom.user_id == int(user_id))
    )
    chatroom = chatroom_result.scalar_one_or_none()
    if not chatroom:
        raise HTTPException(status_code=404, detail="Chatroom not found or not owned by user")

    # Get user and check subscription
    user_result = await db.execute(select(User).where(User.id == int(user_id)))
    user = user_result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Rate limiting for Basic users
    if user.subscription == "Basic":
        today = datetime.utcnow().date()
        count_result = await db.execute(
            select(func.count(Message.id)).where(
                Message.user_id == int(user_id),
                Message.created_at >= today
            )
        )
        count = count_result.scalar()
        if count >= DAILY_LIMIT:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Daily message limit ({DAILY_LIMIT}) reached for Basic plan."
            )

    # Save user message to DB
    new_message = Message(
        chatroom_id=chatroom_id,
        user_id=int(user_id),
        content=message.content,
        role="user"
    )
    db.add(new_message)
    await db.commit()
    await db.refresh(new_message)

    # Enqueue Gemini API call using Celery
    gemini_task.delay(chatroom_id, new_message.id, message.content)

    # Return the saved message (Gemini response will be added asynchronously)
    return new_message

# 2. List all messages in a chatroom
@router.get("/chatroom/{chatroom_id}/messages", response_model=list[MessageOut])
async def get_messages(
    chatroom_id: int,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user)
):
    """
    Lists all messages in a specific chatroom.
    """
    # Check if user owns the chatroom
    chatroom_result = await db.execute(
        select(Chatroom).where(Chatroom.id == chatroom_id, Chatroom.user_id == int(user_id))
    )
    chatroom = chatroom_result.scalar_one_or_none()
    if not chatroom:
        raise HTTPException(status_code=404, detail="Chatroom not found or not owned by user")

    result = await db.execute(
        select(Message).where(Message.chatroom_id == chatroom_id)
    )
    return result.scalars().all()
