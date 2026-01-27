import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Fast page config
st.set_page_config(page_title="DataViz Pro", page_icon="📊", layout="wide")

# Minimal CSS
st.markdown("""<style>
.stMetric {background:#f0f2f6;padding:10px;border-radius:5px}
h1 {color:#1f77b4}
</style>""", unsafe_allow_html=True)

st.title("📊 DataViz Pro Dashboard")

# Sidebar
with st.sidebar:
    st.header("⚙️ Controls")
    uploaded_file = st.file_uploader("Upload CSV/Excel", type=['csv', 'xlsx'])
    theme = st.selectbox("Theme", ["plotly", "plotly_dark"])

# Load data function
@st.cache_data
def load_data(file):
    if file.name.endswith('.csv'):
        return pd.read_csv(file)
    return pd.read_excel(file)

# Demo or uploaded data
if uploaded_file:
    df = load_data(uploaded_file)
    st.success(f"✅ Loaded {len(df):,} rows")
else:
    # Fast demo data
    dates = pd.date_range('2024-01-01', periods=100, freq='D')
    df = pd.DataFrame({
        'Date': dates,
        'Revenue': np.random.randint(10000, 50000, 100),
        'Region': np.random.choice(['North', 'South', 'East', 'West'], 100),
        'Product': np.random.choice(['A', 'B', 'C'], 100)
    })
    st.info("📊 Demo data loaded")

# Auto-detect columns
numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
cat_cols = df.select_dtypes(include=['object']).columns.tolist()
date_cols = [c for c in df.columns if 'date' in c.lower()]

# Convert dates
for col in date_cols:
    df[col] = pd.to_datetime(df[col])

# === METRICS ===
col1, col2, col3 = st.columns(3)
if numeric_cols:
    col1.metric("Total Records", f"{len(df):,}")
    col2.metric(f"Avg {numeric_cols[0]}", f"{df[numeric_cols[0]].mean():,.0f}")
    col3.metric(f"Max {numeric_cols[0]}", f"{df[numeric_cols[0]].max():,.0f}")

st.markdown("---")

# === CHARTS ===
tab1, tab2, tab3 = st.tabs(["📈 Trends", "📊 Analysis", "🔍 Details"])

with tab1:
    if date_cols and numeric_cols:
        st.subheader("Trend Over Time")
        fig = px.line(df, x=date_cols[0], y=numeric_cols[0], 
                     color=cat_cols[0] if cat_cols else None,
                     template=theme)
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    col1, col2 = st.columns(2)
    
    with col1:
        if cat_cols and numeric_cols:
            st.subheader("Top Categories")
            top_data = df.groupby(cat_cols[0])[numeric_cols[0]].sum().sort_values(ascending=False).head(10)
            fig = px.bar(top_data, orientation='h', template=theme)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        if len(numeric_cols) >= 2:
            st.subheader("Correlation")
            fig = px.scatter(df, x=numeric_cols[0], y=numeric_cols[1],
                           color=cat_cols[0] if cat_cols else None,
                           template=theme)
            st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("Raw Data")
    st.dataframe(df, use_container_width=True)
    
    # Quick export
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download CSV", csv, "data.csv", "text/csv")

st.markdown("---")
st.markdown("**Built by DataViz Pro AI • January 2026**")
