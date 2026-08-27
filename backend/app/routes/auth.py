from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
import json
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.notification import Notification
from app.auth import (
    get_password_hash, verify_password, create_access_token, create_refresh_token,
    get_current_user, get_optional_user, set_auth_cookies, clear_auth_cookies,
    resolve_user, _decode_token,
)
from app.schemas.user import UserCreate, UserLogin, UserResponse, UserUpdate
from app.config import settings

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register")
def register(data: UserCreate, db: Session = Depends(get_db)):
    email = data.email.strip().lower()
    existing = db.query(User).filter((User.email == email) | (User.username == data.username)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email or username already registered")
    user = User(
        email=email,
        username=data.username,
        hashed_password=get_password_hash(data.password),
        full_name=data.full_name or data.username,
    )
    db.add(user)
    db.flush()
    db.add(Notification(
        user_id=user.id, type="info", title="Welcome to CareerPath AI!",
        body="Pick a target career to generate your personalized skill roadmap.",
        link="/careers",
    ))
    db.commit()
    db.refresh(user)

    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token(str(user.id))
    body = {
        **UserResponse.model_validate(user).model_dump(mode="json"),
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": refresh_token,
    }
    body = {
        **UserResponse.model_validate(user).model_dump(mode="json"),
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": refresh_token,
    }
    response = Response(
        status_code=200,
        content=json.dumps(body),
        media_type="application/json",
    )
    set_auth_cookies(response, access_token, refresh_token)
    return response


@router.post("/login")
def login(data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email.strip().lower()).first()
    if not user or not verify_password(data.password, user.hashed_password):
        # Uniform message avoids account enumeration
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token(str(user.id))

    response = Response(
        status_code=200,
        content=UserResponse.model_validate(user).model_dump_json(),
        media_type="application/json",
    )
    # Access cookie always short-lived. The refresh cookie persists only when
    # the user opts in via "Remember me" (otherwise it is a session cookie).
    response.set_cookie(
        settings.ACCESS_COOKIE, access_token,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        path="/", secure=settings.COOKIE_SECURE, httponly=True, samesite="lax",
    )
    if data.remember:
        response.set_cookie(
            settings.REFRESH_COOKIE, refresh_token,
            max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 86400,
            path="/", secure=settings.COOKIE_SECURE, httponly=True, samesite="lax",
        )
    else:
        # Session cookie: expires when the browser closes — no max_age set.
        response.set_cookie(
            settings.REFRESH_COOKIE, refresh_token,
            path="/", secure=settings.COOKIE_SECURE, httponly=True, samesite="lax",
        )
    return response


@router.post("/refresh")
def refresh(request: Request, db: Session = Depends(get_db)):
    """Mint a fresh access token from a valid refresh token. Returns the user
    object so the client can rehydrate session state without a second call."""
    refresh_token = request.cookies.get(settings.REFRESH_COOKIE)
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No refresh token")
    payload = _decode_token(refresh_token, expected_type="refresh")
    user = resolve_user(db, payload.get("sub"))
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    access_token = create_access_token({"sub": str(user.id)})
    response = Response(
        status_code=200,
        content=UserResponse.model_validate(user).model_dump_json(),
        media_type="application/json",
    )
    response.set_cookie(
        settings.ACCESS_COOKIE, access_token,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        path="/", secure=settings.COOKIE_SECURE, httponly=True, samesite="lax",
    )
    return response


@router.post("/logout")
def logout(response: Response):
    """Clear both auth cookies. Idempotent — safe to call when already logged out."""
    clear_auth_cookies(response)
    return {"ok": True}


@router.get("/me", response_model=UserResponse)
def get_me(user: User = Depends(get_current_user)):
    return UserResponse.model_validate(user)


@router.put("/me", response_model=UserResponse)
def update_me(data: UserUpdate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    from app.models.career import CareerPath
    if data.full_name is not None:
        user.full_name = data.full_name[:120]
    if data.avatar_url is not None:
        if data.avatar_url and not data.avatar_url.startswith(("http://", "https://")):
            raise HTTPException(status_code=400, detail="avatar_url must be an http(s) URL")
        user.avatar_url = data.avatar_url[:500]
    if data.selected_career_id is not None:
        career = db.query(CareerPath).filter(CareerPath.id == data.selected_career_id).first()
        if not career:
            raise HTTPException(status_code=404, detail="Career path not found")
        changed = user.selected_career_id != career.id
        user.selected_career_id = career.id
        user.onboarding_completed = True
        if changed:
            db.add(Notification(
                user_id=user.id, type="roadmap_update",
                title=f"Roadmap generated: {career.title}",
                body="Your personalized skill DAG is ready. Open the Roadmap tab to start learning.",
                link="/roadmap",
            ))
    if data.onboarding_completed is not None:
        user.onboarding_completed = data.onboarding_completed
    db.commit()
    db.refresh(user)
    return UserResponse.model_validate(user)
