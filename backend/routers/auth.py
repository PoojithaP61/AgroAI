from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta
from typing import Optional

from backend.database import get_db
from backend.models import User, VerificationCode
from backend.auth_utils import (
    verify_password,
    get_password_hash,
    create_access_token,
    get_current_active_user,
    generate_verification_code
)
from backend.config import settings
from backend.notification_service import NotificationService

router = APIRouter(prefix="/auth", tags=["Authentication"])


class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str
    full_name: Optional[str] = None
    phone: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    full_name: Optional[str] = None
    phone: Optional[str] = None
    is_admin: bool
    is_active: bool
    is_verified: bool

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse


class VerifyAccountRequest(BaseModel):
    email: EmailStr
    code: str


class ForgotPasswordRequest(BaseModel):
    email: Optional[EmailStr] = None
    phone: Optional[str] = None


class ResetPasswordRequest(BaseModel):
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    code: str
    new_password: str


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """Register a new user and send verification code"""
    
    # Check if user already exists
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    if db.query(User).filter(User.username == user_data.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    try:
        # Create new user
        hashed_password = get_password_hash(user_data.password)
        db_user = User(
            email=user_data.email,
            username=user_data.username,
            hashed_password=hashed_password,
            full_name=user_data.full_name,
            phone=user_data.phone,
            is_verified=False  # User must verify
        )
        
        db.add(db_user)
        # Flush to get the ID but don't commit yet
        db.flush() 
        
        # Generate verification code
        code = generate_verification_code()
        expires_at = datetime.utcnow() + timedelta(minutes=10)
        
        verification_entry = VerificationCode(
            user_id=db_user.id,
            code=code,
            type="EMAIL_VERIFICATION",
            via="EMAIL",
            expires_at=expires_at
        )
        db.add(verification_entry)
        
        # Commit everything at once
        db.commit()
        db.refresh(db_user)
        
        # Send email in background
        background_tasks.add_task(
            NotificationService.send_verification_code, 
            user_data.email, 
            code, 
            "EMAIL"
        )
        
        return db_user
        
    except Exception as e:
        db.rollback()
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )


@router.post("/verify")
def verify_account(request: VerifyAccountRequest, db: Session = Depends(get_db)):
    """Verify user account with code"""
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.is_verified:
        return {"message": "Account already verified"}
    
    # Find valid code
    verification = db.query(VerificationCode).filter(
        VerificationCode.user_id == user.id,
        VerificationCode.code == request.code,
        VerificationCode.type == "EMAIL_VERIFICATION",
        VerificationCode.is_used == False,
        VerificationCode.expires_at > datetime.utcnow()
    ).first()
    
    if not verification:
        raise HTTPException(status_code=400, detail="Invalid or expired verification code")
    
    # Mark as verified
    user.is_verified = True
    verification.is_used = True
    db.commit()
    
    return {"message": "Account verified successfully"}


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Login and get access token"""
    
    # Find user by username or email
    user = db.query(User).filter(
        (User.username == form_data.username) | (User.email == form_data.username)
    ).first()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
        
    if not user.is_verified:
        raise HTTPException(status_code=400, detail="Account not verified. Please verify your email.")
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }


@router.post("/forgot-password")
def forgot_password(request: ForgotPasswordRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """Request password reset code (Email only)"""
    user = None
    
    if request.email:
        user = db.query(User).filter(User.email == request.email).first()
    
    # Check if user exists but don't reveal it if not
    if not user:
        return {"message": "If an account exists, a code has been sent."}
    
    # Generate code
    code = generate_verification_code()
    expires_at = datetime.utcnow() + timedelta(minutes=10)
    
    verification_entry = VerificationCode(
        user_id=user.id,
        code=code,
        type="PASSWORD_RESET",
        via="EMAIL",
        expires_at=expires_at
    )
    db.add(verification_entry)
    db.commit()
    
    # Send notification
    background_tasks.add_task(
        NotificationService.send_verification_code,
        user.email,
        code,
        "EMAIL"
    )
    
    return {"message": "If an account exists, a code has been sent."}


@router.post("/reset-password")
def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    """Reset password using verification code"""
    user = None
    
    if request.email:
        user = db.query(User).filter(User.email == request.email).first()
    elif request.phone:
        user = db.query(User).filter(User.phone == request.phone).first()
        
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    # Verify code
    verification = db.query(VerificationCode).filter(
        VerificationCode.user_id == user.id,
        VerificationCode.code == request.code,
        VerificationCode.type == "PASSWORD_RESET",
        VerificationCode.is_used == False,
        VerificationCode.expires_at > datetime.utcnow()
    ).first()
    
    if not verification:
        raise HTTPException(status_code=400, detail="Invalid or expired verification code")
        
    # Update password
    user.hashed_password = get_password_hash(request.new_password)
    verification.is_used = True
    db.commit()
    
    return {"message": "Password reset successfully"}


@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_active_user)):
    """Get current user information"""
    return current_user
