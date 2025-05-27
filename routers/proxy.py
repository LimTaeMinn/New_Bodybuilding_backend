from fastapi import APIRouter, Query
from fastapi.responses import Response
import requests

router = APIRouter(prefix="/proxy", tags=["Proxy"])

@router.get("/image")
def proxy_image(url: str = Query(...)):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=5)
        content_type = response.headers.get("Content-Type", "image/jpeg")
        return Response(content=response.content, media_type=content_type)
    except Exception:
        fallback = requests.get("https://upload.wikimedia.org/wikipedia/commons/6/65/No-Image-Placeholder.svg")
        return Response(content=fallback.content, media_type="image/svg+xml")
