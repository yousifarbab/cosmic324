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
from datetime import datetime
from typing import Dict, List, Optional
from types import SimpleNamespace

# ============================================================
# 🌍 نظام الترجمة (المختصر للعربية والإنجليزية)
# ============================================================
LANGUAGES = {
    "ar": {
        "name": "العربية",
        "title": "🚀 كوزميك-324: القيادة المدارية 6G Titan X",
        "subtitle": "منصة المحاكاة الفضائية السيادية",
        "welcome": "🌟 مرحباً بك في منصة كوزميك-324، منصة المحاكاة الفضائية المتكاملة.",
        "params": "⚙️ إعدادات المحاكاة",
        "sat_count": "عدد الأقمار",
        "update_btn": "🔄 تحديث",
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
        "latency_ms": "زمن الانتقال (م.ث)",
        "last_update": "آخر تحديث",
        "avg_alt": "متوسط الارتفاع",
        "max_alt": "أقصى ارتفاع",
        "min_alt": "أدنى ارتفاع",
        "celestrak": "📡 جلب بيانات Celestrak",
        "group": "المجموعة",
        "alert_latency": "⚠️ ارتفاع زمن الانتقال!",
        "alert_satellites": "⚠️ انخفاض الأقمار النشطة!",
        "alert_threshold": "عتبة التنبيه (م.ث)",
        "active_threshold": "الحد الأدنى للأقمار النشطة",
        "3d_globe": "🌍 الخريطة الكونية ثلاثية الأبعاد",
        "pricing": "💰 خطط الاشتراك",
        "coverage": "📡 خريطة التغطية",
        "spectrum": "📶 محلل الطيف 6G",
        "j2_effect": "🌀 تأثير J2",
        "propulsion": "🚀 محرك الدفع",
        "link_analysis": "📡 تحليل الارتباط",
        "cost_analysis": "💰 التحليل المالي",
        "space_weather": "☀️ الطقس الفضائي",
        "debris": "🛸 الحطام والتصادم",
        "ai_optimization": "🧠 تحسين الذكاء الاصطناعي",
        "collaboration": "🤝 مشاركة المهمة",
        "auto_refresh": "⏱️ تحديث تلقائي",
        "refresh_interval": "الفاصل (ثانية)",
        "start_auto": "▶️ تشغيل",
        "stop_auto": "⏹️ إيقاف",
        "performance_mode": "⚡ وضع الأداء",
        "full_resolution": "دقة كاملة (5000)",
        "high_speed": "سرعة عالية (100)",
        "mobile_mode": "📱 وضع الجوال"
    },
    "en": {
        "name": "English",
        "title": "🚀 COSMIC-324: 6G Titan X Orbital Command",
        "subtitle": "Sovereign Space Simulation Platform",
        "welcome": "🌟 Welcome to COSMIC-324, an integrated space simulation platform.",
        "params": "⚙️ Simulation Parameters",
        "sat_count": "Number of Satellites",
        "update_btn": "🔄 Refresh",
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
        "celestrak": "📡 Fetch Celestrak Data",
        "group": "Group",
        "alert_latency": "⚠️ High Latency!",
        "alert_satellites": "⚠️ Low Active Satellites!",
        "alert_threshold": "Alert Threshold (ms)",
        "active_threshold": "Min Active Satellites",
        "3d_globe": "🌍 3D Constellation Globe",
        "pricing": "💰 Pricing Plans",
        "coverage": "📡 Coverage Map",
        "spectrum": "📶 6G Spectrum Analyzer",
        "j2_effect": "🌀 J2 Effect",
        "propulsion": "🚀 Propulsion Engine",
        "link_analysis": "📡 Link Analysis",
        "cost_analysis": "💰 Cost Analysis",
        "space_weather": "☀️ Space Weather",
        "debris": "🛸 Debris & Collision",
        "ai_optimization": "🧠 AI Optimization",
        "collaboration": "🤝 Mission Sharing",
        "auto_refresh": "⏱️ Auto Refresh",
        "refresh_interval": "Interval (sec)",
        "start_auto": "▶️ Start",
        "stop_auto": "⏹️ Stop",
        "performance_mode": "⚡ Performance Mode",
        "full_resolution": "Full Resolution (5000)",
        "high_speed": "High Speed (100)",
        "mobile_mode": "📱 Mobile Mode"
    }
}

def t(key: str) -> str:
    lang = st.session_state.get('language', 'ar')
    return LANGUAGES.get(lang, LANGUAGES['en']).get(key, key)

