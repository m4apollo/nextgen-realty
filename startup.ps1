# 1. Navigate to project
cd "C:\Users\ai realtor ops\Documents\nextgen_realty"

# 2. Create and activate virtual environment
python -m venv venv --clear
.\venv\Scripts\activate

# 3. Install all required packages
pip install -e . fastapi uvicorn sqlmodel stripe alembic pydantic-settings python-dotenv

# 4. Setup database
python -m alembic upgrade head

# 5. Start server
uvicorn backend.main:app --reload