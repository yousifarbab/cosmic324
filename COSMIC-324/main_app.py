import streamlit as st
import pandas as pd
import plotly.express as px
import random
import math
from datetime import datetime

# ============================================================
# ⚙️ إعداد واجهة المستخدم
# ============================================================
st.set_page_config(page_title="COSMIC-324: 6G Orbital Command", page_icon="🚀", layout="wide")

st.markdown("<h1 style='text-align: center; color: #00CCFF;'>🚀 كوزميك-324: القيادة المدارية 6G</h1>", unsafe_allow_html=True)

with st.sidebar:
    st.header("⚙️ إعدادات المحاكاة")
    max_sats = st.slider("الحد الأقصى للأقمار", 10, 500, 100, 10)
    steps = st.number_input("الخطوات الزمنية", 5, 100, 20, 1)
    base_lat = st.number_input("زمن الانتقال الأساسي (م.ث)", 0.5, 15.0, 3.7, 0.1)
    growth = st.slider("معدل النمو", 0.0, 0.3, 0.05, 0.01)
    
    run_btn = st.button("🚀 تنفيذ مهمة 6G", type="primary")

if run_btn:
    with st.spinner("🔄 جاري تنفيذ المحاكاة..."):
        # توليد بيانات محلية 100% لتجنب أي مشاكل انقطاع اتصال بالإنترنت
        lat_data = [{"Step": i, "Latency (ms)": round(base_lat + (growth * i) + random.uniform(0, 0.2), 2)} for i in range(steps)]
        latency_df = pd.DataFrame(lat_data)
        
        topology_df = pd.DataFrame({
            "Node": [f"SAT-LEO-{i+1}" for i in range(min(5, max_sats))],
            "Status": ["Active", "Active", "Degraded", "Active", "Active"][:min(5, max_sats)],
            "Load (kg)": [round(50 + random.uniform(-5, 5), 1) for _ in range(min(5, max_sats))]
        })
        
        current_avg = latency_df['Latency (ms)'].mean()
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("أدنى زمن انتقال", f"{latency_df['Latency (ms)'].min():.2f} ms")
        col2.metric("أقصى زمن انتقال", f"{latency_df['Latency (ms)'].max():.2f} ms")
        col3.metric("متوسط زمن الانتقال", f"{current_avg:.2f} ms")
        col4.metric("الانحراف المعياري", f"{latency_df['Latency (ms)'].std():.2f} ms")
        
        st.markdown("---")
        col_left, col_right = st.columns([2, 1])
        with col_left:
            st.subheader("📈 تطور زمن الانتقال")
            fig = px.line(latency_df, x="Step", y="Latency (ms)", markers=True)
            st.plotly_chart(fig, use_container_width=True)
        
        with col_right:
            st.subheader("🛰️ معاينة الطوبولوجيا")
            st.dataframe(topology_df, use_container_width=True)
        
        st.success(f"✅ {datetime.now().strftime('%H:%M:%S')} - اكتملت المحاكاة بنجاح.")
else:
    st.info("🛰️ النظام في وضع الاستعداد. اضغط على زر التنفيذ في القائمة الجانبية لبدء المحاكاة.")
    preview = pd.DataFrame({
        "Node": ["T-LEO Alpha", "T-LEO Beta", "Ground Station"],
        "Status": ["🟢 Standby", "🟢 Standby", "🟢 Standby"],
        "Load (kg)": [45, 60, 55]
    })
    st.dataframe(preview, use_container_width=True)