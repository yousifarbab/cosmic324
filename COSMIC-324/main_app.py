import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random
import requests
import math
from datetime import datetime
from typing import Dict, List, Optional
from types import SimpleNamespace

# ============================================================
# 🌍 نظام الترجمة (7 لغات) - مختصر للعربية والإنجليزية
# ============================================================
LANGUAGES = {
    "ar": {
        "name": "العربية",
        "title": "🚀 كوزميك-324: القيادة المدارية 6G",
        "subtitle": "منصة التتبع المداري الحي متعددة اللغات",
        "params": "⚙️ إعدادات المحاكاة",
        "sat_count": "عدد الأقمار",
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
        "latency_chart": "📈 تطور زمن الانتقال",
        "step": "الخطوة",
        "latency_ms": "زمن الانتقال (مللي ثانية)",
        "last_update": "آخر تحديث",
        "map_title": "🌍 خريطة الأقمار الصناعية",
        "avg_alt": "متوسط الارتفاع",
        "max_alt": "أقصى ارتفاع",
        "min_alt": "أدنى ارتفاع",
        "celestrak": "📡 جلب بيانات حقيقية من Celestrak",
        "group": "اختر المجموعة"
    },
    "en": {
        "name": "English",
        "title": "🚀 COSMIC-324: 6G Orbital Command",
        "subtitle": "Multi-language Live Orbital Tracking Platform",
        "params": "⚙️ Simulation Parameters",
        "sat_count": "Number of Satellites",
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
        "latency_chart": "📈 Signal Latency Evolution",
        "step": "Step",
        "latency_ms": "Latency (ms)",
        "last_update": "Last Update",
        "map_title": "🌍 Satellite Map",
        "avg_alt": "Avg Altitude",
        "max_alt": "Max Altitude",
        "min_alt": "Min Altitude",
        "celestrak": "📡 Fetch Live Data from Celestrak",
        "group": "Select Group"
    }
}

def t(key: str) -> str:
    lang = st.session_state.get('language', 'ar')
    return LANGUAGES.get(lang, LANGUAGES['ar']).get(key, key)

# ============================================================
# 📡 جلب بيانات Celestrak الحقيقية
# ============================================================
@st.cache_data(ttl=3600)
def fetch_celestrak_data(group: str = "starlink", max_satellites: int = 100) -> List[Dict]:
    url = f"https://celestrak.org/NORAD/elements/gp.php?GROUP={group}&FORMAT=json"
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        if response.text.startswith('{'):
            data = response.json()
            return data[:max_satellites]
        return []
    except Exception as e:
        st.warning(f"⚠️ Could not fetch Celestrak data: {e}")
        return []

def tle_to_orbit(tle_entry: Dict) -> Optional[SimpleNamespace]:
    try:
        mean_motion = float(tle_entry.get('MEAN_MOTION', 0))
        eccentricity = float(tle_entry.get('ECCENTRICITY', 0))
        inclination = math.radians(float(tle_entry.get('INCLINATION', 0)))
        raan = math.radians(float(tle_entry.get('RA_OF_ASC_NODE', 0)))
        arg_perigee = math.radians(float(tle_entry.get('ARG_OF_PERICENTER', 0)))
        mean_anomaly = math.radians(float(tle_entry.get('MEAN_ANOMALY', 0)))
        if mean_motion <= 0:
            return None
        GM = 398600.4418
        n = mean_motion * 2 * math.pi / 86400.0
        a = (GM / (n ** 2)) ** (1.0/3.0)
        period = 86400.0 / mean_motion
        
        def position_at_time(t: float):
            M = mean_anomaly + 2 * math.pi * t / period
            E = M
            for _ in range(6):
                E = E - (E - eccentricity * math.sin(E) - M) / (1 - eccentricity * math.cos(E))
            x_orbit = a * (math.cos(E) - eccentricity)
            y_orbit = a * math.sqrt(1 - eccentricity**2) * math.sin(E)
            z_orbit = 0.0
            x1 = x_orbit * math.cos(arg_perigee) - y_orbit * math.sin(arg_perigee)
            y1 = x_orbit * math.sin(arg_perigee) + y_orbit * math.cos(arg_perigee)
            z1 = z_orbit
            x2 = x1
            y2 = y1 * math.cos(inclination) - z1 * math.sin(inclination)
            z2 = y1 * math.sin(inclination) + z1 * math.cos(inclination)
            x_final = x2 * math.cos(raan) - y2 * math.sin(raan)
            y_final = x2 * math.sin(raan) + y2 * math.cos(raan)
            z_final = z2
            return (x_final, y_final, z_final)
        
        orbit = SimpleNamespace()
        orbit.position_at_time = position_at_time
        orbit.name = tle_entry.get('OBJECT_NAME', 'SAT')
        orbit.altitude = a - 6371
        return orbit
    except Exception:
        return None

