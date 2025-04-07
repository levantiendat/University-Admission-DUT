from pydantic import BaseSettings
import mysql.connector

class Settings(BaseSettings):
    # Cấu hình bảo mật
    SECRET_KEY: str = "your-secret-key"  # Thay đổi theo key thực tế của bạn
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Cấu hình cơ sở dữ liệu
    DB_HOST: str
    DB_PORT: int = 3306
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_DATABASE: str
    DB_SSL_CA: str = None  # Nếu không dùng SSL, có thể để None
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str

    class Config:
        env_file = ".env"  # Đọc biến môi trường từ file .env

settings = Settings()

# Kết nối tới MySQL (nếu cần)
try:
    cnx = mysql.connector.connect(
        user=settings.DB_USERNAME,
        password=settings.DB_PASSWORD,
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        database=settings.DB_DATABASE,
        ssl_ca=settings.DB_SSL_CA,
        ssl_disabled=False  # Kích hoạt SSL nếu có thiết lập ssl_ca
    )
    print("Kết nối thành công!")
except Exception as e:
    print("Kết nối thất bại:", e)
