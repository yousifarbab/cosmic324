import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random
import requests
import math
import numpy as np
from datetime import datetime
from typing import Dict, List
from types import SimpleNamespace
import io

# ============================================================
# 🌍 نظام الترجمة واتجاه الصفحة (RTL/LTR)
# ============================================================
LANGUAGES = {
    "ar": {
        "name": "العربية",
        "dir": "rtl",
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
        "alert_threshold": "عتبة التنبيه (م.ث)",
        "active_threshold": "الحد الأدنى للأقمار النشطة",
        "3d_globe": "🌍 الخريطة الكونية ثلاثية الأبعاد",
        "pricing": "💰 خطط الاشتراك التجاري",
        "auto_refresh": "⏱️ تحديث تلقائي",
        "refresh_interval": "الفاصل (ثانية)",
        "start_auto": "▶️ تشغيل",
        "stop_auto": "⏹️ إيقاف",
        "performance_mode": "⚡ وضع الأداء",
        "full_resolution": "دقة كاملة (5000)",
        "high_speed": "سرعة عالية (100)",
        "mobile_mode": "📱 وضع الجوال",
        "export_section": "📊 تصدير التقارير الرسمية",
        "export_csv": "📥 تحميل تقرير CSV",
        "export_txt": "📥 تحميل تقرير نصي رسمي",
        "p1_title": "🚀 الباقة الأساسية",
        "p1_price": "$499",
        "p1_period": "/ شهرياً",
        "p1_desc": ["✨ محاكاة حتى 500 قمر صناعي", "📡 تحديث بيانات Celestrak", "📊 تقارير زمن الانتقال الأساسية", "💬 دعم فني عبر البريد"],
        "p1_btn": "اختر الأساسية",
        "p2_title": "⚡ الباقة المتقدمة (Titan)",
        "p2_price": "$1,499",
        "p2_period": "/ شهرياً",
        "p2_desc": ["🚀 محاكاة كاملة حتى 5,000 قمر", "🌍 الخريطة الكونية ثلاثية الأبعاد", "🌀 حساب تأثير J2 والتفلطح الأرضي", "🧠 تحسين المهام بالذكاء الاصطناعي"],
        "p2_btn": "اختر المتقدمة",
        "p3_title": "🛡️ الباقة السيادية (Enterprise)",
        "p3_price": "مخصص",
        "p3_period": "",
        "p3_desc": ["🔒 خوادم محاكاة سيادية ومخصصة", "🛰️ ربط مباشر مع محطات التحكم الأرضي", "🤝 دعم فني مخصص على مدار 24/7", "🛠️ تعديلات برمجية مخصصة للعميل"],
        "p3_btn": "تواصل معنا"
    },
    "en": {
        "name": "English",
        "dir": "ltr",
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
        "alert_threshold": "Alert Threshold (ms)",
        "active_threshold": "Min Active Satellites",
        "3d_globe": "🌍 3D Constellation Globe",
        "pricing": "💰 Commercial Pricing Plans",
        "auto_refresh": "⏱️ Auto Refresh",
        "refresh_interval": "Interval (sec)",
        "start_auto": "▶️ Start",
        "stop_auto": "⏹️ Stop",
        "performance_mode": "⚡ Performance Mode",
        "full_resolution": "Full Resolution (5000)",
        "high_speed": "High Speed (100)",
        "mobile_mode": "📱 Mobile Mode",
        "export_section": "📊 Official Report Export",
        "export_csv": "📥 Download CSV Report",
        "export_txt": "📥 Download Official Text Report",
        "p1_title": "🚀 Basic Tier",
        "p1_price": "$499",
        "p1_period": "/ month",
        "p1_desc": ["✨ Simulate up to 500 satellites", "📡 Celestrak data integration", "📊 Basic latency reports", "💬 Email technical support"],
        "p1_btn": "Select Basic",
        "p2_title": "⚡ Advanced Tier (Titan)",
        "p2_price": "$1,499",
        "p2_period": "/ month",
        "p2_desc": ["🚀 Full simulation up to 5,000 sats", "🌍 3D Constellation Globe", "🌀 J2 effect & Earth oblateness", "🧠 AI-powered mission optimization"],
        "p2_btn": "Select Advanced",
        "p3_title": "🛡️ Enterprise Sovereign Tier",
        "p3_price": "Custom",
        "p3_period": "",
        "p3_desc": ["🔒 Dedicated sovereign servers", "🛰️ Direct ground station connection", "🤝 24/7 Dedicated technical support", "🛠️ Custom software modifications"],
        "p3_btn": "Contact Us"
    }
}

