"""
COSMIC-324: 6G Titan X Global Edition
منصة المحاكاة الفضائية والسيادية المتكاملة
الإصدار: v7.6 - Production Ready
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import math
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from types import SimpleNamespace
import json
from pathlib import Path
import os
import logging
import traceback
import hashlib
import hmac
import secrets
import sqlite3
from concurrent.futures import ThreadPoolExecutor

# ============================================================
# 📝 إعداد نظام التسجيل (Logging)
# ============================================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================================
# 🌍 محاولة استيراد pycountry مع بديل متكامل
# ============================================================
class PyCountryFallback:
    """بديل متكامل لـ pycountry مع قائمة شاملة للدول"""
    
    class countries:
        _data = [
            # أفريقيا
            {"name": "Algeria", "alpha_2": "DZ"},
            {"name": "Angola", "alpha_2": "AO"},
            {"name": "Benin", "alpha_2": "BJ"},
            {"name": "Botswana", "alpha_2": "BW"},
            {"name": "Burkina Faso", "alpha_2": "BF"},
            {"name": "Burundi", "alpha_2": "BI"},
            {"name": "Cabo Verde", "alpha_2": "CV"},
            {"name": "Cameroon", "alpha_2": "CM"},
            {"name": "Central African Republic", "alpha_2": "CF"},
            {"name": "Chad", "alpha_2": "TD"},
            {"name": "Comoros", "alpha_2": "KM"},
            {"name": "Congo", "alpha_2": "CG"},
            {"name": "Congo (DRC)", "alpha_2": "CD"},
            {"name": "Djibouti", "alpha_2": "DJ"},
            {"name": "Egypt", "alpha_2": "EG"},
            {"name": "Equatorial Guinea", "alpha_2": "GQ"},
            {"name": "Eritrea", "alpha_2": "ER"},
            {"name": "Eswatini", "alpha_2": "SZ"},
            {"name": "Ethiopia", "alpha_2": "ET"},
            {"name": "Gabon", "alpha_2": "GA"},
            {"name": "Gambia", "alpha_2": "GM"},
            {"name": "Ghana", "alpha_2": "GH"},
            {"name": "Guinea", "alpha_2": "GN"},
            {"name": "Guinea-Bissau", "alpha_2": "GW"},
            {"name": "Ivory Coast", "alpha_2": "CI"},
            {"name": "Kenya", "alpha_2": "KE"},
            {"name": "Lesotho", "alpha_2": "LS"},
            {"name": "Liberia", "alpha_2": "LR"},
            {"name": "Libya", "alpha_2": "LY"},
            {"name": "Madagascar", "alpha_2": "MG"},
            {"name": "Malawi", "alpha_2": "MW"},
            {"name": "Mali", "alpha_2": "ML"},
            {"name": "Mauritania", "alpha_2": "MR"},
            {"name": "Mauritius", "alpha_2": "MU"},
            {"name": "Morocco", "alpha_2": "MA"},
            {"name": "Mozambique", "alpha_2": "MZ"},
            {"name": "Namibia", "alpha_2": "NA"},
            {"name": "Niger", "alpha_2": "NE"},
            {"name": "Nigeria", "alpha_2": "NG"},
            {"name": "Rwanda", "alpha_2": "RW"},
            {"name": "Sao Tome and Principe", "alpha_2": "ST"},
            {"name": "Senegal", "alpha_2": "SN"},
            {"name": "Seychelles", "alpha_2": "SC"},
            {"name": "Sierra Leone", "alpha_2": "SL"},
            {"name": "Somalia", "alpha_2": "SO"},
            {"name": "South Africa", "alpha_2": "ZA"},
            {"name": "South Sudan", "alpha_2": "SS"},
            {"name": "Sudan", "alpha_2": "SD"},
            {"name": "Tanzania", "alpha_2": "TZ"},
            {"name": "Togo", "alpha_2": "TG"},
            {"name": "Tunisia", "alpha_2": "TN"},
            {"name": "Uganda", "alpha_2": "UG"},
            {"name": "Zambia", "alpha_2": "ZM"},
            {"name": "Zimbabwe", "alpha_2": "ZW"},
            
            # آسيا
            {"name": "Afghanistan", "alpha_2": "AF"},
            {"name": "Armenia", "alpha_2": "AM"},
            {"name": "Azerbaijan", "alpha_2": "AZ"},
            {"name": "Bahrain", "alpha_2": "BH"},
            {"name": "Bangladesh", "alpha_2": "BD"},
            {"name": "Bhutan", "alpha_2": "BT"},
            {"name": "Brunei", "alpha_2": "BN"},
            {"name": "Cambodia", "alpha_2": "KH"},
            {"name": "China", "alpha_2": "CN"},
            {"name": "Cyprus", "alpha_2": "CY"},
            {"name": "Georgia", "alpha_2": "GE"},
            {"name": "India", "alpha_2": "IN"},
            {"name": "Indonesia", "alpha_2": "ID"},
            {"name": "Iran", "alpha_2": "IR"},
            {"name": "Iraq", "alpha_2": "IQ"},
            {"name": "Israel", "alpha_2": "IL"},
            {"name": "Japan", "alpha_2": "JP"},
            {"name": "Jordan", "alpha_2": "JO"},
            {"name": "Kazakhstan", "alpha_2": "KZ"},
            {"name": "Kuwait", "alpha_2": "KW"},
            {"name": "Kyrgyzstan", "alpha_2": "KG"},
            {"name": "Laos", "alpha_2": "LA"},
            {"name": "Lebanon", "alpha_2": "LB"},
            {"name": "Malaysia", "alpha_2": "MY"},
            {"name": "Maldives", "alpha_2": "MV"},
            {"name": "Mongolia", "alpha_2": "MN"},
            {"name": "Myanmar", "alpha_2": "MM"},
            {"name": "Nepal", "alpha_2": "NP"},
            {"name": "North Korea", "alpha_2": "KP"},
            {"name": "Oman", "alpha_2": "OM"},
            {"name": "Pakistan", "alpha_2": "PK"},
            {"name": "Palestine", "alpha_2": "PS"},
            {"name": "Philippines", "alpha_2": "PH"},
            {"name": "Qatar", "alpha_2": "QA"},
            {"name": "Russia", "alpha_2": "RU"},
            {"name": "Saudi Arabia", "alpha_2": "SA"},
            {"name": "Singapore", "alpha_2": "SG"},
            {"name": "South Korea", "alpha_2": "KR"},
            {"name": "Sri Lanka", "alpha_2": "LK"},
            {"name": "Syria", "alpha_2": "SY"},
            {"name": "Taiwan", "alpha_2": "TW"},
            {"name": "Tajikistan", "alpha_2": "TJ"},
            {"name": "Thailand", "alpha_2": "TH"},
            {"name": "Timor-Leste", "alpha_2": "TL"},
            {"name": "Turkey", "alpha_2": "TR"},
            {"name": "Turkmenistan", "alpha_2": "TM"},
            {"name": "United Arab Emirates", "alpha_2": "AE"},
            {"name": "Uzbekistan", "alpha_2": "UZ"},
            {"name": "Vietnam", "alpha_2": "VN"},
            {"name": "Yemen", "alpha_2": "YE"},
            
            # أوروبا
            {"name": "Albania", "alpha_2": "AL"},
            {"name": "Andorra", "alpha_2": "AD"},
            {"name": "Austria", "alpha_2": "AT"},
            {"name": "Belarus", "alpha_2": "BY"},
            {"name": "Belgium", "alpha_2": "BE"},
            {"name": "Bosnia and Herzegovina", "alpha_2": "BA"},
            {"name": "Bulgaria", "alpha_2": "BG"},
            {"name": "Croatia", "alpha_2": "HR"},
            {"name": "Czech Republic", "alpha_2": "CZ"},
            {"name": "Denmark", "alpha_2": "DK"},
            {"name": "Estonia", "alpha_2": "EE"},
            {"name": "Finland", "alpha_2": "FI"},
            {"name": "France", "alpha_2": "FR"},
            {"name": "Germany", "alpha_2": "DE"},
            {"name": "Greece", "alpha_2": "GR"},
            {"name": "Hungary", "alpha_2": "HU"},
            {"name": "Iceland", "alpha_2": "IS"},
            {"name": "Ireland", "alpha_2": "IE"},
            {"name": "Italy", "alpha_2": "IT"},
            {"name": "Latvia", "alpha_2": "LV"},
            {"name": "Liechtenstein", "alpha_2": "LI"},
            {"name": "Lithuania", "alpha_2": "LT"},
            {"name": "Luxembourg", "alpha_2": "LU"},
            {"name": "Malta", "alpha_2": "MT"},
            {"name": "Moldova", "alpha_2": "MD"},
            {"name": "Monaco", "alpha_2": "MC"},
            {"name": "Montenegro", "alpha_2": "ME"},
            {"name": "Netherlands", "alpha_2": "NL"},
            {"name": "North Macedonia", "alpha_2": "MK"},
            {"name": "Norway", "alpha_2": "NO"},
            {"name": "Poland", "alpha_2": "PL"},
            {"name": "Portugal", "alpha_2": "PT"},
            {"name": "Romania", "alpha_2": "RO"},
            {"name": "San Marino", "alpha_2": "SM"},
            {"name": "Serbia", "alpha_2": "RS"},
            {"name": "Slovakia", "alpha_2": "SK"},
            {"name": "Slovenia", "alpha_2": "SI"},
            {"name": "Spain", "alpha_2": "ES"},
            {"name": "Sweden", "alpha_2": "SE"},
            {"name": "Switzerland", "alpha_2": "CH"},
            {"name": "Ukraine", "alpha_2": "UA"},
            {"name": "United Kingdom", "alpha_2": "GB"},
            
            # أمريكا الشمالية
            {"name": "Antigua and Barbuda", "alpha_2": "AG"},
            {"name": "Bahamas", "alpha_2": "BS"},
            {"name": "Barbados", "alpha_2": "BB"},
            {"name": "Belize", "alpha_2": "BZ"},
            {"name": "Canada", "alpha_2": "CA"},
            {"name": "Costa Rica", "alpha_2": "CR"},
            {"name": "Cuba", "alpha_2": "CU"},
            {"name": "Dominica", "alpha_2": "DM"},
            {"name": "Dominican Republic", "alpha_2": "DO"},
            {"name": "El Salvador", "alpha_2": "SV"},
            {"name": "Grenada", "alpha_2": "GD"},
            {"name": "Guatemala", "alpha_2": "GT"},
            {"name": "Haiti", "alpha_2": "HT"},
            {"name": "Honduras", "alpha_2": "HN"},
            {"name": "Jamaica", "alpha_2": "JM"},
            {"name": "Mexico", "alpha_2": "MX"},
            {"name": "Nicaragua", "alpha_2": "NI"},
            {"name": "Panama", "alpha_2": "PA"},
            {"name": "United States", "alpha_2": "US"},
            
            # أمريكا الجنوبية
            {"name": "Argentina", "alpha_2": "AR"},
            {"name": "Bolivia", "alpha_2": "BO"},
            {"name": "Brazil", "alpha_2": "BR"},
            {"name": "Chile", "alpha_2": "CL"},
            {"name": "Colombia", "alpha_2": "CO"},
            {"name": "Ecuador", "alpha_2": "EC"},
            {"name": "Guyana", "alpha_2": "GY"},
            {"name": "Paraguay", "alpha_2": "PY"},
            {"name": "Peru", "alpha_2": "PE"},
            {"name": "Suriname", "alpha_2": "SR"},
            {"name": "Uruguay", "alpha_2": "UY"},
            {"name": "Venezuela", "alpha_2": "VE"},
            
            # أوقيانوسيا
            {"name": "Australia", "alpha_2": "AU"},
            {"name": "Fiji", "alpha_2": "FJ"},
            {"name": "Kiribati", "alpha_2": "KI"},
            {"name": "Marshall Islands", "alpha_2": "MH"},
            {"name": "Micronesia", "alpha_2": "FM"},
            {"name": "Nauru", "alpha_2": "NR"},
            {"name": "New Zealand", "alpha_2": "NZ"},
            {"name": "Palau", "alpha_2": "PW"},
            {"name": "Papua New Guinea", "alpha_2": "PG"},
            {"name": "Samoa", "alpha_2": "WS"},
            {"name": "Solomon Islands", "alpha_2": "SB"},
            {"name": "Tonga", "alpha_2": "TO"},
            {"name": "Tuvalu", "alpha_2": "TV"},
            {"name": "Vanuatu", "alpha_2": "VU"},
        ]
        
        @classmethod
        def __iter__(cls):
            return iter(cls._data)
        
        @classmethod
        def get(cls, **kwargs):
            for country in cls._data:
                match = True
                for key, value in kwargs.items():
                    if country.get(key) != value:
                        match = False
                        break
                if match:
                    return type('Country', (), country)
            return None

# محاولة استيراد pycountry
try:
    import pycountry
    USE_PYCOUNTRY = True
    logger.info("✅ تم تحميل pycountry بنجاح")
except ImportError:
    pycountry = PyCountryFallback
    USE_PYCOUNTRY = False
    logger.info("⚠️ استخدام البديل المحلي لـ pycountry (قائمة 150+ دولة)")

# ============================================================
# 🔐 إعداد المفتاح السري للتراخيص
# ============================================================
SECRET_KEY = os.environ.get('COSMIC_SECRET_KEY', 'default-secret-key-change-me-in-production')

# ============================================================
# 📁 تحميل بيانات العقد
# ============================================================
def load_contract_data() -> Dict:
    """تحميل بيانات العقد مع دعم مسارات متعددة"""
    possible_paths = [
        Path(__file__).with_name("cosmic324_data.json"),
        Path(os.getcwd()) / "data" / "cosmic324_data.json",
        Path(os.getcwd()) / "config" / "cosmic324_data.json",
        Path("/etc/cosmic324/config.json"),
    ]
    
    for path in possible_paths:
        if path.exists():
            try:
                with path.open("r", encoding="utf-8") as f:
                    data = json.load(f)
                    logger.info(f"✅ تم تحميل بيانات العقد من: {path}")
                    return data
            except Exception as e:
                logger.warning(f"⚠️ فشل تحميل {path}: {e}")
    
    logger.info("ℹ️ استخدام البيانات الاحتياطية (fallback)")
    return get_default_contract()

def get_default_contract() -> Dict:
    """بيانات احتياطية مدمجة"""
    return {
        "celestrak": {
            "groups": ["starlink", "active", "visual", "weather", "gps", "iridium", "oneweb"],
            "defaultGroup": "starlink",
            "cacheTtlSeconds": 3600
        },
        "model": {
            "earthRadiusKm": 6371.0,
            "earthMuKm3S2": 398600.4418,
            "j2": 0.00108263,
            "speedOfLightKmPerSecond": 299792.458,
            "lineOfSightAngularRadiusDeg": 45.0
        },
        "source": {
            "baseUrl": "https://celestrak.org/NORAD/elements/gp.php",
            "provider": "CelesTrak",
            "dataset": "GP"
        },
        "groundStations": [
            {
                "name": {"ar": "محطة الخرطوم السيادية", "en": "Khartoum Sovereign Station"},
                "latitudeDeg": 15.5007,
                "longitudeDeg": 32.5599
            },
            {
                "name": {"ar": "محطة لندن المدارية", "en": "London Orbital Station"},
                "latitudeDeg": 51.5074,
                "longitudeDeg": -0.1278
            }
        ]
    }

DATA_CONTRACT = load_contract_data()
CELESTRAK_CONFIG = DATA_CONTRACT["celestrak"]
MODEL_CONFIG = DATA_CONTRACT["model"]
SOURCE_CONFIG = DATA_CONTRACT["source"]

# ============================================================
# 🗄️ نظام إدارة التراخيص (SQLite)
# ============================================================
class LicenseManager:
    """مدير التراخيص مع تخزين دائم"""
    
    def __init__(self, db_path: str = "licenses.db"):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS licenses (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        license_key TEXT UNIQUE NOT NULL,
                        client_name TEXT NOT NULL,
                        tier TEXT NOT NULL,
                        expiry_date TEXT NOT NULL,
                        created_at TEXT NOT NULL,
                        is_active INTEGER DEFAULT 1,
                        payment_status TEXT DEFAULT 'pending',
                        payment_gateway TEXT DEFAULT 'none'
                    )
                """)
                conn.execute("CREATE INDEX IF NOT EXISTS idx_license_key ON licenses(license_key)")
                conn.execute("CREATE INDEX IF NOT EXISTS idx_expiry ON licenses(expiry_date)")
        except Exception as e:
            logger.error(f"❌ فشل تهيئة قاعدة البيانات: {e}")
    
    def generate_license(self, client_name: str, tier: str, validity_days: int = 365) -> Tuple[str, str]:
        """توليد مفتاح ترخيص جديد"""
        expiry_date = (datetime.utcnow() + timedelta(days=validity_days)).strftime('%Y-%m-%d')
        license_id = secrets.token_hex(16)
        data = f"{license_id}:{client_name}:{tier}:{expiry_date}"
        signature = hmac.new(
            SECRET_KEY.encode(),
            data.encode(),
            hashlib.sha256
        ).hexdigest()[:16]
        license_key = f"CSM324-{license_id[:8]}-{signature.upper()}"
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO licenses (license_key, client_name, tier, expiry_date, created_at)
                VALUES (?, ?, ?, ?, ?)
            """, (license_key, client_name, tier, expiry_date, datetime.utcnow().isoformat()))
        
        return license_key, expiry_date
    
    def get_active_licenses(self) -> List[Dict]:
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute("""
                    SELECT license_key, client_name, tier, expiry_date, created_at, payment_status
                    FROM licenses
                    WHERE is_active = 1 AND expiry_date >= date('now')
                    ORDER BY expiry_date ASC
                """)
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"❌ فشل جلب التراخيص: {e}")
            return []

license_manager = LicenseManager()

# ============================================================
# 🌍 نظام الترجمة (متعدد اللغات)
# ============================================================
LANGUAGES = {
    "ar": {
        "name": "العربية",
        "dir": "rtl",
        "title": "🚀 كوزميك-324: القيادة المدارية 6G Titan X",
        "subtitle": "منصة المحاكاة الفضائية والسيادية المتكاملة",
        "welcome": "🌟 مرحباً بك في منصة كوزميك-324، البوابة الموحدة للقيادة الفضائية.",
        "params": "⚙️ إعدادات المحاكاة والتحكم",
        "sat_count": "عدد الأقمار",
        "update_btn": "🔄 تحديث البيانات",
        "total": "المجموع",
        "satellite": "القمر",
        "status": "الحالة",
        "latitude": "خط العرض",
        "longitude": "خط الطول",
        "altitude": "الارتفاع (كم)",
        "celestrak": "📡 جلب بيانات Celestrak",
        "group": "المجموعة",
        "alert_threshold": "عتبة التنبيه (م.ث)",
        "active_threshold": "الحد الأدنى للأقمار النشطة",
        "3d_globe": "🌍 الخريطة الكونية ثلاثية الأبعاد",
        "auto_refresh": "⏱️ التحديث التلقائي المداري",
        "refresh_interval": "الفاصل الزمني (ثانية)",
        "start_auto": "▶️ تشغيل التلقائي",
        "stop_auto": "⏹️ إيقاف التلقائي",
        "performance_mode": "⚡ وضع الأداء",
        "full_resolution": "دقة كاملة (5000)",
        "high_speed": "سرعة عالية (100)",
        "mobile_mode": "📱 وضع الجوال",
        "ground_station": "🛰️ إدارة المحطات والدول العالمية",
        "gs_select": "اختر الدولة العالمية أو المحطة السيادية:",
        "visible_sats": "الأقمار المرئية في نطاق المحطة",
        "cataloged": "مفهرس",
        "catalog_source": "مصدر الفهرس",
        "configured_stations": "المحطات المعرفة",
        "propagation_chart": "تقدير الحد الأدنى لزمن الانتشار",
        "sample": "العينة",
        "propagation_ms": "زمن الانتشار التقديري أحادي الاتجاه (م.ث)",
        "nav_dashboard": "📊 لوحة القيادة",
        "nav_licenses": "🔑 إدارة التراخيص",
        "nav_clients": "👥 العملاء وبوابات الدفع",
        "nav_health": "🩺 صحة النظام والشبكة",
        "nav_settings": "⚙️ الإعدادات المتقدمة",
        "license_title": "🔑 نظام إصدار وتوليد المفاتيح السيادية",
        "gen_key_btn": "توليد مفتاح ترخيص جديد",
        "license_key": "مفتاح الترخيص",
        "client_name": "اسم العميل / الجهة",
        "license_tier": "نوع الباقة",
        "expiry_date": "تاريخ الانتهاء",
        "active_licenses": "التراخيص النشطة حالياً",
        "clients_title": "👥 بوابات العملاء ودعم بوابات الدفع (Stripe & PayPal)",
        "client_login": "تسجيل دخول العميل",
        "email": "البريد الإلكتروني",
        "password": "كلمة المرور",
        "login_btn": "دخول البوابة",
        "paypal_sim": "💳 بوابات الدفع العالمية (Stripe / PayPal)",
        "pay_now": "دفع اشتراك الباقة السيادية ($199)",
        "payment_success": "✅ تم اتمام عملية الدفع بنجاح وتفعيل الحساب السيادي فوراً!",
        "health_title": "🩺 صحة النظام والشبكة المدارية والخوادم",
        "server_load": "حمل الخوادم السيادية",
        "network_latency": "متوسط زمن الاستجابة العضوي",
        "packet_loss": "معدل فقدان الحزم",
        "cpu_usage": "استهلاك المعالج المركزي (CPU)",
        "memory_usage": "استهلاك الذاكرة العشوائية (RAM)",
        "settings_title": "⚙️ الإعدادات المتقدمة ومزودات البيانات",
        "api_endpoint": "رابط مزود البيانات الأساسي (API Endpoint)",
        "encryption_level": "مستوى التشفير السيادي",
        "save_settings": "حفظ الإعدادات المتقدمة",
        "settings_saved": "✅ تم حفظ وتطبيق الإعدادات المتقدمة بنجاح!",
        "no_licenses": "لا توجد تراخيص مسجلة حتى الآن",
        "loading": "🔄 جاري تحميل المنصة وحساب المسارات مدارياً...",
        "no_visible_sats": "لا توجد أقمار صناعية حالياً ضمن نطاق الرؤية المباشرة لهذه الدولة.",
        "auto_refresh_active": "⚡ التحديث التلقائي قيد التشغيل (يتم التحديث كل {interval} ثانية)...",
        "payment_gateway": "اختر بوابة الدفع:",
        "stripe_checkout": "Stripe Checkout",
        "paypal_express": "PayPal Express",
        "payment_processed": "✅ تم اتمام الدفع بنجاح عبر بوابة {gateway} وتفعيل الاشتراك السيادي فوراً!"
    },
    "en": {
        "name": "English",
        "dir": "ltr",
        "title": "🚀 COSMIC-324: 6G Titan X Orbital Command",
        "subtitle": "Global Sovereign Space Simulation & Command Platform",
        "welcome": "🌟 Welcome to COSMIC-324, the integrated space command gateway.",
        "params": "⚙️ Simulation Parameters & Control",
        "sat_count": "Number of Satellites",
        "update_btn": "🔄 Refresh Data",
        "total": "Total",
        "satellite": "Satellite",
        "status": "Status",
        "latitude": "Latitude",
        "longitude": "Longitude",
        "altitude": "Altitude (km)",
        "celestrak": "📡 Fetch Celestrak Data",
        "group": "Group",
        "alert_threshold": "Alert Threshold (ms)",
        "active_threshold": "Min Active Satellites",
        "3d_globe": "🌍 3D Constellation Globe",
        "auto_refresh": "⏱️ Orbital Auto-Refresh",
        "refresh_interval": "Interval (seconds)",
        "start_auto": "▶️ Start Auto",
        "stop_auto": "⏹️ Stop Auto",
        "performance_mode": "⚡ Performance Mode",
        "full_resolution": "Full Resolution (5000)",
        "high_speed": "High Speed (100)",
        "mobile_mode": "📱 Mobile Mode",
        "ground_station": "🛰️ Global Ground Station & Country Management",
        "gs_select": "Select Global Country or Sovereign Station:",
        "visible_sats": "Satellites in Line of Sight",
        "cataloged": "Cataloged",
        "catalog_source": "Catalog Source",
        "configured_stations": "Configured Stations",
        "propagation_chart": "Estimated Minimum Propagation Delay",
        "sample": "Sample",
        "propagation_ms": "Estimated One-Way Propagation (ms)",
        "nav_dashboard": "📊 Dashboard",
        "nav_licenses": "🔑 Licenses Management",
        "nav_clients": "👥 Clients & Payment Portals",
        "nav_health": "🩺 System Health",
        "nav_settings": "⚙️ Advanced Settings",
        "license_title": "🔑 Sovereign Key Generation & License Management",
        "gen_key_btn": "Generate New License Key",
        "license_key": "License Key",
        "client_name": "Client / Entity Name",
        "license_tier": "Subscription Tier",
        "expiry_date": "Expiry Date",
        "active_licenses": "Currently Active Licenses",
        "clients_title": "👥 Client Portals & Payment Gateways (Stripe & PayPal)",
        "client_login": "Client Authentication",
        "email": "Email Address",
        "password": "Password",
        "login_btn": "Portal Login",
        "paypal_sim": "💳 Global Payment Gateways (Stripe / PayPal)",
        "pay_now": "Pay Sovereign Tier Subscription ($199)",
        "payment_success": "✅ Payment successfully processed and sovereign account activated!",
        "health_title": "🩺 System Health, Network & Server Performance",
        "server_load": "Sovereign Server Load",
        "network_latency": "Average Organic Latency",
        "packet_loss": "Packet Loss Rate",
        "cpu_usage": "CPU Utilization",
        "memory_usage": "RAM Utilization",
        "settings_title": "⚙️ Advanced Settings & Data Providers",
        "api_endpoint": "Primary Data Provider API Endpoint",
        "encryption_level": "Sovereign Encryption Level",
        "save_settings": "Save Advanced Settings",
        "settings_saved": "✅ Advanced settings successfully saved and applied!",
        "no_licenses": "No licenses registered yet",
        "loading": "🔄 Loading platform and calculating orbital paths...",
        "no_visible_sats": "No satellites currently in line of sight for this country.",
        "auto_refresh_active": "⚡ Auto-refresh is active (updating every {interval} seconds)...",
        "payment_gateway": "Select Payment Gateway:",
        "stripe_checkout": "Stripe Checkout",
        "paypal_express": "PayPal Express",
        "payment_processed": "✅ Payment successfully processed via {gateway} and sovereign subscription activated!"
    }
}

def t(key: str) -> str:
    lang = st.session_state.get('language', 'ar')
    return LANGUAGES.get(lang, LANGUAGES['ar']).get(key, key)

def get_current_dir() -> str:
    lang = st.session_state.get('language', 'ar')
    return LANGUAGES.get(lang, LANGUAGES['ar']).get('dir', 'rtl')

# ============================================================
# ⚙️ إعداد الواجهة
# ============================================================
st.set_page_config(
    page_title="COSMIC-324: 6G Titan X",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تهيئة حالة الجلسة
if 'language' not in st.session_state:
    st.session_state.language = 'ar'
if 'auto_refresh_active' not in st.session_state:
    st.session_state.auto_refresh_active = False
if 'cache_version' not in st.session_state:
    st.session_state.cache_version = 0
if 'licenses_db' not in st.session_state:
    st.session_state.licenses_db = []

current_direction = get_current_dir()

# CSS المتقدم
st.markdown(f"""
<style>
    /* التصميم الأساسي */
    .main, .stApp {{
        background-color: #0a0a12;
        direction: {current_direction};
        text-align: {'right' if current_direction == 'rtl' else 'left'};
    }}
    
    /* بطاقات المقاييس */
    .stMetric {{
        background: linear-gradient(145deg, #1a1a2e, #0d0d1a);
        border-radius: 12px;
        padding: 15px;
        border: 1px solid rgba(0, 204, 255, 0.15);
        transition: all 0.3s ease;
    }}
    .stMetric:hover {{
        border-color: rgba(0, 204, 255, 0.4);
        box-shadow: 0 0 20px rgba(0, 204, 255, 0.1);
        transform: translateY(-2px);
    }}
    
    /* العناوين */
    h1, h2, h3, h4, h5 {{
        color: #00CCFF;
        font-family: 'Arial Black', sans-serif;
        text-shadow: 0 0 30px rgba(0, 204, 255, 0.2);
    }}
    
    /* الأزرار */
    .stButton > button {{
        background: linear-gradient(135deg, #00CCFF, #0066AA);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: bold;
        width: 100%;
        transition: all 0.3s ease;
        cursor: pointer;
    }}
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 5px 20px rgba(0, 204, 255, 0.3);
    }}
    
    /* التذييل */
    .copyright {{
        text-align: center;
        color: #445566;
        font-size: 0.8em;
        padding: 20px 0;
        border-top: 1px solid #1a1a2e;
        margin-top: 20px;
    }}
    
    /* صندوق الترحيب */
    .welcome-box {{
        background: linear-gradient(135deg, #1a1a2e, #0d0d1a);
        border-radius: 12px;
        padding: 20px 25px;
        border: 1px solid rgba(0, 204, 255, 0.2);
        margin-bottom: 20px;
    }}
    .welcome-box h2 {{
        color: #00CCFF;
        margin: 0 0 10px 0;
        font-size: 1.5
