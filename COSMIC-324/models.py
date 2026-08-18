"""
COSMIC-324: Sovereign Database Models
نماذج هياكل البيانات المؤسسية لقاعدة البيانات السيادية
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class LicenseRecord(Base):
    """جدول لتخزين وتتبع التراخيص السيادية النشطة في النظام."""
    __tablename__ = "license_records"

    id = Column(Integer, primary_key=True, index=True)
    client_name = Column(String(255), nullable=False)
    license_key = Column(Text, unique=True, nullable=False)
    issued_date = Column(DateTime, default=datetime.utcnow)
    expiry_date = Column(DateTime, nullable=False)
    max_users = Column(Integer, default=5)
    max_cores = Column(Integer, default=4)
    status = Column(String(50), default="ACTIVE")

class OrbitalAuditLog(Base):
    """جدول لسجلات التدقيق والعمليات الحسابية المدارية لضمان الامتثال والمعايير."""
    __tablename__ = "orbital_audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    user_identifier = Column(String(255), nullable=True)
    operation_type = Column(String(100), nullable=False)  # مثال: J2_PERTURBATION, FSPL_CALC
    input_parameters = Column(Text, nullable=True)
    result_value = Column(Float, nullable=True)
    status = Column(String(50), default="SUCCESS")
