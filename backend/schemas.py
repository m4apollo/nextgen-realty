from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# User Schemas
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    company: Optional[str] = "NextGen Realty"

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserRead(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    company: str
    plan: str
    is_active: bool

# Lead Schemas
class LeadCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str
    source: Optional[str] = "Web"
    notes: Optional[str] = ""

class LeadRead(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: str
    source: str
    status: str
    created_at: datetime

# Payment Schemas
class SubscriptionCreate(BaseModel):
    plan: str  # free, pro, team
    payment_method_id: str

class PaymentIntentCreate(BaseModel):
    amount: int
    currency: str = "usd"

# Analytics Schemas
class AnalyticsReport(BaseModel):
    period: str
    new_leads: int
    conversions: int
    revenue: float
    top_sources: Dict[str, int]