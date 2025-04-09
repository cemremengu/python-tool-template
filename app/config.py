import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    # Application settings
    APP_NAME: str = os.getenv("APP_NAME", "FastAPI Database App")
    APP_VERSION: str = os.getenv("APP_VERSION", "0.1.0")
    
    # Server settings
    SERVER_URL: str = os.getenv("SERVER_URL", "http://localhost:8000")
    SERVER_DESCRIPTION: str = os.getenv("SERVER_DESCRIPTION", "Local Development")

    # Database settings
    DB_USER: str = os.getenv("DB_USER", "")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: str = os.getenv("DB_PORT", "5432")  # Default for PostgreSQL
    DB_NAME: str = os.getenv("DB_NAME", "")  # Database name for PostgreSQL
    DB_SCHEMA: str = os.getenv("DB_SCHEMA", "")

    # Database URL
    @property
    def DATABASE_URL(self) -> str:
        # Format: postgresql://user:password@host:port/dbname
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


# Create settings instance
settings = Settings()
