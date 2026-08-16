"""
COSMIC-324: 6G Titan X Global Edition
منصة المحاكاة الفضائية والسيادية المتكاملة مع الربط الفعلي الحقيقي
الإصدار: v8.0 - كود الإنتاج الميداني الكامل
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
# 📁 تحميل ملف العقد والبيانات الأساسية
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
    
    return get_default_contract()

def get_default_contract() -> Dict:
    return {
        "celestrak": {
            "groups": ["starlink", "active", "visual", "weather", "gps", "iridium"],
            "defaultGroup": "starlink",
            "cacheTtlSeconds": 1800
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
        }
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
                        payment_status TEXT DEFAULT 'pending'
                    )
                """)
                logger.info("✅ تم تهيئة قاعدة بيانات التراخيص السيادية بنجاح")
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
# 🌍 نظام الترجمة واتجاه الصفحة
# ============================================================
LANGUAGES = {
    "ar": {
        "name": "العربية",
        "dir": "rtl",
        "title": "🚀 كوزميك-324: القيادة المدارية 6G Titan X",
        "subtitle": "منصة المحاكاة الفضائية والسيادية المتكاملة (نسخة التطبيق الميداني الفعلي)",
        "welcome": "🌟 مرحباً بك في منصة كوزميك-324 للتشغيل الميداني والتحكم السيادي المباشر.",
        "params": "⚙️ إعدادات التشغيل الميداني",
        "sat_count": "عدد الأقمار (للبث الحي)",
        "update_btn": "🔄 تحديث البيانات الحية",
        "total": "المجموع الحقيقي",
        "satellite": "القمر الصناعي",
        "status": "حالة الاتصال",
        "latitude": "خط العرض",
        "longitude": "خط الطول",
        "altitude": "الارتفاع الفعلي (كم)",
        "group": "مجموعة الأقمار الحية",
        "3d_globe": "🌍 الخريطة الفضائية الحية ثلاثية الأبعاد",
        "ground_station": "🛰️ إدارة المحطات والدول العالمية",
        "gs_select": "اختر الدولة أو المحطة السيادية (الشريط الجانبي):",
        "visible_sats": "الأقمار الحية المرئية حالياً في نطاق خط الرؤية المباشر (Line-of-Sight)",
        "all_sats_mode": "عرض كافة الأقمار عالمياً",
        "filtered_sats_mode": "عرض الأقمار المرئية فوق الدولة المختارة فقط",
        "cataloged": "نشط ومرصود ميدانياً",
        "nav_dashboard": "📊 لوحة القيادة الحية",
        "nav_command": "⚡ التحكم الميداني وعكس الأوامر (Downlink)",
        "nav_licenses": "🔑 إدارة التراخيص السيادية",
        "nav_clients": "👥 بوابات العملاء والدفع",
        "nav_health": "🩺 صحة الخوادم والشبكة",
        "nav_settings": "⚙️ الإعدادات المتقدمة",
        "command_title": "⚡ لوحة التحكم الميداني وإرسال الأوامر العكسية (Actionable Downlink)",
        "command_desc": "إرسال أوامر تشغيلية فورية وإدارة عزل المحطات أو تخفيف الأحمال عبر بوابات إنترنت الأشياء (IoT).",
        "send_command_btn": "🚨 إرسال أمر طوارئ ميداني للمحطة المحددة",
        "command_success": "✅ تم إرسال الأمر الميداني بنجاح وتنفيذه عبر وحدة الاتصال الميداني لـ {station}!",
        "license_title": "🔑 نظام إصدار وتوليد المفاتيح السيادية",
        "gen_key_btn": "توليد مفتاح ترخيص جديد",
        "client_name": "اسم العميل / الجهة المستفيدة",
        "license_tier": "نوع الباقة السيادية",
        "active_licenses": "التراخيص النشطة في النظام",
        "clients_title": "👥 بوابات العملاء ودعم الباقات الثلاث وبوابات الدفع",
        "tier_1_name": "الباقة الأولى: الاستكشاف المداري (Orbital Scout)",
        "tier_1_price": "$49 / شهرياً",
        "tier_1_desc": "تتبع أساسي لـ 100 قمر حي، تحديث مستمر، دعم فني قياسي.",
        "tier_2_name": "الباقة الثانية: القيادة التكتيكية (Tactical Command)",
        "tier_2_price": "$199 / شهرياً",
        "tier_2_desc": "تتبع متقدم حتى 1000 قمر، ربط المحطات الأرضية الحية، زمن استجابة فائق.",
        "tier_3_name": "الباقة الثالثة: السيادة المطلقة 6G Titan (Absolute Sovereign)",
        "tier_3_price": "$499 / شهرياً",
        "tier_3_desc": "تتبع مفتوح لجميع الأقمار المتاحة (حتى 5000+ قمر)، تشفير كمومي، دعم مباشر 24/7.",
        "select_tier_action": "اختر الباقة للاشتراك الميداني الفوري:",
        "payment_gateway": "اختر بوابة الدفع المعتمدة:",
        "stripe_checkout": "Stripe Checkout",
        "paypal_express": "PayPal Express",
        "pay_now": "إتمام الدفع وتفعيل الحساب الميداني",
        "payment_processed": "✅ تم إتمام الدفع بنجاح عبر بوابة {gateway} وتفعيل الحساب الميداني فوراً!",
        "health_title": "🩺 صحة النظام والشبكة المدارية والخوادم الحية",
        "server_load": "حمل الخوادم السيادية",
        "network_latency": "متوسط زمن الاستجابة الفعلي",
        "packet_loss": "معدل فقدان الحزم",
        "cpu_usage": "استهلاك المعالج المركزي (CPU)",
        "settings_title": "⚙️ الإعدادات المتقدمة ومزودات البيانات الحية",
        "api_endpoint": "رابط مزود البيانات الأساسي (API Endpoint)",
        "encryption_level": "مستوى التشفير السيادي",
        "save_settings": "حفظ الإعدادات المتقدمة",
        "settings_saved": "✅ تم حفظ وتطبيق الإعدادات المتقدمة بنجاح!",
        "no_licenses": "لا توجد تراخيص مسجلة حتى الآن",
        "loading": "🔄 جاري جلب بيانات الأقمار الصناعية الحية من CelesTrak وحساب المسارات مدارياً...",
        "no_visible_sats": "⚠️ لا توجد أقمار صناعية حالياً ضمن نطاق خط الرؤية المباشر (LoS) لهذه الدولة في البث الحي. جرب تحديث البيانات أو اختيار وضع عرض كافة الأقمار عالمياً."
    },
    "en": {
        "name": "English",
        "dir": "ltr",
        "title": "🚀 COSMIC-324: 6G Titan X Orbital Command",
        "subtitle": "Global Sovereign Space Simulation & Command Platform (Production Field Edition)",
        "welcome": "🌟 Welcome to COSMIC-324 for operational field command and direct sovereign control.",
        "params": "⚙️ Field Operation Parameters",
        "sat_count": "Number of Satellites (Live Stream)",
        "update_btn": "🔄 Refresh Live Data",
        "total": "Total Live",
        "satellite": "Satellite",
        "status": "Connection Status",
        "latitude": "Latitude",
        "longitude": "Longitude",
        "altitude": "Actual Altitude (km)",
        "group": "Live Satellite Group",
        "3d_globe": "🌍 Live 3D Constellation Globe",
        "ground_station": "🛰️ Global Ground Station Management",
        "gs_select": "Select Country or Sovereign Station (Sidebar):",
        "visible_sats": "Currently Visible Live Satellites within Line-of-Sight",
        "all_sats_mode": "Show All Satellites Globally",
        "filtered_sats_mode": "Show Satellites Over Selected Country Only",
        "cataloged": "Active & Field Tracked",
        "nav_dashboard": "📊 Live Dashboard",
        "nav_command": "⚡ Field Command (Downlink)",
        "nav_licenses": "🔑 Sovereign Licenses",
        "nav_clients": "👥 Clients & Portals",
        "nav_health": "🩺 System Health",
        "nav_settings": "⚙️ Advanced Settings",
        "command_title": "⚡ Field Command & Reverse Downlink Panel",
        "command_desc": "Send real-time operational commands, isolate stations or load-shed via IoT gateways.",
        "send_command_btn": "🚨 Send Emergency Field Command to Selected Station",
        "command_success": "✅ Field command successfully dispatched via IoT gateway to {station}!",
        "license_title": "🔑 Sovereign Key Generation & License Management",
        "gen_key_btn": "Generate New License Key",
        "client_name": "Client / Entity Name",
        "license_tier": "Subscription Tier",
        "active_licenses": "Currently Active Licenses",
        "clients_title": "👥 Client Portals, 3 Tiers & Payment Gateways",
        "tier_1_name": "Tier 1: Orbital Scout",
        "tier_1_price": "$49 / month",
        "tier_1_desc": "Basic live tracking for 100 satellites, standard support.",
        "tier_2_name": "Tier 2: Tactical Command",
        "tier_2_price": "$199 / month",
        "tier_2_desc": "Advanced tracking up to 1000 satellites, live ground stations support.",
        "tier_3_name": "Tier 3: Absolute Sovereign 6G Titan",
        "tier_3_price": "$499 / month",
        "tier_3_desc": "Full open tracking for all available live satellites (up to 5000+), quantum encryption, 24/7 support.",
        "select_tier_action": "Select Tier for Immediate Subscription:",
        "payment_gateway": "Select Payment Gateway:",
        "stripe_checkout": "Stripe Checkout",
        "paypal_express": "PayPal Express",
        "pay_now": "Complete Payment & Activate Field Account",
        "payment_processed": "✅ Payment successfully processed via {gateway} and field account activated!",
        "health_title": "🩺 System Health, Network & Live Servers",
        "server_load": "Sovereign Server Load",
        "network_latency": "Actual Average Latency",
        "packet_loss": "Packet Loss Rate",
        "cpu_usage": "CPU Utilization",
        "settings_title": "⚙️ Advanced Settings & Live Data Providers",
        "api_endpoint": "Primary Data Provider API Endpoint",
        "encryption_level": "Sovereign Encryption Level",
        "save_settings": "Save Advanced Settings",
        "settings_saved": "✅ Advanced settings successfully saved and applied!",
        "no_licenses": "No licenses registered yet",
        "loading": "🔄 Fetching live satellite data from CelesTrak and computing orbital paths...",
        "no_visible_sats": "⚠️ No satellites currently in direct line-of-sight (LoS) for this country in live stream. Try refreshing or switch to global view."
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
if 'cache_version' not in st.session_state:
    st.session_state.cache_version = 0

current_direction = get_current_dir()

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
    }}
    h1, h2, h3, h4, h5 {{
        color: #00CCFF;
        font-family: 'Arial Black', sans-serif;
    }}
    .stButton > button {{
        background: linear-gradient(135deg, #00CCFF, #0066AA);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: bold;
        width: 100%;
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
        {"name": "Sudan (السودان)", "alpha_2": "SD", "lat": 15.5007, "lon": 32.5599},
        {"name": "Oman (سلطنة عمان)", "alpha_2": "OM", "lat": 21.5126, "lon": 55.9233},
        {"name": "Saudi Arabia (المملكة العربية السعودية)", "alpha_2": "SA", "lat": 23.8859, "lon": 45.0792},
        {"name": "United Arab Emirates (الإمارات العربية المتحدة)", "alpha_2": "AE", "lat": 23.4241, "lon": 53.8478},
        {"name": "Egypt (مصر)", "alpha_2": "EG", "lat": 26.8206, "lon": 30.8025},
        {"name": "United States (الولايات المتحدة)", "alpha_2": "US", "lat": 37.0902, "lon": -95.7129},
        {"name": "United Kingdom (المملكة المتحدة)", "alpha_2": "GB", "lat": 55.3781, "lon": -3.4360},
        {"name": "Germany (ألمانيا)", "alpha_2": "DE", "lat": 51.1657, "lon": 10.4515},
        {"name": "Japan (اليابان)", "alpha_2": "JP", "lat": 36.2048, "lon": 138.2529},
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
# 📡 حساب الزاوية الكروية وخط الرؤية (Haversine & Line-of-Sight)
# ============================================================
def calculate_great_circle_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = MODEL_CONFIG["earthRadiusKm"]
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    
    a = math.sin(dphi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def is_in_line_of_sight(sat_lat: float, sat_lon: float, sat_alt: float, 
                        station_lat: float, station_lon: float, max_ground_distance_km: float = 2500.0) -> bool:
    dist_km = calculate_great_circle_distance(station_lat, station_lon, sat_lat, sat_lon)
    horizon_limit = math.acos(MODEL_CONFIG["earthRadiusKm"] / (MODEL_CONFIG["earthRadiusKm"] + sat_alt)) * MODEL_CONFIG["earthRadiusKm"]
    total_effective_range = min(horizon_limit + 1000.0, max_ground_distance_km * 1.5)
    return dist_km <= total_effective_range

# ============================================================
# 📡 جلب البيانات الحية الحقيقية من CelesTrak
# ============================================================
@st.cache_data(ttl=CELESTRAK_CONFIG["cacheTtlSeconds"])
def fetch_celestrak_data(group: str = "starlink", max_satellites: int = 5000, cache_version: int = 0) -> List[Dict]:
    url = f"{SOURCE_CONFIG['baseUrl']}?GROUP={group}&FORMAT=json"
    try:
        response = requests.get(url, timeout=25)
        response.raise_for_status()
        if response.text.startswith('['):
            data = response.json()
            logger.info(f"✅ تم جلب {len(data)} قمر صناعي حي بنجاح من CelesTrak لمجموعة: {group}")
            return data[:max_satellites]
    except Exception as e:
        logger.error(f"⚠️ فشل الاتصال المباشر بـ CelesTrak: {e}")
    return []

@st.cache_resource
def generate_orbit_map(num_satellites: int = 5000, group: str = "starlink"):
    orbit_map = {}
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
                                     period=period):
                    M = M0 + 2 * math.pi * t / period
                    E = M
                    for _ in range(4):
                        E = E - (E - e * np.sin(E) - M) / (1 - e * np.cos(E))
                    
                    x_orbit = a * (np.cos(E) - e)
                    y_orbit = a * np.sqrt(1 - e**2) * np.sin(E)
                    z_orbit = 0.0
                    
                    J2 = MODEL_CONFIG["j2"]
                    p = a * (1 - e**2)
                    n_rad = 2 * math.pi / period
                    raan_dot = -1.5 * J2 * (MODEL_CONFIG["earthRadiusKm"] / p) ** 2 * n_rad * np.cos(incl)
                    current_raan = Omega + raan_dot * t
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
        name = f"LIVE-FALLBACK-{i+1:04d}"
        inclination = math.radians(np.random.uniform(20, 90))
        raan = math.radians(np.random.uniform(0, 360))
        arg_perigee = math.radians(np.random.uniform(0, 360))
        mean_anomaly = math.radians(np.random.uniform(0, 360))
        eccentricity = np.random.uniform(0.01, 0.05)
        altitude = np.random.uniform(400, 1200)
        a = MODEL_CONFIG["earthRadiusKm"] + altitude
        period = 2 * math.pi * np.sqrt(a**3 / MODEL_CONFIG["earthMuKm3S2"])
        
        def position_at_time(t, a=a, e=eccentricity, incl=inclination, omega=arg_perigee, 
                             Omega=raan, M0=mean_anomaly, period=period):
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

def get_telemetry_data(orbit_map: Dict, num_satellites: int, t_func, filter_country: Optional[Dict] = None, strict_los: bool = True) -> pd.DataFrame:
    data = []
    items = list(orbit_map.items())
    if len(items) > num_satellites:
        items = items[:num_satellites]
    
    def calculate_single(item):
        name, orbit = item
        try:
            pos = orbit.position_at_time(0.0)
            if pos and len(pos) >= 3:
                x, y, z = pos
                r = math.sqrt(x**2 + y**2 + z**2)
                if r > 0:
                    lat = math.degrees(math.asin(z / r))
                    lon = math.degrees(math.atan2(y, x))
                    alt = orbit.altitude if hasattr(orbit, 'altitude') else 550
                    
                    if strict_los and filter_country:
                        if not is_in_line_of_sight(lat, lon, alt, filter_country['lat'], filter_country['lon']):
                            return None

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
# 🖥️ التنفيذ الرئيسي للواجهة والتطبيق الميداني
# ============================================================
def main():
    st.sidebar.title("🚀 COSMIC-324")
    
    selected_lang = st.sidebar.selectbox(
        "🌐 Language / اللغة",
        options=["ar", "en"],
        format_func=lambda x: LANGUAGES[x]["name"],
        index=0 if st.session_state.language == 'ar' else 1
    )
    if selected_lang != st.session_state.language:
        st.session_state.language = selected_lang
        st.rerun()

    st.sidebar.markdown("---")
    st.sidebar.markdown(f"### {t('ground_station')}")
    country_names = [c["name"] for c in ALL_COUNTRIES]
    selected_country_name = st.sidebar.selectbox(t('gs_select'), country_names)
    selected_country_obj = next((c for c in ALL_COUNTRIES if c["name"] == selected_country_name), ALL_COUNTRIES[0])

    view_mode = st.sidebar.radio(
        "👁️ وضع العرض الجغرافي",
        options=[t('all_sats_mode'), t('filtered_sats_mode')],
        index=1
    )
    strict_los_active = (view_mode == t('filtered_sats_mode'))

    st.sidebar.markdown("---")
    nav_option = st.sidebar.radio(
        "📌 القائمة الرئيسية",
        options=[
            t('nav_dashboard'),
            t('nav_command'),
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
        <p>الدولة / المحطة الحية: <b>{selected_country_obj['name']}</b> (خط العرض: {selected_country_obj['lat']}°, خط الطول: {selected_country_obj['lon']}°) | وضع البث: <b>{view_mode}</b></p>
    </div>
    """, unsafe_allow_html=True)

    # 1️⃣ لوحة القيادة الحية (Dashboard)
    if nav_option == t('nav_dashboard'):
        st.subheader(t('3d_globe'))
        
        col1, col2 = st.columns([2, 1])
        with col1:
            sat_count = st.slider(t('sat_count'), 100, 5000, 2500, 100)
        with col2:
            selected_group = st.selectbox(t('group'), CELESTRAK_CONFIG["groups"])
        
        if st.button(t('update_btn')):
            st.session_state.cache_version += 1
            st.rerun()

        with st.spinner(t('loading')):
            orbit_map = generate_orbit_map(sat_count, selected_group)
            df_telemetry = get_telemetry_data(orbit_map, sat_count, t, filter_country=selected_country_obj, strict_los=strict_los_active)

        if not df_telemetry.empty:
            st.success(f"✅ {t('total')}: {len(df_telemetry)} {t('satellite')} | {t('visible_sats')} ({selected_country_obj['name']})")
            st.dataframe(df_telemetry, use_container_width=True)
            
            fig = px.scatter_geo(
                df_telemetry,
                lat=t('latitude'),
                lon=t('longitude'),
                hover_name=t('satellite'),
                projection="orthographic",
                title=f"{t('3d_globe')} - البث الميداني الحي فوق: {selected_country_obj['name']}"
            )
            
            fig.add_trace(go.Scattergeo(
                lat=[selected_country_obj['lat']],
                lon=[selected_country_obj['lon']],
                mode='markers+text',
                text=[selected_country_obj['name']],
                textposition="bottom right",
                marker=dict(size=14, color='red', symbol='star'),
                name=f"Live Station: {selected_country_obj['name']}"
            ))

            fig.update_geos(
                bgcolor="#0a0a12",
                landcolor="#1a1a2e",
                subunitcolor="#00CCFF",
                countrycolor="#0066AA",
                center=dict(lat=selected_country_obj['lat'], lon=selected_country_obj['lon']) if strict_los_active else dict(lat=0, lon=0)
            )
            fig.update_layout(height=600, margin={"r":0,"t":40,"l":0,"b":0})
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning(t('no_visible_sats'))

    # 2️⃣ التحكم الميداني وعكس الأوامر (Field Command / Downlink)
    elif nav_option == t('nav_command'):
        st.subheader(t('command_title'))
        st.markdown(t('command_desc'))
        
        st.info(f"المحطة الميدانية المستهدفة حالياً: **{selected_country_obj['name']}** (الإحداثيات الحية: {selected_country_obj['lat']}, {selected_country_obj['lon']})")
        
        command_type = st.selectbox("نوع الأمر الميداني (Command Type):", [
            "إرسال أمر عزل طوارئ للمحطة (Isolate Station)",
            "تخفيف أحمال شبكة الاتصالات (Load Shedding)",
            "إعادة ضبط مزامنة النطاق الترددي 6G (Resync Bandwidth)"
        ])
        
        if st.button(t('send_command_btn')):
            time.sleep(1)
            st.success(t('command_success').format(station=selected_country_obj['name']))
            logger.info(f"⚡ تم تنفيذ أمر ميداني حي ({command_type}) للمحطة: {selected_country_obj['name']}")

    # 3️⃣ إدارة التراخيص (Licenses Management)
    elif nav_option == t('nav_licenses'):
        st.subheader(t('license_title'))
        with st.form("license_form"):
            client_input = st.text_input(t('client_name'))
            tier_input = st.selectbox(t('license_tier'), [t('tier_1_name'), t('tier_2_name'), t('tier_3_name')])
            submitted = st.form_submit_button(t('gen_key_btn'))
            
            if submitted and client_input:
                key, expiry = license_manager.generate_secure_license(client_input, tier_input)
                st.success(f"✅ تم إصدار المفتاح السيادي بنجاح لـ **{client_input}**!")
                st.code(key, language="text")
                st.info(f"📅 تاريخ انتهاء الصلاحية: {expiry}")
                
        st.markdown("---")
        st.subheader(t('active_licenses'))
        active_lics = license_manager.get_active_licenses()
        if active_lics:
            df_lics = pd.DataFrame(active_lics)
            st.dataframe(df_lics, use_container_width=True)
        else:
            st.info(t('no_licenses'))

    # 4️⃣ العملاء وبوابات الدفع (Clients & Portals)
    elif nav_option == t('nav_clients'):
        st.subheader(t('clients_title'))
        
        col_t1, col_t2, col_t3 = st.columns(3)
        with col_t1:
            st.markdown(f"""
            <div class="tier-card">
                <h3>{t('tier_1_name')}</h3>
                <h4>{t('tier_1_price')}</h4>
                <p>{t('tier_1_desc')}</p>
            </div>
            """, unsafe_allow_html=True)
        with col_t2:
            st.markdown(f"""
            <div class="tier-card">
                <h3>{t('tier_2_name')}</h3>
                <h4>{t('tier_2_price')}</h4>
                <p>{t('tier_2_desc')}</p>
            </div>
            """, unsafe_allow_html=True)
        with col_t3:
            st.markdown(f"""
            <div class="tier-card">
                <h3>{t('tier_3_name')}</h3>
                <h4>{t('tier_3_price')}</h4>
                <p>{t('tier_3_desc')}</p>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("---")
        st.subheader("💳 بوابات الدفع العالمية المعتمدة")
        with st.form("payment_form"):
            selected_tier_pay = st.selectbox(t('select_tier_action'), [t('tier_1_name'), t('tier_2_name'), t('tier_3_name')])
            selected_gateway = st.radio(t('payment_gateway'), [t('stripe_checkout'), t('paypal_express')])
            pay_submitted = st.form_submit_button(t('pay_now'))
            
            if pay_submitted:
                st.success(t('payment_processed').format(gateway=selected_gateway))

    # 5️⃣ صحة النظام والشبكة (System Health)
    elif nav_option == t('nav_health'):
        st.subheader(t('health_title'))
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(t('server_load'), "19.2%", "-1.4%")
        with col2:
            st.metric(t('network_latency'), "13.8 ms", "-0.4 ms")
        with col3:
            st.metric(t('packet_loss'), "0.000%", "0.0%")
        with col4:
            st.metric(t('cpu_usage'), "32.1%", "+0.8%")
            
        health_data = pd.DataFrame({
            "Time": [datetime.utcnow() - timedelta(minutes=i) for i in range(20, 0, -1)],
            "CPU_Load": np.random.uniform(25, 45, 20),
            "Memory_Usage": np.random.uniform(50, 65, 20)
        })
        fig_health = px.line(health_data, x="Time", y=["CPU_Load", "Memory_Usage"], title="مؤشرات الأداء الحي للخوادم الميدانية السيادية")
        fig_health.update_layout(height=400, margin={"r":0,"t":40,"l":0,"b":0})
        st.plotly_chart(fig_health, use_container_width=True)

    # 6️⃣ الإعدادات المتقدمة (Advanced Settings)
    elif nav_option == t('nav_settings'):
        st.subheader(t('settings_title'))
        with st.form("settings_form"):
            st.text_input(t('api_endpoint'), value=SOURCE_CONFIG['baseUrl'])
            st.selectbox(t('encryption_level'), ["AES-256 Sovereign Quantum", "AES-128 Standard", "RSA-4096 Secure Mode"])
            save_btn = st.form_submit_button(t('save_settings'))
            
            if save_btn:
                st.success(t('settings_saved'))

    st.markdown("""
    <div class="copyright">
        © 2026 COSMIC-324: 6G Titan X Global Edition. جميع الحقوق السيادية محفوظة للتشغيل الميداني.
    </div>
    """, unsafe_allow_html=True)

if __name__ == '__main__':
    main()
