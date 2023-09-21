import streamlit as st
from google.cloud import bigquery
from google.oauth2 import service_account
from queries import get_streamlit_pypi_data


@st.cache_resource
def get_bigquery_client():
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["bigquery_service_account"]
    )
    return bigquery.Client(credentials=credentials)


client = get_bigquery_client()


@st.cache_data
def get_dataframe_from_sql(query):
    df = client.query(query).to_dataframe()
    return df


st.title("BigQuery App")
days_lookback = st.slider(
    "How many days of data do you want to see?", min_value=1, max_value=30, value=5
)
pypi_query = get_streamlit_pypi_data(days_lookback)

downloads_df = get_dataframe_from_sql(pypi_query)
st.line_chart(downloads_df, x="file_downloads_timestamp_date", y="file_downloads_count")
