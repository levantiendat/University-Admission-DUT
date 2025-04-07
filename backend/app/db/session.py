import urllib.parse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Encode password nếu chứa ký tự đặc biệt
password = urllib.parse.quote_plus(settings.DB_PASSWORD)

# Tạo connection string
connection_str = (
    f"mysql+mysqlconnector://{settings.DB_USERNAME}:{password}"
    f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_DATABASE}"
)

# SSL CA nếu được chỉ định
connect_args = {}
if settings.DB_SSL_CA:
    connect_args["ssl_ca"] = settings.DB_SSL_CA

# Tạo engine và session
engine = create_engine(connection_str, pool_pre_ping=True, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency dùng trong FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
