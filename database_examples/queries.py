def get_streamlit_pypi_data(day_filter):
    streamlit_pypy_query = f"""
    SELECT
    CAST(file_downloads.timestamp  AS DATE)
        AS file_downloads_timestamp_date,
    file_downloads.file.project AS file_downloads_file__project,
    COUNT(*) AS file_downloads_count
    FROM `bigquery-public-data.pypi.file_downloads`
    AS file_downloads
    WHERE (file_downloads.file.project = 'streamlit')
        AND (file_downloads.timestamp >=
        timestamp_add(current_timestamp(),
        INTERVAL -({day_filter}) DAY))
    GROUP BY 1,2
    """
    return streamlit_pypy_query