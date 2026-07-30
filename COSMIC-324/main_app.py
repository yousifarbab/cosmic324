import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random
import requests
import math
import time
from datetime import datetime
from typing import Dict, List, Optional
from types import SimpleNamespace
import io
from fpdf import FPDF

# ============================================================
# 🌍 نظام الترجمة (7 لغات)
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
        "disabled": "🔴 معطل",
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
        "3d_globe": "🌍 الخريطة الكونية ثلاثية الأبعاد",
        "elevation": "الارتفاع",
        "azimuth": "الزاوية الأفقية",
        "distance": "المسافة"
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
        "disabled": "🔴 Disabled",
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
        "3d_globe": "🌍 3D Constellation Globe",
        "elevation": "Elevation",
        "azimuth": "Azimuth",
        "distance": "Distance"
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
        "disabled": "🔴 Désactivé",
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
        "3d_globe": "🌍 Globe 3D de la constellation",
        "elevation": "Élévation",
        "azimuth": "Azimut",
        "distance": "Distance"
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
        "disabled": "🔴 Deaktiviert",
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
        "3d_globe": "🌍 3D-Konstellationsglobus",
        "elevation": "Höhenwinkel",
        "azimuth": "Azimut",
        "distance": "Entfernung"
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
        "disabled": "🔴 Desactivado",
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
        "3d_globe": "🌍 Globo 3D de la constelación",
        "elevation": "Elevación",
        "azimuth": "Azimut",
        "distance": "Distancia"
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
        "disabled": "🔴 禁用",
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
        "3d_globe": "🌍 3D星座球体",
        "elevation": "仰角",
        "azimuth": "方位角",
        "distance": "距离"
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
        "disabled": "🔴 Отключен",
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
        "3d_globe": "🌍 3D-глобус созвездия",
        "elevation": "Угол места",
        "azimuth": "Азимут",
        "distance": "Расстояние"
    }
}

def t(key: str) -> str:
    lang = st.session_state.get('language', 'ar')
    return LANGUAGES.get(lang, LANGUAGES['ar']).get(key, key)

# ============================================================
# 📡 جلب بيانات Celestrak
# ============================================================
_last_successful_data = None

@st.cache_data(ttl=1800)
def fetch_celestrak_data(group: str = "starlink", max_satellites: int = 5000) -> List[Dict]:
    global _last_successful_data
    url = f"https://celestrak.org/NORAD/elements/gp.php?GROUP={group}&FORMAT=json"
    max_retries = 3
    retry_delay = 2
    
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            if response.text and response.text.startswith('{'):
                data = response.json()
                if data:
                    _last_successful_data = data
                    return data[:max_satellites]
                else:
                    raise ValueError("البيانات المستلمة فارغة")
            else:
                raise ValueError("الاستجابة ليست بصيغة JSON صالحة")
        except Exception:
            if attempt < max_retries - 1:
                time.sleep(retry_delay * (attempt + 1))
            else:
                if _last_successful_data:
                    return _last_successful_data[:max_satellites]
                else:
                    return []
    return []

def tle_to_orbit(tle_entry: Dict) -> Optional[SimpleNamespace]:
    try:
        mean_motion = float(tle_entry.get('MEAN_MOTION', 0))
        eccentricity = float(tle_entry.get('ECCENTRICITY', 0))
        inclination = float(tle_entry.get('INCLINATION', 0))
        inclination_rad = math.radians(inclination)
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
            y2 = y1 * math.cos(inclination_rad) - z1 * math.sin(inclination_rad)
            z2 = y1 * math.sin(inclination_rad) + z1 * math.cos(inclination_rad)
            x_final = x2 * math.cos(raan) - y2 * math.sin(raan)
            y_final = x2 * math.sin(raan) + y2 * math.cos(raan)
            z_final = z2
            return (x_final, y_final, z_final)
        
        orbit = SimpleNamespace()
        orbit.position_at_time = position_at_time
        orbit.name = tle_entry.get('OBJECT_NAME', 'SAT')
        orbit.altitude = a - 6371
        orbit.a = a
        orbit.e = eccentricity
        orbit.i = inclination_rad
        return orbit
    except Exception:
        return None

def generate_orbit_map(num_satellites: int = 5000, group: str = "starlink", use_celestrak: bool = True) -> Dict:
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
        orbit.a = a
        orbit.e = e
        orbit.i = incl
        orbit_map[orbit.name] = orbit
    return orbit_map

