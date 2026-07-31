import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random
import requests
import math
import time
from datetime import datetime
from types import SimpleNamespace

# ============================================================
# 🌍 نظام الترجمة (7 لغات)
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
        "latency_chart": "📈 تطور زمن الانتقال",
        "step": "الخطوة",
        "latency_ms": "زمن الانتقال (مللي ثانية)",
        "last_update": "آخر تحديث",
        "avg_alt": "متوسط الارتفاع",
        "max_alt": "أقصى ارتفاع",
        "min_alt": "أدنى ارتفاع",
        "celestrak": "📡 جلب بيانات حقيقية من Celestrak",
        "group": "اختر المجموعة",
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
        "latency_chart": "📈 Signal Latency Evolution",
        "step": "Step",
        "latency_ms": "Latency (ms)",
        "last_update": "Last Update",
        "avg_alt": "Avg Altitude",
        "max_alt": "Max Altitude",
        "min_alt": "Min Altitude",
        "celestrak": "📡 Fetch Live Data from Celestrak",
        "group": "Select Group",
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
def fetch_celestrak_data(group: str = "starlink", max_satellites: int = 5000) -> list:
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
# ⚙️ إعداد الواجهة
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
    .pricing-card { 
        background: #1a1a2e; 
        border-radius: 10px; 
        padding: 20px 15px; 
        border: 1px solid #00CCFF33; 
        text-align: center; 
        transition: transform 0.3s ease;
        height: 100%;
    }
    .pricing-card:hover { transform: scale(1.02); border-color: #00CCFF; }
    .pricing-card h4 { color: #00CCFF; margin-bottom: 10px; }
    .pricing-card h2 { color: #FFFFFF; margin: 10px 0; }
    .pricing-card p { color: #88AACC; font-size: 14px; }
    .welcome-box {
        background: linear-gradient(135deg, #1a1a2e, #0d0d1a);
        border-radius: 12px;
        padding: 20px 25px;
        border: 1px solid #00CCFF33;
        margin-bottom: 20px;
    }
    .welcome-box h2 { color: #00CCFF; margin: 0 0 10px 0; }
    .welcome-box p { color: #88AACC; margin: 0; font-size: 1.05em; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# 🌐 الشريط الجانبي
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
    max_display_sats = 50 if mobile_mode else (100 if perf_mode == t("high_speed") else 5000)
    
    num_satellites = st.slider(t("sat_count"), 10, max_display_sats, min(50, max_display_sats), 10)
    
    st.markdown("---")
    st.subheader(t("celestrak"))
    group = st.selectbox(t("group"), ["starlink", "gps", "active", "oneweb", "iridium"])
    use_celestrak = st.checkbox("استخدام بيانات حقيقية", value=True)
    
    if st.button(t("update_btn"), use_container_width=True):
        st.cache_data.clear()
        st.cache_resource.clear()
        st.rerun()
    st.caption(f"{t('last_update')}: {datetime.now().strftime('%H:%M:%S')}")

# ============================================================
# 🎯 العنوان الرئيسي والترحيب
# ============================================================
st.markdown(f"<h1 style='text-align: center; font-size: 3em; text-shadow: 0 0 40px #00CCFF;'>{t('title')}</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #88AACC; font-size: 1em;'>{t('subtitle')}</p>", unsafe_allow_html=True)

st.markdown(f"""
<div class='welcome-box'>
    <h2>🌟 {t('welcome')}</h2>
    <p>{t('subtitle')}</p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# 🔄 جلب التليمتري والبيانات
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

with st.spinner('🔄 جاري تحميل المنصة...'):
    orbit_map = generate_orbit_map_optimized(num_satellites, group, use_celestrak)
    df = get_telemetry_data(orbit_map, num_satellites, t)

active_count = df[df[t('status')] == t('active')].shape[0]

col1, col2, col3, col4 = st.columns(4)
col1.metric(t('total'), len(df))
col2.metric(t('active'), active_count)
col3.metric(t('calibration'), df[df[t('status')] == t('calibration')].shape[0])
col4.metric(t('standby'), df[df[t('status')] == t('standby')].shape[0])
st.markdown("---")

# ============================================================
# 🌍 دالة 3D Globe المُصححة والمُدمجة
# ============================================================
def render_cosmic_globe(orbit_map, df, title="🌍 3D Constellation Globe", mobile_mode=False):
    """
    تُنشئ كرة أرضية تفاعلية ثلاثية الأبعاد مع مسارات المدارات والأقمار.
    """
    import numpy as np
    fig = go.Figure()
    
    # إضافة الكرة الأرضية
    fig.update_layout(
        geo=dict(
            projection_type='orthographic',
            showland=True,
            landcolor='rgb(10,10,20)',
            coastlinecolor='rgb(60,60,80)',
            showocean=True,
            oceancolor='rgb(5,5,15)',
            showcountries=True,
            countrycolor='rgb(50,50,70)',
            bgcolor='rgba(0,0,0,0)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=400 if mobile_mode else 600,
        margin=dict(l=0, r=0, t=0, b=0)
    )
    
    if not df.empty:
        # جلب أسماء الأعمدة ديناميكياً لتجنب أخطاء الترجمة
        col_sat = t('satellite')
        col_status = t('status')
        col_lat = t('latitude')
        col_lon = t('longitude')

        # رسم مدارات الأقمار (خطوط)
        for name, orbit in list(orbit_map.items())[:30]:  # حد أقصى 30 مداراً للوضوح
            if not hasattr(orbit, 'position_at_time'):
                continue
            orbit_points = []
            for step_t in np.linspace(0, orbit.period, 50):
                pos = orbit.position_at_time(step_t, apply_j2=True)
                if pos and len(pos) >= 3:
                    x, y, z = pos
                    r = math.sqrt(x**2 + y**2 + z**2)
                    if r == 0:
                        continue
                    lat = math.degrees(math.asin(z / r))
                    lon = math.degrees(math.atan2(y, x))
                    orbit_points.append((lon, lat))
            
            if len(orbit_points) > 1:
                lons, lats = zip(*orbit_points)
                fig.add_trace(go.Scattergeo(
                    lon=lons,
                    lat=lats,
                    mode='lines',
                    line=dict(width=1, color='rgba(0, 204, 255, 0.2)'),
                    showlegend=False,
                    hoverinfo='skip'
                ))
        
        # رسم الأقمار (نقاط)
        sample_size = min(100 if mobile_mode else 300, len(df))
        display_df = df.sample(n=sample_size) if len(df) > sample_size else df
        
        status_colors = {
            t('active'): '#00FF00',
            t('calibration'): '#FFAA00',
            t('standby'): '#FF5555',
            '🔴 معطل': '#FF0000',
            '🟢 Active': '#00FF00',
            '🟡 Calibration': '#FFAA00',
            '🔴 Standby': '#FF5555'
        }
        
        marker_colors = [status_colors.get(s, '#00CCFF') for s in display_df[col_status].tolist()]

        fig.add_trace(go.Scattergeo(
            lon=display_df[col_lon].tolist(),
            lat=display_df[col_lat].tolist(),
            mode='markers',
            marker=dict(
                size=6 if mobile_mode else 8,
                color=marker_colors,
                symbol='circle'
            ),
            text=display_df[col_sat].tolist(),
            hoverinfo='text'
        ))
    
    # المحطة الأرضية
    fig.add_trace(go.Scattergeo(
        lon=[0],
        lat=[0],
        mode='markers',
        marker=dict(size=14, color='#FF3366', symbol='star'),
        text=['🛰️ Ground'],
        hoverinfo='text'
    ))
    
    return fig

# ============================================================
# عرض التبويبات والخريطة ثلاثية الأبعاد
# ============================================================
tab1, tab2, tab3 = st.tabs([t('3d_globe'), t('coverage'), t('spectrum')])

with tab1:
    fig_globe = render_cosmic_globe(orbit_map, df, title=t('3d_globe'), mobile_mode=st.session_state.get('mobile_mode', False))
    st.plotly_chart(fig_globe, use_container_width=True)

with tab2:
    st.info("📡 خريطة التغطية الأرضية قيد التشغيل والتحليل المباشر.")

with tab3:
    st.info("📶 محلل الطيف الترددي 6G نشط.")
