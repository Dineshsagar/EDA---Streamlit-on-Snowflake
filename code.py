import streamlit as st
import pandas as pd
from snowflake.snowpark.context import get_active_session
import ydata_profiling as ydp
import tempfile
# Set up the Snowflake session
session = get_active_session()

# CustomS for styling
st.markdown(
    """
    <style>
    body {
        background-image: url('https://i.imgur.com/Xx0w4qM.jpg'); /* Replace with your wallpaper URL */
        background-size: cover;
        color: #fff;
    }
    .stButton > button {
        background-color: #4CAF50; /* Green */
        color: white;
        font-size: 16px;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        transition: background-color 0.3s ease, transform 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #45a049; /* Darker green */
        transform: scale(1.05);
    }
    .header {
        text-align: center;
        color: #4CAF50;
        font-size: 36px;
        margin-top: 50px;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
    }
    .subheader {
        text-align: center;
        font-size: 22px;
        margin-bottom: 20px;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.6);
    }
    .card {
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 10px;
        padding: 20px;
        margin: 20px auto;
        max-width: 600px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    .benefits {
        background-color: rgba(255, 255, 255, 0.8);
        border-radius: 10px;
        padding: 20px;
        margin: 20px auto;
        max-width: 600px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    </style>
    """, unsafe_allow_html=True
)

# Title and description with emojis
st.markdown("<h1 class='header'>🎉 Welcome to Exploratory Data Analysis App 🎉</h1>", unsafe_allow_html=True)
st.markdown("<h2 class='subheader'>📊 Analyze your Snowflake tables with ease! Just enter the table name below.</h2>", unsafe_allow_html=True)

# Card for input
with st.container():
    
    table_name = st.text_input("🔍 Enter the Snowflake table name:")
    st.markdown("</div>", unsafe_allow_html=True)

# Benefits of Data Profiling
st.markdown("<h3>🌟 Benefits of Data Profiling:</h3>", unsafe_allow_html=True)
st.write("""
1. **Improved Data Quality:** Identify inaccuracies, inconsistencies, and missing values in your data.
2. **Enhanced Data Understanding:** Offers a comprehensive view of your dataset, including distributions and relationships.
3. **Compliance and Governance:** Ensures data meets regulatory standards and organizational policies.
4. **Time Efficiency:** Saves time by automating the data inspection process and highlighting critical issues.
""")
st.markdown("</div>", unsafe_allow_html=True)

if st.button("🚀 Generate Profiling Report"):
    if table_name:
        try:
            query = f"SELECT * FROM {table_name}"
            df = session.sql(query).to_pandas()

            # Check the number of rows
            num_rows = len(df)

            if num_rows < 10000:
                st.header('**Input DataFrame**')
                st.write(df)
            else:
                st.warning("⚠️ DataFrame has more than 10,000 rows. Skipping display of the table.")

            # Create a profile report using ydata_profiling
            profile = ydp.ProfileReport(df, title="Data Profiling Report", explorative=True)

            st.write('---')
            st.header('**Pandas Profiling Report Summary**')

            # Save the full report to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp_file:
                profile.to_file(tmp_file.name)
                tmp_file.seek(0)  # Go back to the beginning of the file

                # Provide a download button
                st.download_button(
                    label="📥 Download Full Report",
                    data=tmp_file.read(),
                    file_name="full_report.html",
                    mime="text/html"
                )

        except Exception as e:
            st.error(f"❌ Error: {e}")
    else:
        st.warning("⚠️ Please enter a valid table name.")