# ============================================================
# 🧪 محاكي السيناريوهات
# ============================================================
def apply_scenario(df: pd.DataFrame, scenario: str, custom_jamming: float = 0.0, custom_lost_sats: int = 0) -> pd.DataFrame:
    df_scenario = df.copy()
    jamming_factor = 0.0
    lost_satellites = 0
    
    if scenario == "🔴 فقدان 5 أقمار":
        lost_satellites = 5
        jamming_factor = 0.0
    elif scenario == "🔴🔴 تشويش شديد (Jamming 80%)":
        lost_satellites = 0
        jamming_factor = 0.8
    elif scenario == "🔴🔴🔴 انهيار البوابة الأرضية":
        lost_satellites = 0
        jamming_factor = 0.0
        if not df_scenario.empty:
            df_scenario.loc[0, t('status')] = t('disabled')
    elif scenario == "🎛️ سيناريو مخصص":
        lost_satellites = custom_lost_sats
        jamming_factor = custom_jamming
    else:
        return df_scenario
    
    if lost_satellites > 0 and len(df_scenario) > lost_satellites:
        indices_to_disable = random.sample(range(1, len(df_scenario)), min(lost_satellites, len(df_scenario)-1))
        for idx in indices_to_disable:
            df_scenario.loc[idx, t('status')] = t('disabled')
            
    if jamming_factor > 0:
        st.session_state.jamming_effect = jamming_factor
    else:
        st.session_state.jamming_effect = 0.0
        
    st.session_state.scenario_applied = True
    st.session_state.scenario_name = scenario
    st.session_state.lost_count = lost_satellites
    st.session_state.jamming_applied = jamming_factor
    
    return df_scenario

