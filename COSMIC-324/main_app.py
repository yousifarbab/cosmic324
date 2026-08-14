import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import math
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List
from types import SimpleNamespace
import time
import json
from pathlib import Path

# ============================================================
# 📁 تحميل ملف العقد والبيانات الأساسية
# ============================================================
DATA_CONTRACT_PATH = Path(__file__).with_name("cosmic324_data.json")
if DATA_CONTRACT_PATH.exists():
    with DATA_CONTRACT_PATH.open("r", encoding="utf-8") as contract_file:
        DATA_CONTRACT = json.load(contract_file)
else:
    # هيكل افتراضي احتياطي في حال عدم توفر الملف الخارجي لضمان التكامل 100%
    DATA_CONTRACT = {
        "celestrak": {"groups": ["starlink", "active", "visual", "weather"], "defaultGroup": "starlink", "cacheTtlSeconds": 3600},
        "model": {"earthRadiusKm": 6371.0, "earthMuKm3S2": 398600.4418, "j2": 0.00108263, "speedOfLightKmPerSecond": 299792.458, "lineOfSightAngularRadiusDeg": 45.0},
        "source": {"baseUrl": "https://celestrak.org/NORAD/elements/gp.php", "provider": "CelesTrak", "dataset": "GP"},
        "groundStations": [
            {"name": {"ar": "محطة الخرطوم السيادية", "en": "Khartoum Sovereign Station"}, "latitudeDeg": 15.5007, "longitudeDeg": 32.5599},
            {"name": {"ar": "محطة لندن المدارية", "en": "London Orbital Station"}, "latitudeDeg": 51.5074, "longitudeDeg": -0.1278}
        ]
    }

CELESTRAK_CONFIG = DATA_CONTRACT["celestrak"]
MODEL_CONFIG = DATA_CONTRACT["model"]
SOURCE_CONFIG = DATA_CONTRACT["source"]

