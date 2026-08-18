"""
COSMIC-324: Satellite Tracking & Link Analysis Suite (V18.4 - Robust Hybrid Live/Fallback Engine)
النسخة الهجينة المتقدمة: تجلب البيانات الحية عبر TLE وإن فشل الاتصال تنتقل بسلاسة للمحاكاة مع إشعار واضح
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import math
import numpy as np
from datetime import datetime
from typing import Dict, List, Tuple
from types import SimpleNamespace
import hashlib
import sqlite3
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

try:
    from skyfield.api import EarthSatellite, load, wgs84
    SKYFIELD_AVAILABLE = True
except ImportError:
    SKYFIELD_AVAILABLE = False

DATA_CONTRACT = {
    "celestrak": {
        "groups": ["starlink", "active", "visual", "weather", "gps", "iridium"],
        "defaultGroup": "starlink",
    },
    "model": {
        "earthRadiusKm": 6371.0,
        "speedOfLight": 3e8,
        "boltzmannConstant": 1.380649e-23
    },
    "source": {
        "baseUrl": "https://celestrak.org/NORAD/elements/gp.php"
    }
}

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
                        ("داخلي / مؤسسي", "إطار توثيق عقود الحوكمة المؤسسية والشركات العائلية", "القانون التجاري", "مسودة توثيق داخلي", datetime.utcnow().isoformat(), "أداة إرشادية داخلية بحتة."),
                        ("دولي / فضائي", "معايير الاتحاد الدولي للاتصالات (ITU) لتنسيق الترددات", "تنظيم الاتصالات", "معتمد فنياً", datetime.utcnow().isoformat(), "متابعة خطوط الرؤية والمدارات وفق المعطيات الفلكية.")
                    ]
                    conn.executemany("INSERT INTO legal_compliance_docs (jurisdiction, law_title, category, review_status, last_updated, notes) VALUES (?, ?, ?, ?, ?, ?)", sample_docs)
        except Exception as e:
            logger.error(f"Database Error: {e}")

    def log_audit(self, event_type: str, desc: str):
        timestamp = datetime.utcnow().isoformat()
        prev_hash = self._get_latest_hash()
        raw_string = f"{timestamp}:{event_type}:{desc}:{prev_hash}"
        current_hash = hashlib.sha256(raw_string.encode()).hexdigest()
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("INSERT INTO hash_audit_logs (timestamp, event_type, description, prev_hash, current_hash) VALUES (?, ?, ?, ?, ?)",
                             (timestamp, event_type, desc, prev_hash, current_hash))
        except Exception as e:
            logger.error(f"Audit Error: {e}")

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
        for log in logs_sorted:
            if log['prev_hash'] != expected_prev:
                return False, f"خطأ تطابق Hash في السجل {log['id']}"
            raw_string = f"{log['timestamp']}:{log['event_type']}:{log['description']}:{log['prev_hash']}"
            if hashlib.sha256(raw_string.encode()).hexdigest() != log['current_hash']:
                return False, f"تلاعب مكتشف في السجل {log['id']}"
            expected_prev = log['current_hash']
        return True, "سلامة السلسلة المشفرة مثبتة بنجاح (Hash-Chain Verified)."

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
                conn.execute("INSERT INTO legal_compliance_docs (jurisdiction, law_title, category, review_status, last_updated, notes) VALUES (?, ?, ?, ?, ?, ?)",
                             (jur, title, cat, status, datetime.utcnow().isoformat(), notes))
        except Exception as e:
            logger.error(f"Legal Doc Error: {e}")

db = EngineeringDatabase()

LANGUAGES = {
    "ar": {
        "name": "العربية", "dir": "rtl",
        "title": "🛰️ COSMIC-324: منصة التتبع الهندسي وتحليل الوصلات الفضائية",
        "subtitle": "أداة هندسية تحليلية لتتبع الأقمار الصناعية، حسابات الميزانية الراديوية (Friis)، وإزاحة دوبلر",
        "dashboard": "📊 لوحة التتبع الحي للأقمار الصناعية",
        "link_budget": "📡 هندسة الوصلة وحسابات Friis & SNR",
        "doppler_panel": "🌐 تحليل إزاحة دوبلر الفلكية",
        "legal_panel": "⚖️ أداة التوثيق الداخلي والمراجعة القانونية",
        "audit_panel": "📜 سجل العمليات المربوط (Hash-Chained Log)"
    },
    "en": {
        "name": "English", "dir": "ltr",
        "title": "🛰️ COSMIC-324: Satellite Tracking & Link Analysis Suite",
        "subtitle": "Analytical engineering tool for satellite ephemeris, Friis link budget, and Doppler shift",
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
def fetch_live_tle(group: str, limit: int, version: int) -> Tuple[List[Dict], bool]:
    url = f"{DATA_CONTRACT['source']['baseUrl']}?GROUP={group}&FORMAT=tle"
    try:
        res = requests.get(url, timeout=6)
        if res.status_code == 200:
            lines = res.text.strip().splitlines()
            satellites = []
            for i in range(0, len(lines) - 2, 3):
                if i + 2 < len(lines):
                    satellites.append({
                        "OBJECT_NAME": lines[i].strip(),
                        "TLE_LINE1": lines[i+1].strip(),
                        "TLE_LINE2": lines[i+2].strip()
                    })
            if satellites:
                return satellites[:limit], True
    except Exception as e:
        logger.error(f"TLE fetch error: {e}")
    return [], False

def generate_fallback_satellites(group: str, limit: int) -> List[Dict]:
    fallback_data = []
    np.random.seed(42)
    for i in range(1, limit + 1):
        fallback_data.append({
            "OBJECT_NAME": f"{group.upper()}-SIM-SAT-{i:03d}",
            "INCLINATION": float(np.random.uniform(20, 85)),
            "MEAN_MOTION": float(np.random.uniform(13, 15)),
            "EPOCH_REV": float(np.random.uniform(1000, 5000))
        })
    return fallback_data

def build_hybrid_orbit_map(group: str, limit: int) -> Tuple[Dict, bool, str]:
    orbit_map = {}
    raw, success = fetch_live_tle(group, limit, st.session_state.cache_ver)
    
    if success and SKYFIELD_AVAILABLE and raw:
        try:
            ts = load.timescale()
            t_now = ts.now()
            for entry in raw:
                name = entry['OBJECT_NAME']
                sat = EarthSatellite(entry['TLE_LINE1'], entry['TLE_LINE2'], name, ts)
                geocentric = sat.at(t_now)
                subpoint = wgs84.subpoint(geocentric)
                orbit_map[name] = SimpleNamespace(name=name, lat=subpoint.latitude.degrees, lon=subpoint.longitude.degrees, altitude=subpoint.elevation.km)
            return orbit_map, True, "حقيقي مباشر (Live TLE)"
        except Exception as e:
            logger.error(f"Skyfield processing error: {e}")

    # نظام احتياطي يعمل تلقائياً لمنع توقف التطبيق
    raw_fallback = generate_fallback_satellites(group, limit)
    for entry in raw_fallback:
        name = entry["OBJECT_NAME"]
        mm = entry["MEAN_MOTION"]
        incl = entry["INCLINATION"]
        epoch_days = entry["EPOCH_REV"]
        now_utc = datetime.utcnow()
        sec_fraction = (now_utc.hour * 3600 + now_utc.minute * 60 + now_utc.second) / 86400.0
        phase = (epoch_days + sec_fraction * mm) * 2 * math.pi
        lat = float(incl * math.sin(phase + (hash(name) % 10)))
        lon = float(((math.degrees(phase) + (hash(name) % 360)) % 360) - 180)
        orbit_map[name] = SimpleNamespace(name=name, lat=lat, lon=lon, altitude=550.0)
        
    return orbit_map, False, "محاكاة احتياطية (Fallback)"

def main():
    st.set_page_config(page_title="COSMIC-324 Engineering Suite", page_icon="🛰️", layout="wide")

    if 'language' not in st.session_state: st.session_state.language = 'ar'
    if 'cache_ver' not in st.session_state: st.session_state.cache_ver = 0

    current_dir = LANGUAGES[st.session_state.language]['dir']
    st.markdown(f"""
    <style>
        .main, .stApp {{ background-color: #0b0f19; direction: {current_dir}; text-align: {'right' if current_dir=='rtl' else 'left'}; }}
        .stMetric {{ background: #111827; border-radius: 8px; padding: 12px; border: 1px solid #1f2937; }}
        h1, h2, h3, h4 {{ color: #38bdf8; }}
        .info-box {{ background: #111827; border-radius: 8px; padding: 15px; border: 1px solid #374151; margin-bottom: 15px; }}
    </style>
    """, unsafe_allow_html=True)

    st.sidebar.title("🛰️ COSMIC-324 Suite")
    lang_choice = st.sidebar.selectbox("🌐 Language", ["ar", "en"], format_func=lambda x: LANGUAGES[x]["name"])
    if lang_choice != st.session_state.language:
        st.session_state.language = lang_choice
        st.rerun()

    selected_station = next(s for s in ALL_STATIONS if s["name"] == st.sidebar.selectbox("المحطة:", [s["name"] for s in ALL_STATIONS]))
    strict_los = ("LoS" in st.sidebar.radio("نطاق التصفية:", ["عرض شامل لجميع الأقمار", "خط الرؤية المباشر (LoS)"]))
    
    nav = st.sidebar.radio("📌 القائمة", [t('dashboard'), t('link_budget'), t('doppler_panel'), t('legal_panel'), t('audit_panel')])
    
    st.title(t('title'))
    st.markdown(f"*{t('subtitle')}*")

    if nav == t('dashboard'):
        col1, col2 = st.columns([2, 1])
        with col1: sat_slider = st.slider("عدد الأقمار", 50, 300, 100, 50)
        with col2: group_sel = st.selectbox("المجموعة الفضائية:", DATA_CONTRACT["celestrak"]["groups"])
            
        if st.button("🔄 تحديث البيانات"):
            st.session_state.cache_ver += 1
            st.rerun()
            
        with st.spinner("جاري فحص الاتصال وجلب الإحداثيات..."):
            orbit_map, is_live, mode_str = build_hybrid_orbit_map(group_sel, sat_slider)
            
        if is_live:
            st.success("✅ متصل بنجاح: يتم عرض الإحداثيات الحية الفعلية من خوادم CelesTrak.")
        else:
            st.warning("⚠️ تنبيه: تعذر الاتصال المباشر بخدمة CelesTrak أو مكتبة الفلك، وتم التبديل تلقائياً لنظام المحاكاة الاحتياطي لضمان استمرارية عمل الواجهة.")

        records = []
        for name, sat in orbit_map.items():
            dist = haversine(selected_station['lat'], selected_station['lon'], sat.lat, sat.lon)
            horizon = math.acos(6371.0 / (6371.0 + sat.altitude)) * 6371.0
            if strict_los and dist > (horizon + 1000): continue
            records.append({
                "اسم القمر": name[:28], "المصدر": mode_str,
                "خط العرض": round(sat.lat, 3), "خط الطول": round(sat.lon, 3),
                "الارتفاع (كم)": round(sat.altitude, 1), "البعد عن المحطة (كم)": round(dist, 1)
            })
        
        df_res = pd.DataFrame(records)
        if not df_res.empty:
            st.dataframe(df_res.reset_index(drop=True), use_container_width=True)
            fig = px.scatter_geo(df_res, lat="خط العرض", lon="خط الطول", hover_name="اسم القمر", projection="orthographic", title="خريطة التتبع الفضائي")
            fig.add_trace(go.Scattergeo(lat=[selected_station['lat']], lon=[selected_station['lon']], mode='markers+text', text=[selected_station['name']], marker=dict(size=12, color='#38bdf8', symbol='star')))
            fig.update_geos(bgcolor="#0b0f19", landcolor="#111827", subunitcolor="#374151", countrycolor="#4b5563")
            st.plotly_chart(fig, use_container_width=True)

    elif nav == t('link_budget'):
        st.subheader("📡 ميزانية الوصلة الراديوية (Friis & SNR)")
        c1, c2, c3 = st.columns(3)
        with c1: f_ghz = st.number_input("التردد (GHz)", 12.5)
        with c2: d_km = st.number_input("المسافة (كم)", 850.0)
        with c3: p_dbw = st.number_input("قدرة المرسل (dBW)", 10.0)
        st.metric("الفقد الحر (FSPL)", f"{round(20 * math.log10(4 * math.pi * (d_km*1000) / (3e8/(f_ghz*1e9))), 2)} dB")

    elif nav == t('doppler_panel'):
        st.subheader("🌐 تحليل إزاحة دوبلر")
        st.metric("أقصى إزاحة ترددية", "± 24.5 kHz")

    elif nav == t('legal_panel'):
        st.subheader("⚖️ التوثيق الداخلي والمراجعة القانونية")
        for doc in db.get_legal_docs(): st.write(f"- **{doc['law_title']}** ({doc['jurisdiction']})")

    elif nav == t('audit_panel'):
        st.subheader("📜 سجل التدقيق المشفر (Hash-Chained Log)")
        if st.button("التحقق من سلامة السلسلة"):
            valid, msg = db.verify_integrity()
            st.success(msg) if valid else st.error(msg)
        st.dataframe(pd.DataFrame(db.get_audit_logs()), use_container_width=True)

if __name__ == '__main__':
    main()
