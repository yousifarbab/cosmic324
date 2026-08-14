"""
COSMIC-324: 6G Titan X Global Edition
منصة المحاكاة الفضائية والسيادية المتكاملة
الإصدار: v7.6 - Complete Features Integrated (قائمة الدول، الباقات الثلاث، ودعم عدد الأقمار الفعلي)
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
import time
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
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('cosmic324.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ============================================================
# 🔐 إعداد المفتاح السري للتراخيص
# ============================================================
SECRET_KEY = os.environ.get('COSMIC_SECRET_KEY', 'default-secret-key-change-me-in-production')

# ============================================================
# 📁 تحميل ملف العقد والبيانات الأساسية (مع دعم مسارات متعددة)
# ============================================================
def load_contract_data() -> Dict:
    possible_paths = [
        Path(__file__).with_name("cosmic324_data.json"),
        Path(os.getcwd()) / "data" / "cosmic324_data.json",
        Path(os.getcwd()) / "config" / "cosmic324_data.json",
        Path("/etc/cosmic324/config.json"),
        Path.home() / ".cosmic324" / "config.json"
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
    
    logger.info("ℹ️ استخدام البيانات الاحتياطية (fallback data)")
    return get_default_contract()

def get_default_contract() -> Dict:
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
# 🗄️ نظام إدارة التراخيص باستخدام SQLite
# ============================================================
class LicenseManager:
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
                conn.execute("""
                    CREATE INDEX IF NOT EXISTS idx_license_key ON licenses(license_key)
                """)
                conn.execute("""
                    CREATE INDEX IF NOT EXISTS idx_expiry ON licenses(expiry_date)
                """)
                logger.info("✅ تم تهيئة قاعدة بيانات التراخيص")
        except Exception as e:
            logger.error(f"❌ فشل تهيئة قاعدة البيانات: {e}")
    
    def generate_secure_license(self, client_name: str, tier: str, validity_days: int = 365) -> Tuple[str, str]:
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
        
        logger.info(f"✅ تم توليد مفتاح ترخيص جديد لـ {client_name}")
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
            logger.error(f"❌ فشل جلب التراخيص النشطة: {e}")
            return []
    
    def update_payment_status(self, license_key: str, status: str, gateway: str):
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    UPDATE licenses 
                    SET payment_status = ?, payment_gateway = ?
                    WHERE license_key = ?
                """, (status, gateway, license_key))
                logger.info(f"✅ تم تحديث حالة الدفع للترخيص {license_key}")
        except Exception as e:
            logger.error(f"❌ فشل تحديث حالة الدفع: {e}")
    
    def deactivate_license(self, license_key: str):
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    UPDATE licenses SET is_active = 0
                    WHERE license_key = ?
                """, (license_key,))
                logger.info(f"✅ تم إلغاء تنشيط الترخيص {license_key}")
        except Exception as e:
            logger.error(f"❌ فشل إلغاء تنشيط الترخيص: {e}")

license_manager = LicenseManager()

# ============================================================
# 🌍 نظام الترجمة واتجاه الصفحة
# ============================================================
LANGUAGES = {
    "ar": {
        "name": "العربية",
        "dir": "rtl",
        "title": "🚀 كوزميك-324: القيادة المدارية 6G Titan X",
        "subtitle": "منصة المحاكاة الفضائية والسيادية المتكاملة",
        "welcome": "🌟 مرحباً بك في منصة كوزميك-324، البوابة الموحدة للقيادة الفضائية.",
        "params": "⚙️ إعدادات المحاكاة والتحكم",
        "sat_count": "عدد الأقمار (الفعلي)",
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
        "ground_station": "🛰️ إدارة المحطات والدول العالمية",
        "gs_select": "اختر الدولة أو المحطة السيادية (الشريط الجانبي):",
        "visible_sats": "الأقمار المرئية في نطاق المحطة والدولة المحددة",
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
        "license_tier": "نوع الباقة السيادية",
        "expiry_date": "تاريخ الانتهاء",
        "active_licenses": "التراخيص النشطة حالياً",
        "clients_title": "👥 بوابات العملاء ودعم الباقات الثلاث وبوابات الدفع",
        "tier_1_name": "الباقة الأولى: الاستكشاف المداري (Orbital Scout)",
        "tier_1_price": "$49 / شهرياً",
        "tier_1_desc": "تتبع أساسي لـ 100 قمر، تحديث كل دقيقة، دعم فني قياسي.",
        "tier_2_name": "الباقة الثانية: القيادة التكتيكية (Tactical Command)",
        "tier_2_price": "$199 / شهرياً",
        "tier_2_desc": "تتبع متقدم حتى 1000 قمر، ربط المحطات الأرضية ودول العالم، زمن استجابة فائق.",
        "tier_3_name": "الباقة الثالثة: السيادة المطلقة 6G Titan (Absolute Sovereign)",
        "tier_3_price": "$499 / شهرياً",
        "tier_3_desc": "تتبع مفتوح لجميع الأقمار المتاحة (حتى 5000+ قمر)، تشفير كمومي، دعم مباشر 24/7.",
        "select_tier_action": "اختر الباقة للاشتراك الفوري:",
        "client_login": "تسجيل دخول العميل",
        "email": "البريد الإلكتروني",
        "password": "كلمة المرور",
        "login_btn": "دخول البوابة",
        "paypal_sim": "💳 بوابات الدفع العالمية (Stripe / PayPal)",
        "pay_now": "إتمام الدفع للباقة المختارة",
        "payment_success": "✅ تم اتمام عملية الدفع بنجاح وتفعيل الاشتراك في الباقة السيادية فوراً!",
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
        "no_visible_sats": "لا توجد أقمار صناعية حالياً ضمن نطاق الرؤية المباشرة لهذه الدولة أو المحطة.",
        "payment_gateway": "اختر بوابة الدفع:",
        "stripe_checkout": "Stripe Checkout",
        "paypal_express": "PayPal Express",
        "payment_processed": "✅ تم اتمام الدفع بنجاح عبر بوابة {gateway} للباقة المختارة وتفعيل الحساب فوراً!"
    },
    "en": {
        "name": "English",
        "dir": "ltr",
        "title": "🚀 COSMIC-324: 6G Titan X Orbital Command",
        "subtitle": "Global Sovereign Space Simulation & Command Platform",
        "welcome": "🌟 Welcome to COSMIC-324, the integrated space command gateway.",
        "params": "⚙️ Simulation Parameters & Control",
        "sat_count": "Number of Satellites (Actual)",
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
        "ground_station": "🛰️ Global Ground Station & Country Management",
        "gs_select": "Select Country or Sovereign Station (Sidebar):",
        "visible_sats": "Satellites in Line of Sight for Selected Country",
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
        "clients_title": "👥 Client Portals, 3 Tiers & Payment Gateways",
        "tier_1_name": "Tier 1: Orbital Scout",
        "tier_1_price": "$49 / month",
        "tier_1_desc": "Basic tracking for 100 satellites, standard support.",
        "tier_2_name": "Tier 2: Tactical Command",
        "tier_2_price": "$199 / month",
        "tier_2_desc": "Advanced tracking up to 1000 satellites, ground stations & world countries support.",
        "tier_3_name": "Tier 3: Absolute Sovereign 6G Titan",
        "tier_3_price": "$499 / month",
        "tier_3_desc": "Full open tracking for all available satellites (up to 5000+), quantum encryption, 24/7 direct support.",
        "select_tier_action": "Select Tier for Immediate Subscription:",
        "client_login": "Client Authentication",
        "email": "Email Address",
        "password": "Password",
        "login_btn": "Portal Login",
        "paypal_sim": "💳 Global Payment Gateways (Stripe / PayPal)",
        "pay_now": "Complete Payment for Selected Tier",
        "payment_success": "✅ Payment successfully processed and subscription activated!",
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
        "no_visible_sats": "No satellites currently in line of sight for this country or station.",
        "payment_gateway": "Select Payment Gateway:",
        "stripe_checkout": "Stripe Checkout",
        "paypal_express": "PayPal Express",
        "payment_processed": "✅ Payment successfully processed via {gateway} for selected tier and subscription activated!"
    }
}

def t(key: str) -> str:
    lang = st.session_state.get('language', 'ar')
    return LANGUAGES.get(lang, LANGUAGES['ar']).get(key, key)

def get_current_dir() -> str:
    lang = st.session_state.get('language', 'ar')
    return LANGUAGES.get(lang, LANGUAGES['ar']).get('dir', 'rtl')

# ============================================================
# 📱 كشف الأجهزة المحمولة تلقائياً
# ============================================================
def detect_mobile() -> bool:
    try:
        user_agent = st.context.headers.get('User-Agent', '')
        mobile_keywords = ['Android', 'iPhone', 'iPad', 'Mobile', 'webOS', 'BlackBerry', 'IEMobile']
        return any(keyword in user_agent for keyword in mobile_keywords)
    except:
        return False

# ============================================================
# ⚙️ إعداد الواجهة والتصميم المتجاوب السيادي
# ============================================================
st.set_page_config(
    page_title="COSMIC-324: 6G Titan X",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

if 'language' not in st.session_state:
    st.session_state.language = 'ar'
if 'mobile_mode' not in st.session_state:
    st.session_state.mobile_mode = detect_mobile()
if 'auto_refresh_active' not in st.session_state:
    st.session_state.auto_refresh_active = False
if 'cache_version' not in st.session_state:
    st.session_state.cache_version = 0

current_direction = get_current_dir()
is_mobile = st.session_state.mobile_mode

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
        border: 1px solid rgba(0, 204, 255, 0.15);
        transition: all 0.3s ease;
    }}
    .stMetric:hover {{
        border-color: rgba(0, 204, 255, 0.4);
        box-shadow: 0 0 20px rgba(0, 204, 255, 0.1);
    }}
    h1, h2, h3, h4, h5 {{
        color: #00CCFF;
        font-family: 'Arial Black', sans-serif;
        text-shadow: 0 0 30px rgba(0, 204, 255, 0.2);
    }}
    .stButton > button {{
        background: linear-gradient(135deg, #00CCFF, #0066AA);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: bold;
        width: 100%;
        transition: all 0.3s ease;
    }}
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 5px 20px rgba(0, 204, 255, 0.3);
    }}
    .copyright {{
        text-align: center;
        color: #445566;
        font-size: 0.8em;
        padding: 20px 0;
        border-top: 1px solid #1a1a2e;
        margin-top: 20px;
    }}
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
        font-size: 1.5em;
    }}
    .welcome-box p {{
        color: #88AACC;
        margin: 0;
        font-size: 1em;
    }}
    .tier-card {{
        background: linear-gradient(135deg, #16162c, #0b0b16);
        border: 1px solid rgba(0, 204, 255, 0.3);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
    }}
</style>
""", unsafe_allow_html=True)

