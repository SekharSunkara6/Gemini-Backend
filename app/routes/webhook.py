from fastapi import APIRouter, Request, HTTPException, status
from dotenv import load_dotenv
load_dotenv()

import stripe
import os

router = APIRouter()

# Set your Stripe secret key and webhook secret (use environment variables in production)
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")

if not stripe.api_key:
    raise RuntimeError("STRIPE_SECRET_KEY environment variable not set")
if not STRIPE_WEBHOOK_SECRET:
    raise RuntimeError("STRIPE_WEBHOOK_SECRET environment variable not set")

@router.post("/webhook/stripe")
async def stripe_webhook(request: Request):
    """
    Stripe webhook endpoint to handle events like payment success/failure.
    """
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    if not sig_header:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing Stripe signature header"
        )

    # Verify the webhook signature
    try:
        event = stripe.Webhook.construct_event(
            payload=payload,
            sig_header=sig_header,
            secret=STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        # Invalid payload
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid payload")
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid signature")

    # Handle the event
    event_type = event["type"]
    data_object = event["data"]["object"]

    if event_type == "checkout.session.completed":
        # Example: user_id = data_object.get("client_reference_id")
        # TODO: Mark user's subscription as active in your DB
        pass

    elif event_type == "invoice.payment_failed":
        # Example: user_id = data_object.get("client_reference_id")
        # TODO: Mark user's subscription as inactive/failed in your DB
        pass

    # Add more event types as needed

    return {"status": "success"}