# ============================================================
# 📄 نظام تصدير تقارير PDF
# ============================================================
def generate_pdf_report(df, latency_df, scenario_info, alert_info):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "COSMIC-324: Orbital Status Report", ln=True, align='C')
    pdf.set_font("Arial", 'I', 10)
    pdf.cell(200, 10, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align='C')
    pdf.ln(10)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, "1. Constellation Summary", ln=True)
    pdf.set_font("Arial", '', 10)
    pdf.cell(100, 8, f"Total Satellites: {len(df)}", ln=False)
    pdf.cell(100, 8, f"Active: {df[df[t('status')] == t('active')].shape[0]}", ln=True)
    pdf.cell(100, 8, f"Calibration: {df[df[t('status')] == t('calibration')].shape[0]}", ln=False)
    pdf.cell(100, 8, f"Standby: {df[df[t('status')] == t('standby')].shape[0]}", ln=True)
    pdf.ln(5)
    
    if alert_info:
        pdf.set_font("Arial", 'B', 12)
        pdf.set_text_color(255, 0, 0)
        pdf.cell(200, 10, "2. Active Alerts", ln=True)
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", '', 10)
        for alert in alert_info:
            pdf.cell(200, 8, f"⚠️ {alert}", ln=True)
        pdf.ln(5)
    
    if scenario_info:
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, "3. Applied Scenario", ln=True)
        pdf.set_font("Arial", '', 10)
        pdf.cell(200, 8, f"Scenario: {scenario_info.get('name', 'None')}", ln=True)
        pdf.cell(200, 8, f"Lost Satellites: {scenario_info.get('lost', 0)}", ln=True)
        pdf.cell(200, 8, f"Jamming Level: {scenario_info.get('jamming', 0)*100:.0f}%", ln=True)
        pdf.ln(5)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, "4. Telemetry Data (Sample)", ln=True)
    pdf.set_font("Arial", 'B', 8)
    headers = ["Satellite", "Status", "Latitude", "Longitude", "Altitude (km)"]
    col_widths = [30, 25, 30, 30, 30]
    for i, header in enumerate(headers):
        pdf.cell(col_widths[i], 8, header, border=1)
    pdf.ln()
    
    pdf.set_font("Arial", '', 8)
    for _, row in df.head(10).iterrows():
        pdf.cell(col_widths[0], 8, str(row[t('satellite')])[:10], border=1)
        pdf.cell(col_widths[1], 8, str(row[t('status')]), border=1)
        pdf.cell(col_widths[2], 8, str(row[t('latitude')]), border=1)
        pdf.cell(col_widths[3], 8, str(row[t('longitude')]), border=1)
        pdf.cell(col_widths[4], 8, str(row[t('altitude')]), border=1)
        pdf.ln()
    pdf.ln(5)
    
    if latency_df is not None and not latency_df.empty:
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, "5. Latency Statistics", ln=True)
        pdf.set_font("Arial", '', 10)
        pdf.cell(100, 8, f"Min: {latency_df[t('latency_ms')].min():.2f} ms", ln=False)
        pdf.cell(100, 8, f"Max: {latency_df[t('latency_ms')].max():.2f} ms", ln=True)
        pdf.cell(100, 8, f"Avg: {latency_df[t('latency_ms')].mean():.2f} ms", ln=False)
        pdf.cell(100, 8, f"Jitter: {latency_df[t('latency_ms')].std():.2f} ms", ln=True)
        
    return pdf.output(dest='S').encode('latin1')

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
    
    # محاكي السيناريوهات
    st.markdown("---")
    st.subheader("🧪 محاكي السيناريوهات")

    scenario_options = [
        "بدون سيناريو (Nominal)",
        "🔴 فقدان 5 أقمار",
        "🔴🔴 تشويش شديد (Jamming 80%)",
        "🔴🔴🔴 انهيار البوابة الأرضية",
        "🎛️ سيناريو مخصص"
    ]
    selected_scenario = st.selectbox("اختر السيناريو", scenario_options, index=0)

    if selected_scenario == "🎛️ سيناريو مخصص":
        custom_jamming = st.slider("شدة التشويش (0-1)", 0.0, 1.0, 0.3, 0.05)
        custom_lost_sats = st.slider("عدد الأقمار المفقودة", 0, 20, 5, 1)
        st.caption(f"⚠️ سيتم تعطيل {custom_lost_sats} قمر عشوائي مع تشويش {custom_jamming:.0%}")

    if st.button("▶️ تنفيذ السيناريو", use_container_width=True, type="primary"):
        st.session_state.run_scenario = True
        st.session_state.selected_scenario = selected_scenario
        if selected_scenario == "🎛️ سيناريو مخصص":
            st.session_state.custom_jamming = custom_jamming
            st.session_state.custom_lost_sats = custom_lost_sats
        st.rerun()

    # تصدير التقرير من الشريط الجانبي
    st.markdown("---")
    st.subheader("📄 Export Report")
    
    # تهيئة أولية لبيانات الـ Latency للجلسة إن لم تكن موجودة
    if 'latest_latency_df' not in st.session_state:
        st.session_state.latest_latency_df = pd.DataFrame()

    if st.button("📥 Download PDF Report", use_container_width=True):
        # سنقوم بتوليد بيانات مؤقتة للتقرير إذا دعت الحاجة
        temp_latency_df = st.session_state.latest_latency_df
        scenario_info = {
            'name': st.session_state.get('selected_scenario', 'Nominal'),
            'lost': st.session_state.get('lost_count', 0),
            'jamming': st.session_state.get('jamming_applied', 0.0)
        }
        
        # حساب المتغيرات محلياً للتقرير
        active_cnt_temp = df[df[t('status')] == t('active')].shape[0] if 'df' in locals() else 0
        jam_eff_temp = st.session_state.get('jamming_effect', 0.0)
        base_avg_lat_temp = 10.0
        avg_lat_temp = base_avg_lat_temp * (1.0 + jam_eff_temp * 1.5)
        
        alert_info = []
        if avg_lat_temp > alert_threshold:
            alert_info.append(f"High Latency: {avg_lat_temp:.2f} ms (Threshold: {alert_threshold} ms)")
        if active_cnt_temp < active_threshold:
            alert_info.append(f"Low Active Satellites: {active_cnt_temp} (Threshold: {active_threshold})")
        
        if 'df' in locals() and not df.empty:
            pdf_data = generate_pdf_report(df, temp_latency_df, scenario_info, alert_info)
            st.download_button(
                label="📥 Click here to save PDF",
                data=pdf_data,
                file_name=f"COSMIC324_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mime="application/pdf"
            )

    st.markdown("---")
    if st.button(t("update_btn"), use_container_width=True):
        st.cache_data.clear()
        st.session_state.run_scenario = False
        st.session_state.scenario_applied = False
        st.rerun()
    
    st.caption(f"{t('last_update')}: {datetime.now().strftime('%H:%M:%S')}")

# ============================================================
# 🎯 العنوان الرئيسي
# ============================================================
st.markdown(f"<h1 style='text-align: center; font-size: 3em; text-shadow: 0 0 40px #00CCFF;'>{t('title')}</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #88AACC; font-size: 1.1em;'>{t('subtitle')}</p>", unsafe_allow_html=True)