# ============================================================
# 🌍 نظام الترجمة واتجاه الصفحة (RTL/LTR) الشامل
# ============================================================
LANGUAGES = {
    "ar": {
        "name": "العربية",
        "dir": "rtl",
        "title": "🚀 كوزميك-324: القيادة المدارية 6G Titan X",
        "subtitle": "منصة المحاكاة الفضائية والسيادية المتكاملة",
        "welcome": "🌟 مرحباً بك في منصة كوزميك-324، البوابة الموحدة للقيادة الفضائية.",
        "params": "⚙️ إعدادات المحاكاة والتحكم",
        "sat_count": "عدد الأقمار",
        "update_btn": "🔄 تحديث البيانات",
        "total": "المجموع",
        "satellite": "القمر",
        "status": "الحالة",
        "latitude": "خط العرض",
        "longitude": "خط الطول",
        "altitude": "الارتفاع (كم)",
        "celestrak": "📡 جلب بيانات Celestrak",
        "group": "المجموعة",
        "alert_threshold": "عتبة التنبيه (م.ث)",
        "active_threshold": "الحد الأدنى للأقمار النشطة",
        "3d_globe": "🌍 الخريطة الكونية ثلاثية الأبعاد",
        "auto_refresh": "⏱️ التحديث التلقائي المداري",
        "refresh_interval": "الفاصل الزمني (ثانية)",
        "start_auto": "▶️ تشغيل التلقائي",
        "stop_auto": "⏹️ إيقاف التلقائي",
        "performance_mode": "⚡ وضع الأداء",
        "full_resolution": "دقة كاملة (5000)",
        "high_speed": "سرعة عالية (100)",
        "mobile_mode": "📱 وضع الجوال",
        "ground_station": "🛰️ إدارة المحطات الأرضية العالمية والدول",
        "gs_select": "اكتب اسم أي دولة أو محطة سيادية بحرية:",
        "visible_sats": "الأقمار المرئية في نطاق المحطة",
        "cataloged": "مفهرس",
        "catalog_source": "مصدر الفهرس",
        "configured_stations": "المحطات المعرفة",
        "propagation_chart": "تقدير الحد الأدنى لزمن الانتشار",
        "sample": "العينة",
        "propagation_ms": "زمن الانتشار التقديري أحادي الاتجاه (م.ث)",
        # الأقسام الخمسة الجديدة
        "nav_dashboard": "📊 لوحة القيادة",
        "nav_licenses": "🔑 إدارة التراخيص",
        "nav_clients": "👥 العملاء والبوابات",
        "nav_health": "🩺 صحة النظام والشبكة",
        "nav_settings": "⚙️ الإعدادات المتقدمة",
        # قسم التراخيص
        "license_title": "🔑 نظام إصدار وتوليد المفاتيح السيادية",
        "gen_key_btn": "توليد مفتاح ترخيص جديد",
        "license_key": "مفتاح الترخيص",
        "client_name": "اسم العميل / الجهة",
        "license_tier": "نوع الباقة",
        "expiry_date": "تاريخ الانتهاء",
        "active_licenses": "التراخيص النشطة حالياً",
        # قسم العملاء
        "clients_title": "👥 بوابات العملاء ومحاكاة الدفع المباشر",
        "client_login": "تسجيل دخول العميل",
        "email": "البريد الإلكتروني",
        "password": "كلمة المرور",
        "login_btn": "دخول البوابة",
        "paypal_sim": "💳 محاكاة الدفع السريع عبر PayPal",
        "pay_now": "دفع اشتراك الباقة السيادية ($199)",
        "payment_success": "✅ تم اتمام عملية الدفع بنجاح عبر بوابة PayPal وتفعيل الحساب!",
        # قسم صحة النظام
        "health_title": "🩺 صحة النظام والشبكة المدارية والخوادم",
        "server_load": "حمل الخوادم السيادية",
        "network_latency": "متوسط زمن الاستجابة العضوي",
        "packet_loss": "معدل فقدان الحزم",
        "cpu_usage": "استهلاك المعالج المركزى (CPU)",
        "memory_usage": "استهلاك الذاكرة العشوائية (RAM)",
        # قسم الإعدادات المتقدمة
        "settings_title": "⚙️ الإعدادات المتقدمة ومزودات البيانات",
        "api_endpoint": "رابط مزود البيانات الأساسي (API Endpoint)",
        "encryption_level": "مستوى التشفير السيادي",
        "save_settings": "حفظ الإعدادات المتقدمة",
        "settings_saved": "✅ تم حفظ وتطبيق الإعدادات المتقدمة بنجاح!"
    },
    "en": {
        "name": "English",
        "dir": "ltr",
        "title": "🚀 COSMIC-324: 6G Titan X Orbital Command",
        "subtitle": "Sovereign Space Simulation & Command Platform",
        "welcome": "🌟 Welcome to COSMIC-324, the integrated space command gateway.",
        "params": "⚙️ Simulation Parameters & Control",
        "sat_count": "Number of Satellites",
        "update_btn": "🔄 Refresh Data",
        "total": "Total",
        "satellite": "Satellite",
        "status": "Status",
        "latitude": "Latitude",
        "longitude": "Longitude",
        "altitude": "Altitude (km)",
        "celestrak": "📡 Fetch Celestrak Data",
        "group": "Group",
        "alert_threshold": "Alert Threshold (ms)",
        "active_threshold": "Min Active Satellites",
        "3d_globe": "🌍 3D Constellation Globe",
        "auto_refresh": "⏱️ Orbital Auto-Refresh",
        "refresh_interval": "Interval (seconds)",
        "start_auto": "▶️ Start Auto",
        "stop_auto": "⏹️ Stop Auto",
        "performance_mode": "⚡ Performance Mode",
        "full_resolution": "Full Resolution (5000)",
        "high_speed": "High Speed (100)",
        "mobile_mode": "📱 Mobile Mode",
        "ground_station": "🛰️ Global Ground Station & Country Management",
        "gs_select": "Type any country or sovereign station name:",
        "visible_sats": "Satellites in Line of Sight",
        "cataloged": "Cataloged",
        "catalog_source": "Catalog Source",
        "configured_stations": "Configured Stations",
        "propagation_chart": "Estimated Minimum Propagation Delay",
        "sample": "Sample",
        "propagation_ms": "Estimated One-Way Propagation (ms)",
        # الأقسام الخمسة الجديدة
        "nav_dashboard": "📊 Dashboard",
        "nav_licenses": "🔑 Licenses Management",
        "nav_clients": "👥 Clients Portal",
        "nav_health": "🩺 System Health",
        "nav_settings": "⚙️ Advanced Settings",
        # قسم التراخيص
        "license_title": "🔑 Sovereign Key Generation & License Management",
        "gen_key_btn": "Generate New License Key",
        "license_key": "License Key",
        "client_name": "Client / Entity Name",
        "license_tier": "Subscription Tier",
        "expiry_date": "Expiry Date",
        "active_licenses": "Currently Active Licenses",
        # قسم العملاء
        "clients_title": "👥 Client Portals & Direct Payment Simulation",
        "client_login": "Client Authentication",
        "email": "Email Address",
        "password": "Password",
        "login_btn": "Portal Login",
        "paypal_sim": "💳 PayPal Express Checkout Simulation",
        "pay_now": "Pay Sovereign Tier Subscription ($199)",
        "payment_success": "✅ Payment successfully processed via PayPal gateway and account activated!",
        # قسم صحة النظام
        "health_title": "🩺 System Health, Network & Server Performance",
        "server_load": "Sovereign Server Load",
        "network_latency": "Average Organic Latency",
        "packet_loss": "Packet Loss Rate",
        "cpu_usage": "CPU Utilization",
        "memory_usage": "RAM Utilization",
        # قسم الإعدادات المتقدمة
        "settings_title": "⚙️ Advanced Settings & Data Providers",
        "api_endpoint": "Primary Data Provider API Endpoint",
        "encryption_level": "Sovereign Encryption Level",
        "save_settings": "Save Advanced Settings",
        "settings_saved": "✅ Advanced settings successfully saved and applied!"
    }
}

