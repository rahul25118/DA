import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import io

# Page configuration
st.set_page_config(
    page_title="DataViz Pro Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    h1 {
        color: #1f77b4;
        font-size: 2.5rem;
        font-weight: 700;
    }
    h2 {
        color: #2c3e50;
        font-size: 1.8rem;
        margin-top: 2rem;
    }
    h3 {
        color: #34495e;
        font-size: 1.3rem;
    }
    .insight-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# Title
st.title("📊 DataViz Pro - Executive Dashboard")
st.markdown("### Transform Your Data into Actionable Insights")

# Sidebar
with st.sidebar:
    st.header("⚙️ Dashboard Controls")
    
    # File upload
    uploaded_file = st.file_uploader(
        "Upload Your Dataset",
        type=['csv', 'xlsx', 'xls', 'json'],
        help="Supports CSV, Excel, and JSON formats"
    )
    
    st.markdown("---")
    
    # Theme toggle
    theme = st.selectbox("🎨 Color Theme", 
                        ["Plotly", "Tableau", "Viridis", "Cividis"])
    
    # Dark mode toggle
    dark_mode = st.checkbox("🌙 Dark Mode", value=False)
    
    st.markdown("---")
    st.markdown("**Built by DataViz Pro AI**")
    st.markdown("*January 2026*")

# Function to load data
@st.cache_data
def load_data(file):
    if file is not None:
        if file.name.endswith('.csv'):
            df = pd.read_csv(file)
        elif file.name.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(file)
        elif file.name.endswith('.json'):
            df = pd.read_json(file)
        return df
    return None

# Function to detect column types
def detect_column_types(df):
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    
    # Try to detect datetime columns
    datetime_cols = []
    for col in df.columns:
        if 'date' in col.lower() or 'time' in col.lower():
            try:
                pd.to_datetime(df[col])
                datetime_cols.append(col)
            except:
                pass
    
    return numeric_cols, categorical_cols, datetime_cols

# Function to generate insights
def generate_insights(df, numeric_cols, categorical_cols):
    insights = []
    
    if numeric_cols:
        # Top value insight
        top_col = numeric_cols[0]
        top_value = df[top_col].max()
        insights.append(f"💡 Peak {top_col}: {top_value:,.2f}")
        
        # Growth/decline insight
        if len(df) > 1:
            change = ((df[top_col].iloc[-1] - df[top_col].iloc[0]) / df[top_col].iloc[0] * 100)
            trend = "growth" if change > 0 else "decline"
            insights.append(f"📈 {abs(change):.1f}% {trend} in {top_col}")
    
    if categorical_cols:
        # Top category insight
        top_cat_col = categorical_cols[0]
        top_category = df[top_cat_col].value_counts().index[0]
        count = df[top_cat_col].value_counts().values[0]
        insights.append(f"🏆 Top {top_cat_col}: {top_category} ({count} records)")
    
    return insights

# Main app logic
if uploaded_file is None:
    # Demo data
    st.info("👆 Upload your dataset in the sidebar to get started, or explore the demo below!")
    
    # Generate sample data
    np.random.seed(42)
    dates = pd.date_range(start='2023-01-01', end='2025-12-31', freq='D')
    df = pd.DataFrame({
        'Date': dates,
        'Revenue': np.random.normal(50000, 10000, len(dates)).cumsum() + 1000000,
        'Customers': np.random.poisson(100, len(dates)),
        'Region': np.random.choice(['North', 'South', 'East', 'West'], len(dates)),
        'Product': np.random.choice(['Product A', 'Product B', 'Product C', 'Product D'], len(dates)),
        'Costs': np.random.normal(30000, 5000, len(dates)).cumsum() + 500000
    })
    st.success("📊 Displaying demo dataset with 1,095 records")
else:
    df = load_data(uploaded_file)
    st.success(f"✅ Loaded {len(df):,} rows and {len(df.columns)} columns")

