import streamlit as st
from google.cloud import bigquery
from google.oauth2 import service_account

st.set_page_config(
     page_title="example app",
     page_icon=":knife_fork_plate:",
     layout="centered",
     initial_sidebar_state="auto",
     menu_items={
         'Get Help': 'https://developers.snowflake.com',
         'About': "This is an *extremely* cool app powered by Snowpark for Python & Streamlit"
     }
 )


@st.cache_resource
def get_bigquery_client():
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["bigquery_api"]
    )
    return bigquery.Client(credentials=credentials)

client = get_bigquery_client()

@st.cache_data
def get_dataframe_from_sql(query):
    df = client.query(query).to_dataframe()
    return df


st.title("BigQuery App")
my_first_query = """
    SELECT
    CAST(file_downloads.timestamp  AS DATE) AS file_downloads_timestamp_date,
    file_downloads.file.project AS file_downloads_file__project,
    COUNT(*) AS file_downloads_count
    FROM `bigquery-public-data.pypi.file_downloads`
    AS file_downloads
    WHERE (file_downloads.file.project = 'streamlit')
        AND (file_downloads.timestamp >= timestamp_add(current_timestamp(), INTERVAL -(5) DAY))
    GROUP BY 1,2
    """

downloads_df = get_dataframe_from_sql(my_first_query)
st.line_chart(downloads_df, x="file_downloads_timestamp_date", y="file_downloads_count")