# ✅ 기존 코드
import feedparser
from datetime import datetime
from sqlalchemy.orm import Session
from database import SessionLocal
from models.news import News

# ✅ [1] 새로 추가
import requests
from bs4 import BeautifulSoup

RSS_URL = "https://news.google.com/rss/search?q=보디빌딩&hl=ko&gl=KR&ceid=KR:ko"

# ✅ [2] 썸네일 이미지 추출 함수 추가
def extract_thumbnail(link: str) -> str:
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(link, headers=headers, timeout=5)
        soup = BeautifulSoup(response.content, "html.parser")

        # og:image 메타태그 우선
        og_image = soup.find("meta", property="og:image")
        if og_image and og_image.get("content"):
            return og_image["content"]

        # 없으면 첫 번째 <img> 태그 사용
        img_tag = soup.find("img")
        if img_tag and img_tag.get("src"):
            return img_tag["src"]

    except Exception as e:
        print(f"[썸네일 추출 실패] {link} → {e}")
    return ""  # 실패 시 빈 문자열

# ✅ 기존 fetch_news 함수 그대로 유지하면서 내부만 수정
def fetch_news():
    print("📰 [뉴스 수집] 시작")
    feed = feedparser.parse(RSS_URL)

    db: Session = SessionLocal()

    for entry in feed.entries:
        title = entry.title
        link = entry.link
        published = datetime(*entry.published_parsed[:6])

        # 중복 방지
        existing = db.query(News).filter_by(title=title, link=link).first()
        if existing:
            continue

        # ✅ [3] 썸네일 추출
        image_url = extract_thumbnail(link)

        new_article = News(
            title=title,
            link=link,
            image_url=image_url,  # ← 여기 변경됨
            created_at=published
        )
        db.add(new_article)

    db.commit()
    db.close()
    print("✅ [뉴스 수집] 완료")
