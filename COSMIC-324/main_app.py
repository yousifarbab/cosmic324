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
# 🌍 نظام الترجمة (7 لغات) - كامل
# ============================================================
LANGUAGES = {
    "ar": {
        "name": "العربية",
        "title": "🚀 كوزميك-324: القيادة المدارية 6G",
        "subtitle": "منصة التتبع المداري الحي متعددة اللغات",
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
        "map_title": "🌍 خريطة الأقمار ثلاثية الأبعاد",
        "avg_alt": "متوسط الارتفاع",
        "max_alt": "أقصى ارتفاع",
        "min_alt": "أدنى ارتفاع",
        "celestrak": "📡 جلب بيانات حقيقية من Celestrak (تلقائي كل ساعة)",
        "group": "اختر المجموعة",
        "alert_latency": "⚠️ تنبيه: ارتفاع زمن الانتقال!",
        "alert_satellites": "⚠️ تنبيه: انخفاض عدد الأقمار النشطة!",
        "alert_threshold": "عتبة التنبيه (مللي ثانية)",
        "active_threshold": "الحد الأدنى للأقمار النشطة",
        "3d_globe": "🌍 الخريطة الكونية ثلاثية الأبعاد"
    },
    "en": {
        "name": "English",
        "title": "🚀 COSMIC-324: 6G Orbital Command",
        "subtitle": "Multi-language Live Orbital Tracking Platform",
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
        "map_title": "🌍 3D Satellite Map",
        "avg_alt": "Avg Altitude",
        "max_alt": "Max Altitude",
        "min_alt": "Min Altitude",
        "celestrak": "📡 Fetch Live Data from Celestrak (Auto every hour)",
        "group": "Select Group",
        "alert_latency": "⚠️ Alert: High Latency!",
        "alert_satellites": "⚠️ Alert: Low Active Satellites!",
        "alert_threshold": "Alert Threshold (ms)",
        "active_threshold": "Min Active Satellites",
        "3d_globe": "🌍 3D Constellation Globe"
    },
    "fr": {
        "name": "Français",
        "title": "🚀 COSMIC-324: Commandement Orbital 6G",
        "subtitle": "Plateforme de suivi orbital multilingue",
        "params": "⚙️ Paramètres",
        "sat_count": "Nombre de satellites (jusqu'à 5000)",
        "update_btn": "🔄 Actualiser",
        "active": "🟢 Actif",
        "calibration": "🟡 Étalonnage",
        "standby": "🔴 Veille",
        "total": "Total",
        "satellite": "Satellite",
        "status": "Statut",
        "latitude": "Latitude",
        "longitude": "Longitude",
        "altitude": "Altitude (km)",
        "latency_chart": "📈 Évolution de la latence",
        "step": "Étape",
        "latency_ms": "Latence (ms)",
        "last_update": "Dernière mise à jour",
        "map_title": "🌍 Carte 3D des satellites",
        "avg_alt": "Altitude moyenne",
        "max_alt": "Altitude max",
        "min_alt": "Altitude min",
        "celestrak": "📡 Données en direct de Celestrak (auto toutes les heures)",
        "group": "Choisir le groupe",
        "alert_latency": "⚠️ Alerte: Latence élevée!",
        "alert_satellites": "⚠️ Alerte: Peu de satellites actifs!",
        "alert_threshold": "Seuil d'alerte (ms)",
        "active_threshold": "Min. satellites actifs",
        "3d_globe": "🌍 Globe 3D de la constellation"
    },
    "de": {
        "name": "Deutsch",
        "title": "🚀 COSMIC-324: 6G Orbitalkommando",
        "subtitle": "Mehrsprachige Live-Orbit-Tracking-Plattform",
        "params": "⚙️ Parameter",
        "sat_count": "Anzahl der Satelliten (bis 5000)",
        "update_btn": "🔄 Aktualisieren",
        "active": "🟢 Aktiv",
        "calibration": "🟡 Kalibrierung",
        "standby": "🔴 Bereitschaft",
        "total": "Gesamt",
        "satellite": "Satellit",
        "status": "Status",
        "latitude": "Breitengrad",
        "longitude": "Längengrad",
        "altitude": "Höhe (km)",
        "latency_chart": "📈 Latenzentwicklung",
        "step": "Schritt",
        "latency_ms": "Latenz (ms)",
        "last_update": "Letzte Aktualisierung",
        "map_title": "🌍 3D-Satellitenkarte",
        "avg_alt": "Durchschn. Höhe",
        "max_alt": "Max. Höhe",
        "min_alt": "Min. Höhe",
        "celestrak": "📡 Live-Daten von Celestrak (auto stündlich)",
        "group": "Gruppe wählen",
        "alert_latency": "⚠️ Warnung: Hohe Latenz!",
        "alert_satellites": "⚠️ Warnung: Wenig aktive Satelliten!",
        "alert_threshold": "Warnschwelle (ms)",
        "active_threshold": "Min. aktive Satelliten",
        "3d_globe": "🌍 3D-Konstellationsglobus"
    },
    "es": {
        "name": "Español",
        "title": "🚀 COSMIC-324: Comando Orbital 6G",
        "subtitle": "Plataforma de seguimiento orbital multilingüe",
        "params": "⚙️ Parámetros",
        "sat_count": "Número de satélites (hasta 5000)",
        "update_btn": "🔄 Actualizar",
        "active": "🟢 Activo",
        "calibration": "🟡 Calibración",
        "standby": "🔴 En espera",
        "total": "Total",
        "satellite": "Satélite",
        "status": "Estado",
        "latitude": "Latitud",
        "longitude": "Longitud",
        "altitude": "Altitud (km)",
        "latency_chart": "📈 Evolución de la latencia",
        "step": "Paso",
        "latency_ms": "Latencia (ms)",
        "last_update": "Última actualización",
        "map_title": "🌍 Mapa 3D de satélites",
        "avg_alt": "Altitud media",
        "max_alt": "Altitud máxima",
        "min_alt": "Altitud mínima",
        "celestrak": "📡 Datos en vivo de Celestrak (auto cada hora)",
        "group": "Seleccionar grupo",
        "alert_latency": "⚠️ Alerta: ¡Latencia alta!",
        "alert_satellites": "⚠️ Alerta: ¡Pocos satélites activos!",
        "alert_threshold": "Umbral de alerta (ms)",
        "active_threshold": "Mín. satélites activos",
        "3d_globe": "🌍 Globo 3D de la constelación"
    },
    "zh": {
        "name": "中文",
        "title": "🚀 COSMIC-324: 6G 轨道指挥系统",
        "subtitle": "多语言实时轨道跟踪平台",
        "params": "⚙️ 仿真参数",
        "sat_count": "卫星数量（最多5000）",
        "update_btn": "🔄 刷新数据",
        "active": "🟢 活跃",
        "calibration": "🟡 校准",
        "standby": "🔴 待机",
        "total": "总计",
        "satellite": "卫星",
        "status": "状态",
        "latitude": "纬度",
        "longitude": "经度",
        "altitude": "高度（公里）",
        "latency_chart": "📈 信号延迟演变",
        "step": "步骤",
        "latency_ms": "延迟（毫秒）",
        "last_update": "最后更新",
        "map_title": "🌍 3D卫星地图",
        "avg_alt": "平均高度",
        "max_alt": "最大高度",
        "min_alt": "最小高度",
        "celestrak": "📡 从Celestrak获取实时数据（每小时自动）",
        "group": "选择星群",
        "alert_latency": "⚠️ 警报：高延迟！",
        "alert_satellites": "⚠️ 警报：活跃卫星数量低！",
        "alert_threshold": "警报阈值（毫秒）",
        "active_threshold": "最低活跃卫星数",
        "3d_globe": "🌍 3D星座球体"
    },
    "ru": {
        "name": "Русский",
        "title": "🚀 COSMIC-324: 6G Орбитальное командование",
        "subtitle": "Многоязычная платформа отслеживания орбит",
        "params": "⚙️ Параметры",
        "sat_count": "Количество спутников (до 5000)",
        "update_btn": "🔄 Обновить",
        "active": "🟢 Активен",
        "calibration": "🟡 Калибровка",
        "standby": "🔴 Ожидание",
        "total": "Всего",
        "satellite": "Спутник",
        "status": "Статус",
        "latitude": "Широта",
        "longitude": "Долгота",
        "altitude": "Высота (км)",
        "latency_chart": "📈 Эволюция задержки",
        "step": "Шаг",
        "latency_ms": "Задержка (мс)",
        "last_update": "Последнее обновление",
        "map_title": "🌍 3D-карта спутников",
        "avg_alt": "Сред. высота",
        "max_alt": "Макс. высота",
        "min_alt": "Мин. высота",
        "celestrak": "📡 Живые данные из Celestrak (авто каждый час)",
        "group": "Выбрать группу",
        "alert_latency": "⚠️ Предупреждение: Высокая задержка!",
        "alert_satellites": "⚠️ Предупреждение: Мало активных спутников!",
        "alert_threshold": "Порог предупреждения (мс)",
        "active_threshold": "Мин. активных спутников",
        "3d_globe": "🌍 3D-глобус созвездия"
    }
}