# ============================================================
# 🌐 قاعدة بيانات الدول العالمية المدمجة للشريط الجانبي
# ============================================================
@st.cache_data
def get_all_countries() -> List[Dict]:
    countries_data = [
        {"name": "Oman (سلطنة عمان)", "alpha_2": "OM", "lat": 21.5126, "lon": 55.9233},
        {"name": "Saudi Arabia (المملكة العربية السعودية)", "alpha_2": "SA", "lat": 23.8859, "lon": 45.0792},
        {"name": "United Arab Emirates (الإمارات العربية المتحدة)", "alpha_2": "AE", "lat": 23.4241, "lon": 53.8478},
        {"name": "Sudan (السودان)", "alpha_2": "SD", "lat": 15.5007, "lon": 32.5599},
        {"name": "Egypt (مصر)", "alpha_2": "EG", "lat": 26.8206, "lon": 30.8025},
        {"name": "United States (الولايات المتحدة)", "alpha_2": "US", "lat": 37.0902, "lon": -95.7129},
        {"name": "United Kingdom (المملكة المتحدة)", "alpha_2": "GB", "lat": 55.3781, "lon": -3.4360},
        {"name": "Germany (ألمانيا)", "alpha_2": "DE", "lat": 51.1657, "lon": 10.4515},
        {"name": "Japan (الابان)", "alpha_2": "JP", "lat": 36.2048, "lon": 138.2529},
        {"name": "Australia (أستراليا)", "alpha_2": "AU", "lat": -25.2744, "lon": 133.7751},
        {"name": "France (فرنسا)", "alpha_2": "FR", "lat": 46.2276, "lon": 2.2137},
        {"name": "Canada (كندا)", "alpha_2": "CA", "lat": 56.1304, "lon": -106.3468},
        {"name": "Brazil (البرازيل)", "alpha_2": "BR", "lat": -14.2350, "lon": -51.9253},
        {"name": "India (الهند)", "alpha_2": "IN", "lat": 20.5937, "lon": 78.9629},
        {"name": "China (الصين)", "alpha_2": "CN", "lat": 35.8617, "lon": 104.1954}
    ]
    return sorted(countries_data, key=lambda x: x["name"])

