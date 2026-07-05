from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine("mysql+pymysql://root:Mcwm%406306Sql@localhost:3306/finance_core")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
