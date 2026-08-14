import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random
import time
import json
from datetime import datetime, timedelta
import hashlib
import numpy as np

# ============================================================
# 🌍 نظام الترجمة (ثنائي اللغة مع RTL/LTR) - متوافق مع COSMIC-324
# ============================================================
LANGUAGES = {
    "ar": {
        "name": "العربية",
        "dir": "rtl",
        "title": "🚀 كوزميك-324: البوابة السيادية",
        "subtitle": "منصة القيادة المدارية وإدارة التراخيص والشبكات",
        "dashboard": "📊 لوحة القيادة",
        "satellite_map": "🗺️ الخريطة والمدارات",
        "licenses": "🔑 إدارة التراخيص",
        "clients": "👥 العملاء والبوابات",
        "health": "🩺 صحة النظام والشبكة",
        "settings": "⚙️ الإعدادات المتقدمة",
        "total_sats": "إجمالي الأقمار الصناعية",
        "active_licenses": "التراخيص النشطة",
        "pending_requests": "طلبات الشبكة المعلقة",
        "system_status": "حالة النظام",
        "operational": "🟢 تشغيلي بالكامل",
        "degraded": "🟡 أداء متدهور",
        "offline": "🔴 غير متصل",
        "license_key": "مفتاح الترخيص السيادي",
        "client_name": "اسم الجهة / العميل",
        "expiry_date": "تاريخ انتهاء الصلاحية",
        "status": "حالة الترخيص",
        "active": "نشط",
        "expired": "منتهي",
        "revoked": "ملغي",
        "generate": "توليد ترخيص جديد",
        "revoke": "إلغاء الترخيص",
        "renew": "تجديد فوري",
        "paypal_checkout": "🛒 بوابة دفع PayPal المباشرة",
        "simulate_payment": "محاكاة المعاملة المالية",
        "health_check": "فحص التشخيص الشامل",
        "last_updated": "آخر مزامنة للبيانات",
        "server_load": "حمل وحدة المعالجة المركزية",
        "response_time": "زمن استجابة البوابة (ms)",
        "uptime": "وقت التشغيل المتواصل",
        "english": "English",
        "arabic": "العربية"
    },
    "en": {
        "name": "English",
        "dir": "ltr",
        "title": "🚀 COSMIC-324: Sovereign Portal",
        "subtitle": "Orbital Command, License & Grid Management",
        "dashboard": "📊 Dashboard",
        "satellite_map": "🗺️ Satellites & Map",
        "licenses": "🔑 License Management",
        "clients": "👥 Clients & Portals",
        "health": "🩺 System & Grid Health",
        "settings": "⚙️ Advanced Settings",
        "total_sats": "Total Satellites",
        "active_licenses": "Active Licenses",
        "pending_requests": "Pending Requests",
        "system_status": "System Status",
        "operational": "🟢 Fully Operational",
        "degraded": "🟡 Degraded Performance",
        "offline": "🔴 Offline",
        "license_key": "Sovereign License Key",
        "client_name": "Client / Entity Name",
        "expiry_date": "Expiry Date",
        "status": "Status",
        "active": "Active",
        "expired": "Expired",
        "revoked": "Revoked",
        "generate": "Generate License",
        "revoke": "Revoke License",
        "renew": "Renew",
        "paypal_checkout": "🛒 PayPal Direct Checkout",
        "simulate_payment": "Simulate Payment",
        "health_check": "Comprehensive Health Check",
        "last_updated": "Last Data Sync",
        "server_load": "Server CPU Load",
        "response_time": "Response Time (ms)",
        "uptime": "Continuous Uptime",
        "english": "English",
        "arabic": "العربية"
    }
}

def t(key: str) -> str:
    lang = st.session_state.get('language', 'ar')
    return LANGUAGES.get(lang, LANGUAGES['ar']).get(key, key)

def get_dir() -> str:
    lang = st.session_state.get('language', 'ar')
    return LANGUAGES.get(lang, LANGUAGES['ar']).get('dir', 'rtl')

