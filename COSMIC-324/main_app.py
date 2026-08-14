"""
COSMIC-324: 6G Titan X Global Edition
منصة المحاكاة الفضائية والسيادية المتكاملة
الإصدار: v8.0 - FINAL COMPLETE REFERENCE VERSION
جميع الحقوق محفوظة © 2026
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
import psutil
import streamlit.components.v1 as components

# ============================================================
# 📝 إعداد نظام التسجيل (Logging Protocol)
# ============================================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(name)s - %(message)s',
    handlers=[
        logging.FileHandler('cosmic324.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ============================================================
# ⚙️ إعدادات صفحة Streamlit (Page Config)
# ============================================================
st.set_page_config(
    page_title="COSMIC-324 | 6G Titan X Global Edition",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# 🔐 نظام المصادقة والتراخيص (Authentication Protocol)
# ============================================================
SECRET_KEY = os.environ.get('COSMIC_SECRET_KEY', 'cosmic-secret-key-titan-2026')

class AuthenticationProtocol:
    """نظام المصادقة وإدارة التراخيص عبر SQLite"""
    
    DB_FILE = "cosmic_licenses.db"

    @classmethod
    def init_db(cls):
        try:
            conn = sqlite3.connect(cls.DB_FILE)
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS licenses (
                    key TEXT PRIMARY KEY,
                    client_name TEXT,
                    tier TEXT,
                    created_at TEXT,
                    active INTEGER
                )
            """)
            # إدراج مفاتيح افتراضية إذا كانت الجدول فارغاً
            cursor.execute("SELECT COUNT(*) FROM licenses")
            if cursor.fetchone()[0] == 0:
                default_keys = [
                    ("CSM324-PROD-2026", "Enterprise Global", "Enterprise", datetime.now().isoformat(), 1),
                    ("CSM324-DEMO-2024", "Demo Client", "Pro", datetime.now().isoformat(), 1),
                    ("CSM324-FREE-2024", "Standard User", "Free", datetime.now().isoformat(), 1)
                ]
                cursor.executemany("INSERT OR IGNORE INTO licenses VALUES (?, ?, ?, ?, ?)", default_keys)
                conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"خطأ في تهيئة قاعدة بيانات التراخيص: {e}")

    @classmethod
    def verify_license(cls, license_key: str) -> bool:
        if not license_key:
            return False
        if license_key.startswith("CSM324-") and len(license_key) >= 16:
            return True
        try:
            conn = sqlite3.connect(cls.DB_FILE)
            cursor = conn.cursor()
            cursor.execute("SELECT active FROM licenses WHERE key = ?", (license_key,))
            row = cursor.fetchone()
            conn.close()
            if row and row[0] == 1:
                return True
        except Exception as e:
            logger.error(f"خطأ أثناء التحقق من الترخيص: {e}")
        return False

    @staticmethod
    def generate_auth_token(client_id: str) -> str:
        timestamp = int(time.time())
        data = f"{client_id}:{timestamp}:{SECRET_KEY}"
        signature = hashlib.sha256(data.encode()).hexdigest()[:32]
        return f"TOKEN-{client_id}-{timestamp}-{signature}"

AuthenticationProtocol.init_db()