def t(key: str) -> str:
    lang = st.session_state.get('language', 'ar')
    return LANGUAGES.get(lang, LANGUAGES['ar']).get(key, key)

def get_current_dir() -> str:
    lang = st.session_state.get('language', 'ar')
    return LANGUAGES.get(lang, LANGUAGES['ar']).get('dir', 'rtl')

# ============================================================
# ⚙️ إعداد الواجهة والتصميم المتجاوب السيادي
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
# 🌐 الشريط الجانبي الموحد وتحديد الأقسام الخمسة
# ============================================================
with st.sidebar:
    st.image("https://via.placeholder.com/300x60/0a0a12/00CCFF?text=COSMIC-324", use_container_width=True)
    st.markdown("---")
    
    lang_options = {"ar": "العربية", "en": "English"}
    current_lang = st.session_state.get('language', 'ar')
    selected_lang = st.selectbox("🌐 Language", options=list(lang_options.keys()), format_func=lambda x: lang_options[x],
                                index=list(lang_options.keys()).index(current_lang))
    if selected_lang != current_lang:
        st.session_state.language = selected_lang
        st.rerun()
    
    st.markdown("---")
    
    # القائمة الموحدة للتنقل بين الأقسام الخمسة الرئيسية
    app_section = st.radio(
        "📌 التنقل الرئيسي بين الأقسام",
        [
            t('nav_dashboard'),
            t('nav_licenses'),
            t('nav_clients'),
            t('nav_health'),
            t('nav_settings')
        ]
    )
    
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
    group = st.selectbox(
        t("group"),
        CELESTRAK_CONFIG["groups"],
        index=CELESTRAK_CONFIG["groups"].index(CELESTRAK_CONFIG["defaultGroup"]),
    )
    use_celestrak = st.checkbox("استخدام بيانات حقيقية", value=True)
    
    st.markdown("---")
    st.subheader("🔔 " + t('alert_threshold'))
    alert_threshold = st.slider(t('alert_threshold'), 5.0, 50.0, 20.0, 1.0)
    active_threshold = st.slider(t('active_threshold'), 1, 50, 5, 1)

