import feedparser
from datetime import datetime
from sqlalchemy.orm import Session
from database import SessionLocal
from models.news import News

# ✅ 새로 추가
import requests
from bs4 import BeautifulSoup

RSS_URL = "https://news.google.com/rss/search?q=보디빌딩&hl=ko&gl=KR&ceid=KR:ko"

# ✅ [1] 진짜 뉴스 URL 추출
def extract_real_url(google_link: str) -> str:
    try:
        response = requests.get(google_link, headers={"User-Agent": "Mozilla/5.0"}, timeout=5, allow_redirects=True)
        return response.url  # 구글 리디렉션을 따라가서 진짜 기사 URL 획득
    except Exception as e:
        print(f"[실제 URL 추출 실패] {google_link} → {e}")
        return google_link  # 실패 시 원본 링크라도 유지

# ✅ [2] 썸네일 이미지 추출
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

# ✅ [3] 뉴스 수집
def fetch_news():
    print("📰 [뉴스 수집] 시작")
    feed = feedparser.parse(RSS_URL)

    db: Session = SessionLocal()

    for entry in feed.entries:
        title = entry.title
        raw_link = entry.link  # 구글 리디렉션 링크
        published = datetime(*entry.published_parsed[:6])

        # ✅ 진짜 뉴스 기사 주소 획득
        real_link = extract_real_url(raw_link)

        # 중복 방지
        existing = db.query(News).filter_by(title=title, link=real_link).first()
        if existing:
            continue

        # ✅ 썸네일 추출
        image_url = extract_thumbnail(real_link)

        new_article = News(
            title=title,
            link=real_link,  # ← 진짜 기사 주소 저장
            image_url=image_url,
            created_at=published
        )
        db.add(new_article)

    db.commit()
    db.close()
    print("✅ [뉴스 수집] 완료")
