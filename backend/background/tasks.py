from celery import Celery
from config import settings
from agent_registry import AgentRegistry
from db import get_sync_session
from models import Lead, Appointment
from sqlmodel import Session, select
from datetime import datetime, timedelta

celery = Celery(__name__, broker=settings.REDIS_URL)
registry = AgentRegistry()

@celery.task
def send_scheduled_followups():
    with get_sync_session() as session:
        # Get leads needing follow-up
        stale_leads = session.exec(
            select(Lead).where(
                (Lead.last_contact < datetime.utcnow() - timedelta(days=3)) &
                (Lead.status != "Converted"))
        ).all()
        
        for lead in stale_leads:
            registry.execute_action(
                "follow_up", 
                "send_followup", 
                {"lead_id": lead.id},
                review=False
            )

@celery.task
def send_appointment_reminders():
    with get_sync_session() as session:
        # Get appointments in next 24 hours without reminder
        soon_appointments = session.exec(
            select(Appointment).where(
                (Appointment.time > datetime.utcnow()) &
                (Appointment.time < datetime.utcnow() + timedelta(days=1)) &
                (Appointment.reminder_sent == False))
        ).all()
        
        for appointment in soon_appointments:
            registry.execute_action(
                "customer_support", 
                "send_reminder", 
                {"appointment_id": appointment.id},
                review=False
            )
            appointment.reminder_sent = True
            session.add(appointment)
            session.commit()