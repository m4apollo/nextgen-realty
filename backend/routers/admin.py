# backend/routers/admin.py (NEW)
from fastapi import APIRouter, Depends
from sqlmodel import Session
from db import get_sync_session
from models import User, Lead, Subscription
from utils.security import get_admin_user

router = APIRouter(tags=["Admin"])

@router.get("/system-stats")
async def get_system_stats(
    session: Session = Depends(get_sync_session),
    admin: User = Depends(get_admin_user)
):
    return {
        "users": session.query(User).count(),
        "active_leads": session.query(Lead).filter(Lead.status != "converted").count(),
        "revenue": sum(sub.plan.price for sub in session.query(Subscription).all())
    }
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from db import get_sync_session
from models import User, Lead, Subscription, SubscriptionPlan
from utils.security import get_admin_user

router = APIRouter(tags=["Admin"])

# Your original system stats endpoint
@router.get("/system-stats")
async def get_system_stats(
    session: Session = Depends(get_sync_session),
    admin: User = Depends(get_admin_user)
):
    return {
        "users": session.exec(select(User)).count(),
        "active_leads": session.exec(select(Lead).where(Lead.status != "converted")).count(),
        "revenue": sum(sub.plan.price for sub in session.exec(select(Subscription)).all())
    }

# New endpoints
@router.get("/user/{user_id}")
def get_user_details(user_id: int, session: Session = Depends(get_sync_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(404, "User not found")
    return {
        "user": user,
        "subscription": user.subscription.plan.name if user.subscription else "Free"
    }

@router.put("/subscription/{user_id}")
def update_subscription(user_id: int, plan_id: int, session: Session = Depends(get_sync_session)):
    user = session.get(User, user_id)
    plan = session.get(SubscriptionPlan, plan_id)
    
    if not user or not plan:
        raise HTTPException(400, "Invalid user or plan ID")
    
    if not user.subscription:
        user.subscription = Subscription(plan_id=plan_id, user_id=user_id)
    else:
        user.subscription.plan_id = plan_id
    
    session.commit()
    return {"status": "updated", "plan": plan.name}

@router.get("/revenue")
def get_revenue(session: Session = Depends(get_sync_session)):
    revenue = session.exec(select(Subscription)).all()
    return {
        "total": sum(sub.plan.price for sub in revenue),
        "by_plan": {sub.plan.name: sub.plan.price for sub in revenue}
    }