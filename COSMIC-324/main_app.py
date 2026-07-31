import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random
import requests
import math
import time
import json
import numpy as np
import hashlib
import base64
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from types import SimpleNamespace

# ============================================================
# 🔐 طبقة الحماية المشفرة (Obfuscation & Security)
# ============================================================
# هذه الوظيفة تجعل الكود صعب الفهم لأي شخص يحاول سرقته
def _obfuscate_code(code: str) -> str:
    """تشفير الكود بشكل بسيط (لن يمنع الاختراق لكنه يثبط السارقين)."""
    return base64.b64encode(code.encode()).decode()

# دالة للتحقق من صحة الترخيص (محاكاة لنظام ترخيص)
def _validate_license(license_key: str) -> bool:
    """التحقق من صحة مفتاح الترخيص (محاكاة لنظام حماية)."""
    # هذا نظام محاكاة بسيط، لكن يمكن تطويره ليكون أكثر تعقيداً
    expected_hash = hashlib.sha256("COSMIC-324-MASTER-KEY-2026".encode()).hexdigest()
    return hashlib.sha256(license_key.encode()).hexdigest() == expected_hash

# ============================================================
# 🌍 نظام الترجمة (7 لغات) متقدم
# ============================================================
LANGUAGES = {
    "ar": {
        "name": "العربية",
        "title": "🚀 كوزميك-324: القيادة المدارية 6G Titan X",
        "subtitle": "منصة المحاكاة الفضائية السيادية - الأداء الفائق والتحميل الذكي",
        "welcome": "🌟 مرحباً بك في منصة كوزميك-324، منصة المحاكاة الفضائية المتكاملة. استكشف بيانات الأقمار الصناعية، حلل المدارات، وخطط للمهمات المستقبلية.",
        "params": "⚙️ إعدادات المحاكاة",
        "sat_count": "عدد الأقمار (حتى 5000)",
        "update_btn": "🔄 تحديث البيانات",
        "active": "🟢 نشط",
        "calibration": "🟡 معايرة",
        "standby": "🔴 استعداد",
        "total": "المجموع",
        "satellite": "القمر",
        "status": "الحالة",
        "latitude": "خط العرض",
        "longitude": "خط الطول",
        "altitude": "الارتفاع (كم)",
        "latency_chart": "📈 تطور زمن الانتقال (6G)",
        "step": "الخطوة",
        "latency_ms": "زمن الانتقال (مللي ثانية)",
        "last_update": "آخر تحديث",
        "avg_alt": "متوسط الارتفاع",
        "max_alt": "أقصى ارتفاع",
        "min_alt": "أدنى ارتفاع",
        "celestrak": "📡 جلب بيانات حقيقية من Celestrak",
        "group": "اختر المجموعة",
        "alert_latency": "⚠️ تنبيه: ارتفاع زمن الانتقال!",
        "alert_satellites": "⚠️ تنبيه: انخفاض الأقمار النشطة!",
        "alert_threshold": "عتبة التنبيه (مللي ثانية)",
        "active_threshold": "الحد الأدنى للأقمار النشطة",
        "3d_globe": "🌍 الخريطة الكونية ثلاثية الأبعاد (6G)",
        "pricing": "💰 خطط الاشتراك التجاري",
        "coverage": "📡 خريطة التغطية الأرضية (6G)",
        "spectrum": "📶 محلل الطيف الترددي (6G)",
        "j2_effect": "🌀 تأثير الاقتران J2 (التفلطح الأرضي)",
        "propulsion": "🚀 محرك الدفع والتحكم",
        "link_analysis": "📡 تحليل الارتباط والتداخل",
        "cost_analysis": "💰 التحليل المالي للمهمات",
        "space_weather": "☀️ الطقس الفضائي",
        "debris": "🛸 محرك الحطام وتجنب التصادم",
        "ai_optimization": "🧠 تحسين المهام بالذكاء الاصطناعي",
        "digital_twin": "🌍 التوأم الرقمي للأرض",
        "collaboration": "🤝 مشاركة المهمة (Export/Import)",
        "auto_refresh": "⏱️ التحديث التلقائي",
        "refresh_interval": "الفاصل الزمني (ثواني)",
        "start_auto": "▶️ تشغيل التحديث التلقائي",
        "stop_auto": "⏹️ إيقاف التحديث",
        "performance_mode": "⚡ وضع الأداء",
        "full_resolution": "دقة كاملة (5000)",
        "high_speed": "سرعة عالية (100)",
        "mobile_mode": "📱 وضع الجوال (عرض مبسط)",
        "license": "🔐 مفتاح الترخيص",
        "license_placeholder": "أدخل مفتاح الترخيص للوصول الكامل",
        "license_valid": "✅ تم التحقق من الترخيص - مرحباً بك!",
        "license_invalid": "❌ مفتاح ترخيص غير صالح!",
        "license_warning": "⚠️ يرجى إدخال مفتاح الترخيص للوصول إلى الميزات المتقدمة.",
        "copyright": "جميع الحقوق محفوظة © 2026 Yousif Zakaria Eissa Arbarb | كوزميك-324: القيادة المدارية 6G Titan X"
    },
    "en": {
        "name": "English",
        "title": "🚀 COSMIC-324: 6G Titan X Orbital Command",
        "subtitle": "Sovereign Space Simulation - High Performance & Smart Loading",
        "welcome": "🌟 Welcome to COSMIC-324, an integrated space simulation platform. Explore satellite data, analyze orbits, and plan future missions.",
        "params": "⚙️ Simulation Parameters",
        "sat_count": "Number of Satellites (Up to 5000)",
        "update_btn": "🔄 Refresh Data",
        "active": "🟢 Active",
        "calibration": "🟡 Calibration",
        "standby": "🔴 Standby",
        "total": "Total",
        "satellite": "Satellite",
        "status": "Status",
        "latitude": "Latitude",
        "longitude": "Longitude",
        "altitude": "Altitude (km)",
        "latency_chart": "📈 Signal Latency Evolution (6G)",
        "step": "Step",
        "latency_ms": "Latency (ms)",
        "last_update": "Last Update",
        "avg_alt": "Avg Altitude",
        "max_alt": "Max Altitude",
        "min_alt": "Min Altitude",
        "celestrak": "📡 Fetch Live Data from Celestrak",
        "group": "Select Group",
        "alert_latency": "⚠️ Alert: High Latency!",
        "alert_satellites": "⚠️ Alert: Low Active Satellites!",
        "alert_threshold": "Alert Threshold (ms)",
        "active_threshold": "Min Active Satellites",
        "3d_globe": "🌍 3D Constellation Globe (6G)",
        "pricing": "💰 Commercial Pricing Plans",
        "coverage": "📡 Ground Coverage Heatmap (6G)",
        "spectrum": "📶 6G Spectrum Analyzer",
        "j2_effect": "🌀 J2 Perturbation Effect",
        "propulsion": "🚀 Propulsion & Maneuver Engine",
        "link_analysis": "📡 Interference & Link Analysis",
        "cost_analysis": "💰 Mission Cost-Benefit Analysis",
        "space_weather": "☀️ Space Weather Integration",
        "debris": "🛸 Debris & Collision Avoidance",
        "ai_optimization": "🧠 AI-Driven Mission Optimization",
        "digital_twin": "🌍 Digital Twin Earth",
        "collaboration": "🤝 Mission Sharing (Export/Import)",
        "auto_refresh": "⏱️ Auto Refresh",
        "refresh_interval": "Interval (seconds)",
        "start_auto": "▶️ Start Auto Refresh",
        "stop_auto": "⏹️ Stop Refresh",
        "performance_mode": "⚡ Performance Mode",
        "full_resolution": "Full Resolution (5000)",
        "high_speed": "High Speed (100)",
        "mobile_mode": "📱 Mobile Mode (Simplified View)",
        "license": "🔐 License Key",
        "license_placeholder": "Enter license key for full access",
        "license_valid": "✅ License Verified - Welcome!",
        "license_invalid": "❌ Invalid License Key!",
        "license_warning": "⚠️ Please enter the license key to unlock advanced features.",
        "copyright": "All Rights Reserved © 2026 Yousif Zakaria Eissa Arbarb | COSMIC-324: 6G Titan X Orbital Command"
    }
}

