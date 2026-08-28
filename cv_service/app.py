from fastapi import FastAPI
from fastapi.responses import JSONResponse
from processing import run_video_analysis
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session


from database.db import get_db
from database.models import User
from orchestrator.auth import hash_password


router = APIRouter(prefix="/users", tags=["Users"])


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str = "hr"


class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    role: str | None = None


def user_response(user: User):
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "created_at": user.created_at,
        "updated_at": user.updated_at,
    }


@app.post("/analyze-video")
async def analyze_video(request: VideoRequest):
    """
    Run OpenCV + MediaPipe video analysis.
    """
    # Reject empty or whitespace-only session_id
    if not request.session_id.strip():
        return JSONResponse(
            status_code=422,
            content={
                "session_id": request.session_id,
                "status": "error",
                "error_message": "session_id must not be empty",
            },
        )

    try:
        result = run_video_analysis(request.session_id)
    except Exception as exc:
        return JSONResponse(
            status_code=500,
            content={
                "session_id": request.session_id,
                "status": "error",
                "error_message": f"Video analysis failed: {exc}",
            },
        )

    result["status"] = "ok"
    return result


@router.get("")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).order_by(User.id).all()
    return [user_response(user) for user in users]


@router.get("/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user_response(user)


@router.post("", status_code=201)
def create_user(request: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == request.email).first()

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="User with this email already exists",
        )

    user = User(
        name=request.name,
        email=request.email,
        password_hash=hash_password(request.password),
        role=request.role,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user_response(user)


@router.put("/{user_id}")
def update_user(
    user_id: int,
    request: UserUpdate,
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if request.email is not None:
        existing_user = (
            db.query(User)
            .filter(User.email == request.email, User.id != user_id)
            .first()
        )

        if existing_user:
            raise HTTPException(
                status_code=409,
                detail="Email already belongs to another user",
            )

        user.email = request.email

    if request.name is not None:
        user.name = request.name

    if request.role is not None:
        user.role = request.role

    if request.password:
        user.password_hash = hash_password(request.password)

    db.commit()
    db.refresh(user)

    return user_response(user)


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()

    return {
        "message": "User deleted successfully",
        "id": user_id,
    }
