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
    </style>
""", unsafe_allow_html=True)

# ========== CRITICAL FIX: Initialize ALL session state variables ==========
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
if 'selected_column' not in st.session_state:
    st.session_state.selected_column = None
if 'treatment_method' not in st.session_state:
    st.session_state.treatment_method = None
if 'custom_value' not in st.session_state:
    st.session_state.custom_value = None

# ========== DEFINE CLEANING FUNCTIONS ==========
def fill_column_with_mean(column_name):
    """Fill missing values in a column with mean"""
    if st.session_state.cleaned_data is not None and column_name in st.session_state.cleaned_data.columns:
        mean_val = st.session_state.cleaned_data[column_name].mean()
        st.session_state.cleaned_data[column_name] = st.session_state.cleaned_data[column_name].fillna(mean_val)
        return f"✅ Filled {column_name} with mean: {mean_val:.2f}"
    return "❌ Error: Could not fill with mean"

def fill_column_with_median(column_name):
    """Fill missing values in a column with median"""
    if st.session_state.cleaned_data is not None and column_name in st.session_state.cleaned_data.columns:
        median_val = st.session_state.cleaned_data[column_name].median()
        st.session_state.cleaned_data[column_name] = st.session_state.cleaned_data[column_name].fillna(median_val)
        return f"✅ Filled {column_name} with median: {median_val:.2f}"
    return "❌ Error: Could not fill with median"

def fill_column_with_zero(column_name):
    """Fill missing values in a column with 0"""
    if st.session_state.cleaned_data is not None and column_name in st.session_state.cleaned_data.columns:
        st.session_state.cleaned_data[column_name] = st.session_state.cleaned_data[column_name].fillna(0)
        return f"✅ Filled {column_name} with 0"
    return "❌ Error: Could not fill with 0"

def fill_column_with_custom(column_name, custom_value):
    """Fill missing values in a column with custom value"""
    if st.session_state.cleaned_data is not None and column_name in st.session_state.cleaned_data.columns:
        st.session_state.cleaned_data[column_name] = st.session_state.cleaned_data[column_name].fillna(custom_value)
        return f"✅ Filled {column_name} with {custom_value}"
    return "❌ Error: Could not fill with custom value"

def fill_column_with_mode(column_name):
    """Fill missing values in a column with mode"""
    if st.session_state.cleaned_data is not None and column_name in st.session_state.cleaned_data.columns:
        mode_val = st.session_state.cleaned_data[column_name].mode()
        fill_val = mode_val[0] if len(mode_val) > 0 else "Unknown"
        st.session_state.cleaned_data[column_name] = st.session_state.cleaned_data[column_name].fillna(fill_val)
        return f"✅ Filled {column_name} with mode: {fill_val}"
    return "❌ Error: Could not fill with mode"

def fill_column_with_unknown(column_name):
    """Fill missing values in a column with 'Unknown'"""
    if st.session_state.cleaned_data is not None and column_name in st.session_state.cleaned_data.columns:
        st.session_state.cleaned_data[column_name] = st.session_state.cleaned_data[column_name].fillna("Unknown")
        return f"✅ Filled {column_name} with 'Unknown'"
    return "❌ Error: Could not fill with 'Unknown'"

def drop_rows_with_missing(column_name):
    """Drop rows with missing values in specified column"""
    if st.session_state.cleaned_data is not None and column_name in st.session_state.cleaned_data.columns:
        before = len(st.session_state.cleaned_data)
        st.session_state.cleaned_data = st.session_state.cleaned_data.dropna(subset=[column_name])
        after = len(st.session_state.cleaned_data)
        removed = before - after
        return f"✅ Dropped {removed} rows with missing {column_name}"
    return "❌ Error: Could not drop rows"

def remove_duplicates():
    """Remove duplicate rows"""
    if st.session_state.cleaned_data is not None:
        before = len(st.session_state.cleaned_data)
        st.session_state.cleaned_data = st.session_state.cleaned_data.drop_duplicates()
        after = len(st.session_state.cleaned_data)
        removed = before - after
        return f"✅ Removed {removed} duplicate rows"
    return "❌ Error: Could not remove duplicates"

def drop_all_missing_rows():
    """Drop all rows with any missing values"""
    if st.session_state.cleaned_data is not None:
        before = len(st.session_state.cleaned_data)
        st.session_state.cleaned_data = st.session_state.cleaned_data.dropna()
        after = len(st.session_state.cleaned_data)
        removed = before - after
        return f"✅ Dropped {removed} rows with any missing values"
    return "❌ Error: Could not drop rows"

def reset_column(column_name):
    """Reset column to original values"""
    if (st.session_state.data is not None and st.session_state.cleaned_data is not None and 
        column_name in st.session_state.data.columns):
        st.session_state.cleaned_data[column_name] = st.session_state.data[column_name].copy()
        return f"✅ Reset {column_name} to original values"
    return "❌ Error: Could not reset column"

def reset_all_changes():
    """Reset all changes to original data"""
    if st.session_state.data is not None:
        st.session_state.cleaned_data = st.session_state.data.copy()
        return "✅ All changes reset to original data"
    return "❌ Error: Could not reset changes"

# ========== CALLBACK FUNCTIONS ==========
def apply_treatment_callback():
    """Callback for applying treatment to selected column"""
    if (st.session_state.selected_column and st.session_state.treatment_method):
        result = ""
        
        if st.session_state.treatment_method == "Fill with Mean":
            result = fill_column_with_mean(st.session_state.selected_column)
        elif st.session_state.treatment_method == "Fill with Median":
            result = fill_column_with_median(st.session_state.selected_column)
        elif st.session_state.treatment_method == "Fill with 0":
            result = fill_column_with_zero(st.session_state.selected_column)
        elif st.session_state.treatment_method == "Fill with Custom Value":
            result = fill_column_with_custom(st.session_state.selected_column, st.session_state.custom_value)
        elif st.session_state.treatment_method == "Fill with Mode":
            result = fill_column_with_mode(st.session_state.selected_column)
        elif st.session_state.treatment_method == "Fill with 'Unknown'":
            result = fill_column_with_unknown(st.session_state.selected_column)
        elif st.session_state.treatment_method == "Drop Rows":
            result = drop_rows_with_missing(st.session_state.selected_column)
        
        if result:
            st.session_state.last_result = result
            st.session_state.progress['cleaning'] = True
            
            # Clear selections
            st.session_state.selected_column = None
            st.session_state.treatment_method = None
            st.session_state.custom_value = None
            
            # Force rerun
            st.rerun()

def remove_duplicates_callback():
    """Callback for removing duplicates"""
    result = remove_duplicates()
    if result:
        st.session_state.last_result = result
        st.rerun()

def drop_all_missing_callback():
    """Callback for dropping all missing rows"""
    result = drop_all_missing_rows()
    if result:
        st.session_state.last_result = result
        st.rerun()

def reset_all_callback():
    """Callback for resetting all changes"""
    result = reset_all_changes()
    if result:
        st.session_state.last_result = result
        st.rerun()

def reset_column_callback():
    """Callback for resetting a column"""
    if st.session_state.selected_column:
        result = reset_column(st.session_state.selected_column)
        if result:
            st.session_state.last_result = result
            st.rerun()

# Title
st.markdown("""
    <h1 style='text-align: center; background: linear-gradient(135deg, #3B82F6 0%, #8B5CF6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; padding: 20px; font-size: 48px;'>
        📊 Complete Data Analysis Platform
    </h1>
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

