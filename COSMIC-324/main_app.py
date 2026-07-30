import streamlit as st
import pandas as pd
import plotly.express as px
import random
from datetime import datetime

# ============================================================
# 🌍 نظام الترجمة (7 لغات)
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
        "last_update": "آخر تحديث"
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
        "last_update": "Last Update"
    },
    "fr": {
        "name": "Français",
        "title": "🚀 COSMIC-324: Commandement Orbital 6G",
        "subtitle": "Plateforme de suivi orbital multilingue",
        "params": "⚙️ Paramètres",
        "sat_count": "Nombre de satellites",
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
        "last_update": "Dernière mise à jour"
    },
    "de": {
        "name": "Deutsch",
        "title": "🚀 COSMIC-324: 6G Orbitalkommando",
        "subtitle": "Mehrsprachige Live-Orbit-Tracking-Plattform",
        "params": "⚙️ Parameter",
        "sat_count": "Anzahl der Satelliten",
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
        "last_update": "Letzte Aktualisierung"
    },
    "es": {
        "name": "Español",
        "title": "🚀 COSMIC-324: Comando Orbital 6G",
        "subtitle": "Plataforma de seguimiento orbital multilingüe",
        "params": "⚙️ Parámetros",
        "sat_count": "Número de satélites",
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
        "last_update": "Última actualización"
    },
    "zh": {
        "name": "中文",
        "title": "🚀 COSMIC-324: 6G 轨道指挥系统",
        "subtitle": "多语言实时轨道跟踪平台",
        "params": "⚙️ 仿真参数",
        "sat_count": "卫星数量",
        "update_btn": "🔄 刷新数据",
        "active": "🟢 活跃",
        "calibration": "🟡 校准",
        "standby": "🔴 待机",
        "total": "总计",
        "satellite": "卫星",
        "status": "状态",
        "latitude": "纬度",
        "longitude": "经度",
        "altitude": "高度 (公里)",
        "latency_chart": "📈 信号延迟演变",
        "step": "步骤",
        "latency_ms": "延迟 (毫秒)",
        "last_update": "最后更新"
    },
    "ru": {
        "name": "Русский",
        "title": "🚀 COSMIC-324: 6G Орбитальное командование",
        "subtitle": "Многоязычная платформа отслеживания орбит",
        "params": "⚙️ Параметры",
        "sat_count": "Количество спутников",
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
        "last_update": "Последнее обновление"
    }
}

def t(key: str) -> str:
    """دالة الترجمة السريعة"""
    lang = st.session_state.get('language', 'ar')
    return LANGUAGES.get(lang, LANGUAGES['ar']).get(key, key)

# ============================================================
# ⚙️ إعداد الواجهة
# ============================================================
st.set_page_config(page_title="COSMIC-324: 6G Orbital Command", page_icon="🚀", layout="wide")

# CSS مخصص للثيم الداكن
st.markdown("""
<style>
    .main, .stApp { background-color: #0a0a12; }
    .stMetric { background: linear-gradient(145deg, #1a1a2e, #0d0d1a); border-radius: 12px; padding: 15px; border: 1px solid rgba(0, 204, 255, 0.15); }
    h1, h2, h3, h4, h5 { color: #00CCFF; font-family: 'Arial Black', sans-serif; }
    .stButton > button { background: linear-gradient(135deg, #00CCFF, #0066AA); color: white; border: none; border-radius: 8px; padding: 0.5rem 1rem; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# 🌐 الشريط الجانبي (اللغات والإعدادات)
# ============================================================
with st.sidebar:
    st.markdown("---")
    
    # اختيار اللغة
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
    
    # عدد الأقمار
    num_satellites = st.slider(t("sat_count"), 5, 100, 20, 5)
    
    # زر التحديث
    if st.button(t("update_btn"), use_container_width=True):
        st.rerun()
    
    st.caption(f"{t('last_update')}: {datetime.now().strftime('%H:%M:%S')}")

# ============================================================
# 🎯 العنوان الرئيسي
# ============================================================
st.markdown(f"<h1 style='text-align: center; font-size: 3.5em; text-shadow: 0 0 40px #00CCFF;'>{t('title')}</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #88AACC; font-size: 1.2em;'>{t('subtitle')}</p>", unsafe_allow_html=True)

# ============================================================
# 📊 توليد البيانات
# ============================================================
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
