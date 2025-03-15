import streamlit as st
import pandas as pd

pd.set_option('display.max_columns', 100)

# Load data
df = pd.read_csv("analysis.csv")

# Set page title and layout
st.set_page_config(page_title="Covid-19 Data Visualization", layout="wide")

# Title and description
st.title("Covid-19 Data Visualization App")
st.markdown(
    """
    Welcome to the Covid-19 Data Visualization App.
    This app provides insights into Covid-19 cases powered by **Streamlit.io**
    """
)


# Count occurrences of each category
sex_counts = df['SEX'].value_counts()
intubation_counts = df['INTUBATED'].value_counts()

# Display key statistics
col1, col2, col3, col4 = st.columns(4)

with col1:
    female_cases = sex_counts.get('FEMALE')
    st.markdown(f"""
        <span style='color:gray; font-size:20px;'>Total Female Cases</span><br>
        <span style='color:gray; font-size:24px; font-weight:bold;'>{female_cases:,}</span>
    """, unsafe_allow_html=True)

with col2:
    male_cases = sex_counts.get('MALE')
    st.markdown(f"""
        <span style='color:gray; font-size:20px;'>Total Male Cases</span><br>
        <span style='color:gray; font-size:24px; font-weight:bold;'>{male_cases:,}</span>
    """, unsafe_allow_html=True)

with col3:
    total_cases = df.size
    st.markdown(f"""
        <span style='color:gray; font-size:20px;'>Total Cases</span><br>
        <span style='color:gray; font-size:24px; font-weight:bold;'>{total_cases:,}</span>
    """, unsafe_allow_html=True)

with col4:
    intubation_cases = intubation_counts.get('YES')
    st.markdown(f"""
        <span style='color:gray; font-size:20px;'>Total Intubation Cases</span><br>
        <span style='color:gray; font-size:24px; font-weight:bold;'>{intubation_cases:,}</span>
    """, unsafe_allow_html=True)

st.dataframe(df)

st.markdown(
    """
    Navigate to the charts page for detailed visualizations.
    """
)

