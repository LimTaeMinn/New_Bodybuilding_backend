from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os
from fastapi.middleware.cors import CORSMiddleware
from auth.routes import router as auth_router
from routers import bodyfat
from routers import competition
from routers import routine  # 추가
from routers import news
from routers import user
#<<<<<<< HEAD
from routers import proxy  # 상단 import에 추가
#=======
#>>>>>>> 8313466ef238964fe0fc79354bea89fa283c01c1
from database import init_db  # ✅ 이 줄 추가

from apscheduler.schedulers.background import BackgroundScheduler
from cron.rss_news_fetcher import fetch_news

app = FastAPI()

# ✅ 정적 파일 서빙 추가
app.mount("/static", StaticFiles(directory="static"), name="static")

# ✅ [추가] 앱 실행 시 뉴스 자동 수집 스케줄러 시작
scheduler = BackgroundScheduler()
scheduler.add_job(fetch_news, "interval", seconds=60)

app.include_router(bodyfat.router)
app.include_router(auth_router)
app.include_router(competition.router)
app.include_router(routine.router)  # 추가
app.include_router(news.router)
app.include_router(user.router)
#<<<<<<< HEAD
app.include_router(proxy.router)  # 라우터 등록부에 추가
#=======
#>>>>>>> 8313466ef238964fe0fc79354bea89fa283c01c1



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