# ============================================================
# 📊 توليد البيانات وتطبيق السيناريو
# ============================================================
with st.spinner("🔄 جاري تحميل بيانات الأقمار..."):
    orbit_map = generate_orbit_map(num_satellites, group, use_celestrak)
    
    # حفظ الخريطة في الذاكرة المؤقتة للتحكم لاحقاً
    if 'orbit_map' not in st.session_state:
        st.session_state.orbit_map = orbit_map
    else:
        st.session_state.orbit_map.update(orbit_map)

    data = []
    for name, orbit in list(st.session_state.orbit_map.items())[:num_satellites]:
        pos = orbit.position_at_time(0.0)
        if pos and len(pos) >= 3:
            x, y, z = pos
            lat = math.degrees(math.asin(z / math.sqrt(x**2 + y**2 + z**2))) if (x**2 + y**2 + z**2) > 0 else 0
            lon = math.degrees(math.atan2(y, x))
            alt = orbit.altitude if hasattr(orbit, 'altitude') else 550
            
            # التحقق من الحالة المخزنة يدوياً في الجلسة إن وجدت
            sat_status_key = f"status_{name}"
            if sat_status_key in st.session_state:
                status = st.session_state[sat_status_key]
            else:
                status = random.choice([t('active'), t('calibration'), t('standby')])
                
            data.append({
                t('satellite'): name[:15],
                t('status'): status,
                t('latitude'): round(lat, 4),
                t('longitude'): round(lon, 4),
                t('altitude'): round(alt, 2)
            })
    df = pd.DataFrame(data)

# تطبيق السيناريو إذا تم تفعليه
if st.session_state.get('run_scenario', False):
    scenario = st.session_state.get('selected_scenario', 'بدون سيناريو (Nominal)')
    custom_jamming = st.session_state.get('custom_jamming', 0.0)
    custom_lost_sats = st.session_state.get('custom_lost_sats', 0)
    
    df = apply_scenario(df, scenario, custom_jamming, custom_lost_sats)
    
    st.info(f"🧪 **السيناريو المطبق:** {scenario}")
    if 'lost_count' in st.session_state and st.session_state.lost_count > 0:
        st.warning(f"⚠️ تم تعطيل {st.session_state.lost_count} قمر صناعي")
    if 'jamming_applied' in st.session_state and st.session_state.jamming_applied > 0:
        st.warning(f"📡 تشويش نشط بنسبة {st.session_state.jamming_applied:.0%}")
    
    if st.button("🔄 إعادة ضبط السيناريو"):
        st.session_state.run_scenario = False
        st.session_state.scenario_applied = False
        st.session_state.jamming_effect = 0.0
        st.rerun()

# ============================================================
# 🔔 التنبيهات الذكية
# ============================================================
active_count = df[df[t('status')] == t('active')].shape[0]
jamming_effect = st.session_state.get('jamming_effect', 0.0)
base_avg_latency = round(random.uniform(5, 18), 2)
avg_latency = round(base_avg_latency * (1.0 + jamming_effect * 1.5), 2)

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
    status_val = row[t('status')]
    if status_val == t('active'):
        return ['background-color: #1a3a1a; color: #00FF00'] * len(row)
    elif status_val == t('calibration'):
        return ['background-color: #3a3a1a; color: #FFAA00'] * len(row)
    elif status_val == t('standby'):
        return ['background-color: #3a1a1a; color: #FF5555'] * len(row)
    elif status_val == t('disabled'):
        return ['background-color: #2a0a0a; color: #FF2222; text-decoration: line-through;'] * len(row)
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
# 🎛️ التحكم في العقد المدارية (الميزة الجديدة)
# ============================================================
st.markdown("---")
st.subheader("🎛️ Orbital Node Control")

node_names = df[t('satellite')].tolist()
if node_names:
    selected_node = st.selectbox("Select Satellite for Control", node_names, index=0)
    
    node_row = df[df[t('satellite')] == selected_node]
    if not node_row.empty:
        current_node_status = node_row.iloc[0][t('status')]
        current_node_alt = node_row.iloc[0][t('altitude')]
        st.caption(f"📍 **{selected_node}** | Status: {current_node_status} | Alt: {current_node_alt} km")
        
        col_c1, col_c2, col_c3 = st.columns(3)
        with col_c1:
            if st.button("🟢 Set Active", use_container_width=True):
                st.session_state[f"status_{selected_node}"] = t('active')
                st.rerun()
        with col_c2:
            if st.button("🟡 Set Calibration", use_container_width=True):
                st.session_state[f"status_{selected_node}"] = t('calibration')
                st.rerun()
        with col_c3:
            if st.button("🔴 Set Standby", use_container_width=True):
                st.session_state[f"status_{selected_node}"] = t('standby')
                st.rerun()
                
        if selected_node in st.session_state.get('orbit_map', {}):
            orb_obj = st.session_state.orbit_map[selected_node]
            if hasattr(orb_obj, 'a'):
                st.caption(f"🛰️ Orbital Elements: a={orb_obj.a:.1f} km, e={orb_obj.e:.3f}, i={math.degrees(orb_obj.i):.1f}°")