# ============================================================
# 🎨 تنسيقات الواجهة الاحترافية (CSS متقدم)
# ============================================================
current_dir = get_dir()
st.set_page_config(
    page_title="COSMIC-324 Sovereign Portal",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(f"""
<style>
    .main, .stApp {{
        background-color: #080810;
        direction: {current_dir};
        text-align: {'right' if current_dir == 'rtl' else 'left'};
    }}
    .stMetric {{
        background: linear-gradient(145deg, #15152b, #0a0a16);
        border-radius: 14px;
        padding: 18px;
        border: 1px solid rgba(0, 204, 255, 0.2);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
    }}
    h1, h2, h3, h4, h5 {{
        color: #00CCFF;
        font-family: 'Segoe UI', Tahoma, sans-serif;
        text-shadow: 0 0 12px rgba(0, 204, 255, 0.35);
    }}
    .stButton > button {{
        background: linear-gradient(135deg, #00CCFF, #005599);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        font-weight: bold;
        width: 100%;
        transition: all 0.3s ease;
    }}
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 0 25px rgba(0, 204, 255, 0.5);
    }}
    .license-card {{
        background: linear-gradient(145deg, #121222, #070710);
        border: 1px solid #00CCFF44;
        border-radius: 12px;
        padding: 18px;
        margin: 12px 0;
    }}
    .welcome-box {{
        background: linear-gradient(135deg, #161630, #090914);
        border-radius: 15px;
        padding: 25px;
        border: 1px solid #00CCFF44;
        margin-bottom: 25px;
        box-shadow: inset 0 0 15px rgba(0,204,255,0.1);
    }}
    .copyright {{
        text-align: center;
        color: #556677;
        font-size: 0.85em;
        padding: 20px 0;
        border-top: 1px solid #15152b;
        margin-top: 30px;
    }}
</style>
""", unsafe_allow_html=True)

# ============================================================
# 📊 محاكاة قاعدة البيانات والخدمات السيادية (COSMIC-324 Backend)
# ============================================================
def generate_mock_licenses():
    clients = ["SpaceX Orbital", "NASA Deep Space", "ESA Agency", "Blue Origin Grid", "Rocket Lab", "OneWeb Network"]
    statuses = ["active", "active", "active", "expired", "active", "revoked"]
    tiers = ["Basic Node", "Pro Sovereign", "Titan X Grid"]
    licenses = []
    for i in range(12):
        client = random.choice(clients)
        licenses.append({
            "id": f"COS-LIC-{i+101:04d}",
            "client": client,
            "email": f"admin@{client.lower().replace(' ', '')}.space",
            "key": f"CS324-{hashlib.md5(f'{client}{i}'.encode()).hexdigest()[:12].upper()}",
            "status": random.choice(statuses),
            "created": datetime.now() - timedelta(days=random.randint(5, 300)),
            "expiry": datetime.now() + timedelta(days=random.randint(15, 600)),
            "tier": random.choice(tiers)
        })
    return licenses

def generate_system_health():
    return {
        "status": "operational",
        "load": round(random.uniform(25.5, 78.2), 1),
        "response_time": round(random.uniform(35.0, 180.5), 1),
        "uptime": f"{random.randint(45, 180)}d {random.randint(1, 23)}h",
        "last_check": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "satellites_count": 3240 + random.randint(10, 150)
    }

# ============================================================
# 🌐 الشريط الجانبي الموحد (Navigation & Localization)
# ============================================================
with st.sidebar:
    st.markdown("### 🚀 COSMIC-324 Portal")
    st.caption("Sovereign Command & Control v2.0")
    st.markdown("---")
    
    lang_options = {"ar": "العربية", "en": "English"}
    current_lang = st.session_state.get('language', 'ar')
    selected_lang = st.selectbox(
        "🌐 Language / اللغة",
        options=list(lang_options.keys()),
        format_func=lambda x: lang_options[x],
        index=list(lang_options.keys()).index(current_lang)
    )
    if selected_lang != current_lang:
        st.session_state.language = selected_lang
        st.rerun()
    
    st.markdown("---")
    
    pages = ["dashboard", "satellite_map", "licenses", "clients", "health", "settings"]
    page_icons = ["📊", "🗺️", "🔑", "👥", "🩺", "⚙️"]
    page_names = [t(page) for page in pages]
    
    selected_page_idx = st.radio(
        "Navigation Menu",
        options=range(len(pages)),
        format_func=lambda i: f"{page_icons[i]} {page_names[i]}",
        key="nav_main"
    )
    current_page = pages[selected_page_idx]
    
    st.markdown("---")
    st.caption(f"🛡️ {t('system_status')}: **{t('operational')}**")
    st.caption(f"© 2026 Yousif Zakaria Eissa Arbarb")

# ============================================================
# 📊 لوحة القيادة الرئيسية (Dashboard)
# ============================================================
if current_page == "dashboard":
    st.markdown(f"<h1 style='text-align: center;'>{t('dashboard')}</h1>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class='welcome-box'>
        <h2>🌟 {t('title')}</h2>
        <p>{t('subtitle')}</p>
        <hr style='border-color: rgba(0,204,255,0.2); margin: 15px 0;'>
        <p><strong>معرف العقدة النشطة:</strong> NODE-324-SECURE-AUTH | <strong>بروتوكول الاتصال:</strong> QPSK / AWGN Secured</p>
    </div>
    """, unsafe_allow_html=True)
    
    health = generate_system_health()
    licenses = generate_mock_licenses()
    active_licenses = sum(1 for l in licenses if l['status'] == 'active')
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric(t('total_sats'), f"{health['satellites_count']:,}")
    col2.metric(t('active_licenses'), active_licenses)
    col3.metric(t('pending_requests'), random.randint(2, 12))
    col4.metric(t('system_status'), "99.98%", delta="Optimal")
    
    st.markdown("---")
    st.subheader("📊 تحليل توزيع التراخيص والباقات السيادية")
    
    tier_counts = pd.DataFrame(licenses)['tier'].value_counts().reset_index()
    tier_counts.columns = ['Tier', 'Count']
    
    fig = px.bar(
        tier_counts, x='Tier', y='Count',
        color='Tier',
        color_discrete_sequence=['#00CCFF', '#0077FF', '#00FF88'],
        text='Count'
    )
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        xaxis_title="الباقة السيادية",
        yaxis_title="عدد التراخيص الفعالة"
    )
    st.plotly_chart(fig, use_container_width=True)

# ============================================================
# 🛰️ قسم الخرائط والمدارات والأقمار الصناعية (Satellite Map)
# ============================================================
elif current_page == "satellite_map":
    st.markdown(f"<h1 style='text-align: center;'>{t('satellite_map')}</h1>", unsafe_allow_html=True)
    st.info("🌐 يعرض هذا القسم التوزيع الجغرافي والإحداثيات المدارية اللحظية لشبكة الأقمار الصناعية التابعة للمنصة[cite: 2].")
    
    np.random.seed(42)
    sats_data = pd.DataFrame({
        'Satellite_ID': [f"COS-SAT-{i:03d}" for i in range(1, 26)],
        'Latitude': np.random.uniform(-60, 60, 25),
        'Longitude': np.random.uniform(-180, 180, 25),
        'Altitude_km': np.random.uniform(400, 1200, 25),
        'Signal_Strength_dB': np.random.uniform(-85.0, -45.0, 25),
        'Status': np.random.choice(['Active', 'Syncing', 'Optimal'], 25)
    })
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("🗺️ خريطة الموقع الجغرافي والمداري المباشر")
        st.map(sats_data, latitude='Latitude', longitude='Longitude', size=20, color='#00CCFF')
        
    with col2:
        st.subheader("📊 إحصائيات المدارات النشطة")
        st.metric("متوسط الارتفاع المداري", "780 كم", delta="مستقر")
        st.metric("قوة الإشارة العامة", "-62.4 dBm", delta="ممتاز")
        st.metric("العقد المدارية المتصلة", "25 / 25")
        
    st.markdown("---")
    st.subheader("📋 جدول البيانات المدارية الحية للأقمار")
    st.dataframe(sats_data, use_container_width=True, column_config={
        'Satellite_ID': 'معرف القمر الصناعي',
        'Latitude': 'خط العرض',
        'Longitude': 'خط الطول',
        'Altitude_km': 'الارتفاع (كم)',
        'Signal_Strength_dB': 'قوة الإشارة (dB)',
        'Status': 'حالة الاتصال'
    })

# ============================================================
# 🔑 إدارة التراخيص (Licenses Management)
# ============================================================
elif current_page == "licenses":
    st.markdown(f"<h1 style='text-align: center;'>{t('licenses')}</h1>", unsafe_allow_html=True)
    
    licenses = generate_mock_licenses()
    
    with st.expander("🆕 توليد ترخيص سيادي جديد (New Sovereign License)", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            new_client = st.text_input(t('client_name'), "SpaceX Advanced Systems")
            new_email = st.text_input("البريد الإلكتروني للإشعار", "operations@spacex.space")
        with col2:
            new_tier = st.selectbox("اختر الباقة", ["Basic Node", "Pro Sovereign", "Titan X Grid"])
            new_days = st.number_input("مدة الصلاحية (بالأيام)", min_value=30, max_value=730, value=365)
        
        if st.button("🚀 إصدار وتوليد المفتاح الموثق"):
            generated_key = f"CS324-{hashlib.md5(f'{new_client}{time.time()}'.encode()).hexdigest()[:12].upper()}"
            st.success("✅ تم إصدار المفتاح السيادي بنجاح وترحيله إلى شبكة الكوزميك!")
            st.code(f"🔑 المفتاح: {generated_key}")
            st.info(f"📧 تم إرسال بيانات الاعتماد المشفرة إلى البريد: {new_email}")

    st.markdown("---")
    st.subheader("📋 السجلات النشطة للتراخيص الموثقة")
    
    df_licenses = pd.DataFrame(licenses)
    df_licenses['expiry'] = pd.to_datetime(df_licenses['expiry']).dt.strftime('%Y-%m-%d')
    df_licenses['created'] = pd.to_datetime(df_licenses['created']).dt.strftime('%Y-%m-%d')
    
    st.dataframe(
        df_licenses[['id', 'client', 'key', 'tier', 'status', 'expiry']],
        use_container_width=True,
        column_config={
            'id': 'معرف الترخيص',
            'client': t('client_name'),
            'key': 'مفتاح النظام',
            'tier': 'الباقة',
            'status': t('status'),
            'expiry': t('expiry_date')
        }
    )

# ============================================================
# 👥 العملاء والبوابات (Clients Portal)
# ============================================================
elif current_page == "clients":
    st.markdown(f"<h1 style='text-align: center;'>{t('clients')}</h1>", unsafe_allow_html=True)
    
    st.subheader("🔐 بوابة مصادقة العملاء (Client Sovereign Login)")
    col1, col2 = st.columns(2)
    with col1:
        client_mail = st.text_input("البريد الإلكتروني للعميل", "operations@spacex.space")
        client_pass = st.text_input("كلمة المرور المشفرة", type="password")
    with col2:
        st.info("""
        **💡 إرشادات الوصول التجريبي للمنصة:**
        - استخدم البريد الافتراضي أعلاه.
        - النظام يدعم المصادقة المزدوجة ومراقبة النطاق المداري للعملاء.
        """)
    
    if st.button("🔓 الدخول إلى لوحة العميل المخصصة"):
        st.session_state['client_authenticated'] = True
        st.success("✅ تم التحقق من الهوية السيادية بنجاح!")
        
    if st.session_state.get('client_authenticated', False):
        st.markdown("---")
        st.subheader("🛰️ تراخيص العميل والخدمات المتاحة")
        st.markdown("""
        <div class='license-card'>
            <h4>🔑 مفتاح العقدة المدارية: CS324-A8F9B2C10E44</h4>
            <p><strong>الباقة:</strong> Titan X Grid | <strong>الحالة:</strong> <span style='color: #00FF88;'>نشط (Active)</span></p>
            <p><strong>تاريخ الانتهاء:</strong> 2027-08-14 | <strong>استهلاك النطاق الترددي:</strong> 84.2%</p>
        </div>
        """, unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🛒 تجديد الترخيص عبر PayPal (مباشر)"):
                st.info("🔄 جاري التوجيه الآمن إلى منصة PayPal لإنهاء معاملة الدفع...")
        with c2:
            if st.button("📥 تحميل تقرير أداء النطاق الترددي"):
                st.download_button(
                    label="📄 تحميل التقرير (CSV)",
                    data="Client,Node,Bandwidth,Status\nSpaceX,Node-01,84.2%,Active",
                    file_name="cosmic324_client_report.csv",
                    mime="text/csv"
                )

# ============================================================
# 🩺 صحة النظام والشبكة (System Health)
# ============================================================
elif current_page == "health":
    st.markdown(f"<h1 style='text-align: center;'>{t('health')}</h1>", unsafe_allow_html=True)
    
    if st.button("🔄 إجراء تشخيص فوري لخوادم الشبكة"):
        st.rerun()
        
    health = generate_system_health()
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric(t('server_load'), f"{health['load']}%", delta="-2.1%")
    col2.metric(t('response_time'), f"{health['response_time']} ms", delta="-8.4ms")
    col3.metric(t('uptime'), health['uptime'], delta="Stable")
    col4.metric(t('total_sats'), f"{health['satellites_count']:,}", delta="+12")

    st.markdown("---")
    st.subheader("📈 تتبع استقرار النطاق والأداء المداري (24 ساعة)")
    
    hours = list(range(24))
    load_vals = [random.randint(30, 75) for _ in range(24)]
    resp_vals = [random.randint(40, 150) for _ in range(24)]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=hours, y=load_vals, mode='lines+markers', name='حمل الخادم (%)', line=dict(color='#00CCFF', width=3)))
    fig.add_trace(go.Scatter(x=hours, y=resp_vals, mode='lines+markers', name='زمن الاستجابة (ms)', line=dict(color='#FF6B35', width=3)))
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        xaxis_title="الساعات خلال اليوم",
        yaxis_title="مؤشرات الأداء"
    )
    st.plotly_chart(fig, use_container_width=True)

# ============================================================
# ⚙️ الإعدادات المتقدمة (Settings)
# ============================================================
elif current_page == "settings":
    st.markdown(f"<h1 style='text-align: center;'>{t('settings')}</h1>", unsafe_allow_html=True)
    
    with st.expander("💰 إعدادات بوابة الدفع (PayPal Integration)", expanded=True):
        st.text_input("PayPal Client ID", "AQ324_Sovereign_Sandbox_Client_ID_Secure", disabled=True)
        st.text_input("PayPal Secret Key", "••••••••••••••••••••••••••••••••", disabled=True)
        st.selectbox("وضع التشغيل المالي", ["Live Production", "Sandbox Simulation"], index=1)
        st.info("🔒 هذه المفاتيح مشفرة ومحمية ببروتوكول الأمان السيادي لـ COSMIC-324.")
        
    with st.expander("📡 تكوين ربط الأقمار والبيانات الحية (CelesTrak / Space-Track)"):
        st.selectbox("مزود البيانات المدارية المعتمد", ["CelesTrak API Direct", "Space-Track Feed", "Internal Simulation Engine"])
        st.slider("معدل مزامنة البيانات (ثانية)", 10, 300, 60)
        st.checkbox("تفعيل نظام التنبيهات الفورية عند انقطاع الاتصال", value=True)
        
    if st.button("💾 حفظ وتطبيق الإعدادات السيادية"):
        st.success("✅ تم حفظ التغييرات وتحديث العقد المركزية بنجاح!")
        st.balloons()

# ============================================================
# 📌 تذييل الصفحة وحقوق الملكية
# ============================================================
st.markdown("---")
st.markdown("""
<div class='copyright'>
    <p>🛰️ COSMIC-324: Sovereign Portal & Orbital Command v2.0</p>
    <p>© 2026 Yousif Zakaria Eissa Arbarb. جميع الحقوق محفوظة.</p>
    <p style='color: #00CCFF; font-size: 0.9em;'>مرخص رسمياً ومصمم وفق المعايير الاحترافية المتقدمة للشبكات السيادية.</p>
</div>
""", unsafe_allow_html=True)