def t(key: str) -> str:
    lang = st.session_state.get('language', 'ar')
    return LANGUAGES.get(lang, LANGUAGES['ar']).get(key, key)

# ============================================================
# 📡 جلب بيانات Celestrak التلقائي
# ============================================================
@st.cache_data(ttl=3600)
def fetch_celestrak_data(group: str = "starlink", max_satellites: int = 5000) -> List[Dict]:
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

def generate_orbit_map(num_satellites: int = 100, group: str = "starlink", use_celestrak: bool = True) -> Dict:
    if use_celestrak:
        raw_data = fetch_celestrak_data(group, num_satellites)
        orbit_map = {}
        if raw_data:
            for entry in raw_data:
                orbit = tle_to_orbit(entry)
                if orbit:
                    orbit_map[orbit.name] = orbit
            if orbit_map:
                return orbit_map
    # Mock data
    orbit_map = {}
    for i in range(min(num_satellites, 5000)):
        a = 7000 + random.randint(-500, 500)
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
    .alert-box { padding: 10px 15px; border-radius: 8px; margin: 10px 0; border: 1px solid #FF5555; background-color: rgba(255, 85, 85, 0.1); }
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
    
    num_satellites = st.slider(t("sat_count"), 10, 5000, 100, 50)
    
    st.markdown("---")
    st.subheader(t("celestrak"))
    group = st.selectbox(t("group"), ["starlink", "gps", "active", "oneweb", "iridium"])
    use_celestrak = st.checkbox("استخدام بيانات حقيقية من Celestrak (تحديث كل ساعة)", value=True)
    
    st.markdown("---")
    st.subheader("🔔 إعدادات التنبيهات")
    alert_threshold = st.slider(t("alert_threshold"), 5.0, 50.0, 20.0, 1.0)
    active_threshold = st.slider(t("active_threshold"), 1, 50, 5, 1)
    
    if st.button(t("update_btn"), use_container_width=True):
        st.cache_data.clear()
        st.rerun()
    
    st.caption(f"{t('last_update')}: {datetime.now().strftime('%H:%M:%S')}")

# ============================================================
# 🎯 العنوان الرئيسي
# ============================================================
st.markdown(f"<h1 style='text-align: center; font-size: 3em; text-shadow: 0 0 40px #00CCFF;'>{t('title')}</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #88AACC; font-size: 1.1em;'>{t('subtitle')}</p>", unsafe_allow_html=True)

# ============================================================
# 📊 توليد البيانات
# ============================================================
with st.spinner("🔄 جاري تحميل بيانات الأقمار..."):
    orbit_map = generate_orbit_map(num_satellites, group, use_celestrak)
    
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
                t('satellite'): name[:15],
                t('status'): status,
                t('latitude'): round(lat, 4),
                t('longitude'): round(lon, 4),
                t('altitude'): round(alt, 2)
            })
    df = pd.DataFrame(data)

