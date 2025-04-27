from fastapi import APIRouter, Depends, HTTPException, status, Body, Request
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi.responses import RedirectResponse, JSONResponse
from app.schemas.user import UserCreate, UserLogin, Token
from app.services.auth_service import register_user, login_user, reset_password, check_email_exists, register_user_with_google
from app.db.session import get_db
from app.models.user import User
from app.core.security import verify_access_token, get_password_hash
from app.core.security import create_access_token
from authlib.integrations.starlette_client import OAuth, OAuthError
from app.core.config import settings
from urllib.parse import urlparse

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

@router.post("/register", response_model=Token)
def register(user: UserCreate, db: Session = Depends(get_db)):
    user_obj = register_user(db, user)
    token = create_access_token(data={"sub": user_obj.email})
    return {"access_token": token, "token_type": "bearer", "role": user_obj.role}

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user_in = UserLogin(email=form_data.username, password=form_data.password)
    return login_user(db, user_in)

# Reset mật khẩu
@router.post("/reset-password")
def reset_password_endpoint(
    old_password: str = Body(...), 
    new_password: str = Body(...),
    token: str = Depends(oauth2_scheme),  # 🔥 Token lấy từ header
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Verify token → get email
    email = verify_access_token(token, credentials_exception)
    
    # Get user
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise credentials_exception
    
    # Check old password
    if not user.check_password(old_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Old password is incorrect")
    
    # Update new password
    user.password = get_password_hash(new_password)
    db.commit()
    
    return {"msg": "Password updated successfully"}


oauth = OAuth()
oauth.register(
    name="google",
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    access_token_url="https://oauth2.googleapis.com/token",
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    api_base_url="https://www.googleapis.com/oauth2/v2/",
    client_kwargs={"scope": "openid email profile"},
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
)

# Endpoint chuyển hướng người dùng đến trang đăng nhập Google


@router.get("/google")
async def google_auth(request: Request):
    redirect_uri = request.url_for("google_callback")

    parsed_url = urlparse(str(request.base_url))
    if parsed_url.hostname != "localhost":
        # Chuyển redirect_uri sang HTTPS nếu không phải localhost
        redirect_uri = str(redirect_uri).replace("http://", "https://")

    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/google/callback")
async def google_callback(request: Request, db: Session = Depends(get_db)):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as error:
        return JSONResponse({"error": str(error)}, status_code=400)

    # Lấy thông tin người dùng từ Google
    user_info_response = await oauth.google.get('userinfo', token=token)
    user_data = user_info_response.json()
    user_email = user_data.get("email")

    if not user_email:
        return JSONResponse({"error": "Email không khả dụng trong thông tin Google"}, status_code=400)

    # Đăng ký tài khoản nếu chưa có
    name = user_data.get("name", "")
    account = register_user_with_google(db, email=user_email, name=name)

    # Tạo JWT token
    access_token = create_access_token(data={"sub": user_email})

    # Xác định URL frontend cần redirect
    parsed_url = urlparse(str(request.base_url))
    if parsed_url.hostname == "localhost":
        frontend_url = "http://localhost:8080"  # URL frontend khi chạy local
    else:
        frontend_url = "https://tuvantuyensinh-levantiendat-dut.vercel.app"  # URL frontend production

    # Redirect về frontend callback kèm token
    return RedirectResponse(url=f"{frontend_url}/callback?token={access_token}")