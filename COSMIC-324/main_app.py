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
# 🌍 نظام الترجمة (7 لغات كاملة)
# ============================================================
LANGUAGES = {
    "ar": {
        "name": "العربية",
        "title": "🚀 كوزميك-324: القيادة المدارية 6G Titan X",
        "subtitle": "منصة المحاكاة الفضائية السيادية - الأداء الفائق والتحميل الذكي",
        "welcome": "🌟 مرحباً بك في منصة كوزميك-324، منصة المحاكاة الفضائية المتكاملة.",
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
        "welcome": "🌟 Welcome to COSMIC-324, an integrated space simulation platform.",
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
    },
    "fr": {
        "name": "Français",
        "title": "🚀 COSMIC-324: Commandement Orbital 6G Titan X",
        "subtitle": "Plateforme de simulation spatiale souveraine",
        "welcome": "🌟 Bienvenue sur COSMIC-324, la plateforme de simulation spatiale intégrée.",
        "params": "⚙️ Paramètres de simulation",
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
        "avg_alt": "Altitude moyenne",
        "max_alt": "Altitude max",
        "min_alt": "Altitude min",
        "celestrak": "📡 Données en direct de Celestrak",
        "group": "Groupe",
        "alert_latency": "⚠️ Alerte : Latence élevée!",
        "alert_satellites": "⚠️ Alerte : Peu de satellites actifs!",
        "alert_threshold": "Seuil d'alerte (ms)",
        "active_threshold": "Min. satellites actifs",
        "3d_globe": "🌍 Globe 3D de la constellation",
        "pricing": "💰 Plans tarifaires",
        "coverage": "📡 Carte de couverture",
        "spectrum": "📶 Analyseur de spectre 6G",
        "j2_effect": "🌀 Effet J2 (Aplatissement terrestre)",
        "propulsion": "🚀 Moteur de propulsion",
        "link_analysis": "📡 Analyse de liaison",
        "cost_analysis": "💰 Analyse des coûts",
        "space_weather": "☀️ Météo spatiale",
        "debris": "🛸 Débris et collision",
        "ai_optimization": "🧠 Optimisation IA",
        "digital_twin": "🌍 Jumeau numérique",
        "collaboration": "🤝 Partage de mission",
        "auto_refresh": "⏱️ Actualisation auto",
        "refresh_interval": "Intervalle (sec)",
        "start_auto": "▶️ Démarrer",
        "stop_auto": "⏹️ Arrêter",
        "performance_mode": "⚡ Mode performance",
        "full_resolution": "Résolution complète (5000)",
        "high_speed": "Haute vitesse (100)",
        "mobile_mode": "📱 Mode mobile (Vue simplifiée)"
    },
    "de": {
        "name": "Deutsch",
        "title": "🚀 COSMIC-324: 6G Titan X Orbitalkommando",
        "subtitle": "Souveräne Weltraumsimulationsplattform",
        "welcome": "🌟 Willkommen bei COSMIC-324, der integrierten Weltraumsimulationsplattform.",
        "params": "⚙️ Simulationsparameter",
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
        "avg_alt": "Durchschnittliche Höhe",
        "max_alt": "Maximale Höhe",
        "min_alt": "Minimale Höhe",
        "celestrak": "📡 Live-Daten von Celestrak",
        "group": "Gruppe",
        "alert_latency": "⚠️ Warnung: Hohe Latenz!",
        "alert_satellites": "⚠️ Warnung: Wenig aktive Satelliten!",
        "alert_threshold": "Warngrenze (ms)",
        "active_threshold": "Min. aktive Satelliten",
        "3d_globe": "🌍 3D-Konstellationsglobus",
        "pricing": "💰 Preispläne",
        "coverage": "📡 Abdeckungskarte",
        "spectrum": "📶 6G-Spektrumanalysator",
        "j2_effect": "🌀 J2-Effekt (Abplattung)",
        "propulsion": "🚀 Antriebsmotor",
        "link_analysis": "📡 Verbindungsanalyse",
        "cost_analysis": "💰 Kostenanalyse",
        "space_weather": "☀️ Weltraumwetter",
        "debris": "🛸 Trümmer und Kollision",
        "ai_optimization": "🧠 KI-Optimierung",
        "digital_twin": "🌍 Digitaler Zwilling",
        "collaboration": "🤝 Missionsfreigabe",
        "auto_refresh": "⏱️ Automatische Aktualisierung",
        "refresh_interval": "Intervall (sec)",
        "start_auto": "▶️ Starten",
        "stop_auto": "⏹️ Stoppen",
        "performance_mode": "⚡ Leistungsmodus",
        "full_resolution": "Volle Auflösung (5000)",
        "high_speed": "Hohe Geschwindigkeit (100)",
        "mobile_mode": "📱 Mobilmodus (Vereinfachte Ansicht)"
    },
    "es": {
        "name": "Español",
        "title": "🚀 COSMIC-324: Comando Orbital 6G Titan X",
        "subtitle": "Plataforma de simulación espacial soberana",
        "welcome": "🌟 Bienvenido a COSMIC-324, la plataforma de simulación espacial integrada.",
        "params": "⚙️ Parámetros de simulación",
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
        "avg_alt": "Altitud media",
        "max_alt": "Altitud máxima",
        "min_alt": "Altitud mínima",
        "celestrak": "📡 Datos en vivo de Celestrak",
        "group": "Grupo",
        "alert_latency": "⚠️ Alerta: ¡Latencia alta!",
        "alert_satellites": "⚠️ Alerta: ¡Pocos satélites activos!",
        "alert_threshold": "Umbral de alerta (ms)",
        "active_threshold": "Mín. satélites activos",
        "3d_globe": "🌍 Globo 3D de la constelación",
        "pricing": "💰 Planes de precios",
        "coverage": "📡 Mapa de cobertura",
        "spectrum": "📶 Analizador de espectro 6G",
        "j2_effect": "🌀 Efecto J2 (Achatamiento terrestre)",
        "propulsion": "🚀 Motor de propulsión",
        "link_analysis": "📡 Análisis de enlace",
        "cost_analysis": "💰 Análisis de costos",
        "space_weather": "☀️ Clima espacial",
        "debris": "🛸 Escombros y colisión",
        "ai_optimization": "🧠 Optimización por IA",
        "digital_twin": "🌍 Gemelo digital",
        "collaboration": "🤝 Compartir misión",
        "auto_refresh": "⏱️ Actualización automática",
        "refresh_interval": "Intervalo (seg)",
        "start_auto": "▶️ Iniciar",
        "stop_auto": "⏹️ Detener",
        "performance_mode": "⚡ Modo rendimiento",
        "full_resolution": "Resolución completa (5000)",
        "high_speed": "Alta velocidad (100)",
        "mobile_mode": "📱 Modo móvil (Vista simplificada)"
    },
    "zh": {
        "name": "中文",
        "title": "🚀 COSMIC-324: 6G 泰坦 X 轨道指挥系统",
        "subtitle": "自主空间仿真平台 - 高性能与智能加载",
        "welcome": "🌟 欢迎来到 COSMIC-324，一个集成的空间仿真平台。",
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
        "avg_alt": "平均高度",
        "max_alt": "最大高度",
        "min_alt": "最小高度",
        "celestrak": "📡 从Celestrak获取实时数据",
        "group": "选择星群",
        "alert_latency": "⚠️ 警报：高延迟！",
        "alert_satellites": "⚠️ 警报：活跃卫星数量低！",
        "alert_threshold": "警报阈值（毫秒）",
        "active_threshold": "最低活跃卫星数",
        "3d_globe": "🌍 3D星座球体",
        "pricing": "💰 定价计划",
        "coverage": "📡 覆盖地图",
        "spectrum": "📶 6G频谱分析仪",
        "j2_effect": "🌀 J2效应（地球扁率）",
        "propulsion": "🚀 推进引擎",
        "link_analysis": "📡 链路分析",
        "cost_analysis": "💰 成本分析",
        "space_weather": "☀️ 太空天气",
        "debris": "🛸 碎片与碰撞",
        "ai_optimization": "🧠 AI优化",
        "digital_twin": "🌍 数字孪生",
        "collaboration": "🤝 任务共享",
        "auto_refresh": "⏱️ 自动刷新",
        "refresh_interval": "间隔（秒）",
        "start_auto": "▶️ 开始",
        "stop_auto": "⏹️ 停止",
        "performance_mode": "⚡ 性能模式",
        "full_resolution": "全分辨率（5000）",
        "high_speed": "高速（100）",
        "mobile_mode": "📱 移动模式（简化视图）"
    },
    "ru": {
        "name": "Русский",
        "title": "🚀 COSMIC-324: 6G Titan X Орбитальное командование",
        "subtitle": "Суверенная платформа космического моделирования",
        "welcome": "🌟 Добро пожаловать в COSMIC-324, интегрированную платформу космического моделирования.",
        "params": "⚙️ Параметры моделирования",
        "sat_count": "Количество спутников (до 5000)",
        "update_btn": "🔄 Обновить данные",
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
        "avg_alt": "Средняя высота",
        "max_alt": "Макс. высота",
        "min_alt": "Мин. высота",
        "celestrak": "📡 Получение данных из Celestrak",
        "group": "Группа",
        "alert_latency": "⚠️ Предупреждение: Высокая задержка!",
        "alert_satellites": "⚠️ Предупреждение: Мало активных спутников!",
        "alert_threshold": "Порог предупреждения (мс)",
        "active_threshold": "Мин. активных спутников",
        "3d_globe": "🌍 3D-глобус созвездия",
        "pricing": "💰 Планы подписки",
        "coverage": "📡 Карта покрытия",
        "spectrum": "📶 6G Анализатор спектра",
        "j2_effect": "🌀 Эффект J2 (Сжатие Земли)",
        "propulsion": "🚀 Двигательная установка",
        "link_analysis": "📡 Анализ канала",
        "cost_analysis": "💰 Анализ затрат",
        "space_weather": "☀️ Космическая погода",
        "debris": "🛸 Мусор и столкновения",
        "ai_optimization": "🧠 Оптимизация ИИ",
        "digital_twin": "🌍 Цифровой двойник",
        "collaboration": "🤝 Обмен миссией",
        "auto_refresh": "⏱️ Автообновление",
        "refresh_interval": "Интервал (сек)",
        "start_auto": "▶️ Запустить",
        "stop_auto": "⏹️ Остановить",
        "performance_mode": "⚡ Режим производительности",
        "full_resolution": "Полное разрешение (5000)",
        "high_speed": "Высокая скорость (100)",
        "mobile_mode": "📱 Мобильный режим (Упрощенный вид)"
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
    .pricing-card { 
        background: #1a1a2e; 
        border-radius: 10px; 
        padding: 20px 15px; 
        border: 1px solid #00CCFF33; 
        text-align: center; 
        transition: transform 0.3s ease;
        height: 100%;
    }
    .pricing-card:hover {
        transform: scale(1.02);
        border-color: #00CCFF;
    }
    .pricing-card h4 { color: #00CCFF; margin-bottom: 10px; }
    .pricing-card h2 { color: #FFFFFF; margin: 10px 0; }
    .pricing-card p { color: #88AACC; font-size: 14px; }
    .pricing-card .price-highlight { color: #00CCFF; font-size: 1.5em; font-weight: bold; }
    .stProgress > div { background-color: #00CCFF !important; }
    .welcome-box {
        background: linear-gradient(135deg, #1a1a2e, #0d0d1a);
        border-radius: 12px;
        padding: 20px 25px;
        border: 1px solid #00CCFF33;
        margin-bottom: 20px;
    }
    .welcome-box h2 { color: #00CCFF; margin: 0 0 10px 0; }
    .welcome-box p { color: #88AACC; margin: 0; font-size: 1.05em; }
    .copyright {
        text-align: center;
        color: #445566;
        font-size: 0.8em;
        padding: 20px 0;
        border-top: 1px solid #1a1a2e;
        margin-top: 20px;
    }
    @media (max-width: 640px) {
        .stMetric { padding: 10px; margin: 5px 0; }
        .stDataFrame { font-size: 12px; }
        .stTabs [data-baseweb="tab-list"] { gap: 4px; }
        .stTabs [data-baseweb="tab"] { padding: 6px 10px; font-size: 12px; }
        .pricing-card { padding: 15px 10px; }
        .pricing-card h2 { font-size: 1.5em; }
        .welcome-box { padding: 15px; }
        .welcome-box h2 { font-size: 1.2em; }
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
    selected_lang = st.selectbox("🌐 Language / اللغة", options=list(lang_options.keys()), format_func=lambda x: lang_options[x],
                                 index=list(lang_options.keys()).index(st.session_state.get('language', 'ar')))
    if selected_lang != st.session_state.get('language', 'ar'):
        st.session_state.language = selected_lang
        st.rerun()
    
    st.markdown("---")
    st.header(t("params"))
    
    mobile_mode = st.checkbox(t("mobile_mode"), value=False)

# ============================================================
# 🖥️ المحتوى الرئيسي للتطبيق
# ============================================================
st.markdown(f'<div class="welcome-box"><h2>{t("title")}</h2><p>{t("welcome")}</p></div>', unsafe_allow_html=True)

# إعدادات عامة
col1, col2 = st.columns(2)
with col1:
    num_sats = st.slider(t("sat_count"), min_value=100, max_value=5000, value=500, step=100)
with col2:
    group_choice = st.selectbox(t("group"), options=["starlink", "oneweb", "gps", "glo-operational"], index=0)

if st.button(t("update_btn")):
    st.cache_data.clear()
    st.success("تم تحديث البيانات بنجاح!")

# توليد البيانات أو جلبها
orbit_data = generate_orbit_map(num_satellites=num_sats, group=group_choice, use_celestrak=True)

# محاكاة إحصائيات سريعة
active_count = int(len(orbit_data) * 0.95)
calib_count = len(orbit_data) - active_count

m1, m2, m3 = st.columns(3)
m1.metric(t("total"), len(orbit_data))
m2.metric(t("active"), active_count)
m3.metric(t("calibration"), calib_count)

# جدول عينة من الأقمار
st.subheader("📡 حالة الأقمار المدارية الحية")
df_data = []
for name, sat in list(orbit_data.items())[:15]:
    lat = random.uniform(-60, 60)
    lon = random.uniform(-180, 180)
    alt = round(getattr(sat, 'altitude', 550), 2)
    df_data.append({
        t("satellite"): name,
        t("status"): t("active"),
        t("latitude"): round(lat, 2),
        t("longitude"): round(lon, 2),
        t("altitude"): alt
    })

df_satellites = pd.DataFrame(df_data)
st.dataframe(df_satellites, use_container_width=True)

# رسم بياني لزمن الانتقال
st.subheader(t("latency_chart"))
chart_data = pd.DataFrame({
    t("step"): range(1, 11),
    t("latency_ms"): [random.randint(12, 25) for _ in range(10)]
})
st.line_chart(chart_data, x=t("step"), y=t("latency_ms"), use_container_width=True)

st.markdown(f'<div class="copyright">COSMIC-324 6G Titan X - Sovereign Orbital Simulation Platform © 2026</div>', unsafe_allow_html=True)
