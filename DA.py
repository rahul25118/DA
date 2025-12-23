import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Complete Data Analysis Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 60px;
        padding: 10px 15px;
        background-color: #ffffff;
        border-radius: 10px 10px 0 0;
        font-size: 14px;
        transition: all 0.3s ease;
    }
    .stTabs [data-baseweb="tab"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #3B82F6 0%, #8B5CF6 100%);
        color: white;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    }
    .step-card {
        background: linear-gradient(135deg, #3B82F6 0%, #8B5CF6 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
        margin: 10px 0;
        box-shadow: 0 8px 16px rgba(59, 130, 246, 0.2);
    }
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        transition: transform 0.2s;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 4px 16px rgba(59, 130, 246, 0.2);
    }
    .tooltip-icon {
        cursor: help;
        color: #3B82F6;
        font-size: 18px;
        margin-left: 5px;
    }
    .status-badge {
        padding: 5px 10px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        display: inline-block;
        margin: 2px;
    }
    .status-complete {
        background: #d1fae5;
        color: #065f46;
    }
    .status-pending {
        background: #fef3c7;
        color: #92400e;
    }
    .change-history {
        background: #f8f9fa;
        border-left: 4px solid #3B82F6;
        padding: 10px;
        margin: 5px 0;
        border-radius: 5px;
        font-size: 14px;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'data' not in st.session_state:
    st.session_state.data = None
if 'cleaned_data' not in st.session_state:
    st.session_state.cleaned_data = None
if 'objective' not in st.session_state:
    st.session_state.objective = ""
if 'kpis' not in st.session_state:
    st.session_state.kpis = ""
if 'progress' not in st.session_state:
    st.session_state.progress = {
        'requirements': False,
        'collection': False,
        'cleaning': False,
        'eda': False,
        'analysis': False,
        'visualization': False,
        'insights': False
    }
if 'applied_changes' not in st.session_state:
    st.session_state.applied_changes = []
if 'column_treatment_status' not in st.session_state:
    st.session_state.column_treatment_status = {}

# Title
st.markdown("""
    <h1 style='text-align: center; background: linear-gradient(135deg, #3B82F6 0%, #8B5CF6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; padding: 20px; font-size: 48px;'>
        📊 Complete Data Analysis Platform
    </h1>
    <p style='text-align: center; color: #666; font-size: 18px; margin-bottom: 10px;'>
        Your End-to-End Data Analysis Journey: From Problem Definition to Actionable Insights
    </p>
    <div style='text-align: center; margin-bottom: 30px;'>
        <a href='https://github.com/rahul25118' target='_blank' style='margin: 0 15px; text-decoration: none;'>
            <img src='https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white' alt='GitHub'>
        </a>
        <a href='https://www.linkedin.com/in/rahul-mishra-b71ba21b8/' target='_blank' style='margin: 0 15px; text-decoration: none;'>
            <img src='https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white' alt='LinkedIn'>
        </a>
    </div>
""", unsafe_allow_html=True)

# Progress Indicator
completed = sum(st.session_state.progress.values())
total_steps = len(st.session_state.progress)
progress_percentage = (completed / total_steps) * 100

st.markdown(f"""
    <div style='background: white; padding: 15px; border-radius: 10px; margin-bottom: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
        <div style='display: flex; justify-content: space-between; margin-bottom: 10px;'>
            <span style='font-weight: 600; color: #3B82F6;'>Overall Progress</span>
            <span style='font-weight: 600; color: #3B82F6;'>{completed}/{total_steps} Steps Completed</span>
        </div>
        <div style='background: #E5E7EB; border-radius: 10px; height: 10px; overflow: hidden;'>
            <div style='background: linear-gradient(90deg, #3B82F6 0%, #8B5CF6 100%); height: 100%; width: {progress_percentage}%; transition: width 0.5s ease;'></div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Create tabs for all 7 steps
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📋 1. Requirements", 
    "📥 2. Data Collection", 
    "🧹 3. Data Cleaning", 
    "🔍 4. EDA",
    "🎯 5. Analysis",
    "📈 6. Visualization",
    "💡 7. Insights"
])

# ==================== TAB 1: REQUIREMENT GATHERING ====================
with tab1:
    st.markdown('<div class="step-card"><h2>Step 1: Requirement Gathering</h2><p>Define your objective before touching any data</p></div>', unsafe_allow_html=True)
    
    with st.expander("💡 Why is this important?"):
        st.info("""
        **Requirement gathering ensures:**
        - Clear direction for your analysis
        - Measurable success criteria (KPIs)
        - Efficient use of time and resources
        - Alignment with business goals
        
        **Tip:** A well-defined problem is half solved!
        """)
    
    st.markdown("### 🎯 Define Your Business Problem")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### What are you trying to solve?")
        objective = st.text_area(
            "Business Objective",
            value=st.session_state.objective,
            placeholder="Example: Why are sales dropping in the Midwest region?",
            height=150
        )
        st.session_state.objective = objective
        
        st.markdown("#### Key Performance Indicators (KPIs)")
        kpis = st.text_area(
            "Define your success metrics",
            value=st.session_state.kpis,
            placeholder="Example: Revenue growth, Customer retention rate, Conversion rate",
            height=100
        )
        st.session_state.kpis = kpis
    
    with col2:
        st.markdown("#### Project Constraints")
        timeline = st.date_input("Project Timeline", datetime.now())
        budget = st.number_input("Budget ($)", min_value=0, value=10000)
        
        st.markdown("#### Data Sources Available")
        data_sources = st.multiselect(
            "Select your data sources",
            ["Internal CRM", "ERP System", "Sales Logs", "Social Media", "Government Database", "Third-party APIs", "Surveys", "Web Scraping"]
        )
    
    if objective and kpis:
        st.success("✅ Objective and KPIs defined! Ready to collect data.")
        st.session_state.progress['requirements'] = True
        
        st.markdown("### 📊 Your Analysis Framework")
        st.info(f"""
        **Problem:** {objective}
        
        **Success Metrics:** {kpis}
        
        **Timeline:** {timeline}
        
        **Data Sources:** {', '.join(data_sources) if data_sources else 'Not specified'}
        """)

# ==================== TAB 2: DATA COLLECTION ====================
with tab2:
    st.markdown('<div class="step-card"><h2>Step 2: Data Collection</h2><p>Gather raw data from your identified sources</p></div>', unsafe_allow_html=True)
    
    with st.expander("💡 Data Collection Tips"):
        st.info("""
        **Best Practices:**
        - Ensure data is from reliable sources
        - Check file format compatibility (CSV recommended)
        - Verify data permissions and privacy compliance
        - Document data source for future reference
        
        **Supported Format:** CSV files only
        """)
    
    st.markdown("### 📥 Upload Your Dataset")
    
    uploaded_file = st.file_uploader("Choose a CSV file", type=['csv'])
    
    if uploaded_file is not None:
        try:
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            status_text.text("Loading data... 25%")
            progress_bar.progress(25)
            
            df = pd.read_csv(uploaded_file)
            
            status_text.text("Processing columns... 50%")
            progress_bar.progress(50)
            
            st.session_state.data = df
            st.session_state.cleaned_data = df.copy()
            # Reset column treatment status
            st.session_state.column_treatment_status = {}
            st.session_state.applied_changes = []
            
            status_text.text("Analyzing data types... 75%")
            progress_bar.progress(75)
            
            status_text.text("Complete! 100%")
            progress_bar.progress(100)
            
            st.session_state.progress['collection'] = True
            
            import time
            time.sleep(0.5)
            progress_bar.empty()
            status_text.empty()
            
            st.success(f"✅ Data loaded successfully! {len(df)} rows × {len(df.columns)} columns")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Rows", len(df))
            with col2:
                st.metric("Total Columns", len(df.columns))
            with col3:
                st.metric("Numeric Columns", len(df.select_dtypes(include=[np.number]).columns))
            with col4:
                st.metric("Categorical Columns", len(df.select_dtypes(include=['object']).columns))
            
            st.markdown("### 📋 Data Preview")
            st.dataframe(df.head(10), use_container_width=True)
            
            st.markdown("### 📊 Column Information")
            col_info = pd.DataFrame({
                'Column': df.columns,
                'Data Type': df.dtypes.values,
                'Non-Null Count': df.count().values,
                'Null Count': df.isnull().sum().values,
                'Null %': (df.isnull().sum().values / len(df) * 100).round(2)
            })
            st.dataframe(col_info, use_container_width=True)
            
        except Exception as e:
            st.error(f"Error loading file: {str(e)}")
    else:
        st.info("👆 Please upload a CSV file to begin data collection")

# ==================== TAB 3: DATA CLEANING ====================
with tab3:
    st.markdown('<div class="step-card"><h2>Step 3: Data Cleaning</h2><p>Transform raw data into a clean, analysis-ready dataset</p></div>', unsafe_allow_html=True)
    
    with st.expander("💡 Data Cleaning Best Practices"):
        st.info("""
        **Why Clean Data?**
        - Poor quality data leads to poor insights
        - 80% of analysis time is spent on cleaning
        - Clean data = Accurate results
        
        **Common Issues:**
        - Missing values (handle column by column)
        - Duplicate records (remove carefully)
        - Outliers (decide case by case)
        - Inconsistent formatting
        
        **Tip:** Always review changes before applying!
        """)
    
    if st.session_state.data is not None:
        # Get the current cleaned data
        if st.session_state.cleaned_data is None:
            st.session_state.cleaned_data = st.session_state.data.copy()
        
        df = st.session_state.cleaned_data
        
        st.markdown("### 🧹 Data Quality Overview")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            duplicates = df.duplicated().sum()
            st.metric("Duplicate Rows", duplicates, delta=f"-{duplicates} to remove" if duplicates > 0 else None)
        with col2:
            missing = df.isnull().sum().sum()
            st.metric("Missing Values", missing)
        with col3:
            total_cells = df.shape[0] * df.shape[1]
            completeness = ((total_cells - missing) / total_cells * 100)
            st.metric("Data Completeness", f"{completeness:.1f}%")
        with col4:
            treated_cols = len([c for c, status in st.session_state.column_treatment_status.items() if status.get('treated', False)])
            st.metric("Treated Columns", treated_cols)
        
        st.markdown("---")
        
        # Quick Actions
        st.markdown("### ⚡ Quick Actions")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🗑️ Remove All Duplicates", use_container_width=True):
                before = len(df)
                st.session_state.cleaned_data = df.drop_duplicates()
                after = len(st.session_state.cleaned_data)
                removed = before - after
                st.session_state.applied_changes.append(f"Removed {removed} duplicate rows")
                st.success(f"✅ Removed {removed} duplicate rows!")
                st.rerun()
        
        with col2:
            if st.button("🧹 Drop All Missing Rows", use_container_width=True):
                before = len(df)
                st.session_state.cleaned_data = df.dropna()
                after = len(st.session_state.cleaned_data)
                removed = before - after
                st.session_state.applied_changes.append(f"Dropped {removed} rows with any missing values")
                # Mark all columns as treated
                for col in df.columns:
                    if col not in st.session_state.column_treatment_status:
                        st.session_state.column_treatment_status[col] = {}
                    st.session_state.column_treatment_status[col]['treated'] = True
                    st.session_state.column_treatment_status[col]['method'] = 'Drop Rows'
                st.success(f"✅ Dropped {removed} rows with missing values!")
                st.rerun()
        
        with col3:
            if st.button("🔄 Reset All Changes", use_container_width=True):
                st.session_state.cleaned_data = st.session_state.data.copy()
                st.session_state.column_treatment_status = {}
                st.session_state.applied_changes = []
                st.success("✅ All changes reset to original data!")
                st.rerun()
        
        # Column-by-Column Missing Value Treatment
        st.markdown("---")
        st.markdown("### 🎯 Column-by-Column Missing Value Treatment")
        
        # Get columns with missing values - ALWAYS get fresh from session state
        cols_with_missing = st.session_state.cleaned_data.columns[
            st.session_state.cleaned_data.isnull().any()
        ].tolist()
        
        if len(cols_with_missing) > 0:
            # Show current status
            st.markdown("#### 📊 Current Missing Values Status")
            
            # Create a summary table with FRESH data
            summary_data = []
            for col in cols_with_missing:
                missing_count = st.session_state.cleaned_data[col].isnull().sum()
                missing_percent = (missing_count / len(st.session_state.cleaned_data) * 100)
                treatment_status = st.session_state.column_treatment_status.get(col, {}).get('status', 'Pending')
                treatment_method = st.session_state.column_treatment_status.get(col, {}).get('method', 'Not treated')
                
                summary_data.append({
                    'Column': col,
                    'Missing Count': missing_count,
                    'Missing %': f"{missing_percent:.1f}%",
                    'Data Type': str(st.session_state.cleaned_data[col].dtype),
                    'Status': treatment_status,
                    'Method': treatment_method
                })
            
            summary_df = pd.DataFrame(summary_data)
            st.dataframe(summary_df, use_container_width=True)
            
            st.info(f"Found **{len(cols_with_missing)} columns** with missing values. Select a column to treat:")
            
            # Column selector
            selected_col = st.selectbox(
                "Select a column to treat",
                cols_with_missing,
                key="col_selector"
            )
            
            if selected_col:
                with st.container():
                    st.markdown(f"#### 📊 Treating Column: **{selected_col}**")
                    
                    # Get current column info from session state
                    col_missing = st.session_state.cleaned_data[selected_col].isnull().sum()
                    col_missing_percent = (col_missing / len(st.session_state.cleaned_data) * 100)
                    col_type = st.session_state.cleaned_data[selected_col].dtype
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("**Column Information:**")
                        st.write(f"**Data Type:** {col_type}")
                        st.write(f"**Missing Values:** {col_missing} ({col_missing_percent:.1f}%)")
                        
                        if col_missing < len(st.session_state.cleaned_data):
                            st.markdown("**Sample Values:**")
                            non_missing = st.session_state.cleaned_data[selected_col].dropna()
                            if len(non_missing) > 0:
                                st.write(non_missing.head(5).tolist())
                    
                    with col2:
                        if pd.api.types.is_numeric_dtype(col_type):
                            st.markdown("**Statistics:**")
                            stats = {
                                'Mean': st.session_state.cleaned_data[selected_col].mean(),
                                'Median': st.session_state.cleaned_data[selected_col].median(),
                                'Std Dev': st.session_state.cleaned_data[selected_col].std(),
                                'Min': st.session_state.cleaned_data[selected_col].min(),
                                'Max': st.session_state.cleaned_data[selected_col].max()
                            }
                            for stat_name, stat_value in stats.items():
                                st.write(f"**{stat_name}:** {stat_value:.2f}")
                    
                    st.markdown("---")
                    st.markdown("#### ⚙️ Select Treatment Method")
                    
                    # Method selection based on data type
                    if pd.api.types.is_numeric_dtype(col_type):
                        method = st.radio(
                            f"Choose method for '{selected_col}'",
                            ["Fill with Mean", "Fill with Median", "Fill with Mode", "Fill with 0", 
                             "Fill with Custom Value", "Forward Fill", "Backward Fill", "Drop Rows"],
                            key=f"method_{selected_col}"
                        )
                        
                        if method == "Fill with Custom Value":
                            custom_val = st.number_input(
                                "Enter custom value:",
                                value=0.0,
                                key=f"custom_{selected_col}"
                            )
                    
                    else:  # Categorical/Object type
                        method = st.radio(
                            f"Choose method for '{selected_col}'",
                            ["Fill with Mode", "Fill with 'Unknown'", "Fill with 'Missing'", 
                             "Fill with Custom Value", "Forward Fill", "Backward Fill", "Drop Rows"],
                            key=f"method_{selected_col}"
                        )
                        
                        if method == "Fill with Custom Value":
                            custom_val = st.text_input(
                                "Enter custom value:",
                                value="",
                                key=f"custom_{selected_col}"
                            )
                    
                    # Apply button
                    if st.button(f"✅ Apply Treatment to '{selected_col}'", type="primary", use_container_width=True):
                        try:
                            if method == "Drop Rows":
                                before = len(st.session_state.cleaned_data)
                                st.session_state.cleaned_data = st.session_state.cleaned_data.dropna(subset=[selected_col])
                                after = len(st.session_state.cleaned_data)
                                removed = before - after
                                
                                st.session_state.column_treatment_status[selected_col] = {
                                    'treated': True,
                                    'method': 'Drop Rows',
                                    'status': 'Completed',
                                    'details': f'Removed {removed} rows'
                                }
                                st.session_state.applied_changes.append(f"Dropped {removed} rows for column '{selected_col}'")
                                
                                st.success(f"✅ Dropped {removed} rows with missing values in '{selected_col}'")
                            
                            elif method == "Fill with Mean":
                                mean_val = st.session_state.cleaned_data[selected_col].mean()
                                st.session_state.cleaned_data[selected_col] = st.session_state.cleaned_data[selected_col].fillna(mean_val)
                                
                                st.session_state.column_treatment_status[selected_col] = {
                                    'treated': True,
                                    'method': 'Fill with Mean',
                                    'status': 'Completed',
                                    'details': f'Filled with mean: {mean_val:.2f}'
                                }
                                st.session_state.applied_changes.append(f"Filled column '{selected_col}' with mean: {mean_val:.2f}")
                                
                                st.success(f"✅ Filled '{selected_col}' with mean: {mean_val:.2f}")
                            
                            elif method == "Fill with Median":
                                median_val = st.session_state.cleaned_data[selected_col].median()
                                st.session_state.cleaned_data[selected_col] = st.session_state.cleaned_data[selected_col].fillna(median_val)
                                
                                st.session_state.column_treatment_status[selected_col] = {
                                    'treated': True,
                                    'method': 'Fill with Median',
                                    'status': 'Completed',
                                    'details': f'Filled with median: {median_val:.2f}'
                                }
                                st.session_state.applied_changes.append(f"Filled column '{selected_col}' with median: {median_val:.2f}")
                                
                                st.success(f"✅ Filled '{selected_col}' with median: {median_val:.2f}")
                            
                            elif method == "Fill with Mode":
                                mode_series = st.session_state.cleaned_data[selected_col].mode()
                                mode_val = mode_series[0] if len(mode_series) > 0 else 0
                                st.session_state.cleaned_data[selected_col] = st.session_state.cleaned_data[selected_col].fillna(mode_val)
                                
                                st.session_state.column_treatment_status[selected_col] = {
                                    'treated': True,
                                    'method': 'Fill with Mode',
                                    'status': 'Completed',
                                    'details': f'Filled with mode: {mode_val}'
                                }
                                st.session_state.applied_changes.append(f"Filled column '{selected_col}' with mode: {mode_val}")
                                
                                st.success(f"✅ Filled '{selected_col}' with mode: {mode_val}")
                            
                            elif method == "Fill with 0":
                                st.session_state.cleaned_data[selected_col] = st.session_state.cleaned_data[selected_col].fillna(0)
                                
                                st.session_state.column_treatment_status[selected_col] = {
                                    'treated': True,
                                    'method': 'Fill with 0',
                                    'status': 'Completed',
                                    'details': 'Filled with 0'
                                }
                                st.session_state.applied_changes.append(f"Filled column '{selected_col}' with 0")
                                
                                st.success(f"✅ Filled '{selected_col}' with 0")
                            
                            elif method == "Fill with 'Unknown'":
                                st.session_state.cleaned_data[selected_col] = st.session_state.cleaned_data[selected_col].fillna('Unknown')
                                
                                st.session_state.column_treatment_status[selected_col] = {
                                    'treated': True,
                                    'method': "Fill with 'Unknown'",
                                    'status': 'Completed',
                                    'details': "Filled with 'Unknown'"
                                }
                                st.session_state.applied_changes.append(f"Filled column '{selected_col}' with 'Unknown'")
                                
                                st.success(f"✅ Filled '{selected_col}' with 'Unknown'")
                            
                            elif method == "Fill with 'Missing'":
                                st.session_state.cleaned_data[selected_col] = st.session_state.cleaned_data[selected_col].fillna('Missing')
                                
                                st.session_state.column_treatment_status[selected_col] = {
                                    'treated': True,
                                    'method': "Fill with 'Missing'",
                                    'status': 'Completed',
                                    'details': "Filled with 'Missing'"
                                }
                                st.session_state.applied_changes.append(f"Filled column '{selected_col}' with 'Missing'")
                                
                                st.success(f"✅ Filled '{selected_col}' with 'Missing'")
                            
                            elif method == "Fill with Custom Value":
                                st.session_state.cleaned_data[selected_col] = st.session_state.cleaned_data[selected_col].fillna(custom_val)
                                
                                st.session_state.column_treatment_status[selected_col] = {
                                    'treated': True,
                                    'method': 'Fill with Custom Value',
                                    'status': 'Completed',
                                    'details': f'Filled with: {custom_val}'
                                }
                                st.session_state.applied_changes.append(f"Filled column '{selected_col}' with custom value: {custom_val}")
                                
                                st.success(f"✅ Filled '{selected_col}' with custom value: {custom_val}")
                            
                            elif method == "Forward Fill":
                                st.session_state.cleaned_data[selected_col] = st.session_state.cleaned_data[selected_col].fillna(method='ffill')
                                
                                st.session_state.column_treatment_status[selected_col] = {
                                    'treated': True,
                                    'method': 'Forward Fill',
                                    'status': 'Completed',
                                    'details': 'Applied forward fill'
                                }
                                st.session_state.applied_changes.append(f"Applied forward fill to column '{selected_col}'")
                                
                                st.success(f"✅ Applied forward fill to '{selected_col}'")
                            
                            elif method == "Backward Fill":
                                st.session_state.cleaned_data[selected_col] = st.session_state.cleaned_data[selected_col].fillna(method='bfill')
                                
                                st.session_state.column_treatment_status[selected_col] = {
                                    'treated': True,
                                    'method': 'Backward Fill',
                                    'status': 'Completed',
                                    'details': 'Applied backward fill'
                                }
                                st.session_state.applied_changes.append(f"Applied backward fill to column '{selected_col}'")
                                
                                st.success(f"✅ Applied backward fill to '{selected_col}'")
                            
                            st.session_state.progress['cleaning'] = True
                            st.rerun()
                            
                        except Exception as e:
                            st.error(f"Error applying treatment: {str(e)}")
                
                # Reset button for this column
                if st.button(f"🔄 Reset '{selected_col}'", key=f"reset_{selected_col}"):
                    if selected_col in st.session_state.data.columns:
                        st.session_state.cleaned_data[selected_col] = st.session_state.data[selected_col]
                        if selected_col in st.session_state.column_treatment_status:
                            del st.session_state.column_treatment_status[selected_col]
                        st.session_state.applied_changes.append(f"Reset column '{selected_col}' to original")
                        st.success(f"✅ Reset '{selected_col}' to original values")
                        st.rerun()
        
        else:
            st.success("🎉 No missing values found in the dataset!")
        
        # Applied Changes History
        if st.session_state.applied_changes:
            st.markdown("---")
            st.markdown("#### 📋 Applied Changes History")
            
            for i, change in enumerate(st.session_state.applied_changes[-10:]):  # Show last 10 changes
                st.markdown(f'<div class="change-history">{i+1}. {change}</div>', unsafe_allow_html=True)
            
            if st.button("Clear History"):
                st.session_state.applied_changes = []
                st.rerun()
        
        # Visualization
        st.markdown("---")
        st.markdown("### 📊 Missing Values Visualization")
        
        # Get current missing values from session state
        current_missing = st.session_state.cleaned_data.isnull().sum()
        current_missing = current_missing[current_missing > 0]
        
        if len(current_missing) > 0:
            col1, col2 = st.columns(2)
            
            with col1:
                # Bar chart
                fig = px.bar(
                    x=current_missing.index,
                    y=current_missing.values,
                    title="Missing Values by Column",
                    labels={'x': 'Column', 'y': 'Missing Count'},
                    color=current_missing.values,
                    color_continuous_scale='Reds'
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Pie chart for missing values distribution
                fig = px.pie(
                    values=current_missing.values,
                    names=current_missing.index,
                    title="Distribution of Missing Values",
                    hole=0.4
                )
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.success("🎉 No missing values remaining in the dataset!")
        
        # Current Data Preview
        st.markdown("---")
        st.markdown("### 📋 Current Data Preview")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.dataframe(st.session_state.cleaned_data.head(10), use_container_width=True)
        
        with col2:
            st.markdown("#### 📊 Current Stats")
            st.metric("Total Rows", len(st.session_state.cleaned_data))
            st.metric("Total Columns", len(st.session_state.cleaned_data.columns))
            remaining_missing = st.session_state.cleaned_data.isnull().sum().sum()
            st.metric("Remaining Missing", remaining_missing)
            if remaining_missing == 0:
                st.success("✅ Data is clean!")
            else:
                st.warning(f"⚠️ {remaining_missing} missing values remaining")
        
        # Download Section
        st.markdown("---")
        st.markdown("### 📥 Download Your Data")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            csv_original = st.session_state.data.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Original Data",
                data=csv_original,
                file_name="original_data.csv",
                mime="text/csv",
                help="Download the data as it was originally uploaded",
                use_container_width=True
            )
        
        with col2:
            csv_cleaned = st.session_state.cleaned_data.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Cleaned Data",
                data=csv_cleaned,
                file_name="cleaned_data.csv",
                mime="text/csv",
                help="Download the data with all cleaning operations applied",
                type="primary",
                use_container_width=True
            )
        
        with col3:
            if st.button("🔄 Refresh View", use_container_width=True):
                st.rerun()
    
    else:
        st.warning("⚠️ Please upload data in Step 2 first")

# ==================== TAB 4: EDA ====================
with tab4:
    st.markdown('<div class="step-card"><h2>Step 4: Exploratory Data Analysis</h2><p>Discover patterns, trends, and correlations in your data</p></div>', unsafe_allow_html=True)
    
    with st.expander("💡 What is EDA?"):
        st.info("""
        **Exploratory Data Analysis helps you:**
        - Understand data distribution and patterns
        - Identify relationships between variables
        - Detect outliers and anomalies
        - Make informed decisions for deeper analysis
        
        **Key Techniques:**
        - Descriptive statistics (mean, median, std)
        - Visualizations (histograms, box plots)
        - Correlation analysis
        """)
    
    if st.session_state.cleaned_data is not None:
        df = st.session_state.cleaned_data
        st.session_state.progress['eda'] = True
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        st.markdown("### 📊 Descriptive Statistics")
        st.dataframe(df.describe(), use_container_width=True)
        
        st.markdown("### 📈 Variable Distribution")
        
        selected_col = st.selectbox("Select a column to visualize", df.columns)
        
        if selected_col in numeric_cols:
            col1, col2 = st.columns(2)
            
            with col1:
                fig = px.histogram(df, x=selected_col, 
                                 title=f"Distribution of {selected_col}",
                                 color_discrete_sequence=['#667eea'])
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = px.box(df, y=selected_col,
                           title=f"Box Plot of {selected_col}",
                           color_discrete_sequence=['#764ba2'])
                st.plotly_chart(fig, use_container_width=True)
        else:
            value_counts = df[selected_col].value_counts().head(10)
            fig = px.bar(x=value_counts.index, y=value_counts.values,
                       title=f"Top 10 Values in {selected_col}",
                       labels={'x': selected_col, 'y': 'Count'},
                       color_discrete_sequence=['#667eea'])
            st.plotly_chart(fig, use_container_width=True)
        
        if len(numeric_cols) >= 2:
            st.markdown("### 🔗 Correlation Analysis")
            
            corr_matrix = df[numeric_cols].corr()
            
            fig = px.imshow(corr_matrix,
                          text_auto='.2f',
                          color_continuous_scale='RdBu',
                          title="Correlation Heatmap",
                          aspect="auto")
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("⚠️ Please clean your data in Step 3 first")

# ==================== TAB 5: ANALYSIS ====================
with tab5:
    st.markdown('<div class="step-card"><h2>Step 5: Data Analysis & Modeling</h2><p>Apply statistical techniques to extract insights</p></div>', unsafe_allow_html=True)
    
    with st.expander("💡 Types of Analysis"):
        st.info("""
        **1. Descriptive:** What happened in the past?
        - Summary statistics, distributions
        
        **2. Diagnostic:** Why did it happen?
        - Correlation, causation analysis
        
        **3. Comparative:** How do segments differ?
        - Group comparisons, A/B testing
        
        **4. Trend:** What patterns exist over time?
        - Time series, seasonality
        """)
    
    if st.session_state.cleaned_data is not None:
        df = st.session_state.cleaned_data
        st.session_state.progress['analysis'] = True
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        analysis_type = st.selectbox(
            "Select Analysis Type",
            ["Descriptive Analysis", "Diagnostic Analysis", "Comparative Analysis", "Trend Analysis"]
        )
        
        if analysis_type == "Descriptive Analysis":
            st.markdown("### 📊 What happened in the past?")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Summary Statistics")
                summary_col = st.selectbox("Select column", numeric_cols)
                
                stats = {
                    "Mean": df[summary_col].mean(),
                    "Median": df[summary_col].median(),
                    "Mode": df[summary_col].mode()[0] if not df[summary_col].mode().empty else "N/A",
                    "Std Dev": df[summary_col].std(),
                    "Min": df[summary_col].min(),
                    "Max": df[summary_col].max(),
                    "Range": df[summary_col].max() - df[summary_col].min()
                }
                
                for key, value in stats.items():
                    st.metric(key, f"{value:.2f}" if isinstance(value, (int, float)) else value)
            
            with col2:
                st.markdown("#### Data Distribution")
                fig = px.histogram(df, x=summary_col, marginal="box",
                                 color_discrete_sequence=['#667eea'])
                st.plotly_chart(fig, use_container_width=True)
        
        elif analysis_type == "Diagnostic Analysis":
            st.markdown("### 🔍 Why did it happen?")
            
            if len(numeric_cols) >= 2:
                x_col = st.selectbox("Select X variable (potential cause)", numeric_cols)
                y_col = st.selectbox("Select Y variable (outcome)", [c for c in numeric_cols if c != x_col])
                
                corr = df[x_col].corr(df[y_col])
                
                st.metric("Correlation Coefficient", f"{corr:.3f}")
                
                if abs(corr) > 0.7:
                    st.success(f"Strong {'positive' if corr > 0 else 'negative'} correlation detected!")
                elif abs(corr) > 0.4:
                    st.info(f"Moderate {'positive' if corr > 0 else 'negative'} correlation detected.")
                else:
                    st.warning("Weak correlation. These variables may not be strongly related.")
                
                fig = px.scatter(df, x=x_col, y=y_col, trendline="ols",
                               title=f"Relationship: {x_col} vs {y_col}",
                               color_discrete_sequence=['#764ba2'])
                st.plotly_chart(fig, use_container_width=True)
        
        elif analysis_type == "Comparative Analysis":
            st.markdown("### ⚖️ Compare different segments")
            
            if len(df.select_dtypes(include=['object']).columns) > 0:
                cat_col = st.selectbox("Select category to compare", 
                                      df.select_dtypes(include=['object']).columns)
                num_col = st.selectbox("Select numeric metric", numeric_cols)
                
                comparison = df.groupby(cat_col)[num_col].agg(['mean', 'median', 'count']).reset_index()
                
                fig = px.bar(comparison, x=cat_col, y='mean',
                           title=f"Average {num_col} by {cat_col}",
                           color='mean',
                           color_continuous_scale='Viridis')
                st.plotly_chart(fig, use_container_width=True)
                
                st.dataframe(comparison, use_container_width=True)
        
        elif analysis_type == "Trend Analysis":
            st.markdown("### 📈 Identify trends over time")
            
            date_cols = df.select_dtypes(include=['datetime64']).columns.tolist()
            
            if len(date_cols) > 0:
                date_col = st.selectbox("Select date column", date_cols)
                metric_col = st.selectbox("Select metric to track", numeric_cols)
                
                trend_data = df.groupby(date_col)[metric_col].mean().reset_index()
                
                fig = px.line(trend_data, x=date_col, y=metric_col,
                            title=f"Trend: {metric_col} over time",
                            color_discrete_sequence=['#667eea'])
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No date columns found. Try sorting by another column for trend analysis.")
                
                if len(numeric_cols) >= 2:
                    x_trend = st.selectbox("Select X axis", df.columns)
                    y_trend = st.selectbox("Select Y axis (metric)", numeric_cols)
                    
                    fig = px.line(df.sort_values(x_trend).head(100), 
                                x=x_trend, y=y_trend,
                                title=f"Trend: {y_trend}",
                                color_discrete_sequence=['#667eea'])
                    st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("⚠️ Please clean your data in Step 3 first")

# ==================== TAB 6: VISUALIZATION ====================
with tab6:
    st.markdown('<div class="step-card"><h2>Step 6: Data Visualization</h2><p>Translate findings into compelling visual stories</p></div>', unsafe_allow_html=True)
    
    with st.expander("💡 Visualization Best Practices"):
        st.info("""
        **Choose the right chart:**
        - **Line Chart:** Trends over time, continuous data
        - **Bar Chart:** Comparisons across categories
        - **Scatter Plot:** Relationships between two variables
        - **Pie Chart:** Part-to-whole relationships (use sparingly)
        - **Heatmap:** Correlation matrices, density patterns
        - **Area Chart:** Cumulative totals over time
        
        **Design Tips:**
        - Keep it simple and focused
        - Use appropriate colors
        - Label axes clearly
        - Add context with titles and legends
        """)
    
    if st.session_state.cleaned_data is not None:
        df = st.session_state.cleaned_data
        st.session_state.progress['visualization'] = True
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        st.markdown("### 📊 Create Custom Visualizations")
        
        viz_type = st.selectbox(
            "Select Chart Type",
            ["Line Chart", "Bar Chart", "Scatter Plot", "Pie Chart", "Heatmap", "Area Chart"]
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            if viz_type in ["Line Chart", "Bar Chart", "Scatter Plot", "Area Chart"]:
                x_axis = st.selectbox("X-Axis", df.columns)
                y_axis = st.selectbox("Y-Axis", numeric_cols)
                
                if viz_type == "Line Chart":
                    fig = px.line(df, x=x_axis, y=y_axis, title=f"{y_axis} by {x_axis}")
                elif viz_type == "Bar Chart":
                    fig = px.bar(df, x=x_axis, y=y_axis, title=f"{y_axis} by {x_axis}")
                elif viz_type == "Scatter Plot":
                    fig = px.scatter(df, x=x_axis, y=y_axis, title=f"{y_axis} vs {x_axis}")
                elif viz_type == "Area Chart":
                    fig = px.area(df, x=x_axis, y=y_axis, title=f"{y_axis} by {x_axis}")
                
                st.plotly_chart(fig, use_container_width=True)
            
            elif viz_type == "Pie Chart":
                cat_col = st.selectbox("Category", df.columns)
                value_counts = df[cat_col].value_counts().head(10)
                
                fig = px.pie(values=value_counts.values, names=value_counts.index,
                           title=f"Distribution of {cat_col}")
                st.plotly_chart(fig, use_container_width=True)
            
            elif viz_type == "Heatmap":
                if len(numeric_cols) >= 2:
                    corr = df[numeric_cols].corr()
                    fig = px.imshow(corr, text_auto='.2f', color_continuous_scale='RdBu',
                                  title="Correlation Heatmap")
                    st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### 💡 Visualization Best Practices")
            st.info("""
            **Chart Selection Guide:**
            
            📈 **Line Charts** → Trends over time
            📊 **Bar Charts** → Category comparisons
            🔵 **Scatter Plots** → Variable relationships
            🥧 **Pie Charts** → Proportions (max 5-7 slices)
            🌡️ **Heatmaps** → Correlation/density patterns
            📐 **Area Charts** → Cumulative values
            
            **Pro Tips:**
            - Avoid 3D charts (hard to read)
            - Use color meaningfully
            - Don't overload with data
            - Tell a story with your viz
            """)
    else:
        st.warning("⚠️ Please clean your data in Step 3 first")

# ==================== TAB 7: INSIGHTS & RECOMMENDATIONS ====================
with tab7:
    st.markdown('<div class="step-card"><h2>Step 7: Communication & Implementation</h2><p>Present findings and actionable recommendations</p></div>', unsafe_allow_html=True)
    
    with st.expander("💡 Creating Actionable Insights"):
        st.info("""
        **Good insights are:**
        - Specific and measurable
        - Supported by data evidence
        - Actionable (can be implemented)
        - Relevant to business objectives
        - Clear and concise
        
        **Example Good Insight:**
        "Sales dropped 23% in Midwest region due to increased competition. 
        Recommendation: Increase digital ad spend by 15% targeting this region."
        
        **vs Bad Insight:**
        "Sales are down. Need more marketing."
        """)
    
    if st.session_state.cleaned_data is not None:
        df = st.session_state.cleaned_data
        st.session_state.progress['insights'] = True
        
        st.markdown("### 📝 Generate Analysis Report")
        
        # Summary Statistics
        st.markdown("#### 📊 Executive Summary")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Records", len(df))
        with col2:
            st.metric("Variables Analyzed", len(df.columns))
        with col3:
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            st.metric("Numeric Features", len(numeric_cols))
        with col4:
            completeness = (1 - df.isnull().sum().sum() / (df.shape[0] * df.shape[1])) * 100
            st.metric("Data Quality", f"{completeness:.1f}%")
        
        st.markdown("---")
        
        # Key Findings Section
        st.markdown("#### 🔍 Key Findings")
        
        findings = st.text_area(
            "Document your key discoveries",
            placeholder="Example:\n1. Sales decreased by 23% in Q3 2024\n2. Customer churn is highest among 25-34 age group\n3. Mobile app usage correlates strongly with purchase frequency",
            height=150
        )
        
        # Recommendations Section
        st.markdown("#### 💡 Actionable Recommendations")
        
        recommendations = st.text_area(
            "Provide specific actions based on your analysis",
            placeholder="Example:\n1. Increase digital ad spend in Midwest region by 15%\n2. Launch targeted retention campaign for 25-34 demographic\n3. Optimize mobile app experience to boost conversions",
            height=150
        )
        
        # Implementation Plan
        st.markdown("#### 🎯 Implementation Plan")
        
        col1, col2 = st.columns(2)
        
        with col1:
            priority = st.selectbox("Priority Level", ["High", "Medium", "Low"])
            timeline = st.text_input("Implementation Timeline", "Next 30 days")
            owner = st.text_input("Responsible Team/Person", "Marketing Team")
        
        with col2:
            budget_req = st.number_input("Budget Required ($)", min_value=0, value=5000)
            expected_impact = st.text_input("Expected Impact", "15% increase in regional sales")
            metrics_track = st.text_input("Metrics to Track", "Weekly sales, Customer acquisition cost")
        
        st.markdown("---")
        
        # Generate Report Button
        if st.button("📄 Generate Final Report", type="primary"):
            st.markdown("### 📋 Final Analysis Report")
            
            report = f"""
            ## Data Analysis Report
            **Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            
            ### Original Objective
            {st.session_state.objective if st.session_state.objective else "Not specified"}
            
            ### Key Performance Indicators
            {st.session_state.kpis if st.session_state.kpis else "Not specified"}
            
            ---
            
            ### Executive Summary
            - **Total Records Analyzed:** {len(df):,}
            - **Variables:** {len(df.columns)}
            - **Data Quality Score:** {completeness:.1f}%
            
            ### Key Findings
            {findings if findings else "No findings documented"}
            
            ### Recommendations
            {recommendations if recommendations else "No recommendations provided"}
            
            ### Implementation Plan
            - **Priority:** {priority}
            - **Timeline:** {timeline}
            - **Owner:** {owner}
            - **Budget Required:** ${budget_req:,}
            - **Expected Impact:** {expected_impact}
            - **Metrics to Track:** {metrics_track}
            
            ---
            
            ### Next Steps
            1. Review and approve recommendations with stakeholders
            2. Allocate resources and budget
            3. Begin implementation as per timeline
            4. Set up monitoring dashboard for tracking metrics
            5. Schedule follow-up review in 30 days
            """
            
            st.markdown(report)
            
            st.download_button(
                label="📥 Download Report as Text",
                data=report,
                file_name=f"analysis_report_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain"
            )
            
            st.success("✅ Report generated successfully! Share with your stakeholders.")
        
        # Feedback Loop
        st.markdown("---")
        st.markdown("#### 🔄 Feedback Loop")
        st.info("""
        **After implementation, monitor these indicators:**
        1. Are KPIs improving as expected?
        2. Are there any unintended consequences?
        3. What adjustments are needed?
        4. Should we revisit our analysis with new data?
        
        **Schedule regular reviews** to ensure your recommendations are delivering results.
        """)
        
    else:
        st.warning("⚠️ Please complete the previous steps first")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p style='margin-bottom: 15px;'>Built with ❤️ using Streamlit | Complete Data Analysis Platform v2.0</p>
        <div>
            <a href='https://github.com/rahul25118' target='_blank' style='margin: 0 10px; text-decoration: none;'>
                <img src='https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white' alt='GitHub'>
            </a>
            <a href='https://www.linkedin.com/in/rahul-mishra-b71ba21b8/' target='_blank' style='margin: 0 10px; text-decoration: none;'>
                <img src='https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white' alt='LinkedIn'>
            </a>
        </div>
        <p style='margin-top: 15px; font-size: 14px;'>Connect with me for collaborations and feedback!</p>
    </div>
""", unsafe_allow_html=True)
