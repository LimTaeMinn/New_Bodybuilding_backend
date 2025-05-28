import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# ✅ Render에서는 load_dotenv() 필요 없음
DATABASE_URL = os.getenv("DATABASE_URL")

# ✅ PostgreSQL SSL 연결 옵션
engine = create_engine(
    DATABASE_URL,
    connect_args={"sslmode": "require"}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

Base = declarative_base()

def init_db():
    from models.bodyfat import BodyfatHistory
    from models.competition import CompetitionHistory
    from models.routine import WorkoutRoutine, WorkoutItem
    Base.metadata.create_all(bind=engine)