# ============================================================
# 🌍 الخريطة ثلاثية الأبعاد
# ============================================================
st.markdown("---")
st.subheader(t('3d_globe'))

if not df.empty and len(df) > 0:
    try:
        fig_3d = go.Figure()

        fig_3d.add_trace(go.Scattergeo(
            lon=df[t('longitude')].tolist(),
            lat=df[t('latitude')].tolist(),
            mode='markers',
            marker=dict(
                size=8,
                color=df[t('status')].map({
                    t('active'): '#00FF00',
                    t('calibration'): '#FFAA00',
                    t('standby'): '#FF5555',
                    t('disabled'): '#FF0000'
                }).fillna('#888888').tolist(),
                symbol='circle',
                line=dict(width=1, color='rgba(255,255,255,0.3)')
            ),
            text=df[t('satellite')].tolist(),
            hoverinfo='text',
            hovertext=[
                f"{row[t('satellite')]}<br>Status: {row[t('status')]}<br>Lat: {row[t('latitude')]}°<br>Lon: {row[t('longitude')]}°<br>Alt: {row[t('altitude')]} km"
                for _, row in df.iterrows()
            ]
        ))

        fig_3d.add_trace(go.Scattergeo(
            lon=[0],
            lat=[0],
            mode='markers',
            marker=dict(size=14, color='#FF3366', symbol='star'),
            text=['🛰️ Ground'],
            hoverinfo='text',
            hovertext=['🛰️ Ground Station<br>Lat: 0°<br>Lon: 0°']
        ))

        fig_3d.update_layout(
            title={
                'text': t('3d_globe'),
                'font': {'size': 20, 'color': '#00CCFF', 'family': 'Arial Black'},
                'x': 0.5
            },
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
            height=600,
            margin=dict(l=0, r=0, t=40, b=0)
        )

        st.plotly_chart(fig_3d, use_container_width=True)

    except Exception as e:
        st.error(f"⚠️ حدث خطأ أثناء إنشاء الخريطة: {e}")

# ============================================================
# 📊 تحليلات متقدمة
# ============================================================
st.markdown("---")
st.subheader("📊 تحليلات متقدمة")

col_a1, col_a2, col_a3 = st.columns(3)
col_a1.metric(t('avg_alt'), f"{df[t('altitude')].mean():.1f} km")
col_a2.metric(t('max_alt'), f"{df[t('altitude')].max():.1f} km")
col_a3.metric(t('min_alt'), f"{df[t('altitude')].min():.1f} km")

fig_hist = px.histogram(
    df,
    x=t('altitude'),
    color=t('status'),
    title="توزيع الارتفاعات حسب الحالة",
    color_discrete_map={
        t('active'): '#00FF00',
        t('calibration'): '#FFAA00',
        t('standby'): '#FF5555',
        t('disabled'): '#FF0000'
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

latency_data = []
for i in range(20):
    jamming_add = jamming_effect * random.uniform(3.0, 8.0) * ((i + 1) / 10)
    val = 4.0 + i * 0.2 + random.uniform(-0.2, 0.2) + jamming_add
    latency_data.append({
        t('step'): i + 1,
        t('latency_ms'): round(max(1.0, val), 2)
    })
latency_df = pd.DataFrame(latency_data)
st.session_state.latest_latency_df = latency_df

fig_latency = px.line(
    latency_df,
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

if jamming_effect > 0:
    st.caption(f"📡 تأثير التشويش على زمن الانتقال: +{jamming_effect*100:.0f}% إضافي")

# ============================================================
# 📌 الحالة السفلية
# ============================================================
st.markdown("---")
col_f1, col_f2, col_f3 = st.columns(3)
col_f1.caption(f"🛰️ COSMIC-324 v5.0 | {len(df)} {t('satellite')}")
col_f2.caption(f"🌍 {LANGUAGES[st.session_state.get('language', 'ar')]['name']}")
col_f3.caption(f"🔐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if use_celestrak:
    st.caption(f"📡 بيانات حية من Celestrak (المجموعة: {group}) - تحديث تلقائي كل ساعة")
