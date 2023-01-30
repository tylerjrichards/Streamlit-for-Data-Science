import snowflake.connector
import streamlit as st


def initialize_snowflake_connection():
    session = snowflake.connector.connect(
        **st.secrets["snowflake"], client_session_keep_alive=True
    )
    return session


session = initialize_snowflake_connection()

sql_query = """
    SELECT
    l_returnflag,
    sum(l_quantity) as sum_qty,
    sum(l_extendedprice) as sum_base_price
    FROM
    snowflake_sample_data.tpch_sf1.lineitem
    WHERE
    l_shipdate <= dateadd(day, -90, to_date('1998-12-01'))
    GROUP BY 1
"""


def run_query(session, sql_query):
    df = session.cursor().execute(sql_query).fetch_pandas_all()
    return df


df = run_query(session, sql_query)

st.title("Snowflake TPC-H Explorer")
col_to_graph = st.selectbox(
    "Select a column to graph", ["Order Quantity", "Base Price"]
)
df["SUM_QTY"] = df["SUM_QTY"].astype(float)
df["SUM_BASE_PRICE"] = df["SUM_BASE_PRICE"].astype(float)

if col_to_graph == "Order Quantity":
    st.bar_chart(data=df, x="L_RETURNFLAG", y="SUM_QTY")
else:
    st.bar_chart(data=df, x="L_RETURNFLAG", y="SUM_BASE_PRICE")
