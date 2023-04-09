import numpy as np
import pandas as pd
import plotly.express as px
import requests
import streamlit as st
from streamlit_lottie import st_lottie

st.set_page_config(layout="wide")


def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


file_url = "https://assets4.lottiefiles.com/temp/lf20_aKAfIn.json"
lottie_book = load_lottieurl(file_url)
st_lottie(lottie_book, speed=1, height=200, key="initial")

st.title("Analyzing Your Goodreads Reading Habits")
st.subheader("A Web App by [Tyler Richards](http://www.tylerjrichards.com)")

"""
Hey there! Welcome to Tyler's Goodreads Analysis App. This app analyzes (and never stores!)
the books you've read using the popular service Goodreads, including looking at the distribution
of the age and length of books you've read. Give it a go by uploading your data below!
"""

goodreads_file = st.file_uploader("Please Import Your Goodreads Data")
if goodreads_file is None:
    books_df = pd.read_csv("goodreads_history.csv")
else:
    books_df = pd.read_csv(goodreads_file)

# year finished
books_df["Year Finished"] = pd.to_datetime(books_df["Date Read"]).dt.year
books_per_year = books_df.groupby("Year Finished")["Book Id"].count().reset_index()
books_per_year.columns = ["Year Finished", "Count"]
fig_year_finished = px.bar(
    books_per_year, x="Year Finished", y="Count", title="Books Finished per Year"
)


# time difference
books_df["days_to_finish"] = (
    pd.to_datetime(books_df["Date Read"]) - pd.to_datetime(books_df["Date Added"])
).dt.days
books_finished_filtered = books_df[
    (books_df["Exclusive Shelf"] == "read") & (books_df["days_to_finish"] >= 0)
]
fig_days_finished = px.histogram(
    books_finished_filtered,
    x="days_to_finish",
    title="Time Between Date Added And Date Finished",
    labels={"days_to_finish": "days"},
)

# num pages
fig_num_pages = px.histogram(
    books_df, x="Number of Pages", title="Book Length Histogram"
)

# publication year
books_publication_year = (
    books_df.groupby("Original Publication Year")["Book Id"].count().reset_index()
)
books_publication_year.columns = ["Year Published", "Count"]

fig_year_published = px.bar(
    books_publication_year, x="Year Published", y="Count", title="Book Age Plot"
)
fig_year_published.update_xaxes(range=[1850, 2021])

# rating
books_rated = books_df[books_df["My Rating"] != 0]
fig_my_rating = px.histogram(books_rated, x="My Rating", title="User Rating")

fig_avg_rating = px.histogram(
    books_rated, x="Average Rating", title="Average Goodreads Rating"
)
avg_difference = np.round(
    np.mean(books_rated["My Rating"] - books_rated["Average Rating"]), 2
)
if avg_difference >= 0:
    sign = "higher"
else:
    sign = "lower"

if goodreads_file is None:
    st.subheader("Tyler's Analysis Results:")
else:
    st.subheader("Your Analysis Results:")
books_finished = books_df[books_df["Exclusive Shelf"] == "read"]
u_books = len(books_finished["Book Id"].unique())
u_authors = len(books_finished["Author"].unique())
mode_author = books_finished["Author"].mode()[0]
st.write(
    f"It looks like you have finished {u_books} books with a total of {u_authors} unique authors. Your most read author is {mode_author}!"
)
st.write(
    f"Your app results can be found below, we have analyzed everything from your book length distribution to how you rate books. Take a look around, all the graphs are interactive!"
)

row1_col1, row1_col2 = st.columns(2)
row2_col1, row2_col2 = st.columns(2)
row3_col1, row3_col2 = st.columns(2)

with row1_col1:
    mode_year_finished = int(books_df["Year Finished"].mode()[0])
    st.plotly_chart(fig_year_finished)
    st.write(f"You finished the most books in {mode_year_finished}. Awesome job!")
with row1_col2:
    st.plotly_chart(fig_days_finished)
    mean_days_to_finish = int(books_finished_filtered["days_to_finish"].mean())
    st.write(
        f"It took you an average of {mean_days_to_finish} days between when the book was added to Goodreads and when you finished the book. This is not a perfect metric, as you may have added this book to a to-read list!"
    )
with row2_col1:
    st.plotly_chart(fig_num_pages)
    avg_pages = int(books_df["Number of Pages"].mean())
    st.write(
        f"Your books are an average of {avg_pages} pages long, check out the distribution above!"
    )
with row2_col2:
    st.plotly_chart(fig_year_published)
    st.write(
        "This chart is zoomed into the period of 1850-2021, but is interactive so try zooming in/out on interesting periods!"
    )
with row3_col1:
    st.plotly_chart(fig_my_rating)
    avg_my_rating = round(books_rated["My Rating"].mean(), 2)
    st.write(f"You rate books an average of {avg_my_rating} stars on Goodreads.")
with row3_col2:
    st.plotly_chart(fig_avg_rating)
    st.write(
        f"You rate books {sign} than the average Goodreads user by {abs(avg_difference)}!"
    )