# ==================== TAB 2: DATA COLLECTION ====================
with tab2:
    st.markdown('<div class="step-card"><h2>Step 2: Data Collection</h2><p>Gather raw data from your identified sources</p></div>', unsafe_allow_html=True)
    
    st.markdown("### 📥 Upload Your Dataset")
    
    uploaded_file = st.file_uploader("Choose a CSV file", type=['csv'])
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            
            st.session_state.data = df
            st.session_state.cleaned_data = df.copy()
            st.session_state.progress['collection'] = True
            
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
            
        except Exception as e:
            st.error(f"Error loading file: {str(e)}")
    else:
        st.info("👆 Please upload a CSV file to begin data collection")

# ==================== TAB 3: DATA CLEANING - GUARANTEED WORKING ====================
with tab3:
    st.markdown('<div class="step-card"><h2>Step 3: Data Cleaning</h2><p>Transform raw data into a clean, analysis-ready dataset</p></div>', unsafe_allow_html=True)
    
    # Show last result if exists
    if 'last_result' in st.session_state and st.session_state.last_result:
        if "✅" in st.session_state.last_result:
            st.success(st.session_state.last_result)
        else:
            st.error(st.session_state.last_result)
    
    if st.session_state.data is not None:
        # Initialize cleaned_data if None
        if st.session_state.cleaned_data is None:
            st.session_state.cleaned_data = st.session_state.data.copy()
        
        df = st.session_state.cleaned_data
        
        st.markdown("### 📊 Current Data Status")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Rows", len(df))
        with col2:
            st.metric("Total Columns", len(df.columns))
        with col3:
            missing_total = df.isnull().sum().sum()
            st.metric("Missing Values", missing_total)
        with col4:
            duplicates = df.duplicated().sum()
            st.metric("Duplicates", duplicates)
        
        st.markdown("---")
        
        # Quick Actions
        st.markdown("### ⚡ Quick Actions")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🧹 Remove All Duplicates", use_container_width=True, on_click=remove_duplicates_callback):
                pass
        
        with col2:
            if st.button("🗑️ Drop All Missing Rows", use_container_width=True, on_click=drop_all_missing_callback):
                pass
        
        with col3:
            if st.button("🔄 Reset All Changes", use_container_width=True, on_click=reset_all_callback):
                pass
        
        st.markdown("---")
        
        # Find columns with missing values
        missing_cols = df.columns[df.isnull().any()].tolist()
        
        if len(missing_cols) > 0:
            st.markdown(f"### 🔍 Found {len(missing_cols)} Columns with Missing Values")
            
            # Display missing values summary
            missing_data = []
            for col in missing_cols:
                missing_count = df[col].isnull().sum()
                missing_percent = (missing_count / len(df) * 100)
                missing_data.append({
                    'Column': col,
                    'Missing Count': missing_count,
                    'Missing %': f"{missing_percent:.1f}%",
                    'Data Type': str(df[col].dtype)
                })
            
            missing_df = pd.DataFrame(missing_data)
            st.dataframe(missing_df, use_container_width=True)
            
            st.markdown("---")
            
            # Column selection
            st.markdown("### 🎯 Select Column to Treat")
            
            selected_col = st.selectbox(
                "Choose a column:",
                missing_cols,
                key="column_selector"
            )
            
            if selected_col:
                # Store in session state
                st.session_state.selected_column = selected_col
                
                # Show column info
                col_missing = df[selected_col].isnull().sum()
                col_type = df[selected_col].dtype
                
                st.info(f"**Selected:** {selected_col}")
                st.info(f"**Missing Values:** {col_missing} ({col_missing/len(df)*100:.1f}%)")
                st.info(f"**Data Type:** {col_type}")
                
                # Show sample values
                if col_missing < len(df):
                    non_missing = df[selected_col].dropna().head(5).tolist()
                    st.write(f"**Sample values:** {non_missing}")
                
                st.markdown("---")
                st.markdown("### ⚙️ Select Treatment Method")
                
                # Treatment options based on data type
                if pd.api.types.is_numeric_dtype(col_type):
                    treatment_options = [
                        "Fill with Mean",
                        "Fill with Median", 
                        "Fill with 0",
                        "Fill with Custom Value",
                        "Drop Rows"
                    ]
                else:
                    treatment_options = [
                        "Fill with Mode",
                        "Fill with 'Unknown'",
                        "Fill with Custom Value",
                        "Drop Rows"
                    ]
                
                treatment_method = st.radio(
                    "Choose treatment method:",
                    treatment_options,
                    key="treatment_selector"
                )
                
                # Store in session state
                st.session_state.treatment_method = treatment_method
                
                # Custom value input if needed
                if treatment_method == "Fill with Custom Value":
                    if pd.api.types.is_numeric_dtype(col_type):
                        custom_val = st.number_input(
                            "Enter numeric value:",
                            value=0.0,
                            key="custom_numeric"
                        )
                    else:
                        custom_val = st.text_input(
                            "Enter text value:",
                            value="",
                            key="custom_text"
                        )
                    st.session_state.custom_value = custom_val
                
                st.markdown("---")
                
                # Action buttons
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button(
                        f"✅ Apply {treatment_method}",
                        type="primary",
                        use_container_width=True,
                        on_click=apply_treatment_callback
                    ):
                        pass
                
                with col2:
                    if st.button(
                        f"🔄 Reset {selected_col}",
                        use_container_width=True,
                        on_click=reset_column_callback
                    ):
                        pass
        
        else:
            st.success("🎉 No missing values found in the dataset!")
        
        # Visualization
        st.markdown("---")
        st.markdown("### 📊 Missing Values Visualization")
        
        current_missing = df.isnull().sum()
        current_missing = current_missing[current_missing > 0]
        
        if len(current_missing) > 0:
            fig = px.bar(
                x=current_missing.index,
                y=current_missing.values,
                title="Current Missing Values",
                labels={'x': 'Column', 'y': 'Missing Count'},
                color=current_missing.values,
                color_continuous_scale='Reds'
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.success("✅ All missing values have been treated!")
        
        # Data Preview
        st.markdown("---")
        st.markdown("### 📋 Current Data Preview")
        
        st.dataframe(df.head(10), use_container_width=True)
        
        # Download Section
        st.markdown("---")
        st.markdown("### 📥 Download Your Data")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.session_state.data is not None:
                csv_original = st.session_state.data.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Original Data",
                    data=csv_original,
                    file_name="original_data.csv",
                    mime="text/csv",
                    use_container_width=True
                )
        
        with col2:
            if st.session_state.cleaned_data is not None:
                csv_cleaned = st.session_state.cleaned_data.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Cleaned Data",
                    data=csv_cleaned,
                    file_name="cleaned_data.csv",
                    mime="text/csv",
                    type="primary",
                    use_container_width=True
                )
    
    else:
        st.warning("⚠️ Please upload data in Step 2 first")