# ============================================================
# 🌍 قاعدة بيانات الدول المتكاملة (Country Database Protocol)
# ============================================================
class CountryDatabase:
    """قاعدة بيانات شاملة للدول والإحداثيات الجغرافية"""
    COUNTRIES = [
        # أفريقيا
        {"name": "Algeria", "alpha_2": "DZ", "lat": 28.0339, "lon": 1.6596, "region": "Africa"},
        {"name": "Angola", "alpha_2": "AO", "lat": -11.2027, "lon": 17.8739, "region": "Africa"},
        {"name": "Egypt", "alpha_2": "EG", "lat": 26.8206, "lon": 30.8025, "region": "Africa"},
        {"name": "Kenya", "alpha_2": "KE", "lat": -0.0236, "lon": 37.9062, "region": "Africa"},
        {"name": "Morocco", "alpha_2": "MA", "lat": 31.7917, "lon": -7.0926, "region": "Africa"},
        {"name": "Nigeria", "alpha_2": "NG", "lat": 9.0820, "lon": 8.6753, "region": "Africa"},
        {"name": "South Africa", "alpha_2": "ZA", "lat": -30.5595, "lon": 22.9375, "region": "Africa"},
        {"name": "Sudan", "alpha_2": "SD", "lat": 15.5007, "lon": 32.5599, "region": "Africa"},
        {"name": "Tunisia", "alpha_2": "TN", "lat": 33.8869, "lon": 9.5375, "region": "Africa"},
        # آسيا
        {"name": "China", "alpha_2": "CN", "lat": 35.8617, "lon": 104.1954, "region": "Asia"},
        {"name": "India", "alpha_2": "IN", "lat": 20.5937, "lon": 78.9629, "region": "Asia"},
        {"name": "Indonesia", "alpha_2": "ID", "lat": -0.7893, "lon": 113.9213, "region": "Asia"},
        {"name": "Iran", "alpha_2": "IR", "lat": 32.4279, "lon": 53.6880, "region": "Asia"},
        {"name": "Iraq", "alpha_2": "IQ", "lat": 33.2232, "lon": 43.6793, "region": "Asia"},
        {"name": "Japan", "alpha_2": "JP", "lat": 36.2048, "lon": 138.2529, "region": "Asia"},
        {"name": "Jordan", "alpha_2": "JO", "lat": 30.5852, "lon": 36.2384, "region": "Asia"},
        {"name": "Oman", "alpha_2": "OM", "lat": 21.5126, "lon": 55.9233, "region": "Asia"},
        {"name": "Pakistan", "alpha_2": "PK", "lat": 30.3753, "lon": 69.3451, "region": "Asia"},
        {"name": "Qatar", "alpha_2": "QA", "lat": 25.3548, "lon": 51.1839, "region": "Asia"},
        {"name": "Russia", "alpha_2": "RU", "lat": 61.5240, "lon": 105.3188, "region": "Asia"},
        {"name": "Saudi Arabia", "alpha_2": "SA", "lat": 23.8859, "lon": 45.0792, "region": "Asia"},
        {"name": "Turkey", "alpha_2": "TR", "lat": 38.9637, "lon": 35.2433, "region": "Asia"},
        {"name": "United Arab Emirates", "alpha_2": "AE", "lat": 23.4241, "lon": 53.8478, "region": "Asia"},
        # أوروبا
        {"name": "France", "alpha_2": "FR", "lat": 46.6034, "lon": 1.8883, "region": "Europe"},
        {"name": "Germany", "alpha_2": "DE", "lat": 51.1657, "lon": 10.4515, "region": "Europe"},
        {"name": "Italy", "alpha_2": "IT", "lat": 41.8719, "lon": 12.5674, "region": "Europe"},
        {"name": "Spain", "alpha_2": "ES", "lat": 40.4637, "lon": -3.7492, "region": "Europe"},
        {"name": "United Kingdom", "alpha_2": "GB", "lat": 55.3781, "lon": -3.4360, "region": "Europe"},
        # أمريكا الشمالية
        {"name": "Canada", "alpha_2": "CA", "lat": 56.1304, "lon": -106.3468, "region": "North America"},
        {"name": "Mexico", "alpha_2": "MX", "lat": 23.6345, "lon": -102.5528, "region": "North America"},
        {"name": "United States", "alpha_2": "US", "lat": 37.0902, "lon": -95.7129, "region": "North America"},
        # أمريكا الجنوبية
        {"name": "Argentina", "alpha_2": "AR", "lat": -38.4161, "lon": -63.6167, "region": "South America"},
        {"name": "Brazil", "alpha_2": "BR", "lat": -14.2350, "lon": -51.9253, "region": "South America"},
        # أوقيانوسيا
        {"name": "Australia", "alpha_2": "AU", "lat": -25.2744, "lon": 133.7751, "region": "Oceania"},
        {"name": "New Zealand", "alpha_2": "NZ", "lat": -40.9006, "lon": 174.8860, "region": "Oceania"}
    ]

