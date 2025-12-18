from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from database import Base,engine, get_db
from routes.user_routes import router as user_router
from routes.test_routes import router as test_router
from starlette.middleware.sessions import SessionMiddleware
import os 
from auth.rbac import create_super


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

##create super owner
SUPER_ADMIN=os.getenv("SUPER_ADMIN")
SUPER_KEY=os.getenv("SUPER_KEY")



@app.get("/")
def root(db:Session=Depends(get_db),):

    create_super(db,SUPER_ADMIN,SUPER_ADMIN,SUPER_KEY)
    return {"app is running"}
