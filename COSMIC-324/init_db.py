"""
COSMIC-324: Database Initialization Script
سكربت إنشاء وتفعيل الجداول في قاعدة بيانات PostgreSQL السيادية
"""

from database import engine
from models import Base

def init_db():
    print("جاري إنشاء الجداول في قاعدة البيانات السيادية...")
    # إنشاء كافة الجداول المعرفة في النماذج (Models) داخل قاعدة البيانات
    Base.metadata.create_all(bind=engine)
    print("تم إنشاء الجداول بنجاح وأصبح النظام جاهزاً للتشغيل المؤسسي!")

if __name__ == "__main__":
    init_db()