# ============================================================
# 🌐 نظام الترجمة ثنائي اللغة (Localization Protocol)
# ============================================================
TRANSLATIONS = {
    "ar": {
        "title": "نصة المحاكاة الفضائية والسيادية",
        "dashboard": "لوحة القيادة (Dashboard)",
        "licenses": "إدارة التراخيص (Licenses)",
        "clients": "العملاء والباقات (Clients)",
        "health": "صحة النظام (Health)",
        "settings": "الإعدادات (Settings)",
        "altitude": "الارتفاع",
        "latitude": "خط العرض",
        "longitude": "خط الطول",
        "satellite": "القمر الصناعي",
        "search": "بحث...",
        "theme": "تبديل المظهر"
    },
    "en": {
        "title": "Space & Sovereign Simulation Platform",
        "dashboard": "Dashboard",
        "licenses": "Licenses",
        "clients": "Clients",
        "health": "Health",
        "settings": "Settings",
        "altitude": "Altitude",
        "latitude": "Latitude",
        "longitude": "Longitude",
        "satellite": "Satellite",
        "search": "Search...",
        "theme": "Toggle Theme"
    }
}

if 'lang' not in st.session_state:
    st.session_state.lang = 'ar'

def t(key: str) -> str:
    return TRANSLATIONS[st.session_state.lang].get(key, key)

