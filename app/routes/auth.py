from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime

from app.database import get_db
from app.models import User, OTP
from app.schemas import (
    OTPCreate, OTPVerify, SignupRequest, ForgotPasswordRequest,
    ChangePasswordRequest, UserOut
)
from app.utils.otp import generate_otp, get_expiry
from app.utils.jwt import create_access_token
from app.dependencies import get_current_user

router = APIRouter()

# 1. Signup endpoint
@router.post("/signup")
async def signup(data: SignupRequest, db: AsyncSession = Depends(get_db)):
    """
    Registers a new user with mobile number and optional info.
    """
    result = await db.execute(select(User).where(User.mobile == data.mobile))
    user = result.scalar_one_or_none()
    if user:
        raise HTTPException(status_code=400, detail="User already exists")
    user = User(mobile=data.mobile)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return {"message": "User registered successfully."}

# 2. Send OTP (login)
@router.post("/send-otp")
async def send_otp(data: OTPCreate, db: AsyncSession = Depends(get_db)):
    """
    Sends an OTP to the user’s mobile number (mocked, returned in response).
    If user does not exist, create the user.
    """
    result = await db.execute(select(User).where(User.mobile == data.mobile))
    user = result.scalar_one_or_none()
    if not user:
        user = User(mobile=data.mobile)
        db.add(user)
        await db.commit()
        await db.refresh(user)
    # Generate OTP
    otp_code = generate_otp()
    expires_at = get_expiry()
    otp = OTP(user_id=user.id, otp=otp_code, expires_at=expires_at)
    db.add(otp)
    await db.commit()
    return {"otp": otp_code, "expires_at": expires_at}

# 3. Verify OTP (login)
@router.post("/verify-otp")
async def verify_otp(data: OTPVerify, db: AsyncSession = Depends(get_db)):
    """
    Verifies the OTP and returns a JWT token for the session.
    """
    result = await db.execute(select(User).where(User.mobile == data.mobile))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # Find latest OTP for user
    result = await db.execute(
        select(OTP)
        .where(OTP.user_id == user.id)
        .order_by(OTP.expires_at.desc())
    )
    otp = result.scalars().first()
    if not otp or otp.otp != data.otp or otp.expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")
    # Generate JWT
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}

# 4. Forgot password (send OTP for password reset)
@router.post("/forgot-password")
async def forgot_password(data: ForgotPasswordRequest, db: AsyncSession = Depends(get_db)):
    """
    Sends OTP for password reset.
    """
    result = await db.execute(select(User).where(User.mobile == data.mobile))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    otp_code = generate_otp()
    expires_at = get_expiry()
    otp = OTP(user_id=user.id, otp=otp_code, expires_at=expires_at)
    db.add(otp)
    await db.commit()
    return {"otp": otp_code, "expires_at": expires_at}

# 5. Change password (JWT required)
@router.post("/change-password")
async def change_password(
    data: ChangePasswordRequest,
    user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Allows the user to change password while logged in.
    """
    result = await db.execute(select(User).where(User.id == int(user_id)))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # TODO: Validate old password if you store passwords
    user.password = data.new_password  # Hash in real code!
    db.add(user)
    await db.commit()
    return {"message": "Password changed successfully."}

# # 6. Get current user info (JWT required)
# @router.get("/me", response_model=UserOut)
# async def get_me(
#     user_id: str = Depends(get_current_user),
#     db: AsyncSession = Depends(get_db)
# ):
#     """
#     Returns details about the currently authenticated user.
#     """
#     result = await db.execute(select(User).where(User.id == int(user_id)))
#     user = result.scalar_one_or_none()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user

# 7. Protected route (for testing JWT, optional)
@router.get("/protected")
async def protected_route(user_id: str = Depends(get_current_user)):
    """
    Protected route for testing JWT authentication.
    """
    return {"message": f"Hello user {user_id}, you are authenticated!"}
