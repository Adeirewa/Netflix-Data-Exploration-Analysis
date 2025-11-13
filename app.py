# app.py
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# -------------------------------
# Load & clean data
# -------------------------------
df = pd.read_csv('netflix_titles.csv')

df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
df['year_added'] = df['date_added'].dt.year
df['country'] = df['country'].fillna('Unknown')
df['rating'] = df['rating'].fillna('Not Rated')
df = df.dropna(subset=['year_added'])
df['year_added'] = df['year_added'].astype(int)

# -------------------------------
# Streamlit page setup
# -------------------------------
st.set_page_config(page_title="Netflix Dashboard", layout="wide")
st.title("🎬 Netflix Content Dashboard")
st.write("Explore Netflix content trends over time.")

# -------------------------------
# Sidebar year filter
# -------------------------------
year = st.sidebar.slider(
    "Select Year",
    int(df['year_added'].min()),
    int(df['year_added'].max()),
    value=int(df['year_added'].max())
)
filtered = df[df['year_added'] == year]

# -------------------------------
# Columns for charts
# -------------------------------
col1, col2 = st.columns(2)

# --- Column 1: Content Types ---
with col1:
    st.subheader(f"Content Types in {year}")
    type_count = filtered['type'].value_counts()
    fig1, ax1 = plt.subplots()
    sns.barplot(
        y=type_count.index, x=type_count.values,
        palette=['#E50914', '#F5C518'], ax=ax1
    )
    ax1.set_xlabel("Count")
    ax1.set_ylabel("Type")
    st.pyplot(fig1)

# --- Column 2: Ratings Distribution ---
with col2:
    st.subheader(f"Ratings Distribution in {year}")
    ratings_count = filtered['rating'].value_counts()
    fig2, ax2 = plt.subplots()
    sns.barplot(
        y=ratings_count.index, x=ratings_count.values,
        palette=['#E50914', '#F5C518'], ax=ax2
    )
    ax2.set_xlabel("Count")
    ax2.set_ylabel("Rating")
    st.pyplot(fig2)

# --- Full width: Top 10 Genres ---
st.subheader(f"Top 10 Genres in {year}")
genres = filtered['listed_in'].str.split(', ').explode()
top_genres = genres.value_counts().head(10)
fig3, ax3 = plt.subplots()
sns.barplot(
    y=top_genres.index, x=top_genres.values,
    palette=['#E50914', '#F5C518'], ax=ax3
)
ax3.set_xlabel("Count")
ax3.set_ylabel("Genre")
st.pyplot(fig3)

# --- Optional: Pie chart for content types ---
st.subheader(f"Content Types Pie Chart in {year}")
fig4, ax4 = plt.subplots()
ax4.pie(
    type_count.values, labels=type_count.index,
    autopct='%1.1f%%', colors=['#E50914', '#F5C518']
)
st.pyplot(fig4)