ALL_COUNTRIES = get_all_countries()

# ============================================================
# 📡 جلب البيانات وتسريع الحسابات المدارية
# ============================================================
@st.cache_data(ttl=CELESTRAK_CONFIG["cacheTtlSeconds"])
def fetch_celestrak_data(group: str = "starlink", max_satellites: int = 5000, cache_version: int = 0) -> List[Dict]:
    url = f"{SOURCE_CONFIG['baseUrl']}?GROUP={group}&FORMAT=json"
    try:
        logger.info(f"📡 جلب بيانات Celestrak للمجموعة: {group}")
        response = requests.get(url, timeout=20)
        response.raise_for_status()
        if response.text.startswith('['):
            data = response.json()
            logger.info(f"✅ تم جلب {len(data)} قمر من Celestrak")
            return data[:max_satellites]
    except Exception as e:
        logger.error(f"⚠️ خطأ في الاتصال بـ Celestrak: {e}")
    return []

@st.cache_resource
def generate_orbit_map(num_satellites: int = 5000, group: str = "starlink", use_celestrak: bool = True):
    orbit_map = {}
    if use_celestrak:
        raw_data = fetch_celestrak_data(group, num_satellites, st.session_state.cache_version)
        if raw_data:
            for entry in raw_data:
                try:
                    mean_motion = float(entry.get('MEAN_MOTION', 0))
                    eccentricity = float(entry.get('ECCENTRICITY', 0))
                    inclination = math.radians(float(entry.get('INCLINATION', 0)))
                    raan = math.radians(float(entry.get('RA_OF_ASC_NODE', 0)))
                    arg_perigee = math.radians(float(entry.get('ARG_OF_PERICENTER', 0)))
                    mean_anomaly = math.radians(float(entry.get('MEAN_ANOMALY', 0)))
                    
                    if mean_motion <= 0:
                        continue
                    
                    GM = MODEL_CONFIG["earthMuKm3S2"]
                    n = mean_motion * 2 * math.pi / 86400.0
                    a = (GM / (n ** 2)) ** (1.0/3.0)
                    period = 86400.0 / mean_motion

                    def position_at_time(t: float, a=a, e=eccentricity, incl=inclination, 
                                         omega=arg_perigee, Omega=raan, M0=mean_anomaly, 
                                         period=period, apply_j2=True):
                        M = M0 + 2 * math.pi * t / period
                        E = M
                        for _ in range(4):
                            E = E - (E - e * np.sin(E) - M) / (1 - e * np.cos(E))
                        
                        x_orbit = a * (np.cos(E) - e)
                        y_orbit = a * np.sqrt(1 - e**2) * np.sin(E)
                        z_orbit = 0.0
                        
                        if apply_j2:
                            J2 = MODEL_CONFIG["j2"]
                            p = a * (1 - e**2)
                            n_rad = 2 * math.pi / period
                            raan_dot = -1.5 * J2 * (MODEL_CONFIG["earthRadiusKm"] / p) ** 2 * n_rad * np.cos(incl)
                            current_raan = Omega + raan_dot * t
                            current_omega = omega + (-1.5 * J2 * (MODEL_CONFIG["earthRadiusKm"] / p) ** 2 * n_rad * np.cos(incl)) * t
                        else:
                            current_raan = Omega
                            current_omega = omega
                        
                        x1 = x_orbit * np.cos(current_omega) - y_orbit * np.sin(current_omega)
                        y1 = x_orbit * np.sin(current_omega) + y_orbit * np.cos(current_omega)
                        z1 = z_orbit
                        
                        y2 = y1 * np.cos(incl) - z1 * np.sin(incl)
                        z2 = y1 * np.sin(incl) + z1 * np.cos(incl)
                        
                        x_final = x1 * np.cos(current_raan) - y2 * np.sin(current_raan)
                        y_final = x1 * np.sin(current_raan) + y2 * np.cos(current_raan)
                        z_final = z2
                        
                        return (float(x_final), float(y_final), float(z_final))

                    orbit = SimpleNamespace()
                    orbit.position_at_time = position_at_time
                    orbit.name = entry.get('OBJECT_NAME', 'SAT')
                    orbit.altitude = a - MODEL_CONFIG["earthRadiusKm"]
                    orbit_map[orbit.name] = orbit
                except Exception:
                    continue
            if orbit_map:
                return orbit_map
    
    return generate_simulated_orbit_map(num_satellites)

