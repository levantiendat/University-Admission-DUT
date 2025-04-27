from fastapi import FastAPI
from app.api import auth, users, school_priority, qna, university_admission, university_education, admitted_student, visitors
from app.models.user import Base, User
from app.models.visitor import VisitorCount, ActiveSession  # Thêm dòng này
from app.db.session import engine, SessionLocal
from app.core.security import get_password_hash
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
import os

app = FastAPI(
    title="FastAPI Backend University admission application",
    description="Application to support admissions consulting for candidates applying to universities",
    version="1.0.0"
)

allowed_origins = os.getenv("ALLOWED_ORIGINS", "").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SessionMiddleware, secret_key="a7c8ad017c96e24e27523c40173e677181ed7a8094defdfb65493261ddd8e2c9")
# Tạo bảng nếu chưa có
Base.metadata.create_all(bind=engine)

# Hàm tạo admin user nếu chưa tồn tại
def create_admin_user():
    db = SessionLocal()
    try:
        admin = db.query(User).filter(User.email == "admin@gmail.com").first()
        if not admin:
            admin = User(
                username="admin",
                email="admin@gmail.com",
                role="admin",
                hashed_password=get_password_hash("admin123"),
                phone_number="0000000000"
            )
            db.add(admin)
            db.commit()
            db.refresh(admin)
            print("Đã tạo tài khoản admin: admin@gmail.com / admin123")
        else:
            print("Tài khoản admin đã tồn tại")
    finally:
        db.close()

# Chạy hàm tạo admin khi khởi động ứng dụng
@app.on_event("startup")
def startup_event():
    create_admin_user()

# Include các router
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(school_priority.router, prefix="/api/priorities", tags=["School Priority"])
app.include_router(qna.router, prefix="/api/qna", tags=["Question & Answer"])
app.include_router(university_admission.router, prefix="/api/university-admissions", tags=["University Admission"])
app.include_router(university_education.router, prefix="/api/university-educations", tags=["University Education"])
app.include_router(admitted_student.router, prefix="/api/admitted_students", tags=["Admitted Student"])
app.include_router(visitors.router, prefix="/api/visitors", tags=["Visitors"])  # Thêm dòng này

@app.get("/")
def root():
    return {"msg": "FastAPI Backend University admission application, Swagger UI at /docs"}