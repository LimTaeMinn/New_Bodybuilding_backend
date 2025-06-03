from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from database import get_db
from models.news import News
from schemas.news import NewsOut
from datetime import datetime
from cron.rss_news_fetcher import fetch_news

router = APIRouter(prefix="/news", tags=["News"])

@router.get("/", response_model=list[NewsOut])
def get_news_list(
    keyword: str = Query(None, description="제목 검색 키워드"),
    date: str = Query(None, description="YYYY-MM-DD 형식의 날짜 필터"),
    db: Session = Depends(get_db)
):
    query = db.query(News)

    if keyword:
        query = query.filter(News.title.contains(keyword))

    if date:
        try:
            # 문자열 날짜를 datetime 객체로 변환
            date_obj = datetime.strptime(date, "%Y-%m-%d").date()
            query = query.filter(
                News.created_at >= datetime.combine(date_obj, datetime.min.time()),
                News.created_at <= datetime.combine(date_obj, datetime.max.time())
            )
        except ValueError:
            print(f"❗ 날짜 형식 오류: {date} (예: 2025-05-24)")

    return query.order_by(News.created_at.desc()).all()

@router.get("/refresh")
def refresh_news():
    fetch_news()
    return {"message": "뉴스 새로고침 완료!"}