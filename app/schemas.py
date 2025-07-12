from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# ------------------- User Schemas -------------------

class UserCreate(BaseModel):
    mobile: str
    password: str

class SignupRequest(BaseModel):
    mobile: str
    password: Optional[str] = None  # Optional if not required

class ForgotPasswordRequest(BaseModel):
    mobile: str

class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str

class UserOut(BaseModel):
    id: int
    mobile: str
    subscription_tier: Optional[str] = None

    class Config:
        # For Pydantic v2, use from_attributes = True
        from_attributes = True
        # If using Pydantic v1, use orm_mode = True
        # orm_mode = True

# ------------------- OTP Schemas -------------------

class OTPCreate(BaseModel):
    mobile: str

class OTPVerify(BaseModel):
    mobile: str
    otp: str

# ------------------- Chatroom Schemas -------------------

class ChatroomCreate(BaseModel):
    name: str

class ChatroomOut(BaseModel):
    id: int
    name: str
    created_at: datetime

    class Config:
        from_attributes = True
        # orm_mode = True

# ------------------- Message Schemas -------------------

class MessageCreate(BaseModel):
    content: str  # chatroom_id will be in the URL, not in the body

class MessageOut(BaseModel):
    id: int
    chatroom_id: int
    user_id: int
    content: str
    role: str
    created_at: datetime

    class Config:
        from_attributes = True
        # orm_mode = True

# ------------------- Subscription Schemas -------------------

class SubscriptionOut(BaseModel):
    id: int
    user_id: int
    tier: str
    status: str

    class Config:
        from_attributes = True
        # orm_mode = True