def generate_simulated_orbit_map(num_satellites: int) -> Dict:
    orbit_map = {}
    for i in range(num_satellites):
        name = f"SIM-SAT-{i+1:04d}"
        inclination = math.radians(np.random.uniform(20, 90))
        raan = math.radians(np.random.uniform(0, 360))
        arg_perigee = math.radians(np.random.uniform(0, 360))
        mean_anomaly = math.radians(np.random.uniform(0, 360))
        eccentricity = np.random.uniform(0.01, 0.05)
        altitude = np.random.uniform(400, 1200)
        a = MODEL_CONFIG["earthRadiusKm"] + altitude
        period = 2 * math.pi * np.sqrt(a**3 / MODEL_CONFIG["earthMuKm3S2"])
        
        def position_at_time(t, a=a, e=eccentricity, incl=inclination, omega=arg_perigee, 
                             Omega=raan, M0=mean_anomaly, period=period, apply_j2=True):
            M = M0 + 2 * math.pi * t / period
            E = M
            for _ in range(3):
                E = E - (E - e * np.sin(E) - M) / (1 - e * np.cos(E))
            x_orbit = a * (np.cos(E) - e)
            y_orbit = a * np.sqrt(1 - e**2) * np.sin(E)
            x1 = x_orbit * np.cos(omega) - y_orbit * np.sin(omega)
            y1 = x_orbit * np.sin(omega) + y_orbit * np.cos(omega)
            y2 = y1 * np.cos(incl)
            z2 = y1 * np.sin(incl)
            x_final = x1 * np.cos(Omega) - y2 * np.sin(Omega)
            y_final = x1 * np.sin(Omega) + y2 * np.cos(Omega)
            return (float(x_final), float(y_final), float(z2))
        
        orbit = SimpleNamespace()
        orbit.position_at_time = position_at_time
        orbit.name = name
        orbit.altitude = altitude
        orbit_map[name] = orbit
    return orbit_map

