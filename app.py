import streamlit as st
import pandas as pd
# from pandas_profiling import ProfileReport
# import pandas_profiling
import ydata_profiling
from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
import sys
import os

st.set_page_config(page_title="Data Profiler",layout='wide')

def file_validator(file):
    filename = file.name
    name, extension = os.path.splitext(filename)
    
    if extension in ('.csv', '.xlsx'):
        return extension
    else:
        return False
    
def get_filesize(file):
    size_bytes = sys.getsizeof(file)
    size_mb = size_bytes / (1024**2)
    return size_mb

with st.sidebar:
    st.subheader("Upload a CSV or XLSX file")
    uploaded_file = st.file_uploader(label="Upload a CSV or XLSX file", 
                                    label_visibility="collapsed")
    
    if uploaded_file is not None:
        with st.expander(label="More settings"):
            minimal_report = st.checkbox(label="Do you want minimal report ?")
            
            display_mode = st.radio(label="Display mode : ",
                                    options=('Primary','Dark','Orange'),
                                    index=2)
            
            if display_mode == "Dark":
                dark_mode = True
                orange_mode = False
            elif display_mode =="Orange":
                dark_mode = False
                orange_mode = True
            else:
                dark_mode = False
                orange_mode = False 
    
if uploaded_file is not None:
    extension = file_validator(uploaded_file)
    if extension:
        file_size = get_filesize(uploaded_file)
        if file_size <=10:
            if extension == '.csv':
                # Read CSV file
                df = pd.read_csv(uploaded_file)
            else:
                # Read XLSX file
                xl_file = pd.ExcelFile(uploaded_file)
                sheets_names:tuple = tuple(xl_file.sheet_names)
                sheet_name:str = st.sidebar.selectbox(label="Select the Sheet : ",
                                            options=sheets_names)
                df = xl_file.parse(sheet_name)
                
                
            # Generate report
            with st.spinner("Generating Report..."):
                pr = ProfileReport(df=df,
                                minimal=minimal_report,
                                dark_mode=dark_mode,
                                orange_mode=orange_mode)
                
            
            st_profile_report(pr)
            st.toast("Report processing DONE !!!")
        else:
            st.error(f"Maximum allowed file size is 10 MB.\n But recieved {file_size} MB .")
    
    else:
        st.error("Kindly upload only .csv or .xlsx file")

else:
    st.title("Data Profiler")
    st.info("Upload your data in the left sidebar to generate Report!!!")
    