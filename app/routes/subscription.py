from fastapi import APIRouter, Depends, HTTPException
from app.dependencies import get_current_user

# If using Stripe
# import stripe
# from app.utils.stripe import create_checkout_session, get_user_subscription_status, get_user_subscription_info

router = APIRouter()

# 1. Initiate Pro subscription via Stripe
@router.post("/subscribe/pro")
async def subscribe_pro(user_id: str = Depends(get_current_user)):
    """
    Initiates a Pro subscription via Stripe Checkout.
    """
    # TODO: Implement Stripe Checkout Session creation
    # session_url = create_checkout_session(user_id)
    # return {"checkout_url": session_url}
    return {"message": "Stripe Checkout session would be created here."}

# 2. Stripe webhook endpoint (required by assignment)
@router.post("/webhook/stripe")
async def stripe_webhook():
    """
    Handles Stripe webhook events (e.g., payment success/failure).
    """
    # TODO: Implement Stripe webhook event handling
    return {"message": "Stripe webhook received (to be implemented)."}

# 3. Check current user's subscription status
@router.get("/subscription/status")
async def subscription_status(user_id: str = Depends(get_current_user)):
    """
    Checks the user's current subscription tier (Basic or Pro).
    """
    # TODO: Fetch real subscription status from your DB
    # status = get_user_subscription_status(user_id)
    # return {"subscription": status}
    return {"subscription": "Basic"}  # Placeholder

# 4. Get current user's subscription info
@router.get("/subscriptions/my")
async def my_subscription(user_id: str = Depends(get_current_user)):
    """
    Fetches and returns subscription info for the current user.
    """
    # TODO: Fetch and return real subscription info from your DB
    # info = get_user_subscription_info(user_id)
    # return info
    return {"subscription": "demo"}  # Placeholder