# ============================================================
# 📡 جلب بيانات Celestrak
# ============================================================
@st.cache_data(ttl=600)
def fetch_celestrak_data(group: str = "starlink", max_satellites: int = 5000) -> List[Dict]:
    url = f"https://celestrak.org/NORAD/elements/gp.php?GROUP={group}&FORMAT=json"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        if response.text.startswith('['):
            return response.json()[:max_satellites]
    except:
        pass
    return []

@st.cache_resource
def generate_orbit_map(num_satellites: int = 5000, group: str = "starlink", use_celestrak: bool = True):
    orbit_map = {}
    if use_celestrak:
        raw_data = fetch_celestrak_data(group, num_satellites)
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
                except:
                    continue
            if orbit_map:
                return orbit_map

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
# ⚙️ إعداد الواجهة
# ============================================================
st.set_page_config(page_title="COSMIC-324: 6G Titan X", page_icon="🚀", layout="wide")
st.markdown("""
<style>
    .main, .stApp { background-color: #0a0a12; }
    .stMetric { background: linear-gradient(145deg, #1a1a2e, #0d0d1a); border-radius: 12px; padding: 15px; border: 1px solid rgba(0, 204, 255, 0.15); }
    h1, h2, h3, h4, h5 { color: #00CCFF; font-family: 'Arial Black', sans-serif; }
    .stButton > button { background: linear-gradient(135deg, #00CCFF, #0066AA); color: white; border: none; border-radius: 8px; padding: 0.5rem 1rem; font-weight: bold; }
    .copyright { text-align: center; color: #445566; font-size: 0.8em; padding: 20px 0; border-top: 1px solid #1a1a2e; margin-top: 20px; }
    .welcome-box { background: linear-gradient(135deg, #1a1a2e, #0d0d1a); border-radius: 12px; padding: 20px 25px; border: 1px solid #00CCFF33; margin-bottom: 20px; }
    .welcome-box h2 { color: #00CCFF; margin: 0 0 10px 0; }
    .welcome-box p { color: #88AACC; margin: 0; font-size: 1.05em; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# 🌐 الشريط الجانبي
# ============================================================
with st.sidebar:
    st.image("https://via.placeholder.com/300x60/0a0a12/00CCFF?text=COSMIC-324", use_column_width=True)
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
    if mobile_mode:
        st.session_state.mobile_mode = True
    
    perf_mode = st.radio(t("performance_mode"), [t("full_resolution"), t("high_speed")], index=0)
    max_display_sats = 50 if (perf_mode == t("high_speed") or mobile_mode) else 5000
    
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
    
    if st.button(t("update_btn"), use_container_width=True):
        st.cache_data.clear()
        st.cache_resource.clear()
        st.rerun()
    st.caption(f"{t('last_update')}: {datetime.now().strftime('%H:%M:%S')}")

# ============================================================
# 🎯 المحتوى الرئيسي
# ============================================================
st.markdown(f"<h1 style='text-align: center; font-size: 3.5em; text-shadow: 0 0 40px #00CCFF;'>{t('title')}</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #88AACC; font-size: 1.2em;'>{t('subtitle')}</p>", unsafe_allow_html=True)

st.markdown(f"""
<div class='welcome-box'>
    <h2>🌟 {t('welcome')}</h2>
    <p>{t('subtitle')}</p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# 📊 تحميل البيانات وعرضها
# ============================================================
@st.cache_data(ttl=60)
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

with st.spinner('🔄 جاري تحميل المنصة...'):
    orbit_map = generate_orbit_map(num_satellites, group, use_celestrak)
    df = get_telemetry_data(orbit_map, num_satellites, t)

# ============================================================
# 📈 الإحصائيات
# ============================================================
active_count = df[df[t('status')] == t('active')].shape[0]
calibration_count = df[df[t('status')] == t('calibration')].shape[0]
standby_count = df[df[t('status')] == t('standby')].shape[0]

col1, col2, col3, col4 = st.columns(4)
col1.metric(t('total'), len(df))
col2.metric(t('active'), active_count)
col3.metric(t('calibration'), calibration_count)
col4.metric(t('standby'), standby_count)
st.markdown("---")

# ============================================================
# 🎨 جدول البيانات
# ============================================================
def highlight_status(row):
    if row[t('status')] == t('active'):
        return ['background-color: #1a3a1a; color: #00FF00'] * len(row)
    elif row[t('status')] == t('calibration'):
        return ['background-color: #3a3a1a; color: #FFAA00'] * len(row)
    else:
        return ['background-color: #3a1a1a; color: #FF5555'] * len(row)

display_rows = 10 if st.session_state.get('mobile_mode', False) else 20
st.dataframe(
    df.head(display_rows).style.apply(highlight_status, axis=1),
    use_container_width=True,
    height=300 if st.session_state.get('mobile_mode', False) else 400,
    column_config={
        t('satellite'): "🛰️ " + t('satellite'),
        t('status'): "📊 " + t('status'),
        t('latitude'): st.column_config.NumberColumn(t('latitude'), format="%.4f°"),
        t('longitude'): st.column_config.NumberColumn(t('longitude'), format="%.4f°"),
        t('altitude'): st.column_config.NumberColumn(t('altitude'), format="%.2f km")
    }
)

# ============================================================
# 📈 منحنى Latency
# ============================================================
st.markdown("---")
st.subheader(t('latency_chart'))

latency_data = [{"Step": i+1, "Latency (ms)": round(3.0 + i * 0.12 + random.uniform(-0.2, 0.2), 2)} for i in range(20)]
latency_df = pd.DataFrame(latency_data)
fig_latency = px.line(latency_df, x="Step", y="Latency (ms)", markers=True)
fig_latency.update_traces(line_color='#00CCFF', line_width=3, marker_size=8)
fig_latency.add_hline(y=alert_threshold, line_dash="dash", line_color="red", annotation_text=f"⚠️ Threshold: {alert_threshold} ms")
fig_latency.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig_latency, use_container_width=True)

