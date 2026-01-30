import sys
import os
# Ensure we can import from the backend directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'sris/backend')))

from sris.backend.models.database import Base, engine, SessionLocal, User
from sris.backend.api.auth import register, UserCreate

# Create tables
Base.metadata.create_all(bind=engine)

def test_registration():
    db = SessionLocal()
    try:
        user_in = UserCreate(username="test_debug", email="debug@example.com", password="password123")
        import asyncio
        # We need a dummy request context or just call the function if not using specific FastAPI Request features
        # register is async
        async def run_test():
            try:
                result = await register(user_in, db)
                print("Registration Successful:", result)
            except Exception as e:
                import traceback
                traceback.print_exc()
        
        asyncio.run(run_test())
    finally:
        db.close()

if __name__ == "__main__":
    test_registration()
