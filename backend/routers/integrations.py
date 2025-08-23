from fastapi import APIRouter, Depends
from agent_registry import AgentRegistry
from utils.security import get_current_user
from config import settings

router = APIRouter(tags=["Integrations"])
registry = AgentRegistry()

@router.post("/zillow/import")
async def import_zillow_leads(
    location: str,
    max_results: int = 20,
    current_user: User = Depends(get_current_user)
):
    if not settings.ZILLOW_API_KEY:
        raise HTTPException(400, detail="Zillow integration not configured")
    
    result = registry.execute_action(
        "zillow_finder", 
        "find_fsbo_listings", 
        {"location": location, "max_results": max_results}
    )
    
    if "error" in result:
        raise HTTPException(500, detail=result["error"])
    
    # Process and save leads
    # ... (implementation would save leads to database)
    
    return {"imported": len(result["result"]), "leads": result["result"]}