from fastapi import APIRouter, Depends, Request, HTTPException
from sqlmodel import Session
from db import get_sync_session
from models import User, Subscription, SubscriptionPlan
from utils.security import get_current_user
from utils.stripe import StripeService
from pydantic import BaseModel
from typing import List

router = APIRouter()

class SubscriptionPlanResponse(BaseModel):
    id: int
    name: str
    price_id: str
    amount: int
    currency: str
    interval: str
    features: List[str]

class SubscriptionStatusResponse(BaseModel):
    status: str
    current_period_end: int
    plan: dict

@router.post("/create-session")
async def create_checkout_session(
    price_id: str,
    session: Session = Depends(get_sync_session),
    user: User = Depends(get_current_user)
):
    checkout_session = StripeService.create_checkout_session(price_id, str(user.id))
    return {"session_id": checkout_session.id, "url": checkout_session.url}

@router.get("/subscription-plans")
def get_subscription_plans(
    session: Session = Depends(get_sync_session)
) -> List[SubscriptionPlanResponse]:
    plans = session.query(SubscriptionPlan).filter(SubscriptionPlan.is_active == True).all()
    return [
        SubscriptionPlanResponse(
            id=plan.id,
            name=plan.name,
            price_id=plan.stripe_price_id,
            amount=plan.amount,
            currency=plan.currency,
            interval=plan.interval or "one_time",
            features=plan.features
        )
        for plan in plans
    ]

@router.get("/subscription-status")
def get_subscription_status(
    user: User = Depends(get_current_user),
    session: Session = Depends(get_sync_session)
) -> SubscriptionStatusResponse:
    if not user.subscription:
        raise HTTPException(status_code=404, detail="No active subscription")
    
    subscription = StripeService.get_subscription(user.subscription.stripe_subscription_id)
    return SubscriptionStatusResponse(
        status=subscription.status,
        current_period_end=subscription.current_period_end,
        plan={
            "name": user.subscription.plan.name,
            "amount": user.subscription.plan.amount
        }
    )

@router.post("/cancel-subscription")
def cancel_subscription(
    user: User = Depends(get_current_user),
    session: Session = Depends(get_sync_session)
):
    if not user.subscription:
        raise HTTPException(status_code=404, detail="No active subscription")
    
    StripeService.cancel_subscription(user.subscription.stripe_subscription_id)
    user.subscription.status = "canceled"
    session.commit()
    return {"status": "success"}

@router.post("/webhook")
async def stripe_webhook(request: Request, session: Session = Depends(get_sync_session)):
    payload = await request.body()
    sig_header = request.headers.get('stripe-signature')
    
    try:
        event = StripeService.construct_webhook_event(payload, sig_header)
        event_data = event['data']['object']
        
        if event['type'] == 'checkout.session.completed':
            user_id = int(event_data['client_reference_id'])
            user = session.get(User, user_id)
            if user:
                plan = session.query(SubscriptionPlan).filter(
                    SubscriptionPlan.stripe_price_id == event_data['line_items']['data'][0]['price']['id']
                ).first()
                if plan:
                    user.subscription = Subscription(
                        stripe_subscription_id=event_data['subscription'],
                        plan_id=plan.id,
                        status="active",
                        current_period_end=event_data['subscription_details']['current_period_end']
                    )
                    session.commit()
        
        elif event['type'] == 'customer.subscription.deleted':
            subscription = session.query(Subscription).filter(
                Subscription.stripe_subscription_id == event_data['id']
            ).first()
            if subscription:
                subscription.status = "canceled"
                session.commit()
                
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    return {"status": "success"}