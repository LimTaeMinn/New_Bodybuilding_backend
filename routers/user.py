from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from auth.utils import get_current_user
from auth.models import User
import uuid
import os
import shutil

router = APIRouter()

@router.post("/user/profile-image")
async def upload_profile_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    # 확장자 확인
    extension = os.path.splitext(file.filename)[-1]
    if extension.lower() not in [".jpg", ".jpeg", ".png"]:
        raise HTTPException(status_code=400, detail="지원하지 않는 파일 형식입니다.")

    # 사용자 DB 조회
    user_in_db = db.query(User).filter(User.id == user.id).first()
    if not user_in_db:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")

    # ✅ 기존 이미지 삭제 (있다면)
    if user_in_db.profile_image_url:
        try:
            if os.path.exists(user_in_db.profile_image_url):
                os.remove(user_in_db.profile_image_url)
        except Exception as e:
            # 삭제 실패하더라도 진행 (선택사항)
            print(f"[이미지 삭제 실패] {e}")

    # 새 이미지 저장
    filename = f"profile_{user.id}_{uuid.uuid4().hex}{extension}"
    file_path = f"static/profile_images/{filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # DB에 새로운 이미지 경로 저장
    user_in_db.profile_image_url = file_path
    db.commit()

    return {
        "message": "프로필 이미지 변경 완료",
        "image_url": f"/{file_path}"
    }
    
