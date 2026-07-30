import streamlit as st
import pandas as pd
import numpy as np
import math

# إعداد الصفحة
st.set_page_config(
    page_title="COSMIC-324: 6G Orbital Guidance",
    page_icon="🚀",
    layout="wide"
)

# دالة ترجمة مبسطة للعناصر
def t(key):
    translations = {
        'satellite': 'Satellite',
        'status': 'Status',
        'altitude': 'Altitude',
        'latency': 'Latency'
    }
    return translations.get(key, key)

# محاكاة كلاس المدارات والأقمار (لضمان عمل الكود بسلاسة)
class OrbitSimulator:
    def __init__(self, name):
        self.name = name
    def position_at_time(self, t_future):
        # محاكاة إحداثيات ثلاثية الأبعاد بناءً على الوقت
        return (
            7000.0 + math.sin(t_future / 10000) * 500,
            math.cos(t_future / 10000) * 5000,
            math.sin(t_future / 15000) * 3000
        )

# العنوان الرئيسي
st.markdown("<h1 style='text-align: center;'>🚀 كوزميك-324: القيادة المدارية 6G</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>منصة المحاكاة والتحكم في شبكات الأقمار الصناعية</p>", unsafe_allow_html=True)
st.markdown("---")

# إنشاء بيانات تجريبية للأقمار لضمان عمل الواجهة
@st.cache_data
def load_sample_data():
    data = {
        'Satellite': ['SAT-1', 'SAT-2', 'SAT-3', 'SAT-4', 'SAT-5'],
        'Status': ['نشط', 'نشط', 'Degraded', 'نشط', 'معطل'],
        'Altitude (km)': [486.0, 520.0, 450.0, 600.0, 510.0],
        'Latency (ms)': [12.5, 14.2, 22.0, 11.0, 45.5]
    }
    return pd.DataFrame(data)

df = load_sample_data()

# إنشاء خريطة مدارية افتراضية للأقمار
orbit_map = {sat: OrbitSimulator(sat) for sat in df['Satellite'].tolist()}

# عرض لوحة البيانات المختصرة
st.subheader("📊 حالة الكوكبة الحالية")
col1, col2, col3, col4 = st.columns(4)
col1.metric("إجمالي الأقمار", len(df))
col2.metric("الأقمار النشطة", len(df[df['Status'] == 'نشط']))
col3.metric("متوسط الارتفاع", f"{df['Altitude (km)'].mean():.1f} كم")
col4.metric("متوسط زمن الانتقال", f"{df['Latency (ms)'].mean():.1f} ms")

# ============================================================
# 🗺️ نظام التخطيط المسبق للمهمات (Mission Pre-Planning)
# ============================================================

st.markdown("---")
st.subheader("🗺️ Mission Pre-Planning")

