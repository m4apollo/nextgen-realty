from fastapi import APIRouter, Depends
from sqlmodel import Session
from db import get_sync_session
from models import Lead, LeadCreate, LeadRead
from agent_registry import AgentRegistry
from utils.security import get_current_user

router = APIRouter(tags=["Leads"])
registry = AgentRegistry()

@router.post("/", response_model=LeadRead)
async def create_lead(
    lead: LeadCreate, 
    session: Session = Depends(get_sync_session),
    current_user: User = Depends(get_current_user)
):
    # Process with lead generation agent
    processed = registry.execute_action(
        "lead_generation", 
        "process_web_lead", 
        {"form_data": lead.dict()}
    )
    
    if processed.get("error"):
        raise HTTPException(500, detail=processed["error"])
    
    # Create database record
    db_lead = Lead(**processed["result"], owner_id=current_user.id)
    session.add(db_lead)
    session.commit()
    session.refresh(db_lead)
    
    # Trigger follow-up sequence
    follow_up_result = registry.execute_action(
        "follow_up", 
        "initial_followup", 
        {"lead": db_lead.dict()}
    )
    
    if follow_up_result.get("error"):
        # Log error but don't fail the lead creation
        logger.error(f"Follow-up failed: {follow_up_result['error']}")
    
    return db_lead

@router.get("/", response_model=List[LeadRead])
async def get_leads(
    session: Session = Depends(get_sync_session),
    current_user: User = Depends(get_current_user)
):
    return session.exec(select(Lead).where(Lead.owner_id == current_user.id)).all()