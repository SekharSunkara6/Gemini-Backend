from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models import Chatroom
from app.schemas import ChatroomCreate, ChatroomOut, MessageCreate, MessageOut
from app.dependencies import get_current_user

# For caching (e.g., Redis)
from app.utils.cache import get_cached_chatrooms, set_cached_chatrooms

# For Gemini queue (to be implemented)
# from app.queue.worker import enqueue_gemini_task

router = APIRouter()

# 1. Create a new chatroom
@router.post("", response_model=ChatroomOut)
async def create_chatroom(
    chatroom: ChatroomCreate,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user)
):
    """
    Creates a new chatroom for the authenticated user.
    """
    new_chatroom = Chatroom(name=chatroom.name, user_id=int(user_id))
    db.add(new_chatroom)
    await db.commit()
    await db.refresh(new_chatroom)
    # Invalidate chatroom cache for this user (if caching implemented)
    # await set_cached_chatrooms(user_id, None)
    return new_chatroom

# 2. List all chatrooms (with caching)
@router.get("", response_model=list[ChatroomOut])
async def list_chatrooms(
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user)
):
    """
    Lists all chatrooms for the authenticated user.
    Uses caching for performance (per assignment).
    """
    # Try to get from cache first
    # chatrooms = await get_cached_chatrooms(user_id)
    # if chatrooms is not None:
    #     return chatrooms

    result = await db.execute(select(Chatroom).where(Chatroom.user_id == int(user_id)))
    chatrooms = result.scalars().all()

    # Set cache for next time (TTL 5-10 min)
    # await set_cached_chatrooms(user_id, chatrooms)
    return chatrooms

# 3. Get a specific chatroom
@router.get("/{chatroom_id}", response_model=ChatroomOut)
async def get_chatroom(
    chatroom_id: int,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user)
):
    """
    Retrieves detailed information about a specific chatroom.
    """
    result = await db.execute(
        select(Chatroom).where(Chatroom.id == chatroom_id, Chatroom.user_id == int(user_id))
    )
    chatroom = result.scalar_one_or_none()
    if not chatroom:
        raise HTTPException(status_code=404, detail="Chatroom not found")
    return chatroom

# 4. Send a message and receive Gemini response (async/queue)
@router.post("/{chatroom_id}/message", response_model=MessageOut)
async def send_message(
    chatroom_id: int,
    message: MessageCreate,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user)
):
    """
    Sends a message and receives a Gemini response (via queue/async call).
    """
    # TODO: Enforce rate limiting for Basic users here

    # Save user message to DB (implement your Message model and logic)
    # user_message = Message(
    #     chatroom_id=chatroom_id,
    #     user_id=int(user_id),
    #     content=message.content,
    #     role="user"
    # )
    # db.add(user_message)
    # await db.commit()
    # await db.refresh(user_message)

    # Enqueue Gemini API call (pseudo-code)
    # task_id = enqueue_gemini_task(chatroom_id, user_message.id, message.content)

    # Return message or task ID for polling (implement as needed)
    # return {"task_id": task_id, "status": "pending"}

    # For now, just return a placeholder
    return {
        "id": 1,
        "chatroom_id": chatroom_id,
        "user_id": user_id,
        "content": message.content,
        "role": "user",
        "created_at": "2025-07-11T17:01:47.283843"
    }