def t(key: str) -> str:
    lang = st.session_state.get('language', 'ar')
    return LANGUAGES.get(lang, LANGUAGES['ar']).get(key, key)

def get_current_dir() -> str:
    lang = st.session_state.get('language', 'ar')
    return LANGUAGES.get(lang, LANGUAGES['ar']).get('dir', 'rtl')

# ============================================================
# ⚙️ إعداد الواجهة والتصميم المتجاوب مع الاتجاه الديناميكي
# ============================================================
st.set_page_config(page_title="COSMIC-324: 6G Titan X", page_icon="🚀", layout="wide")

current_direction = get_current_dir()
st.markdown(f"""
<style>
    .main, .stApp {{ background-color: #0a0a12; direction: {current_direction}; text-align: {'right' if current_direction == 'rtl' else 'left'}; }}
    .stMetric {{ background: linear-gradient(145deg, #1a1a2e, #0d0d1a); border-radius: 12px; padding: 15px; border: 1px solid rgba(0, 204, 255, 0.15); }}
    h1, h2, h3, h4, h5 {{ color: #00CCFF; font-family: 'Arial Black', sans-serif; }}
    .stButton > button {{ background: linear-gradient(135deg, #00CCFF, #0066AA); color: white; border: none; border-radius: 8px; padding: 0.5rem 1rem; font-weight: bold; width: 100%; }}
    .copyright {{ text-align: center; color: #445566; font-size: 0.8em; padding: 20px 0; border-top: 1px solid #1a1a2e; margin-top: 20px; }}
    .welcome-box {{ background: linear-gradient(135deg, #1a1a2e, #0d0d1a); border-radius: 12px; padding: 20px 25px; border: 1px solid #00CCFF33; margin-bottom: 20px; }}
    .welcome-box h2 {{ color: #00CCFF; margin: 0 0 10px 0; font-size: 1.5em; }}
    .welcome-box p {{ color: #88AACC; margin: 0; font-size: 1em; }}
    
    .pricing-card {{
        background: linear-gradient(145deg, #1a1a2e, #0d0d1a);
        border-radius: 12px;
        padding: 20px;
        border: 1px solid rgba(0, 204, 255, 0.2);
        text-align: center;
        margin-bottom: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }}
    .pricing-card h3 {{ color: #00CCFF; margin-bottom: 10px; font-size: 1.3em; }}
    .pricing-card .price {{ font-size: 1.8em; color: #FFFFFF; font-weight: bold; margin: 15px 0; }}
    .pricing-card ul {{ list-style: none; padding: 0; text-align: {'right' if current_direction == 'rtl' else 'left'}; color: #AABBCC; font-size: 0.9em; margin-bottom: 20px; }}
    .pricing-card ul li {{ margin: 8px 0; border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 5px; }}

    @media (max-width: 768px) {{
        h1 {{ font-size: 2em !important; }}
        .welcome-box {{ padding: 15px; }}
        .stMetric {{ padding: 10px; }}
    }}
</style>
""", unsafe_allow_html=True)

# ============================================================
# 🌐 الشريط الجانبي
# ============================================================
with st.sidebar:
    st.image("https://via.placeholder.com/300x60/0a0a12/00CCFF?text=COSMIC-324", use_column_width=True)
    st.markdown("---")
    
    lang_options = {"ar": "العربية", "en": "English"}
    current_lang = st.session_state.get('language', 'ar')
    selected_lang = st.selectbox("🌐 Language", options=list(lang_options.keys()), format_func=lambda x: lang_options[x],
                               index=list(lang_options.keys()).index(current_lang))
    if selected_lang != current_lang:
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
    st.caption(f"آخر تحديث: {datetime.now().strftime('%H:%M:%S')}")

# ============================================================
# 🎯 المحتوى الرئيسي
# ============================================================
st.markdown(f"<h1 style='text-align: center; text-shadow: 0 0 40px #00CCFF;'>{t('title')}</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #88AACC; font-size: 1.1em;'>{t('subtitle')}</p>", unsafe_allow_html=True)

