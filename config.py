import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask - Required in production
    SECRET_KEY = os.getenv('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY environment variable is required!")
    
    # MongoDB - Required
    MONGO_URI = os.getenv('MONGO_URI')
    if not MONGO_URI:
        raise ValueError("MONGO_URI environment variable is required!")
    
    # JWT - Required in production
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    if not JWT_SECRET_KEY:
        raise ValueError("JWT_SECRET_KEY environment variable is required!")
    
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
    # Model paths - Required
    MODEL_PATH = os.getenv('MODEL_PATH')
    if not MODEL_PATH:
        raise ValueError("MODEL_PATH environment variable is required!")
    
    MODEL_COLUMNS_PATH = os.getenv('MODEL_COLUMNS_PATH')
    if not MODEL_COLUMNS_PATH:
        raise ValueError("MODEL_COLUMNS_PATH environment variable is required!")
    
    DIABETES_MODEL_PATH = os.getenv('DIABETES_MODEL_PATH')
    if not DIABETES_MODEL_PATH:
        raise ValueError("DIABETES_MODEL_PATH environment variable is required!")
    
    DIABETES_SCALER_PATH = os.getenv('DIABETES_SCALER_PATH')
    if not DIABETES_SCALER_PATH:
        raise ValueError("DIABETES_SCALER_PATH environment variable is required!")
    
    DIABETES_COLUMNS_PATH = os.getenv('DIABETES_COLUMNS_PATH')
    if not DIABETES_COLUMNS_PATH:
        raise ValueError("DIABETES_COLUMNS_PATH environment variable is required!")

