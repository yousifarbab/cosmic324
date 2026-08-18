"""
COSMIC-324: Satellite Tracking & Link Analysis Suite (V18.3 - Live TLE & Skyfield Engine)
النسخة المحدثة للبيانات الحية والفعلية عبر CelesTrak و Skyfield
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
import hashlib
import sqlite3

try:
    from skyfield.api import EarthSatellite, load, wgs84
    SKYFIELD_AVAILABLE = True
except ImportError:
    SKYFIELD_AVAILABLE = False

# ==========================================
# 1. إعدادات التسجيل ونظام السجلات (Logging)
# ==========================================
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ==========================================
# 2. عقود البيانات والمعلمات الفيزيائية
# ==========================================
DATA_CONTRACT = {
    "celestrak": {
        "groups": ["starlink", "active", "visual", "weather", "gps", "iridium"],
        "defaultGroup": "starlink",
        "cacheTtlSeconds": 900
    },
    "model": {
        "earthRadiusKm": 6371.0,
        "speedOfLight": 3e8,  # م/ث
        "boltzmannConstant": 1.380649e-23  # J/K
    },
    "source": {
        "baseUrl": "https://celestrak.org/NORAD/elements/gp.php"
    }
}

# ==========================================
# 3. قاعدة البيانات المحلية وسجل الـ Hash-Chained
# ==========================================
class EngineeringDatabase:
    def __init__(self, db_path: str = "engineering_suite.db"):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS hash_audit_logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TEXT NOT NULL,
                        event_type TEXT NOT NULL,
                        description TEXT NOT NULL,
                        prev_hash TEXT NOT NULL,
                        current_hash TEXT NOT NULL
                    )
                """)
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS legal_compliance_docs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        jurisdiction TEXT NOT NULL,
                        law_title TEXT NOT NULL,
                        category TEXT NOT NULL,
                        review_status TEXT NOT NULL,
                        last_updated TEXT NOT NULL,
                        notes TEXT NOT NULL
                    )
                """)
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM legal_compliance_docs")
                if cursor.fetchone()[0] == 0:
                    sample_docs = [
                        ("داخلي / مؤسسي", "إطار توثيق عقود الحوكمة المؤسسية والشركات العائلية", "القانون التجاري", "مسودة توثيق داخلي", datetime.utcnow().isoformat(), "أداة إرشادية داخلية بحتة ولا تُغني عن الاستشارة القانونية المتخصصة."),
                        ("دولي / فضائي", "معايير الاتحاد الدولي للاتصالات (ITU) لتنسيق الترددات", "تنظيم الاتصالات", "معتمد فنياً", datetime.utcnow().isoformat(), "متابعة خطوط الرؤية والمدارات وفق المعطيات الفلكية.")
                    ]
                    conn.executemany("INSERT INTO legal_compliance_docs (jurisdiction, law_title, category, review_status, last_updated, notes) VALUES (?, ?, ?, ?, ?, ?)", sample_docs)
        except Exception as e:
            logger.error(f"Database Initialization Error: {e}")

    def log_audit(self, event_type: str, desc: str):
        timestamp = datetime.utcnow().isoformat()
        prev_hash = self._get_latest_hash()
        raw_string = f"{timestamp}:{event_type}:{desc}:{prev_hash}"
        current_hash = hashlib.sha256(raw_string.encode()).hexdigest()
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    "INSERT INTO hash_audit_logs (timestamp, event_type, description, prev_hash, current_hash) VALUES (?, ?, ?, ?, ?)",
                    (timestamp, event_type, desc, prev_hash, current_hash)
                )
        except Exception as e:
            logger.error(f"Audit Log Error: {e}")

    def _get_latest_hash(self) -> str:
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("SELECT current_hash FROM hash_audit_logs ORDER BY id DESC LIMIT 1")
                row = cursor.fetchone()
                return row[0] if row else "0" * 64
        except:
            return "0" * 64

    def get_audit_logs(self) -> List[Dict]:
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute("SELECT id, timestamp, event_type, description, prev_hash, current_hash FROM hash_audit_logs ORDER BY id DESC")
                return [dict(row) for row in cursor.fetchall()]
        except:
            return []

    def verify_integrity(self) -> Tuple[bool, str]:
        logs = self.get_audit_logs()
        logs_sorted = list(reversed(logs))
        expected_prev = "0" * 64
        
        for idx, log in enumerate(logs_sorted):
            if log['prev_hash'] != expected_prev:
                return False, f"عدم تطابق في الـ Hash عند السجل رقم {log['id']}"
            
            raw_string = f"{log['timestamp']}:{log['event_type']}:{log['description']}:{log['prev_hash']}"
            recomputed = hashlib.sha256(raw_string.encode()).hexdigest()
            if recomputed != log['current_hash']:
                return False, f"خطأ في بصمة الـ Hash للسجل رقم {log['id']}!"
            expected_prev = log['current_hash']
            
        return True, "سلامة السلسلة مثبتة بنجاح (Hash-Chain Verified)."

    def get_legal_docs(self) -> List[Dict]:
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute("SELECT jurisdiction, law_title, category, review_status, last_updated, notes FROM legal_compliance_docs")
                return [dict(row) for row in cursor.fetchall()]
        except:
            return []

    def add_legal_doc(self, jur: str, title: str, cat: str, status: str, notes: str):
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    "INSERT INTO legal_compliance_docs (jurisdiction, law_title, category, review_status, last_updated, notes) VALUES (?, ?, ?, ?, ?, ?)",
                    (jur, title, cat, status, datetime.utcnow().isoformat(), notes)
                )
        except Exception as e:
            logger.error(f"Add Legal Doc Error: {e}")

db = EngineeringDatabase()

# ==========================================
# 4. واجهة اللغات (عربي / إنجليزي)
# ==========================================
LANGUAGES = {
    "ar": {
        "name": "العربية",
        "dir": "rtl",
        "title": "🛰️ COSMIC-324: منصة التتبع الهندسي وتحليل الوصلات الفضائية",
        "subtitle": "أداة هندسية تحليلية لتتبع الأقمار الصناعية الحية، حسابات الميزانية الراديوية (Friis)، وإزاحة دوبلر",
        "dashboard": "📊 لوحة التتبع الحي للأقمار الصناعية",
        "link_budget": "📡 هندسة الوصلة وحسابات Friis & SNR",
        "doppler_panel": "🌐 تحليل إزاحة دوبلر الفلكية",
        "legal_panel": "⚖️ أداة التوثيق الداخلي والمراجعة القانونية",
        "audit_panel": "📜 سجل العمليات المربوط (Hash-Chained Log)"
    },
    "en": {
        "name": "English",
        "dir": "ltr",
        "title": "🛰️ COSMIC-324: Satellite Tracking & Link Analysis Suite",
        "subtitle": "Analytical engineering tool for live satellite ephemeris, Friis link budget, and Doppler shift",
        "dashboard": "📊 Live Satellite Tracking Dashboard",
        "link_budget": "📡 Link Budget & Friis / SNR Analysis",
        "doppler_panel": "🌐 Doppler Shift Analysis",
        "legal_panel": "⚖️ Internal Legal & Regulatory Documentation Tool",
        "audit_panel": "📜 Hash-Chained Audit Log"
    }
}

def t(key: str) -> str:
    lang = st.session_state.get('language', 'ar')
    return LANGUAGES.get(lang, LANGUAGES['ar']).get(key, key)

def get_current_dir() -> str:
    lang = st.session_state.get('language', 'ar')
    return LANGUAGES.get(lang, LANGUAGES['ar']).get('dir', 'rtl')

# ==========================================
# 5. جلب البيانات الفلكية الحقيقية (Live TLE & Skyfield)
# ==========================================
@st.cache_data
def get_stations() -> List[Dict]:
    return sorted([
        {"name": "محطة الخرطوم البحثية (السودان)", "lat": 15.5007, "lon": 32.5599},
        {"name": "محطة الرياض المركزية (المملكة العربية السعودية)", "lat": 23.8859, "lon": 45.0792},
        {"name": "محطة دبي التقنية (الإمارات)", "lat": 23.4241, "lon": 53.8478},
        {"name": "محطة طوكيو الفضائية (آسيا)", "lat": 36.2048, "lon": 138.2529}
    ], key=lambda x: x["name"])

ALL_STATIONS = get_stations()

def haversine(lat1, lon1, lat2, lon2):
    R = DATA_CONTRACT["model"]["earthRadiusKm"]
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp/2)**2 + math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

@st.cache_data(ttl=900)
def fetch_live_ephemeris(group: str, limit: int, version: int) -> Tuple[List[Dict], bool]:
    """جلب بيانات المدارات الحقيقية (TLE) مباشرة بصيغة نصية أو جيسون من CelesTrak"""
    url = f"https://celestrak.org/NORAD/elements/gp.php?GROUP={group}&FORMAT=tle"
    try:
        res = requests.get(url, timeout=8)
        if res.status_code == 200:
            lines = res.text.strip().splitlines()
            satellites = []
            # ملفات الـ TLE تتألف من 3 أسطر لكل قمر (الاسم، السطر الأول، السطر الثاني)
            for i in range(0, len(lines) - 2, 3):
                if i + 2 < len(lines):
                    name = lines[i].strip()
                    line1 = lines[i+1].strip()
                    line2 = lines[i+2].strip()
                    satellites.append({
                        "OBJECT_NAME": name,
                        "TLE_LINE1": line1,
                        "TLE_LINE2": line2
                    })
            if len(satellites) > 0:
                return satellites[:limit], True
    except Exception as e:
        logger.error(f"Live CelesTrak TLE fetch error: {e}")
    return [], False

def build_live_orbit_map(group: str, limit: int) -> Tuple[Dict, bool]:
    """حساب الإحداثيات الفعلية اللحظية باستخدام Skyfield وبيانات TLE الحقيقية"""
    orbit_map = {}
    raw, success = fetch_live_ephemeris(group, limit, st.session_state.cache_ver)
    
    if not success or not raw:
        return {}, False

    if not SKYFIELD_AVAILABLE:
        return {}, False

    try:
        ts = load.timescale()
        t_now = ts.now()
        
        for entry in raw:
            name = entry.get('OBJECT_NAME', 'SAT')
            line1 = entry.get('TLE_LINE1')
            line2 = entry.get('TLE_LINE2')
            if line1 and line2:
                satellite = EarthSatellite(line1, line2, name, ts)
                geocentric = satellite.at(t_now)
                subpoint = wgs84.subpoint(geocentric)
                lat = subpoint.latitude.degrees
                lon = subpoint.longitude.degrees
                alt = subpoint.elevation.km
                orbit_map[name] = SimpleNamespace(name=name, lat=lat, lon=lon, altitude=alt)
    except Exception as e:
        logger.error(f"Skyfield calculation error: {e}")
        return {}, False
        
    return orbit_map, True

# ==========================================
# 6. الهيكل الرئيسي لتطبيق Streamlit
# ==========================================
def main():
    st.set_page_config(page_title="COSMIC-324 Engineering Suite", page_icon="🛰️", layout="wide", initial_sidebar_state="expanded")

    if 'language' not in st.session_state:
        st.session_state.language = 'ar'
    if 'cache_ver' not in st.session_state:
        st.session_state.cache_ver = 0

    current_dir = get_current_dir()

    st.markdown(f"""
    <style>
        .main, .stApp {{
            background-color: #0b0f19;
            direction: {current_dir};
            text-align: {'right' if current_dir == 'rtl' else 'left'};
        }}
        .stMetric {{
            background: #111827;
            border-radius: 8px;
            padding: 12px;
            border: 1px solid #1f2937;
        }}
        h1, h2, h3, h4 {{
            color: #38bdf8;
            font-family: 'Segoe UI', Tahoma, sans-serif;
        }}
        .info-box {{
            background: #111827;
            border-radius: 8px;
            padding: 15px;
            border: 1px solid #374151;
            margin-bottom: 15px;
        }}
    </style>
    """, unsafe_allow_html=True)

    st.sidebar.title("🛰️ COSMIC-324 Suite")
    
    lang_choice = st.sidebar.selectbox("🌐 Language / اللغة", ["ar", "en"], format_func=lambda x: LANGUAGES[x]["name"], index=0 if st.session_state.language=='ar' else 1)
    if lang_choice != st.session_state.language:
        st.session_state.language = lang_choice
        st.rerun()
        
    st.sidebar.markdown("---")
    st.sidebar.markdown("### اختيار المحطة الأرضية المرجعية:")
    station_names = [s["name"] for s in ALL_STATIONS]
    selected_st_name = st.sidebar.selectbox("المحطة:", station_names)
    selected_station = next(s for s in ALL_STATIONS if s["name"] == selected_st_name)
    
    view_mode_choice = st.sidebar.radio("نطاق التصفية الجغرافية:", ["عرض شامل لجميع الأقمار المتاحة", "تصفية الأقمار في خط الرؤية المباشر (LoS)"], index=0)
    strict_los = ("LoS" in view_mode_choice)
    
    st.sidebar.markdown("---")
    nav = st.sidebar.radio("📌 القائمة الرئيسية", [
        t('dashboard'),
        t('link_budget'),
        t('doppler_panel'),
        t('legal_panel'),
        t('audit_panel')
    ])
    
    st.title(t('title'))
    st.markdown(f"*{t('subtitle')}*")

    st.markdown(f"""
    <div class="info-box">
        <b>المحطة المرجعية النشطة:</b> {selected_station['name']} (خط العرض: {selected_station['lat']}°, خط الطول: {selected_station['lon']}°) | التوقيت العالمي (UTC): <b>{datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}</b>
    </div>
    """, unsafe_allow_html=True)
    
    # ----------------------------------------
    # 1. لوحة التتبع الحي والأقمار الصناعية
    # ----------------------------------------
    if nav == t('dashboard'):
        col1, col2 = st.columns([2, 1])
        with col1: sat_slider = st.slider("عدد الأقمار المراد الاستعلام عنها", 50, 500, 100, 50)
        with col2: group_sel = st.selectbox("المجموعة الفضائية من CelesTrak:", DATA_CONTRACT["celestrak"]["groups"])
            
        if st.button("🔄 جلب الإحداثيات الحية المباشرة"):
            st.session_state.cache_ver += 1
            db.log_audit("FETCH_LIVE_CELESTRAK_TLE", f"Fetched live TLE ephemeris for group: {group_sel}")
            st.rerun()
            
        with st.spinner("جاري الاتصال وسحب مدارات TLE الحية وحساب مواقعها الفلكية الفعلية..."):
            orbit_map, fetch_success = build_live_orbit_map(group_sel, sat_slider)
            
        if not fetch_success or not orbit_map:
            st.error("❌ تعذر جلب البيانات الحية حالياً من خوادم CelesTrak أو تأكد من تثبيت مكتبة `skyfield` عبر النظام البيئي.")
        else:
            st.success("✅ تم جلب البيانات الحية المباشرة وحساب المواقع الفلكية الفعلية بنجاح.")

        records = []
        for name, sat in orbit_map.items():
            try:
                lat, lon, alt = sat.lat, sat.lon, sat.altitude
                dist_to_station = haversine(selected_station['lat'], selected_station['lon'], lat, lon)
                horizon = math.acos(DATA_CONTRACT["model"]["earthRadiusKm"] / (DATA_CONTRACT["model"]["earthRadiusKm"] + alt)) * DATA_CONTRACT["model"]["earthRadiusKm"]
                if strict_los and dist_to_station > (horizon + 1000):
                    continue
                records.append({
                    "اسم القمر": name[:28],
                    "حالة البيانات": "حقيقي مباشر (Live TLE)",
                    "خط العرض": round(lat, 3),
                    "خط الطول": round(lon, 3),
                    "الارتفاع (كم)": round(alt, 1),
                    "البعد عن المحطة (كم)": round(dist_to_station, 1)
                })
            except:
                continue
        df_res = pd.DataFrame(records)
        
        if not df_res.empty:
            st.dataframe(df_res.reset_index(drop=True), use_container_width=True)
            
            fig = px.scatter_geo(
                df_res,
                lat="خط العرض",
                lon="خط الطول",
                hover_name="اسم القمر",
                projection="orthographic",
                title=f"خريطة التتبع الحي الفعلي للمحطة: {selected_station['name']}"
            )
            fig.add_trace(go.Scattergeo(
                lat=[selected_station['lat']],
                lon=[selected_station['lon']],
                mode='markers+text',
                text=[selected_station['name']],
                textposition="top right",
                marker=dict(size=14, color='#38bdf8', symbol='star'),
                name=selected_station['name']
            ))
            fig.update_geos(bgcolor="#0b0f19", landcolor="#111827", subunitcolor="#374151", countrycolor="#4b5563")
            fig.update_layout(height=550, margin={"r":0,"t":40,"l":0,"b":0})
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("⚠️ لا توجد أقمار مطابقة لنطاق التصفية المختار.")

    # ----------------------------------------
    # 2. هندسة الوصلة (Friis Link Budget & SNR)
    # ----------------------------------------
    elif nav == t('link_budget'):
        st.subheader("📡 حسابات ميزانية الوصلة الراديوية (Friis Transmission Equation & SNR)")
        st.write("حساب قوة الإشارة المستقبلة بناءً على معادلة فرايس الحقيقية لفقد المسار الحر، القدرة المشعة المكافئة المتدرجة (EIRP)، وضوضاء جونسون-نايكويست الحرارية.")
        
        c1, c2, c3 = st.columns(3)
        with c1:
            frequency_ghz = st.number_input("التردد التشغيلي (GHz):", value=12.5, step=0.5, min_value=0.1, max_value=100.0)
            distance_km = st.number_input("المسافة بين المحطة والقمر (كم):", value=850.0, step=50.0, min_value=100.0)
        with c2:
            tx_power_dbw = st.number_input("قدرة المرسل (Tx Power in dBW):", value=10.0, step=1.0)
            tx_gain_dbi = st.number_input("كسب هوائي المرسل (Tx Gain dBi):", value=30.0, step=1.0)
        with c3:
            rx_gain_dbi = st.number_input("كسب هوائي المستقبل (Rx Gain dBi):", value=35.0, step=1.0)
            system_temp_k = st.number_input("درجة حرارة النظام المكافئة (Kelvin):", value=290.0, step=10.0)
            bandwidth_mhz = st.number_input("عرض النطاق الترددي (MHz):", value=20.0, step=5.0)

        frequency_hz = frequency_ghz * 1e9
        distance_m = distance_km * 1e3
        wavelength = DATA_CONTRACT["model"]["speedOfLight"] / frequency_hz
        
        eirp_dbw = tx_power_dbw + tx_gain_dbi
        fspl_db = 20 * math.log10(4 * math.pi * distance_m / wavelength)
        pr_dbw = eirp_dbw + rx_gain_dbi - fspl_db
        pr_dbm = pr_dbw + 30
        
        bandwidth_hz = bandwidth_mhz * 1e6
        noise_power_watts = DATA_CONTRACT["model"]["boltzmannConstant"] * system_temp_k * bandwidth_hz
        noise_power_dbw = 10 * math.log10(noise_power_watts)
        
        snr_db = pr_dbw - noise_power_dbw

        st.markdown("---")
        m1, m2, m3, m4 = st.columns(4)
        with m1: st.metric("الفقد الحر للمسار (FSPL)", f"{round(fspl_db, 2)} dB")
        with m2: st.metric("القدرة المشعة (EIRP)", f"{round(eirp_dbw, 2)} dBW")
        with m3: st.metric("قدرة الإشارة المستقبلة (Pr)", f"{round(pr_dbm, 2)} dBm")
        with m4: st.metric("نسبة الإشارة للضوضاء (SNR)", f"{round(snr_db, 2)} dB", "مستقر" if snr_db > 10 else "ضعيف")

        if st.button("💾 تسجيل حسابات الوصلة في سجل العمليات"):
            db.log_audit("LINK_BUDGET_CALC", f"Calculated Friis link budget: Freq={frequency_ghz}GHz, Dist={distance_km}km, SNR={round(snr_db,2)}dB")
            st.success("✅ تم حفظ نتيجة الحساب في سجل التدقيق المشفر بنجاح.")

    # ----------------------------------------
    # 3. تحليل إزاحة دوبلر (Doppler Shift)
    # ----------------------------------------
    elif nav == t('doppler_panel'):
        st.subheader("🌐 تحليل إزاحة دوبلر الفلكية (Doppler Shift Calculation)")
        st.write("حساب التغير الظاهري في تردد الإشارة نتيجة السرعة النسبية بين القمر الصناعي المتحرك والمحطة الأرضية الثابتة.")

        col_d1, col_d2 = st.columns(2)
        with col_d1:
            carrier_freq_ghz = st.number_input("التردد الحامل للأصل (GHz):", value=10.0, step=0.5)
            sat_velocity_kms = st.number_input("سرعة القمر المدارية (كم/ث):", value=7.56, step=0.1)
        with col_d2:
            max_elevation_deg = st.number_input("زاوية الارتفاع القصوى للمرور (درجات):", value=45.0, step=5.0, min_value=5.0, max_value=90.0)

        f_0 = carrier_freq_ghz * 1e9
        v = sat_velocity_kms * 1e3
        c = DATA_CONTRACT["model"]["speedOfLight"]
        
        max_doppler_hz = (v / c) * f_0
        max_doppler_khz = max_doppler_hz / 1e3

        st.markdown("---")
        dm1, dm2 = st.columns(2)
        with dm1: st.metric("أقصى إزاحة ترددية (Max Doppler Shift)", f"± {round(max_doppler_khz, 2)} kHz")
        with dm2: st.metric("سرعة إرسال الموجة النسبية", f"{sat_velocity_kms} كم/ث")

        time_points = np.linspace(-300, 300, 100)
        doppler_curve = max_doppler_khz * np.sin(time_points / 150.0)
        df_doppler = pd.DataFrame({"الزمن النسبي (ثواني)": time_points, "الإزاحة الترددية (kHz)": doppler_curve})
        
        st.plotly_chart(px.line(df_doppler, x="الزمن النسبي (ثواني)", y="الإزاحة الترددية (kHz)", title="منحنى إزاحة دوبلر عبر الزمن أثناء عبور القمر"), use_container_width=True)

        if st.button("💾 تسجيل تحليل دوبلر في سجل العمليات"):
            db.log_audit("DOPPLER_CALC", f"Calculated max Doppler shift: ±{round(max_doppler_khz,2)} kHz at {carrier_freq_ghz} GHz")
            st.success("✅ تم توثيق الحساب في سجل التدقيق بنجاح.")

    # ----------------------------------------
    # 4. أداة التوثيق الداخلي والمراجعة القانونية
    # ----------------------------------------
    elif nav == t('legal_panel'):
        st.subheader("⚖️ أداة التوثيق الداخلي والمراجعة القانونية")
        st.markdown("""
        > **تنويه هام:** هذه الوحدة هي أداة توثيق داخلي لتنظيم وترتيب المذكرات واللوائح القانونية والمؤسسية (مثل عقود الشركات وحوكمة الشركات العائلية وتنظيم الاتصالات). **ولا تُعد بأي حال من الأحوال بديلاً عن الاستشارة القانونية الرسمية**.
        """)

        docs = db.get_legal_docs()
        if docs:
            df_docs = pd.DataFrame(docs)
            st.dataframe(df_docs.reset_index(drop=True), use_container_width=True)
        else:
            st.info("لا توجد مستندات قانونية مسجلة حالياً.")

        with st.expander("➕ إضافة وثيقة أو ملاحظة قانونية جديدة"):
            with st.form("legal_form"):
                jur = st.text_input("النطاق أو الجهة (مثل: داخلي / مؤسسي، تنظيم محلي):")
                title = st.text_input("عنوان المذكرة أو التشريع:")
                cat = st.selectbox("التصنيف:", ["القانون التجاري", "حوكمة الشركات", "تنظيم الاتصالات", "عقود وعمليات"])
                status = st.selectbox("حالة المراجعة:", ["مسودة توثيق داخلي", "قيد المراجعة الفنية", "معتمد للأرشيف"])
                notes = st.text_area("ملاحظات تفصيلية أو إضافية:")
                
                if st.form_submit_button("حفظ المستند في الأرشيف الداخلي") and jur and title:
                    db.add_legal_doc(jur, title, cat, status, notes)
                    db.log_audit("ADD_LEGAL_DOC", f"Added internal legal/compliance document: {title}")
                    st.success("✅ تم حفظ المستند وإضافة العملية لسجل التدقيق المشفر بنجاح.")
                    st.rerun()

    # ----------------------------------------
    # 5. سجل العمليات المشفر (Hash-Chained Log)
    # ----------------------------------------
    elif nav == t('audit_panel'):
        st.subheader("📜 سجل العمليات المربوط (Hash-Chained Audit Log)")
        st.write("كل عملية أو حساب يتم إجراؤه في النظام يتم ربطه رياضياً عبر الـ Hash بالسجل الذي يسبقه (Cryptographic Hash-Chained)، مما يضمن إمكانية كشف أي تعديل أو عبث بالبيانات بشكل فوري.")

        col_v1, col_v2 = st.columns([1, 3])
        with col_v1:
            if st.button("🔍 التحقق من سلامة السلسلة (Verify Integrity)"):
                is_valid, msg = db.verify_integrity()
                if is_valid:
                    st.success(f"✅ {msg}")
                else:
                    st.error(f"❌ تنبيه أمني: {msg}")
        
        logs = db.get_audit_logs()
        if logs:
            df_logs = pd.DataFrame(logs)
            st.dataframe(df_logs.reset_index(drop=True), use_container_width=True)
            
            csv_data = df_logs.to_csv(index=False).encode('utf-8')
            st.download_button("📥 تحميل سجل العمليات بصيغة CSV", data=csv_data, file_name=f"engineering_audit_logs_{datetime.utcnow().strftime('%Y%m%d')}.csv", mime="text/csv")
        else:
            st.info("سجل العمليات فارغ حالياً.")

    st.markdown("""
    <div style="text-align: center; color: #6b7280; font-size: 0.85em; padding: 25px 0; border-top: 1px solid #1f2937; margin-top: 30px;">
        © 2026 COSMIC-324: Satellite Tracking & Link Analysis Suite (V18.3). جميع الحقوق محفوظة للأدوات الهندسية والتحليلية.
    </div>
    """, unsafe_allow_html=True)

if __name__ == '__main__':
    main()
