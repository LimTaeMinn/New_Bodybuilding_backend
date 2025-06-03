import feedparser
from datetime import datetime
from sqlalchemy.orm import Session
from database import SessionLocal
from models.news import News

# ✅ 썸네일 추출용
import requests
from bs4 import BeautifulSoup

# ✅ 연합뉴스 건강 섹션 RSS
RSS_URL = "https://www.yna.co.kr/rss/health.xml"

# ✅ [1] 썸네일 이미지 추출 함수 (유지)
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
    return ""

# ✅ [2] 뉴스 수집
def fetch_news():
    print("📰 [뉴스 수집] 시작")
    feed = feedparser.parse(RSS_URL)

    db: Session = SessionLocal()

    for entry in feed.entries:
        title = entry.title

        # ✅ [✨추가] '보디빌딩' 키워드 필터링
        if "보디빌딩" not in title and "헬스" not in title:
            continue

        # ✅ [🔁수정] 아래 줄 수정: raw_link → link
        link = entry.link

        published = datetime(*entry.published_parsed[:6])

        # ✅ [❌삭제] extract_real_url 관련 줄 삭제
        # real_link = extract_real_url(raw_link)  ← ❌ 삭제

        # ✅ [🔁수정] 아래 줄 수정: real_link → link
        existing = db.query(News).filter_by(title=title, link=link).first()
        if existing:
            continue

        # ✅ 썸네일 추출
        image_url = extract_thumbnail(link)

        new_article = News(
            title=title,
            link=link,  # ← 수정 완료
            image_url=image_url,
            created_at=published
        )
        db.add(new_article)

    db.commit()
    db.close()
    print("✅ [뉴스 수집] 완료")
