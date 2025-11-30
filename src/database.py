
import sqlalchemy

from sqlalchemy.orm import declarative_base,sessionmaker

db_url="sqlite:///./testdb"
Base=declarative_base()
engine=sqlalchemy.create_engine(db_url,connect_args={"check_same_thread":False})

SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

def get_db():
    db=SessionLocal()
    try:
        
        yield db
    finally:
        db.close()