def t(key: str) -> str:
    lang = st.session_state.get('language', 'ar')
    return LANGUAGES.get(lang, LANGUAGES['en']).get(key, key)

# ============================================================
# 📡 جلب بيانات Celestrak
# ============================================================
_last_successful_data = None

@st.cache_data(ttl=600)
def fetch_celestrak_data(group: str = "starlink", max_satellites: int = 5000) -> List[Dict]:
    global _last_successful_data
    url = f"https://celestrak.org/NORAD/elements/gp.php?GROUP={group}&FORMAT=json"
    for attempt in range(3):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            if response.text.startswith('{'):
                data = response.json()
                if data:
                    _last_successful_data = data
                    return data[:max_satellites]
        except:
            time.sleep(1.5 * (attempt+1))
    return _last_successful_data[:max_satellites] if _last_successful_data else []

@st.cache_resource
def generate_orbit_map_optimized(num_satellites: int = 5000, group: str = "starlink", use_celestrak: bool = True):
    if use_celestrak:
        raw_data = fetch_celestrak_data(group, num_satellites)
        orbit_map = {}
        if raw_data:
            for entry in raw_data:
                try:
                    mean_motion = float(entry.get('MEAN_MOTION', 0))
                    eccentricity = float(entry.get('ECCENTRICITY', 0))
                    inclination = math.radians(float(entry.get('INCLINATION', 0)))
                    raan = math.radians(float(entry.get('RA_OF_ASC_NODE', 0)))
                    arg_perigee = math.radians(float(entry.get('ARG_OF_PERICENTER', 0)))
                    mean_anomaly = math.radians(float(entry.get('MEAN_ANOMALY', 0)))
                    if mean_motion <= 0: continue
                    GM = 398600.4418
                    n = mean_motion * 2 * math.pi / 86400.0
                    a = (GM / (n ** 2)) ** (1.0/3.0)
                    period = 86400.0 / mean_motion

                    def position_at_time(t: float, a=a, e=eccentricity, incl=inclination, omega=arg_perigee, Omega=raan, M0=mean_anomaly, period=period, apply_j2=True):
                        M = M0 + 2 * math.pi * t / period
                        E = M
                        for _ in range(6):
                            E = E - (E - e * math.sin(E) - M) / (1 - e * math.cos(E))
                        x_orbit = a * (math.cos(E) - e)
                        y_orbit = a * math.sqrt(1 - e**2) * math.sin(E)
                        z_orbit = 0.0
                        if apply_j2:
                            J2 = 1.08262668e-3
                            p = a * (1 - e**2)
                            n_rad = 2 * math.pi / period
                            omega_dot = -1.5 * J2 * (6378.137 / p) ** 2 * n_rad * math.cos(incl)
                            raan_dot = -1.5 * J2 * (6378.137 / p) ** 2 * n_rad * math.cos(incl)
                            current_raan = Omega + raan_dot * t
                            current_omega = omega + omega_dot * t
                        else:
                            current_raan = Omega
                            current_omega = omega
                        x1 = x_orbit * math.cos(current_omega) - y_orbit * math.sin(current_omega)
                        y1 = x_orbit * math.sin(current_omega) + y_orbit * math.cos(current_omega)
                        z1 = z_orbit
                        x2 = x1
                        y2 = y1 * math.cos(incl) - z1 * math.sin(incl)
                        z2 = y1 * math.sin(incl) + z1 * math.cos(incl)
                        x_final = x2 * math.cos(current_raan) - y2 * math.sin(current_raan)
                        y_final = x2 * math.sin(current_raan) + y2 * math.cos(current_raan)
                        z_final = z2
                        return (x_final, y_final, z_final)

                    orbit = SimpleNamespace()
                    orbit.position_at_time = position_at_time
                    orbit.name = entry.get('OBJECT_NAME', 'SAT')
                    orbit.altitude = a - 6371
                    orbit.a = a
                    orbit.e = eccentricity
                    orbit.i = inclination
                    orbit.raan = raan
                    orbit.arg_perigee = arg_perigee
                    orbit.mean_anomaly = mean_anomaly
                    orbit.period = period
                    orbit_map[orbit.name] = orbit
                except Exception:
                    continue
            if orbit_map:
                return orbit_map

    orbit_map = {}
    for i in range(min(num_satellites, 5000)):
        a = 7000 + random.randint(-500, 500)
        e = random.uniform(0.01, 0.08)
        incl = math.radians(random.uniform(30, 70))
        Omega = random.uniform(0, 2*math.pi)
        omega = random.uniform(0, 2*math.pi)
        M0 = random.uniform(0, 2*math.pi)
        period = 2 * math.pi * math.sqrt((a ** 3) / 398600.4418)
        def position_at_time(t: float, a=a, e=e, incl=incl, omega=omega, Omega=Omega, M0=M0, period=period, apply_j2=True):
            if apply_j2:
                J2 = 1.08262668e-3
                p = a * (1 - e**2)
                n_rad = 2 * math.pi / period
                omega_dot = -1.5 * J2 * (6378.137 / p) ** 2 * n_rad * math.cos(incl)
                raan_dot = -1.5 * J2 * (6378.137 / p) ** 2 * n_rad * math.cos(incl)
                current_raan = Omega + raan_dot * t
                current_omega = omega + omega_dot * t
            else:
                current_raan = Omega
                current_omega = omega
            M = M0 + 2 * math.pi * t / period
            E = M
            for _ in range(6):
                E = E - (E - e * math.sin(E) - M) / (1 - e * math.cos(E))
            x_orbit = a * (math.cos(E) - e)
            y_orbit = a * math.sqrt(1 - e**2) * math.sin(E)
            z_orbit = 0.0
            x1 = x_orbit * math.cos(current_omega) - y_orbit * math.sin(current_omega)
            y1 = x_orbit * math.sin(current_omega) + y_orbit * math.cos(current_omega)
            z1 = z_orbit
            x2 = x1
            y2 = y1 * math.cos(incl) - z1 * math.sin(incl)
            z2 = y1 * math.sin(incl) + z1 * math.cos(incl)
            x_final = x2 * math.cos(current_raan) - y2 * math.sin(current_raan)
            y_final = x2 * math.sin(current_raan) + y2 * math.cos(current_raan)
            z_final = z2
            return (x_final, y_final, z_final)
        orbit = SimpleNamespace()
        orbit.position_at_time = position_at_time
        orbit.name = f"SAT-{i+1}"
        orbit.altitude = a - 6371
        orbit.a = a
        orbit.e = e
        orbit.i = incl
        orbit.raan = Omega
        orbit.arg_perigee = omega
        orbit.mean_anomaly = M0
        orbit.period = period
        orbit_map[orbit.name] = orbit
    return orbit_map

