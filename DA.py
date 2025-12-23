import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Simple Data Cleaner", layout="wide")
st.title("🧹 Simple Data Cleaner")

# Initialize session state
if 'df' not in st.session_state:
    st.session_state.df = None
if 'df_original' not in st.session_state:
    st.session_state.df_original = None

# Upload section
uploaded_file = st.file_uploader("Upload CSV", type=['csv'])

if uploaded_file is not None:
    if st.session_state.df is None:
        df = pd.read_csv(uploaded_file)
        st.session_state.df = df
        st.session_state.df_original = df.copy()
    
    df = st.session_state.df
    
    # Show current data
    st.subheader("Current Data")
    st.dataframe(df.head())
    
    # Show missing values
    st.subheader("Missing Values")
    missing = df.isnull().sum()
    missing = missing[missing > 0]
    
    if len(missing) > 0:
        for col, count in missing.items():
            st.write(f"**{col}**: {count} missing values")
            
            # Create a form for each column
            with st.form(key=f"form_{col}"):
                st.write(f"Treat **{col}**")
                
                if pd.api.types.is_numeric_dtype(df[col]):
                    method = st.radio(f"Method for {col}", 
                                     ["Fill with Mean", "Fill with 0", "Drop Rows"],
                                     key=f"method_{col}")
                else:
                    method = st.radio(f"Method for {col}", 
                                     ["Fill with 'Unknown'", "Drop Rows"],
                                     key=f"method_{col}")
                
                submit = st.form_submit_button(f"Apply to {col}")
                
                if submit:
                    if method == "Fill with Mean":
                        fill_val = df[col].mean()
                        df[col] = df[col].fillna(fill_val)
                        st.success(f"Filled {col} with mean: {fill_val:.2f}")
                        
                    elif method == "Fill with 0":
                        df[col] = df[col].fillna(0)
                        st.success(f"Filled {col} with 0")
                        
                    elif method == "Fill with 'Unknown'":
                        df[col] = df[col].fillna("Unknown")
                        st.success(f"Filled {col} with 'Unknown'")
                        
                    elif method == "Drop Rows":
                        df = df.dropna(subset=[col])
                        st.success(f"Dropped rows with missing {col}")
                    
                    # Update session state
                    st.session_state.df = df
                    st.experimental_rerun()
    else:
        st.success("No missing values!")
    
    # Download buttons
    st.subheader("Download")
    
    col1, col2 = st.columns(2)
    with col1:
        csv_original = st.session_state.df_original.to_csv(index=False)
        st.download_button("Download Original", csv_original, "original.csv")
    
    with col2:
        csv_cleaned = df.to_csv(index=False)
        st.download_button("Download Cleaned", csv_cleaned, "cleaned.csv")
    
    # Reset button
    if st.button("Reset All"):
        st.session_state.df = st.session_state.df_original.copy()
        st.experimental_rerun()
