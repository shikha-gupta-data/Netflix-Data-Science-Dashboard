
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Netflix Business Dashboard",
    page_icon="🎬",
    layout="wide"
)

# Professional Netflix Dashboard Styling
st.markdown("""
<style>
.stApp {
    background-color: #141414;
    color: white;
}

h1, h2, h3 {
    color: #E50914 !important;
    font-weight: bold;
}

div[data-testid="stMetric"] {
    background-color: #222222;
    border: 1px solid #E50914;
    padding: 20px;
    border-radius: 12px;
}

div[data-testid="stMetric"] label {
    color: white !important;
}

div[data-testid="stMetric"] [data-testid="stMetricValue"] {
    color: #E50914 !important;
}

section[data-testid="stSidebar"] {
    background-color: #222222;
}

.stDownloadButton button {
    background-color: #E50914;
    color: white;
    border-radius: 8px;
    border: none;
}
</style>
""", unsafe_allow_html=True)



df = pd.read_csv("Dataset.csv")

st.title("🎬 Netflix Business Insights Dashboard")
st.write("Interactive Data Science Dashboard")

# Sidebar filters
st.sidebar.header("Dashboard Filters")

content_types = ["All"] + sorted(df["type"].dropna().unique().tolist())
selected_type = st.sidebar.selectbox("Content Type", content_types)

countries = (
    df["country"].dropna().str.split(",").explode().str.strip().unique()
)
countries = sorted(countries)

selected_country = st.sidebar.selectbox(
    "Country",
    ["All"] + countries
)

years = sorted(df["release_year"].dropna().unique(), reverse=True)
selected_year = st.sidebar.selectbox(
    "Release Year",
    ["All"] + years
)

# Apply filters
filtered_df = df.copy()

if selected_type != "All":
    filtered_df = filtered_df[filtered_df["type"] == selected_type]

if selected_country != "All":
    filtered_df = filtered_df[
        filtered_df["country"].fillna("").str.contains(
            selected_country, case=False, regex=False
        )
    ]

if selected_year != "All":
    filtered_df = filtered_df[
        filtered_df["release_year"] == selected_year
    ]

# KPI metrics
st.subheader("Business KPIs")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Titles", len(filtered_df))
col2.metric("Movies", (filtered_df["type"] == "Movie").sum())
col3.metric("TV Shows", (filtered_df["type"] == "TV Show").sum())
col4.metric("Countries", filtered_df["country"].nunique())

# Content distribution
st.subheader("Content Distribution")

content = filtered_df["type"].value_counts().reset_index()
content.columns = ["Type", "Count"]

fig1 = px.pie(
    content,
    names="Type",
    values="Count",
    title="Movies vs TV Shows",
    hole=0.4
)
# Top countries
country_data = (
    filtered_df["country"].dropna()
    .str.split(",").explode().str.strip()
    .value_counts().head(10).reset_index()
)
country_data.columns = ["Country", "Titles"]

fig2 = px.bar(
    country_data,
    x="Country",
    y="Titles",
    title="Top 10 Countries"
)

# Two-column chart layout
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.plotly_chart(fig2, use_container_width=True)

# Top genres
st.subheader("Top 10 Genres")

genre_data = (
    filtered_df["listed_in"].dropna()
    .str.split(",").explode().str.strip()
    .value_counts().head(10).reset_index()
)
genre_data.columns = ["Genre", "Titles"]

fig3 = px.bar(
    genre_data,
    x="Titles",
    y="Genre",
    orientation="h",
    title="Top 10 Genres"
)

# Year-wise Content Growth Trend
st.subheader("📈 Year-wise Content Growth Trend")

year_data = (
    filtered_df.groupby("release_year")
    .size()
    .reset_index(name="Total Titles")
    .sort_values("release_year")
)

fig4 = px.line(
    year_data,
    x="release_year",
    y="Total Titles",
    markers=True,
    title="Netflix Content Growth by Release Year"
)

col3, col4 = st.columns(2)

with col3:
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.plotly_chart(fig4, use_container_width=True, key="yearly_growth_chart")

# Download filtered data
st.subheader("Download Data")

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Filtered Netflix Data",
    data=csv,
    file_name="netflix_filtered_data.csv",
    mime="text/csv"
)

st.success("Netflix Dashboard Loaded Successfully!")

# Business Insights
st.subheader("💡 Business Insights & Recommendations")

total_movies = (filtered_df["type"] == "Movie").sum()
total_shows = (filtered_df["type"] == "TV Show").sum()

if total_movies > total_shows:
    st.write("🎬 Movies dominate the selected Netflix content.")
else:
    st.write("📺 TV Shows have a stronger presence in the selected content.")

top_genre = (
    filtered_df["listed_in"].dropna()
    .str.split(",").explode().str.strip()
    .value_counts()
)

if not top_genre.empty:
    st.write(f"🏆 Most common genre: {top_genre.index[0]}")

st.markdown("""
### Business Recommendations

1. Invest in popular content categories.
2. Explore international content markets.
3. Increase TV Show content where audience demand supports it.
4. Use release trends for future content planning.
""")
