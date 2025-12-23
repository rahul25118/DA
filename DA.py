import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime
import time

# Page configuration
st.set_page_config(page_title="Complete Data Analysis Platform", page_icon="📊", layout="wide")

# Custom CSS
st.markdown("""
<style>
.main {background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);}
.step-card {background: linear-gradient(135deg, #3B82F6 0%, #8B5CF6 100%); color: white; padding: 20px; border-radius: 15px; margin: 10px 0;}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'data' not in st.session_state: st.session_state.data = None
if 'cleaned_data' not in st.session_state: st.session_state.cleaned_data = None
if 'objective' not in st.session_state: st.session_state.objective = ""
if 'kpis' not in st.session_state: st.session_state.kpis = ""
if 'progress' not in st.session_state:
    st.session_state.progress = {'requirements': False, 'collection': False, 'cleaning': False, 'eda': False, 'analysis': False, 'visualization': False, 'insights': False}
if 'treated_columns' not in st.session_state: st.session_state.treated_columns = set()

# Title & Progress
st.markdown("<h1 style='text-align: center; background: linear-gradient(135deg, #3B82F6 0%, #8B5CF6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>📊 Complete Data Analysis Platform</h1>", unsafe_allow_html=True)

progress_pct = sum(st.session_state.progress.values()) / len(st.session_state.progress) * 100
st.progress(progress_pct)

# Tabs
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["📋 1. Requirements", "📥 2. Data Collection", "🧹 3. Data Cleaning", "🔍 4. EDA", "🎯 5. Analysis", "📈 6. Visualization", "💡 7. Insights"])

# TAB 1
with tab1:
    st.markdown('<div class="step-card"><h2>Step 1: Requirements</h2></div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.objective = st.text_area("Objective", value=st.session_state.objective, height=100)
        st.session_state.kpis = st.text_area("KPIs", value=st.session_state.kpis, height=80)
    if st.session_state.objective and st.session_state.kpis:
        st.session_state.progress['requirements'] = True
        st.success("✅ Ready!")

# TAB 2
with tab2:
    st.markdown('<div class="step-card"><h2>Step 2: Data Collection</h2></div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload CSV", type='csv')
    if uploaded_file:
        with st.spinner("Loading..."):
            df = pd.read_csv(uploaded_file)
            st.session_state.data = df.copy()
            st.session_state.cleaned_data = df.copy()
            st.session_state.treated_columns = set()  # Reset
            st.session_state.progress['collection'] = True
        
        col1, col2, col3, col4 = st.columns(4)
        with col1: st.metric("Rows", len(df))
        with col2: st.metric("Columns", len(df.columns))
        with col3: st.metric("Numeric", len(df.select_dtypes(include=[np.number]).columns))
        with col4: st.metric("Categorical", len(df.select_dtypes(include='object').columns))
        st.dataframe(df.head())

# TAB 3 - ✅ FIXED VERSION
with tab3:
    st.markdown('<div class="step-card"><h2>Step 3: Data Cleaning</h2></div>', unsafe_allow_html=True)
    
    if st.session_state.data is not None:
        df = st.session_state.cleaned_data.copy()
        
        # Metrics
        col1, col2, col3 = st.columns(3)
        with col1: st.metric("Duplicates", df.duplicated().sum())
        with col2: st.metric("Missing", df.isnull().sum().sum())
        with col3: st.metric("Completeness", f"{100*(1-df.isnull().sum().sum()/(len(df)*len(df.columns))):.1f}%")
        
        # Quick actions
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🗑️ Remove Duplicates"):
                st.session_state.cleaned_data = st.session_state.cleaned_data.drop_duplicates().reset_index(drop=True)
                st.rerun()
        with col2:
            if st.button("Drop All Missing"):
                st.session_state.cleaned_data = st.session_state.cleaned_data.dropna().reset_index(drop=True)
                st.rerun()
        
        st.markdown("---")
        
        # ✅ FIXED: Column-by-column treatment
        cols_missing = df.columns[df.isnull().sum() > 0].tolist()
        remaining_cols = [c for c in cols_missing if c not in st.session_state.treated_columns]
        
        col1, col2 = st.columns([1, 2])
        with col1:
            st.metric("Total Missing Cols", len(cols_missing))
            st.metric("Treated", len(st.session_state.treated_columns))
        with col2:
            if st.session_state.treated_columns:
                st.success(f"✅ Treated: {', '.join(list(st.session_state.treated_columns)[-3:])}")
        
        if remaining_cols:
            st.info(f"📋 Remaining ({len(remaining_cols)}): {', '.join(remaining_cols[:4])}")
            
            # ✅ FIXED: Loop with SIMPLE STRING KEYS
            for idx, col in enumerate(remaining_cols[:6]):
                col_key = f"col_treatment_{idx}_{col.replace(' ', '_').replace('/', '_')}"
                
                with st.expander(f"🔧 {col} ({df[col].isnull().sum()} missing)", expanded=False):
                    c1, c2 = st.columns([3, 2])
                    
                    with c1:
                        st.write(f"**Type:** {df[col].dtype}")
                        st.write(f"**Missing:** {df[col].isnull().sum()}/{len(df)}")
                        st.write("**Samples:**", df[col].dropna().head(3).tolist())
                    
                    with c2:
                        is_numeric = pd.api.types.is_numeric_dtype(df[col])
                        
                        options = ["Drop Rows", "Fill Mean", "Fill Median"] if is_numeric else ["Drop Rows", "Fill Mode"]
                        options += ["Custom Value", "Forward Fill", "Backward Fill"] if is_numeric else ["Fill Unknown", "Custom Value"]
                        
                        method = st.selectbox("Method", options, key=f"{col_key}_method")
                        
                        custom_val = None
                        if method == "Custom Value":
                            if is_numeric:
                                custom_val = st.number_input("Value", value=0.0, key=f"{col_key}_custom_num")
                            else:
                                custom_val = st.text_input("Value", key=f"{col_key}_custom_txt")
                        
                        if st.button(f"✅ Apply {method}", key=f"{col_key}_apply"):
                            if method == "Drop Rows":
                                before = len(st.session_state.cleaned_data)
                                st.session_state.cleaned_data = st.session_state.cleaned_data.dropna(subset=[col]).reset_index(drop=True)
                                st.success(f"✅ Dropped {before-len(st.session_state.cleaned_data)} rows")
                            elif method == "Fill Mean" and is_numeric:
                                fill_val = st.session_state.cleaned_data[col].mean()
                                st.session_state.cleaned_data[col] = st.session_state.cleaned_data[col].fillna(fill_val)
                                st.success(f"✅ Mean: {fill_val:.2f}")
                            elif method == "Fill Median" and is_numeric:
                                fill_val = st.session_state.cleaned_data[col].median()
                                st.session_state.cleaned_data[col] = st.session_state.cleaned_data[col].fillna(fill_val)
                                st.success(f"✅ Median: {fill_val:.2f}")
                            elif method == "Fill Mode":
                                fill_val = st.session_state.cleaned_data[col].mode().iloc[0]
                                st.session_state.cleaned_data[col] = st.session_state.cleaned_data[col].fillna(fill_val)
                                st.success(f"✅ Mode: {fill_val}")
                            elif method == "Fill Unknown":
                                st.session_state.cleaned_data[col] = st.session_state.cleaned_data[col].fillna("Unknown")
                                st.success("✅ 'Unknown'")
                            elif method == "Custom Value" and custom_val is not None:
                                st.session_state.cleaned_data[col] = st.session_state.cleaned_data[col].fillna(custom_val)
                                st.success(f"✅ Custom: {custom_val}")
                            elif method == "Forward Fill":
                                st.session_state.cleaned_data[col] = st.session_state.cleaned_data[col].ffill()
                                st.success("✅ Forward fill")
                            elif method == "Backward Fill":
                                st.session_state.cleaned_data[col] = st.session_state.cleaned_data[col].bfill()
                                st.success("✅ Backward fill")
                            
                            # ✅ MARK TREATED
                            st.session_state.treated_columns.add(col)
                            st.session_state.progress['cleaning'] = True
                            st.rerun()
        else:
            st.balloons()
            st.success("🎉 All columns cleaned!")
        
        # Downloads
        col1, col2 = st.columns(2)
        with col1:
            st.download_button("📥 Original", st.session_state.data.to_csv(index=False), "original.csv")
        with col2:
            st.download_button("📥 Cleaned", st.session_state.cleaned_data.to_csv(index=False), "cleaned.csv", type="primary")
        
        st.dataframe(st.session_state.cleaned_data.head())
    else:
        st.warning("⚠️ Upload data first")

# Simplified other tabs
with tab4:
    st.markdown('<div class="step-card"><h2>EDA</h2></div>', unsafe_allow_html=True)
    if st.session_state.cleaned_data is not None:
        st.session_state.progress['eda'] = True
        df = st.session_state.cleaned_data
        st.dataframe(df.describe())
        col = st.selectbox("Column", df.columns)
        fig = px.histogram(df, x=col)
        st.plotly_chart(fig)

with tab5: 
    st.markdown('<div class="step-card"><h2>Analysis</h2></div>', unsafe_allow_html=True)
    if st.session_state.cleaned_data is not None: st.session_state.progress['analysis'] = True

with tab6: 
    st.markdown('<div class="step-card"><h2>Visualization</h2></div>', unsafe_allow_html=True)
    if st.session_state.cleaned_data is not None: st.session_state.progress['visualization'] = True

with tab7:
    st.markdown('<div class="step-card"><h2>Insights</h2></div>', unsafe_allow_html=True)
    if st.session_state.cleaned_data is not None: 
        st.session_state.progress['insights'] = True
        st.success("Analysis Complete! 🎉")

