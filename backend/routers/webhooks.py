from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
import stripe
from ..config import settings
import json

router = APIRouter()
stripe.api_key = settings.stripe_secret_key

@router.post("/stripe-webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.stripe_webhook_secret
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError as e:
        raise HTTPException(status_code=400, detail="Invalid signature")

    # Handle events
    if event.type == "checkout.session.completed":
        session = event.data.object
        # Handle successful subscription creation
        print(f"Subscription created for {session.customer}")

    elif event.type == "invoice.payment_succeeded":
        invoice = event.data.object
        # Handle recurring payment success
        print(f"Payment succeeded for {invoice.customer}")

    return JSONResponse(status_code=200, content={"status": "success"})