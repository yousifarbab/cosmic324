"""
COSMIC-324: 6G Titan X Global Edition
منصة المحاكاة الفضائية والسيادية المتكاملة
الإصدار: v7.6 - مع دعم pycountry البديل
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
import streamlit.components.v1 as components

# ============================================================
# 📝 إعداد نظام التسجيل (Logging)
# ============================================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================================
# 🌍 محاولة استيراد pycountry مع بديل
# ============================================================
class PyCountryFallback:
    """بديل pycountry للاستخدام عندما لا يكون مثبتاً"""
    
    class countries:
        _data = [
            {"name": "United States", "alpha_2": "US"},
            {"name": "United Kingdom", "alpha_2": "GB"},
            {"name": "Canada", "alpha_2": "CA"},
            {"name": "Australia", "alpha_2": "AU"},
            {"name": "Germany", "alpha_2": "DE"},
            {"name": "France", "alpha_2": "FR"},
            {"name": "Italy", "alpha_2": "IT"},
            {"name": "Spain", "alpha_2": "ES"},
            {"name": "Brazil", "alpha_2": "BR"},
            {"name": "India", "alpha_2": "IN"},
            {"name": "China", "alpha_2": "CN"},
            {"name": "Japan", "alpha_2": "JP"},
            {"name": "Russia", "alpha_2": "RU"},
            {"name": "South Africa", "alpha_2": "ZA"},
            {"name": "Egypt", "alpha_2": "EG"},
            {"name": "Saudi Arabia", "alpha_2": "SA"},
            {"name": "United Arab Emirates", "alpha_2": "AE"},
            {"name": "Turkey", "alpha_2": "TR"},
            {"name": "Pakistan", "alpha_2": "PK"},
            {"name": "Malaysia", "alpha_2": "MY"},
            {"name": "Singapore", "alpha_2": "SG"},
            {"name": "South Korea", "alpha_2": "KR"},
            {"name": "Mexico", "alpha_2": "MX"},
            {"name": "Argentina", "alpha_2": "AR"},
            {"name": "New Zealand", "alpha_2": "NZ"},
            {"name": "Netherlands", "alpha_2": "NL"},
            {"name": "Belgium", "alpha_2": "BE"},
            {"name": "Switzerland", "alpha_2": "CH"},
            {"name": "Sweden", "alpha_2": "SE"},
            {"name": "Norway", "alpha_2": "NO"},
            {"name": "Denmark", "alpha_2": "DK"},
            {"name": "Finland", "alpha_2": "FI"},
            {"name": "Ireland", "alpha_2": "IE"},
            {"name": "Portugal", "alpha_2": "PT"},
            {"name": "Greece", "alpha_2": "GR"},
            {"name": "Poland", "alpha_2": "PL"},
            {"name": "Ukraine", "alpha_2": "UA"},
            {"name": "Israel", "alpha_2": "IL"},
            {"name": "Iran", "alpha_2": "IR"},
            {"name": "Iraq", "alpha_2": "IQ"},
            {"name": "Syria", "alpha_2": "SY"},
            {"name": "Lebanon", "alpha_2": "LB"},
            {"name": "Jordan", "alpha_2": "JO"},
            {"name": "Kuwait", "alpha_2": "KW"},
            {"name": "Qatar", "alpha_2": "QA"},
            {"name": "Oman", "alpha_2": "OM"},
            {"name": "Bahrain", "alpha_2": "BH"},
            {"name": "Yemen", "alpha_2": "YE"},
            {"name": "Sudan", "alpha_2": "SD"},
            {"name": "Libya", "alpha_2": "LY"},
            {"name": "Tunisia", "alpha_2": "TN"},
            {"name": "Algeria", "alpha_2": "DZ"},
            {"name": "Morocco", "alpha_2": "MA"},
            {"name": "Nigeria", "alpha_2": "NG"},
            {"name": "Kenya", "alpha_2": "KE"},
            {"name": "Ethiopia", "alpha_2": "ET"},
            {"name": "Ghana", "alpha_2": "GH"},
            {"name": "Colombia", "alpha_2": "CO"},
            {"name": "Chile", "alpha_2": "CL"},
            {"name": "Peru", "alpha_2": "PE"},
            {"name": "Venezuela", "alpha_2": "VE"},
            {"name": "Indonesia", "alpha_2": "ID"},
            {"name": "Philippines", "alpha_2": "PH"},
            {"name": "Vietnam", "alpha_2": "VN"},
            {"name": "Thailand", "alpha_2": "TH"},
            {"name": "Palestine", "alpha_2": "PS"},
            {"name": "Afghanistan", "alpha_2": "AF"},
            {"name": "Albania", "alpha_2": "AL"},
            {"name": "Andorra", "alpha_2": "AD"},
            {"name": "Angola", "alpha_2": "AO"},
            {"name": "Armenia", "alpha_2": "AM"},
            {"name": "Austria", "alpha_2": "AT"},
            {"name": "Azerbaijan", "alpha_2": "AZ"},
            {"name": "Bangladesh", "alpha_2": "BD"},
            {"name": "Barbados", "alpha_2": "BB"},
            {"name": "Belarus", "alpha_2": "BY"},
            {"name": "Belize", "alpha_2": "BZ"},
            {"name": "Benin", "alpha_2": "BJ"},
            {"name": "Bhutan", "alpha_2": "BT"},
            {"name": "Bolivia", "alpha_2": "BO"},
            {"name": "Botswana", "alpha_2": "BW"},
            {"name": "Brunei", "alpha_2": "BN"},
            {"name": "Bulgaria", "alpha_2": "BG"},
            {"name": "Burkina Faso", "alpha_2": "BF"},
            {"name": "Cambodia", "alpha_2": "KH"},
            {"name": "Cameroon", "alpha_2": "CM"},
            {"name": "Cape Verde", "alpha_2": "CV"},
            {"name": "Central African Republic", "alpha_2": "CF"},
            {"name": "Chad", "alpha_2": "TD"},
            {"name": "Comoros", "alpha_2": "KM"},
            {"name": "Congo", "alpha_2": "CG"},
            {"name": "Costa Rica", "alpha_2": "CR"},
            {"name": "Croatia", "alpha_2": "HR"},
            {"name": "Cuba", "alpha_2": "CU"},
            {"name": "Cyprus", "alpha_2": "CY"},
            {"name": "Czech Republic", "alpha_2": "CZ"},
            {"name": "Djibouti", "alpha_2": "DJ"},
            {"name": "Dominica", "alpha_2": "DM"},
            {"name": "Dominican Republic", "alpha_2": "DO"},
            {"name": "Ecuador", "alpha_2": "EC"},
            {"name": "El Salvador", "alpha_2": "SV"},
            {"name": "Equatorial Guinea", "alpha_2": "GQ"},
            {"name": "Eritrea", "alpha_2": "ER"},
            {"name": "Estonia", "alpha_2": "EE"},
            {"name": "Eswatini", "alpha_2": "SZ"},
            {"name": "Fiji", "alpha_2": "FJ"},
            {"name": "Gabon", "alpha_2": "GA"},
            {"name": "Georgia", "alpha_2": "GE"},
            {"name": "Guatemala", "alpha_2": "GT"},
            {"name": "Guinea", "alpha_2": "GN"},
            {"name": "Guyana", "alpha_2": "GY"},
            {"name": "Haiti", "alpha_2": "HT"},
            {"name": "Honduras", "alpha_2": "HN"},
            {"name": "Hungary", "alpha_2": "HU"},
            {"name": "Iceland", "alpha_2": "IS"},
            {"name": "Jamaica", "alpha_2": "JM"},
            {"name": "Kazakhstan", "alpha_2": "KZ"},
            {"name": "Kyrgyzstan", "alpha_2": "KG"},
            {"name": "Laos", "alpha_2": "LA"},
            {"name": "Latvia", "alpha_2": "LV"},
            {"name": "Lesotho", "alpha_2": "LS"},
            {"name": "Liberia", "alpha_2": "LR"},
            {"name": "Liechtenstein", "alpha_2": "LI"},
            {"name": "Lithuania", "alpha_2": "LT"},
            {"name": "Luxembourg", "alpha_2": "LU"},
            {"name": "Madagascar", "alpha_2": "MG"},
            {"name": "Malawi", "alpha_2": "MW"},
            {"name": "Maldives", "alpha_2": "MV"},
            {"name": "Mali", "alpha_2": "ML"},
            {"name": "Malta", "alpha_2": "MT"},
            {"name": "Mauritania", "alpha_2": "MR"},
            {"name": "Mauritius", "alpha_2": "MU"},
            {"name": "Moldova", "alpha_2": "MD"},
            {"name": "Monaco", "alpha_2": "MC"},
            {"name": "Mongolia", "alpha_2": "MN"},
            {"name": "Montenegro", "alpha_2": "ME"},
            {"name": "Mozambique", "alpha_2": "MZ"},
            {"name": "Myanmar", "alpha_2": "MM"},
            {"name": "Namibia", "alpha_2": "NA"},
            {"name": "Nepal", "alpha_2": "NP"},
            {"name": "Nicaragua", "alpha_2": "NI"},
            {"name": "Niger", "alpha_2": "NE"},
            {"name": "North Korea", "alpha_2": "KP"},
            {"name": "North Macedonia", "alpha_2": "MK"},
            {"name": "Panama", "alpha_2": "PA"},
            {"name": "Papua New Guinea", "alpha_2": "PG"},
            {"name": "Paraguay", "alpha_2": "PY"},
            {"name": "Romania", "alpha_2": "RO"},
            {"name": "Rwanda", "alpha_2": "RW"},
            {"name": "Samoa", "alpha_2": "WS"},
            {"name": "San Marino", "alpha_2": "SM"},
            {"name": "Senegal", "alpha_2": "SN"},
            {"name": "Serbia", "alpha_2": "RS"},
            {"name": "Seychelles", "alpha_2": "SC"},
            {"name": "Sierra Leone", "alpha_2": "SL"},
            {"name": "Slovakia", "alpha_2": "SK"},
            {"name": "Slovenia", "alpha_2": "SI"},
            {"name": "Solomon Islands", "alpha_2": "SB"},
            {"name": "Somalia", "alpha_2": "SO"},
            {"name": "Sri Lanka", "alpha_2": "LK"},
            {"name": "Suriname", "alpha_2": "SR"},
            {"name": "Tajikistan", "alpha_2": "TJ"},
            {"name": "Tanzania", "alpha_2": "TZ"},
            {"name": "Timor-Leste", "alpha_2": "TL"},
            {"name": "Togo", "alpha_2": "TG"},
            {"name": "Tonga", "alpha_2": "TO"},
            {"name": "Trinidad and Tobago", "alpha_2": "TT"},
            {"name": "Turkmenistan", "alpha_2": "TM"},
            {"name": "Tuvalu", "alpha_2": "TV"},
            {"name": "Uganda", "alpha_2": "UG"},
            {"name": "Uruguay", "alpha_2": "UY"},
            {"name": "Uzbekistan", "alpha_2": "UZ"},
            {"name": "Vanuatu", "alpha_2": "VU"},
            {"name": "Zambia", "alpha_2": "ZM"},
            {"name": "Zimbabwe", "alpha_2": "ZW"},
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
    logger.info("✅ تم تحميل pycountry بنجاح")
    USE_PYCOUNTRY = True
except ImportError:
    pycountry = PyCountryFallback
    USE_PYCOUNTRY = False
    logger.info("⚠️ استخدام البديل المحلي لـ pycountry")

# ============================================================
# 🔐 إعداد المفتاح السري للتراخيص
# ============================================================
SECRET_KEY = os.environ.get('COSMIC_SECRET_KEY', 'default-secret-key-change-me-in-production')

# ============================================================
# 📁 تحميل ملف العقد والبيانات الأساسية
# ============================================================
def load_contract_data() -> Dict:
    """تحميل بيانات العقد من ملف JSON مع دعم مسارات متعددة"""
    possible_paths = [
        Path(__file__).with_name("cosmic324_data.json"),
        Path(os.getcwd()) / "data" / "cosmic324_data.json",
        Path(os.getcwd()) / "config" / "cosmic324_data.json",
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
    
    logger.info("ℹ️ استخدام البيانات الاحتياطية")
    return get_default_contract()

def get_default_contract() -> Dict:
    """توفير بيانات احتياطية"""
    return {
        "celestrak": {
            "groups": ["starlink", "active", "visual", "weather", "gps", "iridium"],
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
# 🗄️ نظام إدارة التراخيص
# ============================================================
class LicenseManager:
    """مدير التراخيص مع تخزين في SQLite"""
    
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
                logger.info("✅ تم تهيئة قاعدة بيانات التراخيص")
        except Exception as e:
            logger.error(f"❌ فشل تهيئة قاعدة البيانات: {e}")
    
    def generate_secure_license(self, client_name: str, tier: str, validity_days: int = 365) -> Tuple[str, str]:
        """توليد مفتاح ترخيص آمن"""
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
# 🌍 نظام الترجمة
# ============================================================
LANGUAGES = {
    "ar": {
        "name": "العربية",
        "dir": "rtl",
        "title": "🚀 كوزميك-324: القيادة المدارية 6G Titan X",
        "subtitle": "منصة المحاكاة الفضائية والسيادية المتكاملة",
        "welcome": "🌟 مرحباً بك في منصة كوزميك-324",
        "params": "⚙️ إعدادات المحاكاة",
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
        "3d_globe": "🌍 الخريطة الكونية",
        "auto_refresh": "⏱️ التحديث التلقائي",
        "refresh_interval": "الفاصل الزمني (ثانية)",
        "start_auto": "▶️ تشغيل",
        "stop_auto": "⏹️ إيقاف",
        "performance_mode": "⚡ وضع الأداء",
        "full_resolution": "دقة كاملة",
        "high_speed": "سرعة عالية",
        "mobile_mode": "📱 وضع الجوال",
        "ground_station": "🛰️ إدارة المحطات والدول",
        "gs_select": "اختر الدولة:",
        "visible_sats": "الأقمار المرئية",
        "cataloged": "مفهرس",
        "catalog_source": "مصدر الفهرس",
        "configured_stations": "المحطات المعرفة",
        "propagation_chart": "تقدير زمن الانتشار",
        "sample": "العينة",
        "propagation_ms": "زمن الانتشار (م.ث)",
        "nav_dashboard": "📊 لوحة القيادة",
        "nav_licenses": "🔑 إدارة التراخيص",
        "nav_clients": "👥 العملاء والدفع",
        "nav_health": "🩺 صحة النظام",
        "nav_settings": "⚙️ الإعدادات",
        "license_title": "🔑 نظام إصدار المفاتيح",
        "gen_key_btn": "توليد مفتاح جديد",
        "license_key": "مفتاح الترخيص",
        "client_name": "اسم العميل",
        "license_tier": "نوع الباقة",
        "expiry_date": "تاريخ الانتهاء",
        "active_licenses": "التراخيص النشطة",
        "clients_title": "👥 بوابات العملاء والدفع",
        "client_login": "تسجيل دخول",
        "email": "البريد الإلكتروني",
        "password": "كلمة المرور",
        "login_btn": "دخول",
        "paypal_sim": "💳 بوابات الدفع",
        "pay_now": "دفع $199",
        "payment_success": "✅ تم الدفع بنجاح!",
        "health_title": "🩺 صحة النظام",
        "server_load": "حمل الخادم",
        "network_latency": "زمن الاستجابة",
        "packet_loss": "فقدان الحزم",
        "cpu_usage": "استخدام CPU",
        "memory_usage": "استخدام RAM",
        "settings_title": "⚙️ الإعدادات المتقدمة",
        "api_endpoint": "رابط API",
        "encryption_level": "مستوى التشفير",
        "save_settings": "حفظ الإعدادات",
        "settings_saved": "✅ تم حفظ الإعدادات!",
        "no_licenses": "لا توجد تراخيص مسجلة",
        "loading": "🔄 جاري التحميل...",
        "no_visible_sats": "لا توجد أقمار في النطاق",
    },
    "en": {
        "name": "English",
        "dir": "ltr",
        "title": "🚀 COSMIC-324: 6G Titan X Orbital Command",
        "subtitle": "Global Sovereign Space Simulation Platform",
        "welcome": "🌟 Welcome to COSMIC-324",
        "params": "⚙️ Simulation Parameters",
        "sat_count": "Satellites Count",
        "update_btn": "🔄 Refresh Data",
        "total": "Total",
        "satellite": "Satellite",
        "status": "Status",
        "latitude": "Latitude",
        "longitude": "Longitude",
        "altitude": "Altitude (km)",
        "celestrak": "📡 Fetch Celestrak",
        "group": "Group",
        "alert_threshold": "Alert Threshold (ms)",
        "active_threshold": "Min Active",
        "3d_globe": "🌍 3D Globe",
        "auto_refresh": "⏱️ Auto-Refresh",
        "refresh_interval": "Interval (sec)",
        "start_auto": "▶️ Start",
        "stop_auto": "⏹️ Stop",
        "performance_mode": "⚡ Performance",
        "full_resolution": "Full Resolution",
        "high_speed": "High Speed",
        "mobile_mode": "📱 Mobile Mode",
        "ground_station": "🛰️ Ground Stations",
        "gs_select": "Select Country:",
        "visible_sats": "Visible Satellites",
        "cataloged": "Cataloged",
        "catalog_source": "Catalog Source",
        "configured_stations": "Stations",
        "propagation_chart": "Propagation Delay",
        "sample": "Sample",
        "propagation_ms": "Propagation (ms)",
        "nav_dashboard": "📊 Dashboard",
        "nav_licenses": "🔑 Licenses",
        "nav_clients": "👥 Clients",
        "nav_health": "🩺 Health",
        "nav_settings": "⚙️ Settings",
        "license_title": "🔑 License Management",
        "gen_key_btn": "Generate Key",
        "license_key": "License Key",
        "client_name": "Client Name",
        "license_tier": "Tier",
        "expiry_date": "Expiry Date",
        "active_licenses": "Active Licenses",
        "clients_title": "👥 Client Portals",
        "client_login": "Client Login",
        "email": "Email",
        "password": "Password",
        "login_btn": "Login",
        "paypal_sim": "💳 Payment Gateways",
        "pay_now": "Pay $199",
        "payment_success": "✅ Payment successful!",
        "health_title": "🩺 System Health",
        "server_load": "Server Load",
        "network_latency": "Latency",
        "packet_loss": "Packet Loss",
        "cpu_usage": "CPU Usage",
        "memory_usage": "RAM Usage",
        "settings_title": "⚙️ Advanced Settings",
        "api_endpoint": "API Endpoint",
        "encryption_level": "Encryption",
        "save_settings": "Save Settings",
        "settings_saved": "✅ Settings saved!",
        "no_licenses": "No licenses registered",
        "loading": "🔄 Loading...",
        "no_visible_sats": "No visible satellites",
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
    layout="wide"
)

# تهيئة حالة الجلسة
if 'language' not in st.session_state:
    st.session_state.language = 'ar'
if 'auto_refresh_active' not in st.session_state:
    st.session_state.auto_refresh_active = False
if 'cache_version' not in st.session_state:
    st.session_state.cache_version = 0

current_direction = get_current_dir()

# CSS للتنسيق العام والتوافق مع الاتجاهين RTL/LTR
st.markdown(f"""
<style>
    .main, .stApp {{
        background-color: #0a0a12;
        direction: {current_direction};
        text-align: {'right' if current_direction == 'rtl' else 'left'};
    }}
    .stMetric {{
        background: linear-gradient(145deg, #1a1a2e, #0d0d1a);
        border-radius: 12px;
        padding: 15px;
        border: 1px solid #2e2e48;
    }}
</style>
""", unsafe_allow_html=True)
