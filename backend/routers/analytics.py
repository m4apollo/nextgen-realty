from fastapi import APIRouter, Depends
from sqlmodel import Session
from db import get_sync_session
from models import Lead, User
from agent_registry import AgentRegistry
from utils.security import get_current_user
from datetime import datetime, timedelta

router = APIRouter(tags=["Analytics"])
registry = AgentRegistry()

@router.get("/dashboard")
async def get_dashboard_analytics(
    session: Session = Depends(get_sync_session),
    current_user: User = Depends(get_current_user)
):
    # Basic metrics
    total_leads = session.exec(
        select(func.count(Lead.id)).where(Lead.owner_id == current_user.id)
    ).first()
    
    converted_leads = session.exec(
        select(func.count(Lead.id)).where(
            (Lead.owner_id == current_user.id) & 
            (Lead.status == "Converted"))
    ).first()
    
    # Get advanced analytics from agent
    analytics = registry.execute_action(
        "analytics", 
        "generate_user_report", 
        {"user_id": current_user.id},
        review=False
    )
    
    return {
        "total_leads": total_leads,
        "converted_leads": converted_leads,
        "conversion_rate": converted_leads / total_leads if total_leads else 0,
        "advanced": analytics.get("result", {})
    }