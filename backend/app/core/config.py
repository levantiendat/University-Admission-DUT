from pydantic_settings import BaseSettings
import mysql.connector
from mysql.connector import errorcode

class Settings(BaseSettings):
    # Cấu hình bảo mật
    SECRET_KEY: str = "your-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Cấu hình cơ sở dữ liệu
    DB_HOST: str
    DB_PORT: int = 3306
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_DATABASE: str
    DB_SSL_CA: str | None = None  # Hỗ trợ cả None
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    FRONTEND_URL: str = "http://localhost:8080"  # URL của frontend ứng dụng

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()

# Kết nối tới MySQL
try:
    connection_args = {
        "user": settings.DB_USERNAME,
        "password": settings.DB_PASSWORD,
        "host": settings.DB_HOST,
        "port": settings.DB_PORT,
        "database": settings.DB_DATABASE,
    }

    if settings.DB_SSL_CA:
        connection_args["ssl_ca"] = settings.DB_SSL_CA
        connection_args["ssl_disabled"] = False
    else:
        connection_args["ssl_disabled"] = True

    cnx = mysql.connector.connect(**connection_args)
    print("✅ Kết nối MySQL thành công!")

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("❌ Sai tên người dùng hoặc mật khẩu.")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("❌ Không tìm thấy cơ sở dữ liệu.")
    else:
        print("❌ Kết nối thất bại:", err)