def generate_orbit_map(num_satellites: int = 100, group: str = "starlink") -> Dict:
    raw_data = fetch_celestrak_data(group, num_satellites)
    orbit_map = {}
    if raw_data:
        for entry in raw_data:
            orbit = tle_to_orbit(entry)
            if orbit:
                orbit_map[orbit.name] = orbit
        if orbit_map:
            return orbit_map
    # Mock data if Celestrak fails
    for i in range(num_satellites):
        a = 7000 + random.randint(-300, 300)
        e = random.uniform(0.01, 0.08)
        incl = math.radians(random.uniform(30, 70))
        omega = random.uniform(0, 2 * math.pi)
        Omega = random.uniform(0, 2 * math.pi)
        M0 = random.uniform(0, 2 * math.pi)
        period = 2 * math.pi * math.sqrt((a ** 3) / 398600.4418)
        
        def position_at_time(t: float, a=a, e=e, incl=incl, omega=omega, Omega=Omega, M0=M0, period=period):
            M = M0 + 2 * math.pi * t / period
            E = M
            for _ in range(6):
                E = E - (E - e * math.sin(E) - M) / (1 - e * math.cos(E))
            x_orbit = a * (math.cos(E) - e)
            y_orbit = a * math.sqrt(1 - e**2) * math.sin(E)
            z_orbit = 0.0
            x1 = x_orbit * math.cos(omega) - y_orbit * math.sin(omega)
            y1 = x_orbit * math.sin(omega) + y_orbit * math.cos(omega)
            z1 = z_orbit
            x2 = x1
            y2 = y1 * math.cos(incl) - z1 * math.sin(incl)
            z2 = y1 * math.sin(incl) + z1 * math.cos(incl)
            x_final = x2 * math.cos(Omega) - y2 * math.sin(Omega)
            y_final = x2 * math.sin(Omega) + y2 * math.cos(Omega)
            z_final = z2
            return (x_final, y_final, z_final)
        
        orbit = SimpleNamespace()
        orbit.position_at_time = position_at_time
        orbit.name = f"SAT-{i+1}"
        orbit.altitude = a - 6371
        orbit_map[orbit.name] = orbit
    return orbit_map

# ============================================================
# ⚙️ إعداد الواجهة
# ============================================================
st.set_page_config(page_title="COSMIC-324: 6G Orbital Command", page_icon="🚀", layout="wide")

