from environs import Env

env = Env()
env.read_env()

SECRET_KEY = env.str("SECRET_KEY", "your_secret_key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_SECONDS = 3600  # 1 hour
DATABASE_URL = env.str("DATABASE_URL", "sqlite:///./test.db")
ZYMBIT_CONNECNTED = env.bool("ZYMBIT_CONNECNTED", False)
CORS_ALLOWED_ORIGINS = env.list(
    "CORS_ALLOWED_ORIGINS",
    [
        "http://localhost:3000",
        "https://your-production-domain.com",
    ],
)
CORS_ALLOWED_REGEX_ORIGINS = env.str("CORS_ALLOWED_REGEX_ORIGINS", "")
CORS_USE_REGEX = env.bool("CORS_USE_REGEX", False)