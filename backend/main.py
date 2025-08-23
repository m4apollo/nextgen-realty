from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import users, payments, agents, leads, analytics, integrations
from backend.db import get_session, engine
from backend.models import Base
from backend.config import settings

from db import get_session, engine
from models import Base
from config import settings

app = FastAPI(
    title="NextGen Realty AI Platform",
    version="5.0",
    description="AI-powered CRM for real estate professionals"
)

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users.router, prefix="/users")
app.include_router(payments.router, prefix="/payments")
app.include_router(agents.router, prefix="/agents")
app.include_router(leads.router, prefix="/leads")
app.include_router(analytics.router, prefix="/analytics")
app.include_router(integrations.router, prefix="/integrations")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/health")
async def health_check():
    return {
        "status": "operational",
        "version": "5.0",
        "company": "NextGen Realty",
        "agents": 22
    }