# ============================================================
# 🌍 الخريطة 3D
# ============================================================
def render_cosmic_globe(df, title="🌍 3D Constellation Globe"):
    fig = go.Figure()
    fig.update_layout(
        geo=dict(
            projection_type='orthographic',
            showland=True, landcolor='rgb(10,10,20)',
            coastlinecolor='rgb(60,60,80)',
            showocean=True, oceancolor='rgb(5,5,15)',
            showcountries=True, countrycolor='rgb(50,50,70)',
            bgcolor='rgba(0,0,0,0)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=600, margin=dict(l=0, r=0, t=40, b=0),
        title=dict(text=title, font=dict(size=22, color='#00CCFF'), x=0.5)
    )
    
    if not df.empty:
        fig.add_trace(go.Scattergeo(
            lon=df[t('longitude')].tolist(),
            lat=df[t('latitude')].tolist(),
            mode='markers+text',
            marker=dict(
                size=8,
                color=df[t('status')].map({
                    t('active'): '#00FF00',
                    t('calibration'): '#FFAA00',
                    t('standby'): '#FF5555'
                }).tolist(),
                symbol='circle'
            ),
            text=df[t('satellite')].tolist(),
            textposition='top center',
            textfont=dict(size=9, color='white'),
            hoverinfo='text'
        ))
    
    fig.add_trace(go.Scattergeo(
        lon=[0], lat=[0],
        mode='markers+text',
        marker=dict(size=16, color='#FF3366', symbol='star'),
        text=['🛰️ Ground'],
        textposition='bottom center',
        textfont=dict(size=12, color='#FF6699'),
        name='Ground Station'
    ))
    return fig

st.markdown("---")
st.subheader(t('3d_globe'))
st.plotly_chart(render_cosmic_globe(df, t('3d_globe')), use_container_width=True)

# ============================================================
# 📊 تحليلات متقدمة
# ============================================================
st.markdown("---")
st.subheader("📊 تحليلات متقدمة")
col_a1, col_a2, col_a3 = st.columns(3)
col_a1.metric(t('avg_alt'), f"{df[t('altitude')].mean():.1f} km")
col_a2.metric(t('max_alt'), f"{df[t('altitude')].max():.1f} km")
col_a3.metric(t('min_alt'), f"{df[t('altitude')].min():.1f} km")

# ============================================================
# 📌 حقوق الملكية الفكرية
# ============================================================
st.markdown("---")
st.markdown(f"""
<div class='copyright'>
    <p>🛰️ COSMIC-324: 6G Titan X Orbital Command v6.0</p>
    <p>© 2026 Yousif Zakaria Eissa Arbarb. جميع الحقوق محفوظة.</p>
    <p style='font-size: 0.8em; color: #334455;'>Licensed under AGPL-3.0 & Apache 2.0</p>
</div>
""", unsafe_allow_html=True)