st.markdown("""
<style>
    .main, .stApp { background-color: #0a0a12; }
    .stMetric { background: linear-gradient(145deg, #1a1a2e, #0d0d1a); border-radius: 12px; padding: 15px; border: 1px solid rgba(0, 204, 255, 0.15); }
    h1, h2, h3, h4, h5 { color: #00CCFF; font-family: 'Arial Black', sans-serif; }
    .stButton > button { background: linear-gradient(135deg, #00CCFF, #0066AA); color: white; border: none; border-radius: 8px; padding: 0.5rem 1rem; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# 🌐 الشريط الجانبي
# ============================================================
with st.sidebar:
    st.image("https://via.placeholder.com/300x60/0a0a12/00CCFF?text=COSMIC-324", use_column_width=True)
    st.markdown("---")
    
    lang_options = {code: info["name"] for code, info in LANGUAGES.items()}
    selected_lang = st.selectbox(
        "🌐 Language / اللغة",
        options=list(lang_options.keys()),
        format_func=lambda x: lang_options[x],
        index=list(lang_options.keys()).index(st.session_state.get('language', 'ar'))
    )
    if selected_lang != st.session_state.get('language', 'ar'):
        st.session_state.language = selected_lang
        st.rerun()
    
    st.markdown("---")
    st.header(t("params"))
    
    num_satellites = st.slider(t("sat_count"), 5, 100, 20, 5)
    
    st.markdown("---")
    st.subheader(t("celestrak"))
    group = st.selectbox(t("group"), ["starlink", "gps", "active", "oneweb", "iridium"])
    use_celestrak = st.checkbox("استخدام بيانات حقيقية من Celestrak")
    
    if st.button(t("update_btn"), use_container_width=True):
        st.rerun()
    
    st.caption(f"{t('last_update')}: {datetime.now().strftime('%H:%M:%S')}")

# ============================================================
# 🎯 العنوان الرئيسي
# ============================================================
st.markdown(f"<h1 style='text-align: center; font-size: 3em; text-shadow: 0 0 40px #00CCFF;'>{t('title')}</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #88AACC; font-size: 1.1em;'>{t('subtitle')}</p>", unsafe_allow_html=True)

# ============================================================
# 📊 توليد البيانات (مع خيار Celestrak)
# ============================================================
if use_celestrak:
    orbit_map = generate_orbit_map(num_satellites, group)
    data = []
    for name, orbit in list(orbit_map.items())[:num_satellites]:
        pos = orbit.position_at_time(0.0)
        if pos and len(pos) >= 3:
            x, y, z = pos
            lat = math.degrees(math.asin(z / math.sqrt(x**2 + y**2 + z**2))) if (x**2 + y**2 + z**2) > 0 else 0
            lon = math.degrees(math.atan2(y, x))
            alt = orbit.altitude if hasattr(orbit, 'altitude') else 550
            status = random.choice([t('active'), t('calibration'), t('standby')])
            data.append({
                t('satellite'): name[:12],
                t('status'): status,
                t('latitude'): round(lat, 4),
                t('longitude'): round(lon, 4),
                t('altitude'): round(alt, 2)
            })
    df = pd.DataFrame(data)
else:
    def generate_satellite_data(n: int) -> pd.DataFrame:
        data = []
        statuses = [t('active'), t('calibration'), t('standby')]
        for i in range(n):
            data.append({
                t('satellite'): f"SAT-{i+1}",
                t('status'): random.choice(statuses),
                t('latitude'): round(random.uniform(-90, 90), 4),
                t('longitude'): round(random.uniform(-180, 180), 4),
                t('altitude'): round(random.uniform(400, 1200), 2)
            })
        return pd.DataFrame(data)
    df = generate_satellite_data(num_satellites)

# ============================================================
# 📈 الإحصائيات السريعة
# ============================================================
col1, col2, col3, col4 = st.columns(4)
col1.metric(t('total'), len(df))
col2.metric(t('active'), df[df[t('status')] == t('active')].shape[0])
col3.metric(t('calibration'), df[df[t('status')] == t('calibration')].shape[0])
col4.metric(t('standby'), df[df[t('status')] == t('standby')].shape[0])

st.markdown("---")

# ============================================================
# 🎨 جدول البيانات الملون
# ============================================================
def highlight_status(row):
    if row[t('status')] == t('active'):
        return ['background-color: #1a3a1a; color: #00FF00'] * len(row)
    elif row[t('status')] == t('calibration'):
        return ['background-color: #3a3a1a; color: #FFAA00'] * len(row)
    elif row[t('status')] == t('standby'):
        return ['background-color: #3a1a1a; color: #FF5555'] * len(row)
    return [''] * len(row)

st.dataframe(
    df.style.apply(highlight_status, axis=1),
    use_container_width=True,
    height=400,
    column_config={
        t('satellite'): "🛰️ " + t('satellite'),
        t('status'): "📊 " + t('status'),
        t('latitude'): st.column_config.NumberColumn(t('latitude'), format="%.4f°"),
        t('longitude'): st.column_config.NumberColumn(t('longitude'), format="%.4f°"),
        t('altitude'): st.column_config.NumberColumn(t('altitude'), format="%.2f km")
    }
)

# ============================================================
# 🌍 خريطة 2D تفاعلية
# ============================================================
st.markdown("---")
st.subheader(t('map_title'))

fig_map = px.scatter_mapbox(
    df,
    lat=t('latitude'),
    lon=t('longitude'),
    color=t('status'),
    hover_name=t('satellite'),
    hover_data={t('altitude'): True},
    color_discrete_map={
        t('active'): '#00FF00',
        t('calibration'): '#FFAA00',
        t('standby'): '#FF5555'
    },
    zoom=2,
    height=500,
    title=t('map_title')
)
fig_map.update_layout(mapbox_style="dark", mapbox_accesstoken=None)
fig_map.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig_map, use_container_width=True)

# ============================================================
# 📊 تحليلات متقدمة
# ============================================================
st.markdown("---")
st.subheader("📊 تحليلات متقدمة")

col_a1, col_a2, col_a3 = st.columns(3)
col_a1.metric(t('avg_alt'), f"{df[t('altitude')].mean():.1f} km")
col_a2.metric(t('max_alt'), f"{df[t('altitude')].max():.1f} km")
col_a3.metric(t('min_alt'), f"{df[t('altitude')].min():.1f} km")

fig_hist = px.histogram(df, x=t('altitude'), color=t('status'), 
                         title="توزيع الارتفاعات حسب الحالة",
                         color_discrete_map={
                             t('active'): '#00FF00',
                             t('calibration'): '#FFAA00',
                             t('standby'): '#FF5555'
                         })
fig_hist.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig_hist, use_container_width=True)

# ============================================================
# 📈 منحنى Latency
# ============================================================
st.markdown("---")
st.subheader(t('latency_chart'))

latency_data = pd.DataFrame({
    t('step'): list(range(1, 21)),
    t('latency_ms'): [round(3.0 + i * 0.1 + random.uniform(-0.2, 0.2), 2) for i in range(20)]
})

fig = px.line(
    latency_data,
    x=t('step'),
    y=t('latency_ms'),
    title=t('latency_chart'),
    markers=True
)
fig.update_traces(line_color='#00CCFF', line_width=3, marker_size=8)
fig.update_layout(
    xaxis_title=t('step'),
    yaxis_title=t('latency_ms'),
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)'
)
st.plotly_chart(fig, use_container_width=True)

# ============================================================
# 📌 الحالة السفلية
# ============================================================
st.markdown("---")
col_f1, col_f2, col_f3 = st.columns(3)
col_f1.caption(f"🛰️ COSMIC-324 v3.0 | {len(df)} {t('satellite')}")
col_f2.caption(f"🌍 {LANGUAGES[st.session_state.get('language', 'ar')]['name']}")
col_f3.caption(f"🔐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