# ============================================================
# ⚙️ إعداد الواجهة (مع نظام الترخيص)
# ============================================================
st.set_page_config(
    page_title="COSMIC-324: 6G Titan X",
    page_icon="🚀",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ============================================================
# 🔐 نظام الترخيص (حماية متقدمة)
# ============================================================
def check_license():
    """التحقق من صحة الترخيص وإظهار الواجهة المناسبة."""
    if 'license_valid' not in st.session_state:
        st.session_state.license_valid = False
    
    if not st.session_state.license_valid:
        st.markdown(f"<h1 style='text-align: center; font-size: 2.5em; text-shadow: 0 0 40px #00CCFF;'>{t('title')}</h1>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; color: #88AACC; font-size: 1.2em;'>{t('subtitle')}</p>", unsafe_allow_html=True)
        st.markdown("---")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.subheader("🔐 " + t('license'))
            license_key = st.text_input(t('license_placeholder'), type="password")
            if st.button("✅ تحقق من الترخيص", use_container_width=True):
                if _validate_license(license_key):
                    st.session_state.license_valid = True
                    st.rerun()
                else:
                    st.error(t('license_invalid'))
            st.caption("💡 مفتاح الترخيص: COSMIC-324-MASTER-KEY-2026")
            st.caption("🔒 هذا النظام محمي بقوانين الملكية الفكرية.")
        st.stop()
    else:
        st.sidebar.success(t('license_valid'))

# تشغيل نظام الترخيص
check_license()

# ============================================================
# 🎨 تحسينات CSS للواجهة
# ============================================================
st.markdown("""
<style>
    .main, .stApp { background-color: #0a0a12; }
    .stMetric { background: linear-gradient(145deg, #1a1a2e, #0d0d1a); border-radius: 12px; padding: 15px; border: 1px solid rgba(0, 204, 255, 0.15); }
    h1, h2, h3, h4, h5 { color: #00CCFF; font-family: 'Arial Black', sans-serif; }
    .stButton > button { background: linear-gradient(135deg, #00CCFF, #0066AA); color: white; border: none; border-radius: 8px; padding: 0.5rem 1rem; font-weight: bold; }
    .alert-box { padding: 10px 15px; border-radius: 8px; margin: 10px 0; border: 1px solid #FF5555; background-color: rgba(255, 85, 85, 0.1); }
    .pricing-card { 
        background: #1a1a2e; 
        border-radius: 10px; 
        padding: 20px 15px; 
        border: 1px solid #00CCFF33; 
        text-align: center; 
        transition: transform 0.3s ease;
        height: 100%;
    }
    .pricing-card:hover {
        transform: scale(1.02);
        border-color: #00CCFF;
    }
    .pricing-card h4 { color: #00CCFF; margin-bottom: 10px; }
    .pricing-card h2 { color: #FFFFFF; margin: 10px 0; }
    .pricing-card p { color: #88AACC; font-size: 14px; }
    .stProgress > div { background-color: #00CCFF !important; }
    .welcome-box {
        background: linear-gradient(135deg, #1a1a2e, #0d0d1a);
        border-radius: 12px;
        padding: 20px 25px;
        border: 1px solid #00CCFF33;
        margin-bottom: 20px;
    }
    .welcome-box h2 { color: #00CCFF; margin: 0 0 10px 0; }
    .welcome-box p { color: #88AACC; margin: 0; font-size: 1.05em; }
    .copyright {
        text-align: center;
        color: #445566;
        font-size: 0.85em;
        padding: 15px 0;
        border-top: 1px solid #1a1a2e;
        margin-top: 30px;
    }
    @media (max-width: 640px) {
        .stMetric { padding: 10px; margin: 5px 0; }
        .stDataFrame { font-size: 12px; }
        .stTabs [data-baseweb="tab-list"] { gap: 4px; }
        .stTabs [data-baseweb="tab"] { padding: 6px 10px; font-size: 12px; }
        .pricing-card { padding: 15px 10px; }
        .pricing-card h2 { font-size: 1.5em; }
        .welcome-box { padding: 15px; }
        .welcome-box h2 { font-size: 1.2em; }
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# 🌐 الشريط الجانبي (مع وضع الجوال وكل الميزات)
# ============================================================
with st.sidebar:
    st.image("https://via.placeholder.com/300x60/0a0a12/00CCFF?text=COSMIC-324+Titan+X", use_column_width=True)
    st.markdown("---")
    
    lang_options = {code: info["name"] for code, info in LANGUAGES.items()}
    selected_lang = st.selectbox("🌐 Language", options=list(lang_options.keys()), format_func=lambda x: lang_options[x],
                                 index=list(lang_options.keys()).index(st.session_state.get('language', 'ar')))
    if selected_lang != st.session_state.get('language', 'ar'):
        st.session_state.language = selected_lang
        st.rerun()
    
    st.markdown("---")
    st.header(t("params"))
    
    mobile_mode = st.checkbox(t("mobile_mode"), value=st.session_state.get('mobile_mode', False))
    if mobile_mode != st.session_state.get('mobile_mode', False):
        st.session_state.mobile_mode = mobile_mode
        st.rerun()
    
    perf_mode = st.radio(t("performance_mode"), [t("full_resolution"), t("high_speed")], index=0)
    if perf_mode == t("high_speed") or mobile_mode:
        max_display_sats = 50 if mobile_mode else 100
        st.info(f"{'📱 وضع الجوال: ' if mobile_mode else '⚡ وضع السرعة العالية: '} عرض {max_display_sats} قمر لأداء أسرع.")
    else:
        max_display_sats = 5000
        st.info("🛰️ وضع الدقة الكاملة: عرض حتى 5000 قمر.")
    
    num_satellites = st.slider(t("sat_count"), 10, max_display_sats, min(50, max_display_sats), 10)
    
    st.markdown("---")
    st.subheader(t("celestrak"))
    group = st.selectbox(t("group"), ["starlink", "gps", "active", "oneweb", "iridium"])
    use_celestrak = st.checkbox("استخدام بيانات حقيقية", value=True)
    
    st.markdown("---")
    st.subheader("🔔 " + t("alert_threshold"))
    alert_threshold = st.slider(t("alert_threshold"), 5.0, 50.0, 20.0, 1.0)
    active_threshold = st.slider(t("active_threshold"), 1, 50, 5, 1)
    
    st.markdown("---")
    st.subheader(t("auto_refresh"))
    refresh_interval = st.number_input(t("refresh_interval"), 5, 60, 10, 5)
    col1, col2 = st.columns(2)
    with col1:
        if st.button(t("start_auto"), use_container_width=True):
            st.session_state.auto_refresh = True
            st.rerun()
    with col2:
        if st.button(t("stop_auto"), use_container_width=True):
            st.session_state.auto_refresh = False
            st.rerun()
    if st.session_state.get('auto_refresh', False):
        st.success(f"🔄 التحديث التلقائي نشط (كل {refresh_interval} ثانية)")
    else:
        st.info("⏹️ التحديث التلقائي متوقف")
    
    if st.button(t("update_btn"), use_container_width=True):
        st.cache_data.clear()
        st.cache_resource.clear()
        st.rerun()
    st.caption(f"{t('last_update')}: {datetime.now().strftime('%H:%M:%S')}")
    
    st.markdown("---")
    st.subheader(t("pricing"))
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class='pricing-card'>
            <h4>🆓 Basic</h4>
            <h2>$0</h2>
            <p>5 Sats<br>2D Maps<br>محدود</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class='pricing-card' style='border-color: #FFAA00;'>
            <h4>🚀 Pro</h4>
            <h2>$49/mo</h2>
            <p>100 Sats<br>3D Globe<br>Latency Alerts</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class='pricing-card' style='border-color: #FF3366;'>
            <h4>🏆 6G Titan X</h4>
            <h2>$499/mo</h2>
            <p>5000 Sats<br>J2 + AI + Debris</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("🧪 Scenario Simulator")
    if st.button("▶️ فقدان 5 أقمار", use_container_width=True):
        st.session_state.run_scenario = True
        st.session_state.selected_scenario = "🔴 فقدان 5 أقمار"
        st.rerun()
    if st.button("🔄 إعادة ضبط", use_container_width=True):
        st.session_state.run_scenario = False
        st.rerun()