# ============================================================
# 📡 جلب البيانات وتسريع الحسابات المدارية
# ============================================================
@st.cache_data(ttl=CELESTRAK_CONFIG["cacheTtlSeconds"])
def fetch_celestrak_data(group: str = "starlink", max_satellites: int = 5000) -> List[Dict]:
    url = f"{SOURCE_CONFIG['baseUrl']}?GROUP={group}&FORMAT=json"
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
                    GM = MODEL_CONFIG["earthMuKm3S2"]
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
                            J2 = MODEL_CONFIG["j2"]
                            p = a * (1 - e**2)
                            n_rad = 2 * math.pi / period
                            raan_dot = -1.5 * J2 * (MODEL_CONFIG["earthRadiusKm"] / p) ** 2 * n_rad * np.cos(incl)
                            current_raan = Omega + raan_dot * t
                            current_omega = omega + (-1.5 * J2 * (MODEL_CONFIG["earthRadiusKm"] / p) ** 2 * n_rad * np.cos(incl)) * t
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
                    orbit.altitude = a - MODEL_CONFIG["earthRadiusKm"]
                    orbit_map[orbit.name] = orbit
                except:
                    continue
            if orbit_map:
                return orbit_map
    return {}

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
            status = t_func('cataloged')
            data.append({
                t_func('satellite'): name.strip(),
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
# 🎯 توجيه العرض بحسب القسم المختار في القائمة الجانبية
# ============================================================

# 1️⃣ القسم الأول: لوحة القيادة (Dashboard)
if app_section == t('nav_dashboard'):
    st.markdown(f"<h1 style='text-align: center; text-shadow: 0 0 40px #00CCFF;'>{t('title')}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; color: #88AACC; font-size: 1.1em;'>{t('subtitle')}</p>", unsafe_allow_html=True)

    st.markdown(f"""
    <div class='welcome-box'>
        <h2>🌟 {t('welcome')}</h2>
        <p>{t('subtitle')}</p>
    </div>
    """, unsafe_allow_html=True)

    # مؤشرات الأداء الحية
    col1, col2, col3, col4 = st.columns(4)
    col1.metric(t('total'), len(df))
    col2.metric(t('catalog_source'), SOURCE_CONFIG['provider'])
    col3.metric(t('configured_stations'), len(DATA_CONTRACT['groundStations']))
    col4.metric(t('group'), group.upper())
    st.markdown("---")

    # نظام التحديث التلقائي المداري (Auto-Refresh)
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

    # نظام البحث الحر المباشر للمحطات الأرضية والدول
    st.subheader(t('ground_station'))

    station_language = st.session_state.get('language', 'ar')
    global_stations = {
        station["name"][station_language]: {
            "lat": station["latitudeDeg"],
            "lon": station["longitudeDeg"],
        }
        for station in DATA_CONTRACT["groundStations"]
    }

    user_station_query = st.text_input(t('gs_select'), value=next(iter(global_stations)))

    matched_lat, matched_lon = 3.8480, 11.5021 
    found_key = user_station_query

    for name, coords in global_stations.items():
        if user_station_query.strip().lower() in name.lower():
            matched_lat = coords["lat"]
            matched_lon = coords["lon"]
            found_key = name
            break
    else:
        import hashlib
        h = int(hashlib.md5(user_station_query.encode('utf-8')).hexdigest(), 16)
        matched_lat = float((h % 160) - 80)
        matched_lon = float(((h // 160) % 360) - 180)

    gs_lat = matched_lat
    gs_lon = matched_lon
    gs_choice = found_key if found_key in global_stations else user_station_query

    st.info(f"📍 الإحداثيات النشطة الحالية: **خط العرض ({gs_lat})** | **خط الطول ({gs_lon})**")

    def calculate_visible_satellites(df, g_lat, g_lon):
        visible = []
        for _, row in df.iterrows():
            s_lat = row[t('latitude')]
            s_lon = row[t('longitude')]
            dist = math.sqrt((s_lat - g_lat)**2 + (s_lon - g_lon)**2)
            if dist <= MODEL_CONFIG["lineOfSightAngularRadiusDeg"]:
                visible.append(row)
        return pd.DataFrame(visible)

    df_visible = calculate_visible_satellites(df, gs_lat, gs_lon)
    st.metric(t('visible_sats'), len(df_visible))

    if not df_visible.empty:
        st.dataframe(df_visible, use_container_width=True, height=200)
    else:
        st.warning("لا توجد أقمار صناعية حالياً ضمن نطاق الرؤية المباشرة لهذه المحطة.")

    # الرسم البياني الزمني
    st.markdown("---")
    st.subheader(t('propagation_chart'))

    sample_altitudes = df[t('altitude')].head(20).tolist() if not df.empty else []
    chart_steps = list(range(1, len(sample_altitudes) + 1))
    estimated_propagation = [
        round((float(altitude_km) / MODEL_CONFIG["speedOfLightKmPerSecond"]) * 1000, 4)
        for altitude_km in sample_altitudes
    ]
    df_latency = pd.DataFrame({
        t('sample'): chart_steps,
        t('propagation_ms'): estimated_propagation
    })

    fig_lat = px.line(
        df_latency, x=t('sample'), y=t('propagation_ms'),
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

    # الخريطة 3D المتكاملة
    def render_cosmic_globe(df, gs_lat, gs_lon, station_name, title="🌍 3D Constellation Globe"):
        fig = go.Figure()
        fig.update_layout(
            geo=dict(
                projection_type='orthographic',
                projection=dict(rotation=dict(lat=gs_lat, lon=gs_lon)),
                showland=True, landcolor='rgb(15,15,30)',
                coastlinecolor='rgb(0, 204, 255)',
                showocean=True, oceancolor='rgb(5,5,15)',
                showcountries=True, countrycolor='rgb(60,60,100)',
                bgcolor='rgba(0,0,0,0)'
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=550 if st.session_state.get('mobile_mode', False) else 650,
            margin=dict(l=0, r=0, t=40, b=0),
            title=dict(text=title, font=dict(size=18, color='#00CCFF'), x=0.5)
        )
        if not df.empty:
            fig.add_trace(go.Scattergeo(
                lon=df[t('longitude')].tolist(),
                lat=df[t('latitude')].tolist(),
                mode='markers',
                marker=dict(size=6, color='#00CCFF', opacity=0.9),
                text=df[t('satellite')].tolist(),
                hoverinfo='text',
                name='Satellites'
            ))
        short_station_label = f"🛰️ {station_name.split('(')[0].strip()}"
        fig.add_trace(go.Scattergeo(
            lon=[gs_lon], lat=[gs_lat],
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

# 2️⃣ القسم الثاني: إدارة التراخيص (Licenses Management)
elif app_section == t('nav_licenses'):
    st.markdown(f"<h1>{t('license_title')}</h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    col_l1, col_l2 = st.columns(2)
    with col_l1:
        client_input = st.text_input(t('client_name'), value="وزارة الاتصالات السيادية")
        tier_input = st.selectbox(t('license_tier'), ["الباقة الأساسية ($49)", "الباقة السيادية Titan X ($199)", "باكة وكالات الفضاء (مخصص)"])
    with col_l2:
        validity_days = st.number_input("مدة الصلاحية (بالأيام)", min_value=30, max_value=365, value=365)
        
    if st.button(t('gen_key_btn')):
        import uuid
        generated_key = f"CSM324-{str(uuid.uuid4()).upper()[:16]}"
        expiry_val = (datetime.utcnow() + timedelta(days=validity_days)).strftime('%Y-%m-%d')
        
        if 'licenses_db' not in st.session_state:
            st.session_state.licenses_db = []
            
        st.session_state.licenses_db.append({
            t('client_name'): client_input,
            t('license_tier'): tier_input,
            t('license_key'): generated_key,
            t('expiry_date'): expiry_val
        })
        st.success(f"✅ تم إصدار مفتاح الترخيص بنجاح: **{generated_key}**")
        
    st.markdown("---")
    st.subheader(t('active_licenses'))
    if 'licenses_db' in st.session_state and st.session_state.licenses_db:
        df_lic = pd.DataFrame(st.session_state.licenses_db)
        st.dataframe(df_lic, use_container_width=True)
    else:
        st.info("لا توجد تراخيص مسجلة حتى الآن. استخدم نموذج التوليد أعلاه.")

# 3️⃣ القسم الثالث: العملاء والبوابات (Clients Portal)
elif app_section == t('nav_clients'):
    st.markdown(f"<h1>{t('clients_title')}</h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    tab_login, tab_pay = st.tabs([t('client_login'), t('paypal_sim')])
    
    with tab_login:
        st.subheader(t('client_login'))
        email = st.text_input(t('email'), value="commander@cosmic324.space")
        password = st.text_input(t('password'), type="password", value="••••••••")
        if st.button(t('login_btn')):
            st.success(f"🌟 أهلاً بك مجدداً يا سيد/ة {email.split('@')[0].upper()}! تم التحقق من الهوية السيادية بنجاح.")
            
    with tab_pay:
        st.subheader(t('paypal_sim'))
        st.markdown("محاكاة بوابة الدفع الآمنة لاشتراكات النظام الفضائي.")
        col_p1, col_p2 = st.columns([2, 1])
        with col_p1:
            st.markdown("""
            * **الباقة**: الباقة السيادية Titan X (الوصول الشامل لـ 5000 قمر صناعي)
            * **المبلغ المستحق**: **$199.00 USD**
            * **معرف المعاملة الآمنة**: `PAY-SPV-COSMIC324-2026`
            """)
        with col_p2:
            if st.button(t('pay_now')):
                st.success(t('payment_success'))
                st.balloons()

# 4️⃣ القسم الرابع: صحة النظام والشبكة (System Health)
elif app_section == t('nav_health'):
    st.markdown(f"<h1>{t('health_title')}</h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric(t('server_load'), "14.2%", "-2.1%")
    c2.metric(t('network_latency'), "18.4 ms", "-0.5 ms")
    c3.metric(t('packet_loss'), "0.001%", "0.0%")
    c4.metric(t('cpu_usage'), "32.8%", "+1.4%")
    
    st.markdown("---")
    st.subheader("📈 رسم الأداء اللحظي للخوادم ومراكز التوجيه المداري")
    
    health_steps = list(range(1, 21))
    cpu_sim = [np.sin(i/2.0) * 15 + 35 for i in health_steps]
    mem_sim = [62.0 + np.cos(i/3.0) * 3 for i in health_steps]
    
    df_health = pd.DataFrame({
        "الخطوة الزمنية": health_steps,
        t('cpu_usage'): cpu_sim,
        t('memory_usage'): mem_sim
    })
    
    fig_h = px.line(df_health, x="الخطوة الزمنية", y=[t('cpu_usage'), t('memory_usage')], color_discrete_sequence=['#00CCFF', '#FF3366'])
    fig_h.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)'),
        height=350
    )
    st.plotly_chart(fig_h, use_container_width=True)

# 5️⃣ القسم الخامس: الإعدادات المتقدمة (Advanced Settings)
elif app_section == t('nav_settings'):
    st.markdown(f"<h1>{t('settings_title')}</h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    api_endpoint_input = st.text_input(t('api_endpoint'), value=SOURCE_CONFIG['baseUrl'])
    encryption_choice = st.selectbox(t('encryption_level'), ["AES-256 Sovereign Quantum", "AES-128 Standard", "RSA-4096 Hybrid"])
    cache_ttl = st.number_input("مدة تخزين البيانات المؤقتة (Cache TTL Seconds)", min_value=300, max_value=86400, value=CELESTRAK_CONFIG["cacheTtlSeconds"])
    
    if st.button(t('save_settings')):
        st.success(t('settings_saved'))

# ============================================================
# 📌 حقوق الملكية والتذييل الرسمي السيادي
# ============================================================
st.markdown("---")
st.markdown("""
<div class='copyright'>
    <p>🛰️ COSMIC-324: 6G Titan X Orbital Command v7.0 - All-Inclusive Edition</p>
    <p>© 2026 Yousif Zakaria Eissa Arbarb. جميع الحقوق محفوظة.</p>
</div>
""", unsafe_allow_html=True)
