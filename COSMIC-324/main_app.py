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
import time

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
        "latency_chart": "📈 تطور زمن الانتقال وزمن الإشارة",
        "step": "الخطوة",
        "latency_ms": "زمن الانتقال (م.ث)",
        "last_update": "آخر تحديث",
        "celestrak": "📡 جلب بيانات Celestrak",
        "group": "المجموعة",
        "alert_threshold": "عتبة التنبيه (م.ث)",
        "active_threshold": "الحد الأدنى للأقمار النشطة",
        "3d_globe": "🌍 الخريطة الكونية ثلاثية الأبعاد",
        "pricing": "💰 خطط الاشتراك التجاري",
        "auto_refresh": "⏱️ التحديث التلقائي المداري",
        "refresh_interval": "الفاصل الزمني (ثانية)",
        "start_auto": "▶️ تشغيل التلقائي",
        "stop_auto": "⏹️ إيقاف التلقائي",
        "performance_mode": "⚡ وضع الأداء",
        "full_resolution": "دقة كاملة (5000)",
        "high_speed": "سرعة عالية (100)",
        "mobile_mode": "📱 وضع الجوال",
        "export_section": "📊 تصدير التقارير الرسمية والسيادية",
        "export_csv": "📥 تحميل تقرير القيادة (CSV)",
        "export_txt": "📥 تحميل التقرير الفني الرسمي (TXT)",
        "ground_station": "🛰️ إدارة المحطات الأرضية",
        "gs_select": "اكتب أو اختر الدولة / المحطة السيادية",
        "gs_lat": "خط عرض المحطة",
        "gs_lon": "خط طول المحطة",
        "visible_sats": "الأقمار المرئية في نطاق المحطة"
    },
    "en": {
        "name": "English",
        "dir": "ltr",
        "title": "🚀 COSMIC-324: 6G Titan X Orbital Command",
        "subtitle": "Sovereign Space Simulation Platform",
        "welcome": "🌟 Welcome to COSMIC-324, an integrated space simulation platform.",
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
        "latency_chart": "📈 Signal Latency & Evolution",
        "step": "Step",
        "latency_ms": "Latency (ms)",
        "last_update": "Last Update",
        "celestrak": "📡 Fetch Celestrak Data",
        "group": "Group",
        "alert_threshold": "Alert Threshold (ms)",
        "active_threshold": "Min Active Satellites",
        "3d_globe": "🌍 3D Constellation Globe",
        "pricing": "💰 Commercial Pricing Plans",
        "auto_refresh": "⏱️ Orbital Auto-Refresh",
        "refresh_interval": "Interval (seconds)",
        "start_auto": "▶️ Start Auto",
        "stop_auto": "⏹️ Stop Auto",
        "performance_mode": "⚡ Performance Mode",
        "full_resolution": "Full Resolution (5000)",
        "high_speed": "High Speed (100)",
        "mobile_mode": "📱 Mobile Mode",
        "export_section": "📊 Sovereign & Official Report Export",
        "export_csv": "📥 Download Command Report (CSV)",
        "export_txt": "📥 Download Official Technical Report (TXT)",
        "ground_station": "🛰️ Ground Station Management",
        "gs_select": "Type or Select Sovereign Station / Country",
        "gs_lat": "Station Latitude",
        "gs_lon": "Station Longitude",
        "visible_sats": "Satellites in Line of Sight"
    }
}

def t(key: str) -> str:
    lang = st.session_state.get('language', 'ar')
    return LANGUAGES.get(lang, LANGUAGES['ar']).get(key, key)

def get_current_dir() -> str:
    lang = st.session_state.get('language', 'ar')
    return LANGUAGES.get(lang, LANGUAGES['ar']).get('dir', 'rtl')