st.markdown(f"""
<div class='welcome-box'>
    <h2>🌟 {t('welcome')}</h2>
    <p>{t('subtitle')}</p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# 📡 جلب البيانات وتسريع الحسابات باستخدام NumPy (Vectorized)
# ============================================================
@st.cache_data(ttl=600)
def fetch_celestrak_data(group: str = "starlink", max_satellites: int = 5000) -> List[Dict]:
    url = f"https://celestrak.org/NORAD/elements/gp.php?GROUP={group}&FORMAT=json"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        if response.text.startswith('{'):
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
                        for _ in range(4):
                            E = E - (E - e * np.sin(E) - M) / (1 - e * np.cos(E))
                        x_orbit = a * (np.cos(E) - e)
                        y_orbit = a * np.sqrt(1 - e**2) * np.sin(E)
                        z_orbit = 0.0
                        if apply_j2:
                            J2 = 1.08262668e-3
                            p = a * (1 - e**2)
                            n_rad = 2 * math.pi / period
                            raan_dot = -1.5 * J2 * (6378.137 / p) ** 2 * n_rad * np.cos(incl)
                            current_raan = Omega + raan_dot * t
                            current_omega = omega + (-1.5 * J2 * (6378.137 / p) ** 2 * n_rad * np.cos(incl)) * t
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
                    orbit.altitude = a - 6371
                    orbit_map[orbit.name] = orbit
                except:
                    continue
            if orbit_map:
                return orbit_map

    count = min(num_satellites, 5000)
    a_arr = 7000 + np.random.uniform(-500, 500, count)
    e_arr = np.random.uniform(0.01, 0.08, count)
    incl_arr = np.radians(np.random.uniform(30, 70, count))
    omega_arr = np.random.uniform(0, 2*math.pi, count)
    Omega_arr = np.random.uniform(0, 2*math.pi, count)
    M0_arr = np.random.uniform(0, 2*math.pi, count)
    periods = 2 * math.pi * np.sqrt((a_arr ** 3) / 398600.4418)

    for i in range(count):
        a, e, incl, Omega, omega, M0, period = a_arr[i], e_arr[i], incl_arr[i], Omega_arr[i], omega_arr[i], M0_arr[i], periods[i]
        def position_at_time(t: float, a=a, e=e, incl=incl, omega=omega, Omega=Omega, M0=M0, period=period, apply_j2=True):
            if apply_j2:
                J2 = 1.08262668e-3
                p = a * (1 - e**2)
                n_rad = 2 * math.pi / period
                dot = -1.5 * J2 * (6378.137 / p) ** 2 * n_rad * np.cos(incl)
                current_raan = Omega + dot * t
                current_omega = omega + dot * t
            else:
                current_raan = Omega
                current_omega = omega
            M = M0 + 2 * math.pi * t / period
            E = M
            for _ in range(4):
                E = E - (E - e * np.sin(E) - M) / (1 - e * np.cos(E))
            x_orbit = a * (np.cos(E) - e)
            y_orbit = a * np.sqrt(1 - e**2) * np.sin(E)
            x1 = x_orbit * np.cos(current_omega) - y_orbit * np.sin(current_omega)
            y1 = x_orbit * np.sin(current_omega) + y_orbit * np.cos(current_omega)
            y2 = y1 * np.cos(incl)
            z2 = y1 * np.sin(incl)
            x_final = x1 * np.cos(current_raan) - y2 * np.sin(current_raan)
            y_final = x1 * np.sin(current_raan) + y2 * np.cos(current_raan)
            z_final = z2
            return (float(x_final), float(y_final), float(z_final))
        
        orbit = SimpleNamespace()
        orbit.position_at_time = position_at_time
        orbit.name = f"SAT-{i+1}"
        orbit.altitude = float(a - 6371)
        orbit_map[orbit.name] = orbit
        
    return orbit_map

def get_telemetry_data(orbit_map, num_satellites, t_func):
    data = []
    items = list(orbit_map.items())
    if len(items) > num_satellites:
        items = items[:num_satellites]
    for name, orbit in items:
        pos = orbit.position_at_time(0.0, apply_j2=True)
        if pos and len(pos) >= 3:
            x, y, z = pos
            r = math.sqrt(x**2 + y**2 + z**2)
            lat = math.degrees(math.asin(z / r)) if r > 0 else 0
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

with st.spinner('🔄 جاري تحميل المنصة وحساب المسارات مدارياً...'):
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
# 📊 تصدير التقارير الرسمية (New Feature)
# ============================================================
st.markdown("---")
st.subheader(t('export_section'))

col_exp1, col_exp2 = st.columns(2)

with col_exp1:
    csv_data = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label=t('export_csv'),
        data=csv_data,
        file_name=f"cosmic_324_telemetry_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv",
        use_container_width=True
    )

with col_exp2:
    report_content = f"""==================================================
COSMIC-324: 6G Titan X - OFFICIAL TELEMETRY REPORT
==================================================
Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Total Satellites Simulated: {len(df)}
Active Satellites: {active_count}
Calibration Satellites: {calibration_count}
Standby Satellites: {standby_count}
Average Altitude: {df[t('altitude')].mean():.2f} km
--------------------------------------------------
DATA SAMPLE (First 20 Satellites):
--------------------------------------------------
{df.head(20).to_string(index=False)}
==================================================
© 2026 Yousif Zakaria Eissa Arbarb. All Rights Reserved.
"""
    st.download_button(
        label=t('export_txt'),
        data=report_content,
        file_name=f"cosmic_324_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
        mime="text/plain",
        use_container_width=True
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
        height=500 if st.session_state.get('mobile_mode', False) else 600,
        margin=dict(l=0, r=0, t=40, b=0),
        title=dict(text=title, font=dict(size=18, color='#00CCFF'), x=0.5)
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
# 💰 خطط الأسعار والاشتراكات
# ============================================================
st.markdown("---")
st.subheader(t('pricing'))

p1, p2, p3 = st.columns(3)

with p1:
    st.markdown(f"""
    <div class="pricing-card">
        <h3>{t('p1_title')}</h3>
        <div class="price">{t('p1_price')} <span style="font-size: 0.5em; color: #88AACC;">{t('p1_period')}</span></div>
        <ul>
            <li>{t('p1_desc')[0]}</li>
            <li>{t('p1_desc')[1]}</li>
            <li>{t('p1_desc')[2]}</li>
            <li>{t('p1_desc')[3]}</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    if st.button(t('p1_btn'), use_container_width=True, key="btn_p1"):
        st.success("تم اختيار الباقة بنجاح!")

with p2:
    st.markdown(f"""
    <div class="pricing-card" style="border: 2px solid #00CCFF;">
        <h3>{t('p2_title')}</h3>
        <div class="price">{t('p2_price')} <span style="font-size: 0.5em; color: #88AACC;">{t('p2_period')}</span></div>
        <ul>
            <li>{t('p2_desc')[0]}</li>
            <li>{t('p2_desc')[1]}</li>
            <li>{t('p2_desc')[2]}</li>
            <li>{t('p2_desc')[3]}</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    if st.button(t('p2_btn'), use_container_width=True, key="btn_p2"):
        st.success("تم اختيار الباقة بنجاح!")

with p3:
    st.markdown(f"""
    <div class="pricing-card">
        <h3>{t('p3_title')}</h3>
        <div class="price">{t('p3_price')} <span style="font-size: 0.5em; color: #88AACC;">{t('p3_period')}</span></div>
        <ul>
            <li>{t('p3_desc')[0]}</li>
            <li>{t('p3_desc')[1]}</li>
            <li>{t('p3_desc')[2]}</li>
            <li>{t('p3_desc')[3]}</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    if st.button(t('p3_btn'), use_container_width=True, key="btn_p3"):
        st.success("تم استلام الطلب بنجاح!")

# ============================================================
# 📌 حقوق الملكية الفكرية
# ============================================================
st.markdown("---")
st.markdown(f"""
<div class='copyright'>
    <p>🛰️ COSMIC-324: 6G Titan X Orbital Command v6.4</p>
    <p>© 2026 Yousif Zakaria Eissa Arbarb. جميع الحقوق محفوظة.</p>
    <p style='font-size: 0.8em; color: #334455;'>Licensed under AGPL-3.0 & Apache 2.0</p>
</div>
""", unsafe_allow_html=True)