# ============================================================
# 🔔 التنبيهات الذكية
# ============================================================
active_count = df[df[t('status')] == t('active')].shape[0]
avg_latency = round(random.uniform(5, 25), 2)

if avg_latency > alert_threshold:
    st.markdown(f"<div class='alert-box'>🚨 {t('alert_latency')} (القيمة الحالية: {avg_latency} ms، الحد الأقصى: {alert_threshold} ms)</div>", unsafe_allow_html=True)

if active_count < active_threshold:
    st.markdown(f"<div class='alert-box'>🚨 {t('alert_satellites')} (النشطة: {active_count}، الحد الأدنى: {active_threshold})</div>", unsafe_allow_html=True)

# ============================================================
# 📈 الإحصائيات السريعة
# ============================================================
col1, col2, col3, col4 = st.columns(4)
col1.metric(t('total'), len(df))
col2.metric(t('active'), active_count)
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
# 🌍 خريطة 3D (المصححة)
# ============================================================
st.markdown("---")
st.subheader(t('3d_globe'))

# إنشاء كائن الشكل الفارغ أولاً، ثم إضافة البيانات إليه
fig_3d = go.Figure()

# إضافة الأقمار
fig_3d.add_trace(go.Scattergeo(
    lon=df[t('longitude')],
    lat=df[t('latitude')],
    mode='markers+text',
    marker=dict(
        size=8,
        color=df[t('status')].map({
            t('active'): '#00FF00',
            t('calibration'): '#FFAA00',
            t('standby'): '#FF5555'
        }),
        symbol='circle',
        line=dict(width=1, color='rgba(255,255,255,0.3)')
    ),
    text=df[t('satellite')],
    textposition='top center',
    textfont=dict(size=9, color='white'),
    hoverinfo='text',
    hovertext=df.apply(lambda row: f"{row[t('satellite')]}<br>Lat: {row[t('latitude')]}°<br>Lon: {row[t('longitude')]}°<br>Alt: {row[t('altitude')]} km", axis=1)
))