if df is not None:
    # Detect column types
    numeric_cols, categorical_cols, datetime_cols = detect_column_types(df)
    
    # Convert datetime columns
    for col in datetime_cols:
        try:
            df[col] = pd.to_datetime(df[col])
        except:
            pass
    
    # ============ EXECUTIVE SUMMARY ============
    st.markdown("## 🎯 Executive Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if numeric_cols:
            st.metric(
                label=f"Total {numeric_cols[0]}",
                value=f"{df[numeric_cols[0]].sum():,.0f}",
                delta=f"{df[numeric_cols[0]].mean():.0f} avg"
            )
    
    with col2:
        st.metric(
            label="Total Records",
            value=f"{len(df):,}",
            delta=f"{len(df.columns)} columns"
        )
    
    with col3:
        if numeric_cols and len(numeric_cols) > 1:
            st.metric(
                label=f"Avg {numeric_cols[1]}",
                value=f"{df[numeric_cols[1]].mean():,.0f}"
            )
    
    with col4:
        if categorical_cols:
            st.metric(
                label=f"Unique {categorical_cols[0]}",
                value=f"{df[categorical_cols[0]].nunique()}"
            )
    
    # Key Insights
    insights = generate_insights(df, numeric_cols, categorical_cols)
    st.markdown("### 🔑 Key Insights")
    for insight in insights:
        st.markdown(f"""
        <div class="insight-card">
            <h3 style="margin:0; color:white;">{insight}</h3>
        </div>
        """, unsafe_allow_html=True)
    
    # ============ CORE VISUALIZATIONS ============
    st.markdown("## 📈 Comprehensive Data Analysis")
    
    # 1. TRENDS - Line Chart
    if datetime_cols and numeric_cols:
        st.markdown("### 1️⃣ Trends Over Time")
        date_col = datetime_cols[0]
        value_col = st.selectbox("Select Metric for Trend", numeric_cols, key="trend")
        
        if categorical_cols:
            group_col = st.selectbox("Group by (optional)", ["None"] + categorical_cols, key="trend_group")
            if group_col != "None":
                fig1 = px.line(df, x=date_col, y=value_col, color=group_col,
                              title=f"{value_col} Trend by {group_col}",
                              template="plotly_white" if not dark_mode else "plotly_dark")
            else:
                fig1 = px.line(df, x=date_col, y=value_col,
                              title=f"{value_col} Trend Over Time",
                              template="plotly_white" if not dark_mode else "plotly_dark")
        else:
            fig1 = px.line(df, x=date_col, y=value_col,
                          title=f"{value_col} Trend Over Time",
                          template="plotly_white" if not dark_mode else "plotly_dark")
        
        fig1.update_layout(height=400, hovermode='x unified')
        st.plotly_chart(fig1, use_container_width=True)
    
    # 2. CATEGORY RANKING - Horizontal Bar
    if categorical_cols and numeric_cols:
        st.markdown("### 2️⃣ Category Rankings")
        col1, col2 = st.columns(2)
        
        with col1:
            cat_col = st.selectbox("Select Category", categorical_cols, key="cat")
        with col2:
            val_col = st.selectbox("Select Value", numeric_cols, key="val")
        
        df_grouped = df.groupby(cat_col)[val_col].sum().sort_values(ascending=True).tail(10)
        
        fig2 = px.bar(df_grouped, x=df_grouped.values, y=df_grouped.index,
                     orientation='h',
                     title=f"Top 10 {cat_col} by {val_col}",
                     labels={'x': val_col, 'y': cat_col},
                     template="plotly_white" if not dark_mode else "plotly_dark")
        fig2.update_layout(height=400)
        st.plotly_chart(fig2, use_container_width=True)
    
    # 3. RELATIONSHIPS - Scatter Plot
    if len(numeric_cols) >= 2:
        st.markdown("### 3️⃣ Relationships & Correlations")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            x_col = st.selectbox("X-Axis", numeric_cols, key="scatter_x")
        with col2:
            y_col = st.selectbox("Y-Axis", [c for c in numeric_cols if c != x_col], key="scatter_y")
        with col3:
            color_col = st.selectbox("Color by", ["None"] + categorical_cols, key="scatter_color")
        
        if color_col != "None":
            fig3 = px.scatter(df, x=x_col, y=y_col, color=color_col,
                            title=f"{y_col} vs {x_col}",
                            template="plotly_white" if not dark_mode else "plotly_dark",
                            trendline="ols")
        else:
            fig3 = px.scatter(df, x=x_col, y=y_col,
                            title=f"{y_col} vs {x_col}",
                            template="plotly_white" if not dark_mode else "plotly_dark",
                            trendline="ols")
        
        fig3.update_layout(height=400)
        st.plotly_chart(fig3, use_container_width=True)
    
    # 4. COMPOSITION - Treemap
    if categorical_cols and numeric_cols:
        st.markdown("### 4️⃣ Composition & Hierarchy")
        
        col1, col2 = st.columns(2)
        with col1:
            path_col = st.selectbox("Hierarchy Level", categorical_cols, key="tree")
        with col2:
            size_col = st.selectbox("Size by", numeric_cols, key="tree_size")
        
        df_tree = df.groupby(path_col)[size_col].sum().reset_index()
        
        fig4 = px.treemap(df_tree, path=[path_col], values=size_col,
                         title=f"{path_col} Composition by {size_col}",
                         template="plotly_white" if not dark_mode else "plotly_dark")
        fig4.update_layout(height=400)
        st.plotly_chart(fig4, use_container_width=True)
    
    # 5. DISTRIBUTION - Histogram + Box Plot
    if numeric_cols:
        st.markdown("### 5️⃣ Distribution Analysis")
        
        dist_col = st.selectbox("Select Metric for Distribution", numeric_cols, key="dist")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig5a = px.histogram(df, x=dist_col, nbins=30,
                               title=f"{dist_col} Distribution",
                               template="plotly_white" if not dark_mode else "plotly_dark")
            fig5a.update_layout(height=300)
            st.plotly_chart(fig5a, use_container_width=True)
        
        with col2:
            fig5b = px.box(df, y=dist_col,
                          title=f"{dist_col} Box Plot",
                          template="plotly_white" if not dark_mode else "plotly_dark")
            fig5b.update_layout(height=300)
            st.plotly_chart(fig5b, use_container_width=True)
    
    # ============ ADVANCED ANALYTICS ============
    st.markdown("## 🔬 Advanced Analytics")
    
    # 6. CORRELATION HEATMAP
    if len(numeric_cols) >= 2:
        st.markdown("### 6️⃣ Correlation Matrix")
        
        corr_matrix = df[numeric_cols].corr()
        
        fig6 = px.imshow(corr_matrix,
                        labels=dict(color="Correlation"),
                        x=numeric_cols,
                        y=numeric_cols,
                        color_continuous_scale="RdBu_r",
                        title="Feature Correlation Heatmap",
                        template="plotly_white" if not dark_mode else "plotly_dark")
        fig6.update_layout(height=500)
        st.plotly_chart(fig6, use_container_width=True)
    
    # 7. FORECAST (Simple Moving Average)
    if datetime_cols and numeric_cols:
        st.markdown("### 7️⃣ Forecast & Predictions")
        
        forecast_col = st.selectbox("Select Metric to Forecast", numeric_cols, key="forecast")
        
        # Simple moving average forecast
        df_sorted = df.sort_values(datetime_cols[0])
        df_sorted['MA_7'] = df_sorted[forecast_col].rolling(window=7).mean()
        df_sorted['MA_30'] = df_sorted[forecast_col].rolling(window=30).mean()
        
        fig7 = go.Figure()
        fig7.add_trace(go.Scatter(x=df_sorted[datetime_cols[0]], y=df_sorted[forecast_col],
                                 mode='lines', name='Actual', line=dict(color='blue')))
        fig7.add_trace(go.Scatter(x=df_sorted[datetime_cols[0]], y=df_sorted['MA_7'],
                                 mode='lines', name='7-Day MA', line=dict(color='orange', dash='dash')))
        fig7.add_trace(go.Scatter(x=df_sorted[datetime_cols[0]], y=df_sorted['MA_30'],
                                 mode='lines', name='30-Day MA', line=dict(color='green', dash='dot')))
        
        fig7.update_layout(title=f"{forecast_col} with Moving Averages",
                          template="plotly_white" if not dark_mode else "plotly_dark",
                          height=400,
                          hovermode='x unified')
        st.plotly_chart(fig7, use_container_width=True)
    
    # 8. ANOMALY DETECTION
    if numeric_cols:
        st.markdown("### 8️⃣ Anomaly Detection")
        
        anomaly_col = st.selectbox("Select Metric for Anomaly Detection", numeric_cols, key="anomaly")
        
        # Simple anomaly detection using z-score
        mean = df[anomaly_col].mean()
        std = df[anomaly_col].std()
        df['z_score'] = (df[anomaly_col] - mean) / std
        df['is_anomaly'] = abs(df['z_score']) > 2
        
        anomalies = df[df['is_anomaly']]
        
        fig8 = go.Figure()
        fig8.add_trace(go.Scatter(x=df.index, y=df[anomaly_col],
                                 mode='markers', name='Normal',
                                 marker=dict(color='blue', size=5)))
        fig8.add_trace(go.Scatter(x=anomalies.index, y=anomalies[anomaly_col],
                                 mode='markers', name='Anomaly',
                                 marker=dict(color='red', size=10, symbol='x')))
        
        fig8.update_layout(title=f"{anomaly_col} - Anomaly Detection (Z-Score > 2)",
                          template="plotly_white" if not dark_mode else "plotly_dark",
                          height=400)
        st.plotly_chart(fig8, use_container_width=True)
        
        st.info(f"🚨 Detected {len(anomalies)} anomalies ({len(anomalies)/len(df)*100:.1f}% of data)")
    
    # ============ DATA EXPORT ============
    st.markdown("## 💾 Export Data")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name="dashboard_data.csv",
            mime="text/csv"
        )
    
    with col2:
        # Excel export
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Data')
        buffer.seek(0)
        st.download_button(
            label="📥 Download Excel",
            data=buffer,
            file_name="dashboard_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    
    with col3:
        json_data = df.to_json(orient='records', indent=2)
        st.download_button(
            label="📥 Download JSON",
            data=json_data,
            file_name="dashboard_data.json",
            mime="application/json"
        )
    
    # ============ RAW DATA VIEW ============
    with st.expander("🔍 View Raw Data"):
        st.dataframe(df, use_container_width=True)
        
        st.markdown("#### Data Summary")
        st.write(df.describe())

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #7f8c8d; padding: 20px;'>
        <p><strong>Built by DataViz Pro AI • January 2026</strong></p>
        <p>Transform your data into actionable insights</p>
    </div>
    """, unsafe_allow_html=True)
