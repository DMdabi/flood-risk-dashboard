
import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
@st.cache_data
def load_data():
    return pd.read_excel("data for model development.xlsx")

data = load_data()

st.title("Flood Risk Dashboard - Ghana")

# Sidebar filters
st.sidebar.header("Filter Data")
years = data['Year'].unique()
locations = data['Location'].unique()

selected_year = st.sidebar.multiselect("Select Year(s)", sorted(years), default=sorted(years))
selected_location = st.sidebar.multiselect("Select Location(s)", sorted(locations), default=sorted(locations))

filtered_data = data[
    (data['Year'].isin(selected_year)) &
    (data['Location'].isin(selected_location))
]

# KPIs
st.subheader("Key Indicators")
col1, col2, col3 = st.columns(3)
col1.metric("Avg. Flood Risk", f"{filtered_data['Flood_Risk_Index'].mean():.2f}")
col2.metric("Avg. Rainfall (mm)", f"{filtered_data['Rainfall'].mean():.2f}")
col3.metric("Avg. Vulnerability", f"{filtered_data['Vulnerability_Score'].mean():.2f}")

# Charts
st.subheader("Flood Risk Over Time")
fig1 = px.line(filtered_data, x="Year", y="Flood_Risk_Index", color="Location", markers=True)
st.plotly_chart(fig1)

st.subheader("Rainfall vs Flood Risk")
fig2 = px.scatter(filtered_data, x="Rainfall", y="Flood_Risk_Index",
                  color="Vulnerability_Score", size="Runoff", hover_data=['Location', 'Year'],
                  title="Rainfall vs. Flood Risk (Bubble Size = Runoff Volume)")
st.plotly_chart(fig2)

st.subheader("Top 10 High-Risk Locations")
top10 = filtered_data.groupby("Location")["Flood_Risk_Index"].mean().nlargest(10).reset_index()
fig3 = px.bar(top10, x="Location", y="Flood_Risk_Index", title="Top 10 Locations by Average Flood Risk")
st.plotly_chart(fig3)

st.subheader("Raw Data")
st.dataframe(filtered_data)

# Download Option
st.download_button("Download Filtered Data as CSV", filtered_data.to_csv(index=False), "filtered_data.csv", "text/csv")

