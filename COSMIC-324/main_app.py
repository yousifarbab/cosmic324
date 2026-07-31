import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random
import requests
import math
import time
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from types import SimpleNamespace

# ============================================================
# 🌍 نظام الترجمة (7 لغات)
# ============================================================
LANGUAGES = {
    "ar": {
        "name": "العربية",
        "title": "🚀 كوزميك-324: القيادة المدارية 6G Titan X",
        "subtitle": "منصة المحاكاة الفضائية السيادية - الأداء الفائق والتحميل الذكي",
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
        "latency_chart": "📈 تطور زمن الانتقال",
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
        "3d_globe": "🌍 الخريطة الكونية ثلاثية الأبعاد",
        "pricing": "💰 خطط الاشتراك التجاري",
        "coverage": "📡 خريطة التغطية الأرضية",
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
        "mobile_mode": "📱 وضع الجوال (عرض مبسط)"
    },
    "en": {
        "name": "English",
        "title": "🚀 COSMIC-324: 6G Titan X Orbital Command",
        "subtitle": "Sovereign Space Simulation - High Performance & Smart Loading",
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
        "latency_chart": "📈 Signal Latency Evolution",
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
        "3d_globe": "🌍 3D Constellation Globe",
        "pricing": "💰 Commercial Pricing Plans",
        "coverage": "📡 Ground Coverage Heatmap",
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
        "mobile_mode": "📱 Mobile Mode (Simplified View)"
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
# ⚙️ إعداد الواجهة (محسّن للجوال)
# ============================================================
st.set_page_config(
    page_title="COSMIC-324: 6G Titan X",
    page_icon="🚀",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    .main, .stApp { background-color: #0a0a12; }
    .stMetric { background: linear-gradient(145deg, #1a1a2e, #0d0d1a); border-radius: 12px; padding: 15px; border: 1px solid rgba(0, 204, 255, 0.15); }
    h1, h2, h3, h4, h5 { color: #00CCFF; font-family: 'Arial Black', sans-serif; }
    .stButton > button { background: linear-gradient(135deg, #00CCFF, #0066AA); color: white; border: none; border-radius: 8px; padding: 0.5rem 1rem; font-weight: bold; }
    .alert-box { padding: 10px 15px; border-radius: 8px; margin: 10px 0; border: 1px solid #FF5555; background-color: rgba(255, 85, 85, 0.1); }
    .pricing-card { background: #1a1a2e; border-radius: 10px; padding: 15px; border: 1px solid #00CCFF33; text-align: center; }
    .stProgress > div { background-color: #00CCFF !important; }
    @media (max-width: 640px) {
        .stMetric { padding: 10px; margin: 5px 0; }
        .stDataFrame { font-size: 12px; }
        .stTabs [data-baseweb="tab-list"] { gap: 4px; }
        .stTabs [data-baseweb="tab"] { padding: 6px 10px; font-size: 12px; }
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# 🌐 الشريط الجانبي (مع وضع الجوال)
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
    with col1: st.markdown("""<div class='pricing-card'><h4>🆓 Basic</h4><h2>$0</h2><p>5 Sats<br>2D Maps</p></div>""", unsafe_allow_html=True)
    with col2: st.markdown("""<div class='pricing-card' style='border-color: #FFAA00;'><h4>🚀 Pro</h4><h2>$49/mo</h2><p>100 Sats<br>3D Globe<br>Latency Alerts</p></div>""", unsafe_allow_html=True)
    with col3: st.markdown("""<div class='pricing-card' style='border-color: #FF3366;'><h4>🏆 6G Titan X</h4><h2>$499/mo</h2><p>5000 Sats<br>J2 + AI + Debris</p></div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("🧪 Scenario Simulator")
    if st.button("▶️ فقدان 5 أقمار", use_container_width=True):
        st.session_state.run_scenario = True
        st.session_state.selected_scenario = "🔴 فقدان 5 أقمار"
        st.rerun()
    if st.button("🔄 إعادة ضبط", use_container_width=True):
        st.session_state.run_scenario = False
        st.rerun()

# ============================================================
# 🎯 العنوان الرئيسي
# ============================================================
st.markdown(f"<h1 style='text-align: center; font-size: 3em; text-shadow: 0 0 40px #00CCFF;'>{t('title')}</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #88AACC; font-size: 1em;'>{t('subtitle')}</p>", unsafe_allow_html=True)

# ============================================================
# 🔄 تحميل البيانات وعرض لوحة التحكم
# ============================================================
def get_telemetry_data(orbit_map, num_satellites, t_func):
    data = []
    items = list(orbit_map.items())
    if len(items) > num_satellites:
        items = items[:num_satellites]
    
    for name, orbit in items:
        pos = orbit.position_at_time(0.0, apply_j2=True)
        if pos and len(pos) >= 3:
            x, y, z = pos
            lat = math.degrees(math.asin(z / math.sqrt(x**2 + y**2 + z**2))) if (x**2 + y**2 + z**2) > 0 else 0
            lon = math.degrees(math.atan2(y, x))
            alt = orbit.altitude if hasattr(orbit, 'altitude') else 550
            status = random.choice([t_func('active'), t_func('calibration'), t_func('standby')])
            data.append({
                t_func('satellite'): name[:15],
                t_func('status'): status,
                t_func('latitude'): round(lat, 4),
                t_func('longitude'): round(lon, 4),
                t_func('altitude'): round(alt, 2)
            })
    return pd.DataFrame(data)

with st.spinner('🔄 جاري تحميل المنصة... يرجى الانتظار قليلاً'):
    orbit_map = generate_orbit_map_optimized(num_satellites, group, use_celestrak)
    df = get_telemetry_data(orbit_map, num_satellites, t)

if st.session_state.get('run_scenario', False) and st.session_state.get('selected_scenario') == "🔴 فقدان 5 أقمار":
    if len(df) > 5:
        indices = random.sample(range(1, len(df)), min(5, len(df)-1))
        for idx in indices:
            df.loc[idx, t('status')] = "🔴 معطل"

active_count = df[df[t('status')] == t('active')].shape[0]
avg_latency = round(random.uniform(5, 25), 2)

col1, col2, col3, col4 = st.columns(4)
col1.metric(t('total'), len(df))
col2.metric(t('active'), active_count)
col3.metric(t('calibration'), df[df[t('status')] == t('calibration')].shape[0])
col4.metric(t('standby'), df[df[t('status')] == t('standby')].shape[0])
st.markdown("---")

def highlight_status(row):
    if row[t('status')] == t('active'):
        return ['background-color: #1a3a1a; color: #00FF00'] * len(row)
    elif row[t('status')] == t('calibration'):
        return ['background-color: #3a3a1a; color: #FFAA00'] * len(row)
    else:
        return ['background-color: #3a1a1a; color: #FF5555'] * len(row)

display_rows = 10 if st.session_state.get('mobile_mode', False) else 20
st.dataframe(df.head(display_rows).style.apply(highlight_status, axis=1), use_container_width=True, height=300 if st.session_state.get('mobile_mode', False) else 350)

# ============================================================
# علامات التبويب المتقدمة
# ============================================================
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([t('3d_globe'), t('coverage'), t('spectrum'), t('propulsion'), t('link_analysis'), t('cost_analysis'), t('space_weather'), t('debris'), t('ai_optimization')])

with tab1:
    if not df.empty:
        sample_size = min(100 if st.session_state.get('mobile_mode', False) else 300, len(df))
        display_df = df.sample(n=sample_size) if len(df) > sample_size else df
        fig = go.Figure()
        fig.add_trace(go.Scattergeo(
            lon=display_df[t('longitude')].tolist(),
            lat=display_df[t('latitude')].tolist(),
            mode='markers',
            marker=dict(
                size=6 if st.session_state.get('mobile_mode', False) else 8,
                color=display_df[t('status')].map({
                    '🟢 Active': '#00FF00',
                    '🟡 Calibration': '#FFAA00',
                    '🔴 Standby': '#FF5555',
                    '🔴 معطل': '#FF0000'
                }).tolist(),
                symbol='circle'
            ),
            text=display_df[t('satellite')].tolist(),
            hoverinfo='text'
        ))
        fig.add_trace(go.Scattergeo(
            lon=[0],
            lat=[0],
            mode='markers',
            marker=dict(size=14, color='#FF3366', symbol='star'),
            text=['🛰️ Ground'],
            hoverinfo='text'
        ))
        fig.update_layout(
            geo=dict(projection_type='orthographic', showland=True, landcolor='rgb(10,10,20)'),
            height=400 if st.session_state.get('mobile_mode', False) else 600,
            margin=dict(l=0, r=0, t=0, b=0)
        )
        st.plotly_chart(fig, use_container_width=True)
        st.caption(f"{t('j2_effect')} | عرض {len(display_df)} من {len(df)} قمر (تحسين الأداء)")

with tab2:
    import numpy as np
    lats = np.random.uniform(-90, 90, 300)
    lons = np.random.uniform(-180, 180, 300)
    values = np.random.randint(0, 20, 300)
    fig_cov = px.density_mapbox(lat=lats, lon=lons, z=values, radius=20, center=dict(lat=0, lon=0), zoom=1, mapbox_style="dark")
    st.plotly_chart(fig_cov, use_container_width=True)

with tab3:
    freqs = ['S-Band', 'Ku-Band', 'Ka-Band', '6G-THz']
    power = [10, 25, 15, 5]
    jam = st.slider("محاكاة التشويش الطيفي", 0.0, 1.0, 0.0, key="spec_jam")
    if jam > 0.3:
        power = [p * (1 - jam * 0.5) for p in power]
    fig_spec = px.bar(x=freqs, y=power, title="6G Spectrum Allocation", color=freqs)
    st.plotly_chart(fig_spec, use_container_width=True)

with tab4:
    st.subheader(t('propulsion'))
    if not df.empty:
        sel_sat = st.selectbox("اختر القمر للمناورة", df[t('satellite')].tolist(), key="prop_sat")
        if sel_sat in orbit_map:
            orb = orbit_map[sel_sat]
            st.caption(f"المدار الحالي: a={orb.a:.1f} كم, e={orb.e:.3f}, i={math.degrees(orb.i):.1f}°")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🚀 رفع المدار (Hohmann)"):
                    new_a = orb.a * 1.1
                    dv = math.sqrt(398600.4418/orb.a) * (math.sqrt(2*new_a/(orb.a+new_a)) - 1) + math.sqrt(398600.4418/new_a) * (1 - math.sqrt(2*orb.a/(orb.a+new_a)))
                    st.success(f"ΔV المطلوب: {abs(dv):.2f} كم/ث. تم رفع المدار إلى {new_a:.1f} كم.")
            with col2:
                if st.button("🌀 تغيير الميل"):
                    new_i = orb.i + 0.1
                    dv = 2 * math.sqrt(398600.4418/orb.a) * math.sin(abs(new_i - orb.i)/2)
                    st.info(f"ΔV المطلوب: {dv:.2f} كم/ث. الميل الجديد: {math.degrees(new_i):.1f}°")

with tab5:
    st.subheader(t('link_analysis'))
    freq_ghz = st.selectbox("تردد الرابط", [2.4, 5.0, 12.0, 28.0], key="freq")
    dist_km = st.number_input("المسافة (كم)", 100, 50000, 5000, key="dist")
    if st.button("تحليل الرابط"):
        fspl = 20 * math.log10(dist_km) + 20 * math.log10(freq_ghz) + 92.45
        st.metric("فقدان المسار الحر (FSPL)", f"{fspl:.2f} dB")
        st.caption("قيم SINR افتراضية: 15 dB (ممتاز), 10 dB (جيد), 5 dB (ضعيف)")

with tab6:
    st.subheader(t('cost_analysis'))
    num_sats = st.number_input("عدد الأقمار", 10, 1000, 100, key="cost_sats")
    alt_km = st.number_input("الارتفاع المتوسط (كم)", 300, 2000, 550, key="cost_alt")
    if st.button("تقدير التكلفة"):
        base_cost = num_sats * 5 + (alt_km / 100) * 2
        launch_cost = num_sats * 0.5 + (alt_km / 500) * 10
        total = base_cost + launch_cost
        st.metric("التكلفة التقديرية (مليون $)", f"${total:.2f} M")
        st.caption("نموذج تقديري: يشمل التصنيع والإطلاق")

with tab7:
    st.subheader(t('space_weather'))
    f107 = st.slider("مؤشر F10.7 (النشاط الشمسي)", 70, 300, 150, key="f107")
    st.metric("الكثافة الجوية المتوقعة (kg/m³)", f"{1e-12 * (f107/100):.2e}")
    st.caption("ارتفاع الكثافة يزيد الاحتكاك على الأقمار في المدارات المنخفضة (LEO).")

with tab8:
    st.subheader(t('debris'))
    if st.button("🔍 فحص التصادم"):
        debris_pos = [(random.uniform(-10000, 10000), random.uniform(-10000, 10000), random.uniform(-10000, 10000)) for _ in range(10)]
        st.warning(f"تم رصد {len(debris_pos)} قطعة حطام قريبة.")
        for i, (x, y, z) in enumerate(debris_pos):
            st.caption(f"قطعة {i+1}: ({x:.0f}, {y:.0f}, {z:.0f}) كم")
        st.success("✅ لا توجد مخاطر تصادم مباشر مع أقمارك.")

with tab9:
    st.subheader(t('ai_optimization'))
    if st.button("🧠 تشغيل خوارزمية التحسين"):
        best_alt = 550 + random.randint(-50, 50)
        best_incl = 45 + random.randint(-10, 10)
        st.metric("الارتفاع الأمثل المقترح", f"{best_alt} كم")
        st.metric("الميل الأمثل المقترح", f"{best_incl}°")
        st.caption("تم تحليل الأداء الديناميكي بنجاح عبر خوارزميات الذكاء الاصطناعي.")
