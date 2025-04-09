from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, Token, UserOut, UserBase, UserUpdate
from app.services.user_service import create_user, update_user
from app.db.session import get_db
from app.core.security import verify_access_token, create_access_token
from fastapi.security import OAuth2PasswordBearer
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
router = APIRouter()

# Dependency để lấy current user từ token
@router.post("/me", response_model=UserOut)
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    email = verify_access_token(token, credentials_exception)
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise credentials_exception
    return user

@router.post("/admin/create-user", response_model=Token)
def admin_create_user(
    user: UserCreate,
    role: str = Header(..., description="Header role, ví dụ: user hoặc instructor"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Kiểm tra quyền admin
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Giới hạn role chỉ được là 'user' hoặc 'instructor'
    if role not in ["user", "instructor"]:
        raise HTTPException(
            status_code=400,
            detail="Role must be either 'user' or 'instructor'"
        )
    
    user_obj = create_user(db, user, role)
    token = create_access_token(data={"sub": user_obj.email})
    return {"access_token": token, "token_type": "bearer", "role": user_obj.role}

@router.put("/update", response_model=UserOut)
def update_user_data(
    user_update: UserUpdate,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    email = verify_access_token(token, credentials_exception)
    user = db.query(User).filter(User.email == email).first()
    
    if not user:
        raise credentials_exception
    user = update_user(db, user, user_update.dict(exclude_unset=True))
    
    return user

@router.put("/admin/update-user/{user_id}", response_model=UserOut)
def admin_update_user_data(
    user_id: int,
    user_update: UserUpdate,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    email = verify_access_token(token, credentials_exception)
    current_user = db.query(User).filter(User.email == email).first()
    
    if not current_user or current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user = update_user(db, user, user_update.dict(exclude_unset=True))
    
    return user

@router.put("/admin/update-user-by-email", response_model=UserOut)
def admin_update_user_by_email(
    email: str,
    user_update: UserUpdate,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    email = verify_access_token(token, credentials_exception)
    current_user = db.query(User).filter(User.email == email).first()
    
    if not current_user or current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    user = db.query(User).filter(User.email == email).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user = update_user(db, user, user_update.dict(exclude_unset=True))
    
    return user

@router.put("/admin/update-user-role/{user_id}", response_model=UserOut)
def admin_update_user_role(
    user_id: int,
    role: str = Header(..., description="Header role, ví dụ: user hoặc instructor"),
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    email = verify_access_token(token, credentials_exception)
    current_user = db.query(User).filter(User.email == email).first()
    
    if not current_user or current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    if role not in ["user", "instructor"]:
        raise HTTPException(
            status_code=400,
            detail="Role must be either 'user' or 'instructor'"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.role = role
    db.commit()
    
    return user

@router.get("/admin/get-users", response_model=list[UserOut])
def admin_get_users(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    email = verify_access_token(token, credentials_exception)
    current_user = db.query(User).filter(User.email == email).first()
    
    if not current_user or current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    users = db.query(User).all()
    
    return users

@router.get("/admin/get-user/{user_id}", response_model=UserOut)
def admin_get_user(
    user_id: int,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    email = verify_access_token(token, credentials_exception)
    current_user = db.query(User).filter(User.email == email).first()
    
    if not current_user or current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

@router.delete("/admin/delete-user/{user_id}")
def admin_delete_user(
    user_id: int,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    email = verify_access_token(token, credentials_exception)
    current_user = db.query(User).filter(User.email == email).first()
    
    if not current_user or current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()
    
    return {"msg": "User deleted successfully"}

@router.get("admin/search-user", response_model=list[UserOut])
def admin_search_user(
    query_input: str = None,
    role: str = None,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    email = verify_access_token(token, credentials_exception)
    current_user = db.query(User).filter(User.email == email).first()
    
    if not current_user or current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    query = db.query(User)
    
    if query_input:
        query = query.filter(
            (User.name.ilike(f"%{query_input}%")) |
            (User.email.ilike(f"%{query_input}%")) |
            (User.phone_number.ilike(f"%{query_input}%"))
        )
    
    if role:
        query = query.filter(User.role == role)
    
    users = query.all()
    
    return users

