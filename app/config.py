import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    # Application settings
    APP_NAME: str = os.getenv("APP_NAME", "FastAPI Database App")
    APP_VERSION: str = os.getenv("APP_VERSION", "0.1.0")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() in ("true", "1", "t")

    # Database settings
    DB_TYPE: str = os.getenv("DB_TYPE", "oracle").lower()  # oracle or postgresql
    DB_USER: str = os.getenv("DB_USER", "")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: str = os.getenv("DB_PORT", "1521")  # Default for Oracle
    DB_NAME: str = os.getenv(
        "DB_NAME", ""
    )  # Service name for Oracle, database name for PostgreSQL
    DB_SCHEMA: str = os.getenv("DB_SCHEMA", "")

    # Database URL
    @property
    def DATABASE_URL(self) -> str:
        if self.DB_TYPE == "postgresql":
            # Format: postgresql://user:password@host:port/dbname
            return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        else:
            # Format for oracledb driver: oracle+oracledb://user:password@host:port/?service_name=service
            return f"oracle+oracledb://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/?service_name={self.DB_NAME}"


# Create settings instance
settings = Settings()
