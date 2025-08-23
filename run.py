# nextgen_realty/run.py
import uvicorn
from backend.main import app

if __name__ == "__main__":
    uvicorn.run("backend.main:app", reload=True)