from fastapi import FastAPI, Depends
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI()

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Temporary session placeholder (to be replaced in Phase 4 with SQLModel)
async def get_session():
    yield None  # Placeholder for database session

class Lead(BaseModel):
    name: str
    email: str
    phone: str
    message: str

@app.post("/api/leads")
async def create_lead(lead: Lead):
    # Placeholder: In a real app, save to database (Phase 4)
    print(f"Received lead: {lead}")
    return {"message": "Lead created successfully"}

class OnboardingData(BaseModel):
    name: str
    email: str
    date: str

@app.post("/api/onboarding")
async def onboard_agent(data: OnboardingData, db: AsyncSession = Depends(get_session)):
    # Placeholder: Save to database
    return {"message": f"Demo scheduled for {data.name} on {data.date}"}