# ============================================================
# ⚙️ إعداد الواجهة والتصميم المتجاوب
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
    .pricing-card {{ background: linear-gradient(145deg, #151528, #0a0a12); border: 1px solid #00CCFF55; border-radius: 15px; padding: 20px; text-align: center; }}
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
    if st.button(t('update_btn')):
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
# 📡 جلب البيانات وتسريع الحسابات
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

with st.spinner('🔄 جاري تحميل المنصة والحساب المسارات مدارياً...'):
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
# ⏱️ نظام التحديث التلقائي المداري (Auto-Refresh)
# ============================================================
st.subheader(t('auto_refresh'))
col_ar1, col_ar2, col_ar3 = st.columns(3)
with col_ar1:
    refresh_interval = st.number_input(t('refresh_interval'), min_value=5, max_value=300, value=30)
with col_ar2:
    if 'auto_refresh_active' not in st.session_state:
        st.session_state.auto_refresh_active = False
    if st.button(t('start_auto')):
        st.session_state.auto_refresh_active = True
with col_ar3:
    if st.button(t('stop_auto')):
        st.session_state.auto_refresh_active = False

if st.session_state.auto_refresh_active:
    st.info(f"⚡ التحديث التلقائي قيد التشغيل (يتم التحديث كل {refresh_interval} ثانية)...")
    time.sleep(refresh_interval)
    st.rerun()

st.markdown("---")

# ============================================================
# 🛰️ إدارة المحطات الأرضية ودعم البحث الحر المباشر
# ============================================================
st.subheader(t('ground_station'))

predefined_stations = {
    "الكاميرون (Cameroon)": {"lat": 3.8480, "lon": 11.5021},
    "السودان (Sudan)": {"lat": 15.5007, "lon": 32.5599},
    "الدانمارك (Denmark)": {"lat": 55.6761, "lon": 12.5683},
    "مسقط، سلطنة عمان (Muscat)": {"lat": 23.5880, "lon": 58.3829},
    "لواندا، أنغولا (Luanda, Angola)": {"lat": -8.8390, "lon": 13.2894},
    "اليابان - طوكيو (Japan)": {"lat": 35.6762, "lon": 139.6503},
    "الهند - نيودلهي (India)": {"lat": 28.6139, "lon": 77.2090},
    "الولايات المتحدة - واشنطن (USA)": {"lat": 38.9072, "lon": -77.0369},
    "المملكة المتحدة - لندن (UK)": {"lat": 51.5074, "lon": -0.1278},
    "ألمانيا - برلين (Germany)": {"lat": 52.5200, "lon": 13.4050}
}

gs_input_name = st.selectbox(t('gs_select'), options=list(predefined_stations.keys()))

# ربط الإحداثيات تلقائياً ودون أي خطأ بناءً على الاختيار الفعلي
gs_lat = predefined_stations[gs_input_name]["lat"]
gs_lon = predefined_stations[gs_input_name]["lon"]
gs_choice = gs_input_name

def calculate_visible_satellites(df, g_lat, g_lon):
    visible = []
    for _, row in df.iterrows():
        s_lat = row[t('latitude')]
        s_lon = row[t('longitude')]
        dist = math.sqrt((s_lat - g_lat)**2 + (s_lon - g_lon)**2)
        if dist <= 45.0:
            visible.append(row)
    return pd.DataFrame(visible)

df_visible = calculate_visible_satellites(df, gs_lat, gs_lon)
st.metric(t('visible_sats'), len(df_visible))

if not df_visible.empty:
    st.dataframe(df_visible, use_container_width=True, height=200)
else:
    st.warning("لا توجد أقمار صناعية حالياً ضمن نطاق الرؤية المباشرة لهذه المحطة.")

# ============================================================
# 📈 الرسم البياني الزمني (Latency Chart)
# ============================================================
st.markdown("---")
st.subheader(t('latency_chart'))

chart_steps = list(range(1, 21))
simulated_latency = [round(random.uniform(8.5, 35.2), 2) for _ in chart_steps]
df_latency = pd.DataFrame({
    t('step'): chart_steps,
    t('latency_ms'): simulated_latency
})

fig_lat = px.line(
    df_latency, x=t('step'), y=t('latency_ms'),
    markers=True,
    line_shape='spline',
    color_discrete_sequence=['#00CCFF']
)
fig_lat.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color='white'),
    xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)'),
    yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)'),
    margin=dict(l=20, r=20, t=20, b=20),
    height=300
)
st.plotly_chart(fig_lat, use_container_width=True)

