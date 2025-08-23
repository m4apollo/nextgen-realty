import os
from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, RedisDsn

class Settings(BaseSettings):
    # Database
    DATABASE_URL: PostgresDsn = "postgresql://user:pass@localhost:5432/nextgen"
    REDIS_URL: RedisDsn = "redis://localhost:6379/0"
    
    # Authentication
    SECRET_KEY: str = "your-secret-key-here"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours
    
    # Payment Processing
    STRIPE_SECRET_KEY: str
    STRIPE_PUBLIC_KEY: str
    STRIPE_WEBHOOK_SECRET: str
    STRIPE_SUCCESS_URL: str = "http://localhost:3000/billing/success"
    STRIPE_CANCEL_URL: str = "http://localhost:3000/billing"
    STRIPE_WEBHOOK_ENABLED: bool = True
    
    # Email
    SMTP_HOST: str = "smtp.example.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = "user@example.com"
    SMTP_PASS: str = "password"
    EMAIL_FROM: str = "noreply@nextgenrealty.com"
    
    # AI Configuration
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    DEFAULT_AI_MODEL: str = "mistral"
    
    # Frontend
    FRONTEND_URL: str = "http://localhost:3000"
    
    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    class Config:
        env_file = Path(__file__).parent / '.env'
        env_file_encoding = 'utf-8'
        extra = "ignore"

settings = Settings()