import streamlit as st
import pandas as pd
import random

# إعداد صفحة المنصة
st.set_page_config(page_title="COSMIC-324 6G", layout="wide")

st.markdown("<h1 style='text-align: center; color: #00CCFF;'>🚀 كوزميك-324: القيادة المدارية 6G</h1>", unsafe_allow_html=True)

# الشريط الجانبي للإعدادات
with st.sidebar:
    st.header("⚙️ إعدادات المحاكاة")
    max_sats = st.slider("الحد الأقصى للأقمار", 10, 100, 20)
    steps = st.slider("الخطوات الزمنية", 5, 50, 20)
    run_btn = st.button("🚀 تنفيذ المهمة", type="primary")

# توليد البيانات المدارية
data = []
for i in range(max_sats):
    data.append({
        "القمر": f"SAT-{i+1}",
        "الحالة": random.choice(["🟢 نشط", "🟡 معايرة", "🔴 استعداد"]),
        "خط العرض": round(random.uniform(-90, 90), 4),
        "خط الطول": round(random.uniform(-180, 180), 4),
        "الارتفاع (كم)": round(random.uniform(400, 1200), 2)
    })
df = pd.DataFrame(data)

# دالة لتلوين الصفوف حسب الحالة
def highlight_status(row):
    if row['الحالة'] == '🟢 نشط':
        return ['background-color: #1a3a1a; color: #00FF00'] * len(row)
    elif row['الحالة'] == '🟡 معايرة':
        return ['background-color: #3a3a1a; color: #FFAA00'] * len(row)
    elif row['الحالة'] == '🔴 استعداد':
        return ['background-color: #3a1a1a; color: #FF5555'] * len(row)
    return [''] * len(row)

# عرض البيانات في الواجهة
if run_btn:
    st.success("✅ تمت محاكاة الأقمار الصناعية بنجاح.")
else:
    st.info("📌 النظام في وضع الاستعداد. اضغط على زر التنفيذ في القائمة الجانبية لبدء المحاكاة.")

st.subheader("🛰️ جدول حالة الأسطول المداري")
st.dataframe(
    df.style.apply(highlight_status, axis=1),
    use_container_width=True,
    height=400,
    column_config={
        "القمر": "🛰️ القمر",
        "الحالة": "📊 الحالة",
        "خط العرض": st.column_config.NumberColumn("خط العرض", format="%.4f°"),
        "خط الطول": st.column_config.NumberColumn("خط الطول", format="%.4f°"),
        "الارتفاع (كم)": st.column_config.NumberColumn("الارتفاع (كم)", format="%.2f km")
    }
)