# ==================== OTHER TABS (Simplified) ====================
with tab4:
    st.markdown('<div class="step-card"><h2>Step 4: Exploratory Data Analysis</h2></div>', unsafe_allow_html=True)
    
    if st.session_state.cleaned_data is not None:
        df = st.session_state.cleaned_data
        st.session_state.progress['eda'] = True
        
        st.markdown("### 📊 Descriptive Statistics")
        st.dataframe(df.describe(), use_container_width=True)
        
    else:
        st.warning("⚠️ Please clean your data in Step 3 first")

with tab5:
    st.markdown('<div class="step-card"><h2>Step 5: Data Analysis & Modeling</h2></div>', unsafe_allow_html=True)
    
    if st.session_state.cleaned_data is not None:
        st.session_state.progress['analysis'] = True
        st.info("Analysis features will be available after data cleaning")

with tab6:
    st.markdown('<div class="step-card"><h2>Step 6: Data Visualization</h2></div>', unsafe_allow_html=True)
    
    if st.session_state.cleaned_data is not None:
        st.session_state.progress['visualization'] = True
        st.info("Visualization features will be available after data cleaning")

with tab7:
    st.markdown('<div class="step-card"><h2>Step 7: Communication & Implementation</h2></div>', unsafe_allow_html=True)
    
    if st.session_state.cleaned_data is not None:
        st.session_state.progress['insights'] = True
        st.info("Insights features will be available after data analysis")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p>Built with ❤️ using Streamlit | Complete Data Analysis Platform</p>
    </div>
""", unsafe_allow_html=True)