# التحقق من وجود بيانات الأقمار
if not df.empty and len(df) > 0:
    # اختيار قمر المصدر والهدف
    col_mission1, col_mission2 = st.columns(2)
    with col_mission1:
        source_sat = st.selectbox(
            "🚀 Source Satellite",
            options=df['Satellite'].tolist(),
            key="source_sat"
        )
    with col_mission2:
        target_sat = st.selectbox(
            "🎯 Target Satellite",
            options=df['Satellite'].tolist(),
            key="target_sat",
            index=min(1, len(df)-1)
        )
    
    # شريط التمرير الزمني (المستقبل)
    future_hours = st.slider(
        "⏳ Future Time Horizon (hours)",
        min_value=0.0,
        max_value=48.0,
        value=6.0,
        step=0.5,
        help="حدد عدد الساعات القادمة لمحاكاة المهمة"
    )
    
    # زر تنفيذ المحاكاة
    if st.button("🔄 Simulate Mission", type="primary", use_container_width=True):
        with st.spinner("🔄 جاري حساب المسار المستقبلي..."):
            # 1. الحصول على مدارات المصدر والهدف
            source_orbit = orbit_map.get(source_sat)
            target_orbit = orbit_map.get(target_sat)
            
            if source_orbit is None or target_orbit is None:
                st.error("⚠️ لا تتوفر مدارات لأحد الأقمار المحددة.")
            else:
                # 2. حساب المواقع في الزمن المستقبلي
                t_future = future_hours * 3600  # تحويل الساعات إلى ثواني
                pos_source = source_orbit.position_at_time(t_future)
                pos_target = target_orbit.position_at_time(t_future)
                
                # 3. حساب المسافة بين المصدر والهدف في المستقبل
                dx = pos_source[0] - pos_target[0]
                dy = pos_source[1] - pos_target[1]
                dz = pos_source[2] - pos_target[2]
                distance_km = math.sqrt(dx**2 + dy**2 + dz**2)
                
                # 4. تقدير زمن الانتقال (بافتراض سرعة الضوء أو سرعة الارسال)
                speed_of_light = 299792.458  # كم/ث
                estimated_latency_ms = (distance_km / speed_of_light) * 1000  # بالمللي ثانية
                
                # 5. تقييم المخاطر (بناءً على وجود أقمار معطلة أو قريبة جداً)
                risk_level = "Low"
                risk_factors = []
                
                # 5a. التحقق من وجود أقمار معطلة في المسار
                disabled_sats = df[df['Status'].str.contains("معطل|Degraded|Standby")]['Satellite'].tolist()
                if source_sat in disabled_sats or target_sat in disabled_sats:
                    risk_level = "High"
                    risk_factors.append("⚠️ أحد الأقمار المحددة في حالة غير نشطة")
                
                # 5b. التحقق من الازدحام أو المسافة الطويلة
                if distance_km > 10000:
                    risk_factors.append("📏 مسافة طويلة جداً (أكثر من 10000 كم) قد تزيد من زمن الانتقال")
                    if risk_level == "Low":
                        risk_level = "Medium"
                
                # 5c. إضافة عامل المخاطر العام للـ Latency
                if estimated_latency_ms > 50:
                    risk_factors.append("⏱️ زمن انتقال متوقع مرتفع (> 50 مللي ثانية)")
                    if risk_level == "Low":
                        risk_level = "Medium"
                
                # 6. عرض نتائج المحاكاة
                st.success("✅ اكتملت محاكاة المهمة بنجاح")
                
                # عرض النتائج في بطاقات
                col_r1, col_r2, col_r3, col_r4 = st.columns(4)
                col_r1.metric("📡 المسافة", f"{distance_km:.1f} كم")
                col_r2.metric("⏱️ زمن الانتقال المتوقع", f"{estimated_latency_ms:.2f} مللي ثانية")
                col_r3.metric("🕒 الأفق الزمني", f"{future_hours:.1f} ساعة")
                col_r4.metric("⚠️ مستوى المخاطر", risk_level, delta="احتمالية النجاح" if risk_level == "Low" else "انتباه")
                
                # عرض عوامل الخطر (إن وجدت)
                if risk_factors:
                    st.warning("⚠️ عوامل الخطر المحتملة:")
                    for factor in risk_factors:
                        st.caption(f"• {factor}")
                else:
                    st.info("✅ لا توجد عوامل خطر ملحوظة. المسار آمن.")
                
                # عرض مواقع المصدر والهدف في المستقبل
                st.caption(f"📍 موقع {source_sat} في المستقبل: ({pos_source[0]:.1f}, {pos_source[1]:.1f}, {pos_source[2]:.1f}) كم")
                st.caption(f"📍 موقع {target_sat} في المستقبل: ({pos_target[0]:.1f}, {pos_target[1]:.1f}, {pos_target[2]:.1f}) كم")
                
                # حفظ نتائج المحاكاة في الجلسة للتصدير لاحقاً
                st.session_state.mission_result = {
                    "source": source_sat,
                    "target": target_sat,
                    "future_hours": future_hours,
                    "distance_km": distance_km,
                    "estimated_latency_ms": estimated_latency_ms,
                    "risk_level": risk_level,
                    "risk_factors": risk_factors,
                    "pos_source": pos_source,
                    "pos_target": pos_target
                }
    
    # عرض نتيجة المحاكاة السابقة (إذا كانت موجودة)
    if 'mission_result' in st.session_state:
        st.markdown("---")
        st.subheader("📋 آخر نتيجة محاكاة")
        res = st.session_state.mission_result
        st.caption(f"🚀 {res['source']} → 🎯 {res['target']} | الأفق الزمني: {res['future_hours']:.1f} ساعة")
        st.caption(f"📡 المسافة: {res['distance_km']:.1f} كم | ⏱️ زمن الانتقال: {res['estimated_latency_ms']:.2f} مللي ثانية")
        st.caption(f"⚠️ مستوى المخاطر: {res['risk_level']}")
        if res.get('risk_factors'):
            for factor in res['risk_factors']:
                st.caption(f"• {factor}")
else:
    st.info("⚠️ لا توجد بيانات كافية لتخطيط المهمات. تأكد من تحميل بيانات الأقمار.")
