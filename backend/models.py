from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
from pydantic import EmailStr

class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True)
    full_name: str
    company: str = "NextGen Realty"
    phone: Optional[str] = None
    is_active: bool = True
    is_admin: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
    last_login: Optional[datetime] = None
    plan: str = Field(default="free")
    message_quota: int = Field(default=50)
    messages_used: int = Field(default=0)
    stripe_customer_id: Optional[str] = None
    
    leads: List["Lead"] = Relationship(back_populates="owner")
    subscriptions: List["Subscription"] = Relationship(back_populates="user")

class UserCreate(SQLModel):
    email: EmailStr
    password: str
    full_name: str
    company: Optional[str] = "NextGen Realty"

class UserRead(UserBase):
    id: int
    plan: str
    is_active: bool

class LeadBase(SQLModel):
    name: str
    email: EmailStr
    phone: str
    source: str = "Web"
    status: str = "New"
    notes: str = ""
    last_contact: Optional[datetime] = None

class Lead(LeadBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    owner_id: int = Field(foreign_key="user.id")
    owner: User = Relationship(back_populates="leads")
    
    appointments: List["Appointment"] = Relationship(back_populates="lead")

class LeadCreate(LeadBase):
    pass

class Subscription(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    stripe_id: str
    plan: str
    status: str
    start_date: datetime = Field(default_factory=datetime.utcnow)
    end_date: Optional[datetime] = None
    user: User = Relationship(back_populates="subscriptions")

class Appointment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    lead_id: int = Field(foreign_key="lead.id")
    time: datetime
    location: str
    notes: str = ""
    reminder_sent: bool = False
    lead: Lead = Relationship(back_populates="appointments")

class AgentActivity(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    last_active: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = False
    last_error: Optional[str] = None

class SubscriptionPlan(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    name: str
    price: float
    stripe_price_id: str
    features: str  # JSON string of features
    class SubscriptionPlan(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    stripe_product_id: str = Field(index=True)
    stripe_price_id: str = Field(index=True)
    amount: int  # in cents
    currency: str = Field(default="usd", max_length=3)
    interval: Optional[str]  # month, year, etc.
    features: List[str] = Field(default=[], sa_type=JSON)
    is_active: bool = Field(default=True)

class Subscription(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    plan_id: int = Field(foreign_key="subscriptionplan.id")
    stripe_subscription_id: str
    status: str = Field(default="active")  # active, canceled, incomplete
    created_at: datetime = Field(default_factory=datetime.utcnow)
    current_period_end: Optional[datetime]