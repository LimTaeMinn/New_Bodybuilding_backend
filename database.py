from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. DB 연결 주소
DATABASE_URL = "sqlite:///./test.db"

# 2. 엔진 & 세션 설정
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 3. 베이스 클래스 생성
Base = declarative_base()

# 4. DB 테이블 생성 함수 (모델 import는 이 함수 안에서!)
def init_db():
    from models.bodyfat import BodyfatHistory  # ✨ 함수 안에서 import (순환참조 방지)
    from models.competition import CompetitionHistory  # ✅ 이 줄 추가!
    Base.metadata.create_all(bind=engine)
