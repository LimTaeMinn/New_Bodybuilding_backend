from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from auth import models as auth_models
from models.routine import WorkoutRoutine, WorkoutItem
from schemas.routine import WorkoutRoutineCreate, WorkoutRoutineUpdate, WorkoutRoutine as RoutineResponse
from database import get_db
from auth.utils import get_current_user

router = APIRouter(
    prefix="/routines",
    tags=["routines"]
)

@router.post("/", response_model=RoutineResponse)
def create_routine(
    routine_data: WorkoutRoutineCreate,
    db: Session = Depends(get_db),
    current_user: auth_models.User = Depends(get_current_user)
):
    routine = WorkoutRoutine(
        title=routine_data.title,
        user_id=current_user.id
    )
    db.add(routine)
    db.flush()

    for item in routine_data.items:
        db.add(WorkoutItem(
            name=item.name,
            count=item.count,
            routine_id=routine.id
        ))

    db.commit()
    db.refresh(routine)
    return routine

@router.get("/", response_model=list[RoutineResponse])
def get_my_routines(
    db: Session = Depends(get_db),
    current_user: auth_models.User = Depends(get_current_user)
):
    return db.query(WorkoutRoutine).filter(WorkoutRoutine.user_id == current_user.id).all()

@router.get("/{routine_id}", response_model=RoutineResponse)
def get_routine_detail(
    routine_id: int,
    db: Session = Depends(get_db),
    current_user: auth_models.User = Depends(get_current_user)
):
    routine = db.query(WorkoutRoutine).filter(
        WorkoutRoutine.id == routine_id,
        WorkoutRoutine.user_id == current_user.id
    ).first()

    if not routine:
        raise HTTPException(status_code=404, detail="루틴을 찾을 수 없습니다.")
    return routine

@router.delete("/{routine_id}")
def delete_routine(
    routine_id: int,
    db: Session = Depends(get_db),
    current_user: auth_models.User = Depends(get_current_user)
):
    routine = db.query(WorkoutRoutine).filter(
        WorkoutRoutine.id == routine_id,
        WorkoutRoutine.user_id == current_user.id
    ).first()

    if not routine:
        raise HTTPException(status_code=404, detail="루틴을 찾을 수 없습니다.")

    db.delete(routine)
    db.commit()
    return {"message": "루틴이 삭제되었습니다."}

@router.put("/{routine_id}", response_model=RoutineResponse)
def update_routine(
    routine_id: int,
    routine_data: WorkoutRoutineUpdate,      # ← 업데이트 스키마 사용
    db: Session = Depends(get_db),
    current_user: auth_models.User = Depends(get_current_user)
):
    # 1) 소유권 확인 및 조회
    routine = db.query(WorkoutRoutine).filter(
        WorkoutRoutine.id == routine_id,
        WorkoutRoutine.user_id == current_user.id
    ).first()
    if not routine:
        raise HTTPException(status_code=404, detail="루틴을 찾을 수 없습니다.")

    # 2) 제목 변경
    routine.title = routine_data.title

    # 3) 기존 아이템 전부 삭제 (cascade delete도 설정되어 있지만, 직접 삭제로 안전하게 처리)
    db.query(WorkoutItem).filter(WorkoutItem.routine_id == routine.id).delete()

    # 4) 새로운 아이템 삽입
    for item in routine_data.items:
        db.add(WorkoutItem(
            name=item.name,
            count=item.count,
            routine_id=routine.id
        ))

    # 5) 커밋 & 반환
    db.commit()
    db.refresh(routine)
    return routine
