from fastapi import APIRouter, Depends, HTTPException
from agent_registry import AgentRegistry
from utils.security import get_current_user
from utils.logging import logger

router = APIRouter(tags=["Agents"])
registry = AgentRegistry()

@router.post("/{agent_name}/{action}")
async def execute_agent_action(
    agent_name: str, 
    action: str, 
    data: dict,
    current_user: User = Depends(get_current_user)
):
    # Add user context to data
    data["user_id"] = current_user.id
    data["company"] = current_user.company or "NextGen Realty"
    
    result = registry.execute_action(agent_name, action, data)
    
    if "error" in result:
        logger.error(f"Agent error: {result['error']}")
        raise HTTPException(500, detail=result["error"])
    
    if result["status"] == "revision_required":
        logger.warning(f"Agent revision required: {agent_name}/{action}")
        return result
    
    return result["result"]
# backend/routers/agents.py (UPDATE)
@router.post("/{agent_name}/{action}")
async def execute_agent_action(...):
    try:
        # ... existing code ...
    except Exception as e:
        logger.error(f"Agent failure: {agent_name}/{action} - {str(e)}")
        return {
            "status": "error",
            "error_code": "AGENT_EXECUTION_FAILED",
            "details": str(e),
            "retry_suggested": True
        }