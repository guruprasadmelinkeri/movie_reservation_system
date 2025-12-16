from fastapi import FastAPI
from database import Base,engine
from routes.user_routes import router as user_router
from routes.test_routes import router as test_router
from starlette.middleware.sessions import SessionMiddleware
import os 


session_key=os.getenv("session_key")
app=FastAPI()
app.add_middleware(SessionMiddleware,
                   secret_key=session_key,
                   session_cookie="session",
                   same_site="lax",
                   https_only=True)

app.include_router(user_router)
app.include_router(test_router)
Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"app is running"}
