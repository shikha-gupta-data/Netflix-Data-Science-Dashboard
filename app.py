
import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(
    page_title="Netflix Data Science Dashboard",
    layout="wide"
)

st.title("🎬 Netflix Data Science Dashboard")
st.write("Explore Netflix Movies and TV Shows")

if os.path.exists("Dataset.csv"):
    df = pd.read_csv("Dataset.csv")
else:
    uploaded_file = st.sidebar.file_uploader(
        "Upload Netflix Dataset",
        type=["csv"]
    )
    if uploaded_file is None:
        st.info("Please upload your Netflix CSV dataset.")
        st.stop()
    df = pd.read_csv(uploaded_file)

st.sidebar.header("Filters")

if "type" in df.columns:
    types = st.sidebar.multiselect(
        "Select Content Type",
        df["type"].dropna().unique(),
        default=df["type"].dropna().unique()
    )
    df = df[df["type"].isin(types)]

col1, col2, col3 = st.columns(3)

col1.metric("Total Titles", len(df))

if "type" in df.columns:
    col2.metric("Movies", (df["type"] == "Movie").sum())
    col3.metric("TV Shows", (df["type"] == "TV Show").sum())

if "type" in df.columns:
    st.subheader("Content Type Distribution")
    fig = px.pie(df, names="type", hole=0.4)
    st.plotly_chart(fig, use_container_width=True)

if "release_year" in df.columns:
    st.subheader("Year-wise Content Growth Trend")
    yearly = df.groupby("release_year").size().reset_index(name="Titles")
    fig = px.line(
        yearly,
        x="release_year",
        y="Titles",
        markers=True
    )
    st.plotly_chart(fig, use_container_width=True)

if "listed_in" in df.columns:
    st.subheader("Top 10 Genres")
    genres = (
        df["listed_in"]
        .dropna()
        .str.split(",")
        .explode()
        .str.strip()
    )
    genre_data = genres.value_counts().head(10).reset_index()
    genre_data.columns = ["Genre", "Count"]
    fig = px.bar(
        genre_data,
        x="Count",
        y="Genre",
        orientation="h"
    )
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Netflix Dataset Preview")
st.dataframe(df, use_container_width=True)

st.download_button(
    "Download Filtered Dataset",
    df.to_csv(index=False),
    "netflix_filtered.csv",
    "text/csv"
)