# إضافة المحطة الأرضية
fig_3d.add_trace(go.Scattergeo(
    lon=[0],
    lat=[0],
    mode='markers+text',
    marker=dict(size=16, color='#FF3366', symbol='star'),
    text=['🛰️ Ground'],
    textposition='bottom center',
    textfont=dict(size=12, color='#FF6699'),
    hoverinfo='text',
    hovertext=['🛰️ Ground Station<br>Lat: 0°<br>Lon: 0°<br>Altitude: 0 km']
))

# تحديث التخطيط
fig_3d.update_layout(
    title=dict(
        text=t('3d_globe'),
        font=dict(size=22, color='#00CCFF', family='Arial Black'),
        x=0.5
    ),
    geo=dict(
        projection_type='orthographic',
        showland=True,
        landcolor='rgb(10, 10, 20)',
        coastlinecolor='rgb(60, 60, 80)',
        showocean=True,
        oceancolor='rgb(5, 5, 15)',
        showcountries=True,
        countrycolor='rgb(50, 50, 70)',
        bgcolor='rgba(0,0,0,0)'
    ),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    height=650,
    margin=dict(l=0, r=0, t=40, b=0),
    updatemenus=[dict(
        type="buttons",
        buttons=[
            dict(label="🔄 Rotate", method="relayout", args={"geo.projection.rotation.lon": 20, "geo.projection.rotation.lat": 5}),
            dict(label="⏺ Reset", method="relayout", args={"geo.projection.rotation.lon": 0, "geo.projection.rotation.lat": 0})
        ],
        direction="right",
        x=0.05,
        y=0.02
    )]
)

st.plotly_chart(fig_3d, use_container_width=True)

# ============================================================
# 📊 تحليلات متقدمة
# ============================================================
st.markdown("---")
st.subheader("📊 تحليلات متقدمة")

col_a1, col_a2, col_a3 = st.columns(3)
col_a1.metric(t('avg_alt'), f"{df[t('altitude')].mean():.1f} km")
col_a2.metric(t('max_alt'), f"{df[t('altitude')].max():.1f} km")
col_a3.metric(t('min_alt'), f"{df[t('altitude')].min():.1f} km")

# رسم بياني لتوزيع الارتفاعات
fig_hist = px.histogram(
    df,
    x=t('altitude'),
    color=t('status'),
    title="توزيع الارتفاعات حسب الحالة",
    color_discrete_map={
        t('active'): '#00FF00',
        t('calibration'): '#FFAA00',
        t('standby'): '#FF5555'
    },
    nbins=20
)
fig_hist.update_layout(
    xaxis_title=t('altitude'),
    yaxis_title="العدد",
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    bargap=0.1
)
st.plotly_chart(fig_hist, use_container_width=True)

# ============================================================
# 📈 منحنى Latency
# ============================================================
st.markdown("---")
st.subheader(t('latency_chart'))

latency_data = pd.DataFrame({
    t('step'): list(range(1, 21)),
    t('latency_ms'): [round(3.0 + i * 0.15 + random.uniform(-0.3, 0.3), 2) for i in range(20)]
})

fig_latency = px.line(
    latency_data,
    x=t('step'),
    y=t('latency_ms'),
    title=t('latency_chart'),
    markers=True
)
fig_latency.update_traces(line_color='#00CCFF', line_width=3, marker_size=8)
fig_latency.add_hline(
    y=alert_threshold,
    line_dash="dash",
    line_color="red",
    annotation_text=f"⚠️ Alert Threshold: {alert_threshold} ms"
)
fig_latency.update_layout(
    xaxis_title=t('step'),
    yaxis_title=t('latency_ms'),
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)'),
    yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)')
)
st.plotly_chart(fig_latency, use_container_width=True)

# ============================================================
# 📌 الحالة السفلية
# ============================================================
st.markdown("---")
col_f1, col_f2, col_f3 = st.columns(3)
col_f1.caption(f"🛰️ COSMIC-324 v4.0 | {len(df)} {t('satellite')}")
col_f2.caption(f"🌍 {LANGUAGES[st.session_state.get('language', 'ar')]['name']}")
col_f3.caption(f"🔐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if use_celestrak:
    st.caption(f"📡 بيانات حية من Celestrak (المجموعة: {group}) - تحديث تلقائي كل ساعة")