# ============================================================
# 🌍 الخريطة 3D (مصححة جذرياً لتدوير الكاميرا وإسقاط النجمة معاً)
# ============================================================
def render_cosmic_globe(df, gs_lat, gs_lon, station_name, title="🌍 3D Constellation Globe"):
    fig = go.Figure()
    
    # تصحيح تدوير الخريطة وإجبار الكاميرا والمنظور على التمركز فوراً فوق إحداثيات الدولة المختارة
    fig.update_layout(
        geo=dict(
            projection_type='orthographic',
            projection=dict(
                rotation=dict(lat=gs_lat, lon=gs_lon)
            ),
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
    
    # رسومات الأقمار الصناعية
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
                }).tolist()
            ),
            text=df[t('satellite')].tolist(),
            textposition='top center',
            textfont=dict(size=9, color='white'),
            hoverinfo='text'
        ))
    
    # النجمة الحمراء للمحطة الأرضية مرتبطة تماماً بإحداثيات الدولة المختارة (`gs_lon` و `gs_lat`)
    short_station_label = f"🛰️ {station_name.split('(')[0].strip()}"
    fig.add_trace(go.Scattergeo(
        lon=[gs_lon], 
        lat=[gs_lat],
        mode='markers+text',
        marker=dict(size=16, color='#FF3366', symbol='star'),
        text=[short_station_label],
        textposition='bottom center',
        textfont=dict(size=12, color='#FF6699', family='Arial Black'),
        name='Ground Station'
    ))
    return fig

st.markdown("---")
st.subheader(t('3d_globe'))
st.plotly_chart(render_cosmic_globe(df, gs_lat, gs_lon, gs_choice, t('3d_globe')), use_container_width=True)

# ============================================================
# 💰 خطط الاشتراك التجاري
# ============================================================
st.markdown("---")
st.subheader(t('pricing'))
p1, p2, p3 = st.columns(3)

with p1:
    st.markdown("""
    <div class='pricing-card'>
        <h3>🌱 الباقة الأساسية</h3>
        <p style='color:#00CCFF; font-size:1.5em; font-weight:bold;'>$49 / شهرياً</p>
        <p>مراقبة حتى 500 قمر صناعي</p>
        <p>تحديث مباشر كل دقيقة</p>
    </div>
    """, unsafe_allow_html=True)

with p2:
    st.markdown("""
    <div class='pricing-card' style='border: 2px solid #00CCFF;'>
        <h3>🚀 الباقة السيادية (Titan X)</h3>
        <p style='color:#00CCFF; font-size:1.5em; font-weight:bold;'>$199 / شهرياً</p>
        <p>مراقبة كاملة (5000 قمر صناعي)</p>
        <p>محطات أرضية متعددة ودعم 6G</p>
    </div>
    """, unsafe_allow_html=True)

with p3:
    st.markdown("""
    <div class='pricing-card'>
        <h3>🌌 باقة الوكالات الفضائية</h3>
        <p style='color:#00CCFF; font-size:1.5em; font-weight:bold;'>مخصص</p>
        <p>ربط مباشر مع منصات Celestrak</p>
        <p>دعم فني هندسي مخصص على مدار الساعة</p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# 📊 تصدير التقارير الرسمية والسيادية
# ============================================================
st.markdown("---")
st.subheader(t('export_section'))

col_ex1, col_ex2 = st.columns(2)

with col_ex1:
    csv_data = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label=t('export_csv'),
        data=csv_data,
        file_name='cosmic_324_telemetry_report.csv',
        mime='text/csv'
    )

with col_ex2:
    report_text = f"""==================================================
COSMIC-324: 6G Titan X - OFFICIAL SOVEREIGN REPORT
==================================================
Timestamp: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC
Total Satellites Monitored: {len(df)}
Active Satellites: {active_count}
Calibration Satellites: {calibration_count}
Standby Satellites: {standby_count}
Selected Ground Station: {gs_choice} (Lat: {gs_lat}, Lon: {gs_lon})
Visible Satellites Count: {len(df_visible)}
--------------------------------------------------
System Status: STABLE & OPERATIONAL
Authorized by: Yousif Zakaria Eissa Arbarb © 2026
==================================================
"""
    st.download_button(
        label=t('export_txt'),
        data=report_text,
        file_name='cosmic_324_official_report.txt',
        mime='text/plain'
    )

# ============================================================
# 📌 حقوق الملكية
# ============================================================
st.markdown("---")
st.markdown("""
<div class='copyright'>
    <p>🛰️ COSMIC-324: 6G Titan X Orbital Command v6.9</p>
    <p>© 2026 Yousif Zakaria Eissa Arbarb. جميع الحقوق محفوظة.</p>
</div>
""", unsafe_allow_html=True)
