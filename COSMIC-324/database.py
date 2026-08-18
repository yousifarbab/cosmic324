"""
COSMIC-324: Sovereign Database Connectivity Module
وحدة الاتصال بقاعدة البيانات السيادية - تدعم الأمان والربط المؤسسي
"""

import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

# إعداد رابط قاعدة البيانات (يُفضل استخدامه كمتغير بيئة في الإنتاج)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:secure_password_csm324@db:5432/cosmic_sovereign")

# إنشاء محرك الاتصال (Engine)
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@contextmanager
def get_db():
    """
    إدارة الجلسات (Sessions) لضمان إغلاق الاتصال بعد كل عملية 
    للحفاظ على استقرار النظام (Context Manager).
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def initialize_database():
    """
    التحقق من اتصال قاعدة البيانات عند تشغيل التطبيق.
    """
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return True
    except Exception as e:
        print(f"خطأ في الاتصال بقاعدة البيانات: {e}")
        return False