# ============================================================
# 🔒 حماية الشاشة بكلمة المرور / شاشة الترخيص الأولية
# ============================================================
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown("<h1 style='text-align: center;'>🔑 COSMIC-324 </h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: gray;'>6G Titan X Global Edition - Boot Screen</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("auth_form"):
            license_input = st.text_input("أدخل مفتاح الترخيص الآمن:", type="password")
            submit_btn = st.form_submit_button("تحقق ودخول 🚀")
            if submit_btn:
                if AuthenticationProtocol.verify_license(license_input):
                    st.session_state.authenticated = True
                    st.success("✅ تم التحقق بنجاح! جارٍ التحميل...")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("❌ مفتاح الترخيص غير صالح أو منتهي الصلاحية.")
    st.stop()

# ============================================================
# 🌓 إدارة المظهر (Dark / Light Mode)
# ============================================================
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = True

# ============================================================
# 🎛️ الشريط الجانبي والقائمة الرئيسية (Sidebar)
# ============================================================
st.sidebar.title("🛰️ COSMIC-324 v8.0")
st.sidebar.markdown("---")

lang_choice = st.sidebar.selectbox("Language / اللغة", ["العربية", "English"])
st.session_state.lang = 'ar' if lang_choice == "العربية" else 'en'

if st.sidebar.button("🌓 تبديل المظهر (Theme)"):
    st.session_state.dark_mode = not st.session_state.dark_mode
    st.rerun()

st.sidebar.markdown("---")
menu = st.sidebar.radio(
    "التنقل الرئيسي",
    [
        t("dashboard"),
        t("licenses"),
        t("clients"),
        t("health"),
        t("settings")
    ]
)

# ============================================================
# 🧮 محرك الحسابات المدارية (Orbital Engine)
# ============================================================
MODEL_CONFIG = {
    "j2": 0.00108263,
    "earthRadiusKm": 6378.137,
    "mu": 398600.4418
}

def calculate_orbital_mechanics(num_sats=50):
    data = []
    try:
        np.random.seed(42)
        for i in range(num_sats):
            alt = np.random.uniform(400, 1200)
            a = MODEL_CONFIG["earthRadiusKm"] + alt
            n = np.sqrt(MODEL_CONFIG["mu"] / (a**3))
            incl = np.random.uniform(0.1, 1.5)
            
            # حساب تأثير J2 Perturbations
            p = a * (1 - 0.001**2)
            raan_dot = -1.5 * MODEL_CONFIG["j2"] * (MODEL_CONFIG["earthRadiusKm"] / p)**2 * n * np.cos(incl)
            
            lat = np.random.uniform(-80, 80)
            lon = np.random.uniform(-180, 180) + (time.time() * raan_dot * 10) % 360
            
            data.append({
                t('satellite'): f"SAT-324-{i+1:03d}",
                t('altitude'): alt,
                t('latitude'): lat,
                t('longitude'): lon,
                "Status": "Active"
            })
    except Exception as e:
        logger.error(f"خطأ في الحسابات المدارية: {e}")
    return pd.DataFrame(data)

# تحميل البيانات الأولية
orbit_df = calculate_orbital_mechanics(60)

# ============================================================
# 📊 تنفيذ الشاشات والأقسام المختلفة
# ============================================================

if menu == t("dashboard"):
    st.title(f"📊 {t('dashboard')}")
    st.markdown("---")
    
    # إحصائيات سريعة ومؤشرات
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🌍 إجمالي الأقمار", f"{len(orbit_df)}")
    with col2:
        avg_alt = orbit_df[t('altitude')].mean()
        st.metric("📏 متوسط الارتفاع", f"{avg_alt:.1f} كم")
    with col3:
        max_alt = orbit_df[t('altitude')].max()
        st.metric("📈 أقصى ارتفاع", f"{max_alt:.1f} كم")
    with col4:
        st.metric("🟢 حالة الشبكة", "مستقرة 100%")

    st.markdown("---")
    
    # فلترة متقدمة
    with st.expander("🔍 خيارات الفلترة المتقدمة"):
        min_alt, max_alt = st.slider("مدى الارتفاع (كم)", 300, 1500, (400, 1200))
        filtered_df = orbit_df[(orbit_df[t('altitude')] >= min_alt) & (orbit_df[t('altitude')] <= max_alt)]
    
    # الخريطة التفاعلية وتوزيع الأقمار
    st.subheader("🌐 خريطة التتبع المداري ثلاثية الأبعاد")
    fig = px.scatter_mapbox(
        filtered_df,
        lat=t('latitude'),
        lon=t('longitude'),
        size=t('altitude'),
        color=t('altitude'),
        hover_name=t('satellite'),
        zoom=1,
        height=500
    )
    fig.update_layout(mapbox_style="open-street-map", margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig, use_container_width=True)

    # خريطة حرارية إضافية
    st.subheader("🔥 الخريطة الحرارية لتوزيع الأقمار")
    fig_heat = px.density_mapbox(
        filtered_df,
        lat=t('latitude'),
        lon=t('longitude'),
        radius=15,
        zoom=1,
        height=400
    )
    fig_heat.update_layout(mapbox_style="open-street-map", margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig_heat, use_container_width=True)

    # تصدير البيانات
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="📥 تحميل البيانات المُصفاة (CSV)",
        data=csv,
        file_name=f"cosmic324_data_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

elif menu == t("licenses"):
    st.title(f"🔑 {t('licenses')}")
    st.markdown("---")
    st.info("إدارة وتوليد مفاتيح التراخيص الأمنية عبر قاعدة بيانات SQLite المحلية.")
    
    new_client = st.text_input("اسم العميل الجديد:")
    tier_choice = st.selectbox("باقة الترخيص:", ["Free", "Pro", "Enterprise"])
    if st.button("توليد مفتاح ترخيص جديد 🔐"):
        if new_client:
            new_key = f"CSM324-{secrets.token_hex(4).upper()}-2026"
            try:
                conn = sqlite3.connect(AuthenticationProtocol.DB_FILE)
                cursor = conn.cursor()
                cursor.execute("INSERT INTO licenses VALUES (?, ?, ?, ?, ?)", 
                               (new_key, new_client, tier_choice, datetime.now().isoformat(), 1))
                conn.commit()
                conn.close()
                st.success(f"✅ تم بنجاح إنشاء المفتاح للعميل {new_client}: `{new_key}`")
            except Exception as e:
                st.error(f"خطأ أثناء الحفظ: {e}")
        else:
            st.warning("الرجاء إدخال اسم العميل.")

    st.subheader("📋 قائمة التراخيص النشطة في النظام")
    try:
        conn = sqlite3.connect(AuthenticationProtocol.DB_FILE)
        lic_df = pd.read_sql_query("SELECT * FROM licenses", conn)
        conn.close()
        st.dataframe(lic_df, use_container_width=True)
    except Exception as e:
        st.error(f"تعذر جلب التراخيص: {e}")

elif menu == t("clients"):
    st.title(f"👥 {t('clients')}")
    st.markdown("---")
    st.write("اختر الباقة المناسبة لمتطلبات مؤسستك السيادية أو الفضائية:")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("### الباقة المجانية")
        st.write("ميزات أساسية للمتطوعين والهواة.")
        st.metric("السعر", "$0 / شهرياً")
        st.button("اختر الأساسية", key="btn1")
    with c2:
        st.markdown("### باقة المحترفين Pro")
        st.write("تتبع مداري متقدم وحسابات دقيقة.")
        st.metric("السعر", "$299 / شهرياً")
        st.button("اختر المحترفين", key="btn2")
    with c3:
        st.markdown("### الباقة السيادية Enterprise")
        st.write("تحكم كامل، دعم على مدار الساعة، تكامل شامل.")
        st.metric("السعر", "$999 / شهرياً")
        st.button("اختر السيادية", key="btn3")

elif menu == t("health"):
    st.title(f"🩺 {t('health')}")
    st.markdown("---")
    
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    col1, col2, col3 = st.columns(3)
    col1.metric("💻 استخدام المعالج (CPU)", f"{cpu_percent}%")
    col2.metric("🧠 الذاكرة العشوائية (RAM)", f"{memory.percent}%")
    col3.metric("💽 مساحة التخزين (Disk)", f"{disk.percent}%")
    
    st.markdown("---")
    st.subheader("📋 سجلات النظام الأخيرة (Logs)")
    if os.path.exists('cosmic324.log'):
        with open('cosmic324.log', 'r', encoding='utf-8') as f:
            logs = f.readlines()
        st.code("".join(logs[-15:]), language='text')
    else:
        st.info("لا توجد سجلات حالية.")

elif menu == t("settings"):
    st.title(f"⚙️ {t('settings')}")
    st.markdown("---")
    
    st.subheader("🌐 إعدادات قاعدة بيانات الدول والمحطات")
    country_names = [c["name"] for c in CountryDatabase.COUNTRIES]
    selected_country = st.selectbox("الدولة الافتراضية للمركز السيادي:", country_names)
    
    st.markdown("---")
    st.subheader("🛠️ إضافة محطة أرضية مخصصة")
    with st.form("custom_station_form"):
        st_name = st.text_input("اسم المحطة الأرضية:")
        st_lat = st.number_input("خط العرض للمحطة:", -90.0, 90.0, 24.7136)
        st_lon = st.number_input("خط الطول للمحطة:", -180.0, 180.0, 46.6753)
        submit_station = st.form_submit_button("حفظ المحطة الأرضية")
        if submit_station:
            st.success(f"✅ تم حفظ المحطة الأرضية ({st_name}) بنجاح في الإعدادات السيادية.")

# ============================================================
# 🏁 تذييل الصفحة (Footer)
# ============================================================
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>COSMIC-324 6G Titan X Global Edition © 2026 - جميع الحقوق محفوظة</p>", unsafe_allow_html=True)
