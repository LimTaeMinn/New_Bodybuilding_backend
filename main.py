from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from auth.routes import router as auth_router
from routers import bodyfat
from routers import competition
from routers import routine  # 추가
from routers import news
from database import init_db  # ✅ 이 줄 추가

from apscheduler.schedulers.background import BackgroundScheduler
from cron.rss_news_fetcher import fetch_news

app = FastAPI()

# ✅ [추가] 앱 실행 시 뉴스 자동 수집 스케줄러 시작
scheduler = BackgroundScheduler()
scheduler.add_job(fetch_news, "interval", seconds=60)

app.include_router(bodyfat.router)
app.include_router(auth_router)
app.include_router(competition.router)
app.include_router(routine.router)  # 추가
app.include_router(news.router)


# ✅ CORS 설정 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "서버 정상 작동 중!"}

@app.on_event("startup")
def start_scheduler():
    scheduler.start()


# ✅ 서버 시작 시 DB 테이블 생성
init_db()