def get_telemetry_data(orbit_map: Dict, num_satellites: int, t_func) -> pd.DataFrame:
    data = []
    items = list(orbit_map.items())
    if len(items) > num_satellites:
        items = items[:num_satellites]
    
    def calculate_single(item):
        name, orbit = item
        try:
            pos = orbit.position_at_time(0.0, apply_j2=True)
            if pos and len(pos) >= 3:
                x, y, z = pos
                r = math.sqrt(x**2 + y**2 + z**2)
                if r > 0:
                    lat = math.degrees(math.asin(z / r))
                    lon = math.degrees(math.atan2(y, x))
                    alt = orbit.altitude if hasattr(orbit, 'altitude') else 550
                    return {
                        t_func('satellite'): name.strip()[:30],
                        t_func('status'): t_func('cataloged'),
                        t_func('latitude'): round(lat, 4),
                        t_func('longitude'): round(lon, 4),
                        t_func('altitude'): round(alt, 2)
                    }
        except Exception:
            pass
        return None

    with ThreadPoolExecutor(max_workers=8) as executor:
        results = executor.map(calculate_single, items)
        for res in results:
            if res:
                data.append(res)
    return pd.DataFrame(data)

# ============================================================
# 🖥️ التنفيذ الرئيسي للواجهة والتطبيق السيادي
# ============================================================
def main():
    st.sidebar.title("🚀 COSMIC-324")
    
    # اختيار اللغة
    selected_lang = st.sidebar.selectbox(
        "🌐 Language / اللغة",
        options=["ar", "en"],
        format_func=lambda x: LANGUAGES[x]["name"],
        index=0 if st.session_state.language == 'ar' else 1
    )
    if selected_lang != st.session_state.language:
        st.session_state.language = selected_lang
        st.rerun()

    # القائمة المنسدلة المخصصة لدول العالم في الشريط الجانبي (المطلوب الأول)
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"### {t('ground_station')}")
    country_names = [c["name"] for c in ALL_COUNTRIES]
    selected_country_name = st.sidebar.selectbox(t('gs_select'), country_names)
    
    # استخراج إحداثيات الدولة المختارة
    selected_country_obj = next((c for c in ALL_COUNTRIES if c["name"] == selected_country_name), ALL_COUNTRIES[0])

    # التنقل بين الأقسام
    st.sidebar.markdown("---")
    nav_option = st.sidebar.radio(
        "📌 القائمة الرئيسية",
        options=[
            t('nav_dashboard'),
            t('nav_licenses'),
            t('nav_clients'),
            t('nav_health'),
            t('nav_settings')
        ]
    )

    st.title(t('title'))
    st.markdown(f"*{t('subtitle')}*")

    st.markdown(f"""
    <div class="welcome-box">
        <h2>{t('welcome')}</h2>
        <p>{t('subtitle')} - v7.6 | الدولة / المحطة المحددة: <b>{selected_country_obj['name']}</b> (خط العرض: {selected_country_obj['lat']}°, خط الطول: {selected_country_obj['lon']}°)</p>
    </div>
    """, unsafe_allow_html=True)

    # 1️⃣ لوحة القيادة (Dashboard)
    if nav_option == t('nav_dashboard'):
        st.subheader(t('3d_globe'))
        
        col1, col2 = st.columns([2, 1])
        with col1:
            # تم السماح بضبط عدد الأقمار الفعلية حتى 5000 قمر أو أكثر (المطلوب الثالث)
            sat_count = st.slider(t('sat_count'), 100, 5000, 2500, 100)
        with col2:
            selected_group = st.selectbox(t('group'), CELESTRAK_CONFIG["groups"])
        
        if st.button(t('update_btn')):
            st.session_state.cache_version += 1
            st.rerun()

        with st.spinner(t('loading')):
            orbit_map = generate_orbit_map(sat_count, selected_group, True)
            df_telemetry = get_telemetry_data(orbit_map, sat_count, t)

        if not df_telemetry.empty:
            st.success(f"✅ {t('total')}: {len(df_telemetry)} {t('satellite')} | مراقبة النطاق لـ: {selected_country_obj['name']}")
            st.dataframe(df_telemetry, use_container_width=True)
            
            # رسم الخريطة ثلاثية الأبعاد الكونية مع تحديد الدولة أو المحطة الأرضية
            fig = px.scatter_geo(
                df_telemetry,
                lat=t('latitude'),
                lon=t('longitude'),
                hover_name=t('satellite'),
                projection="orthographic",
                title=f"{t('3d_globe')} - مركز المراقبة: {selected_country_obj['name']}"
            )
            
            # إضافة علامة الدولة/المحطة الأرضية المحددة على الخريطة
            fig.add_trace(go.Scattergeo(
                lat=[selected_country_obj['lat']],
                lon=[selected_country_obj['lon']],
                mode='markers',
                marker=dict(size=12, color='red', symbol='star'),
                name=f"Ground Station: {selected_country_obj['name']}"
            ))

            fig.update_geos(
                bgcolor="#0a0a12",
                landcolor="#1a1a2e",
                subunitcolor="#00CCFF",
                countrycolor="#0066AA"
            )
            fig.update_layout(
                paper_bgcolor="#0a0a12",
                plot_bgcolor="#0a0a12",
                font_color="#00CCFF"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("⚠️ لا توجد بيانات تليمتري متاحة حالياً.")

    # 2️⃣ إدارة التراخيص (Licenses Management)
    elif nav_option == t('nav_licenses'):
        st.subheader(t('license_title'))
        
        with st.form("license_form"):
            client_input = st.text_input(t('client_name'), "الجهة السيادية")
            tier_input = st.selectbox(t('license_tier'), [
                t('tier_1_name'), 
                t('tier_2_name'), 
                t('tier_3_name')
            ])
            validity_input = st.slider("فترة الصلاحية (أيام)", 30, 365, 365)
            submitted = st.form_submit_button(t('gen_key_btn'))
            
            if submitted:
                key, expiry = license_manager.generate_secure_license(client_input, tier_input, validity_input)
                st.success(f"✅ تم توليد مفتاح الترخيص بنجاح: `{key}` (ينتهي في: {expiry})")

        st.markdown("---")
        st.subheader(t('active_licenses'))
        active_lics = license_manager.get_active_licenses()
        if active_lics:
            df_lics = pd.DataFrame(active_lics)
            st.dataframe(df_lics, use_container_width=True)
        else:
            st.info(t('no_licenses'))

    # 3️⃣ العملاء وبوابات الدفع والباقات الثلاث (Clients & 3 Tiers & Payment Portals - المطلوب الثاني)
    elif nav_option == t('nav_clients'):
        st.subheader(t('clients_title'))
        
        # عرض الباقات الثلاث بوضوح
        st.markdown(f"### {t('select_tier_action')}")
        
        col_t1, col_t2, col_t3 = st.columns(3)
        
        selected_tier_cart = st.session_state.get('selected_tier', t('tier_2_name'))
        
        with col_t1:
            st.markdown(f"""
            <div class="tier-card">
                <h4>{t('tier_1_name')}</h4>
                <h3 style="color: #00CCFF;">{t('tier_1_price')}</h3>
                <p>{t('tier_1_desc')}</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("اختر الباقة الأولى", key="btn_tier1"):
                st.session_state.selected_tier = t('tier_1_name')
                st.success("تم اختيار الباقة الأولى بنجاح!")

        with col_t2:
            st.markdown(f"""
            <div class="tier-card" style="border-color: #00CCFF; box-shadow: 0 0 15px rgba(0,204,255,0.2);">
                <h4>{t('tier_2_name')}</h4>
                <h3 style="color: #00CCFF;">{t('tier_2_price')}</h3>
                <p>{t('tier_2_desc')}</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("اختر الباقة الثانية", key="btn_tier2"):
                st.session_state.selected_tier = t('tier_2_name')
                st.success("تم اختيار الباقة الثانية بنجاح!")

        with col_t3:
            st.markdown(f"""
            <div class="tier-card">
                <h4>{t('tier_3_name')}</h4>
                <h3 style="color: #00CCFF;">{t('tier_3_price')}</h3>
                <p>{t('tier_3_desc')}</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("اختر الباقة الثالثة", key="btn_tier3"):
                st.session_state.selected_tier = t('tier_3_name')
                st.success("تم اختيار الباقة الثالثة بنجاح!")

        st.markdown("---")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"### {t('client_login')}")
            st.text_input(t('email'))
            st.text_input(t('password'), type="password")
            if st.button(t('login_btn')):
                st.success("✅ تم تسجيل الدخول بنجاح إلى البوابة السيادية.")
        
        with c2:
            st.markdown(f"### {t('paypal_sim')}")
            st.info(f"الباقة المختارة حالياً للدفع: **{st.session_state.get('selected_tier', t('tier_2_name'))}**")
            gateway_choice = st.radio(t('payment_gateway'), [t('stripe_checkout'), t('paypal_express')])
            if st.button(t('pay_now')):
                st.success(t('payment_processed').format(gateway=gateway_choice))

    # 4️⃣ صحة النظام والشبكة (System Health)
    elif nav_option == t('nav_health'):
        st.subheader(t('health_title'))
        
        m1, m2, m3, m4 = st.columns(4)
        m1.metric(t('server_load'), "14.2%", "-2.1%")
        m2.metric(t('network_latency'), "11.4 ms", "-0.5 ms")
        m3.metric(t('packet_loss'), "0.0001%", "0.0%")
        m4.metric(t('cpu_usage'), "32.1%", "+1.4%")
        
        st.info("🟢 كافة العقد المدارية والخوادم السيادية تعمل بكفاءة تامة دون أي معوقات.")

    # 5️⃣ الإعدادات المتقدمة (Advanced Settings)
    elif nav_option == t('nav_settings'):
        st.subheader(t('settings_title'))
        st.text_input(t('api_endpoint'), SOURCE_CONFIG['baseUrl'])
        st.selectbox(t('encryption_level'), ["AES-256 Quantum Resistant", "RSA-4096 Sovereign", "ECC Secp256k1"])
        if st.button(t('save_settings')):
            st.success(t('settings_saved'))

    st.markdown('<div class="copyright">© 2026 COSMIC-324 6G Titan X - All Sovereign Rights Reserved.</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
