import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

def create_hourly_bikesharing_df(df):
    hour_df = all_df.groupby(by="hr").cnt.nunique().reset_index()
    hour_df.rename(columns={
        "cnt": "count",
        "hr": "hour"
    }, inplace=True)
    return hour_df 

all_df = pd.read_csv("dashboard/main_data.csv")

all_df["dteday"] = pd.to_datetime(all_df["dteday"])
min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()

with st.sidebar:
    # Menambahkan logo dari freepick.com
    st.image("bike-icon.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
            label='Rentang Waktu',
            min_value=min_date.date(),  # Convert to date
            max_value=max_date.date(),  # Convert to date
            value=(min_date.date(), max_date.date())  # Set default values as a tuple of dates
        )

    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    main_df = all_df[(all_df["dteday"] >= start_date) & (all_df["dteday"] <= end_date)]

hour_df = create_hourly_bikesharing_df(main_df)

st.header('Bike Sharing Dashboard :sparkles:')

#Daily Bike Sharing
st.subheader('Daily Bike Sharing Activity')

max_count_index = hour_df['count'].idxmax()
min_count_index = hour_df['count'].idxmin()

colors = [
    '#72BCD4' if i == max_count_index else
    '#FF6347' if i == min_count_index else
    '#D3D3D3'
    for i in range(len(hour_df))
]

fig, ax = plt.subplots(figsize=(20, 10)) 
 
sns.barplot(
    y="count", 
    x="hour",
    data=hour_df.sort_values(by="count", ascending=False),
    palette=colors,
    ax=ax
)
ax.set_xlabel('Hour')
ax.set_ylabel('Count')
ax.tick_params(axis='x', labelsize=12)
st.pyplot(fig)


st.subheader('Bike Sharing Activity Based on Season and Weather')

#Bike sharing based on season and weather
season_colors = {
    'Springer': '#A4D65E',  
    'Summer': '#FBBE43',  
    'Fall': '#E65100',    
    'Winter': '#8BC6E6'    
}

# Scatter plot for bike-sharing activity against Humidity
fig, ax = plt.subplots(figsize=(15, 6))
sns.scatterplot(x='hum', y='cnt', hue='season', data=main_df, alpha=0.6, palette=season_colors)
ax.set_title('Bike-Sharing Activity vs. Humidity')
ax.set_xlabel('Humidity')
ax.set_ylabel('Count')
st.pyplot(fig)

# Scatter plot for bike-sharing activity against Temperature
fig, ax = plt.subplots(figsize=(15, 6))
sns.scatterplot(x='temp', y='cnt', hue='season', data=main_df, alpha=0.6, palette=season_colors)
ax.set_title('Bike-Sharing Activity vs. Temperature')
ax.set_xlabel('Temperature')
ax.set_ylabel('Count')
st.pyplot(fig)

# Scatter plot for bike-sharing activity against wind speed
fig, ax = plt.subplots(figsize=(15, 6))
sns.scatterplot(x='windspeed', y='cnt', hue='season', data=main_df, alpha=0.6, palette=season_colors)
ax.set_title('Bike-Sharing Activity vs. Wind Speed')
ax.set_xlabel('Wind Speed')
ax.set_ylabel('Count')
st.pyplot(fig)   

weather_mapping = {
    1: "Clear, Few clouds, Partly cloudy",
    2: "Mist + Cloudy, Mist + Broken clouds",
    3: "Light Snow, Light Rain + Thunderstorm",
    4: "Heavy Rain + Ice Pellets + Thunderstorm"
}

main_df['weather_desc'] = main_df['weathersit'].map(weather_mapping)

fig, ax = plt.subplots(figsize=(20, 10))

colors = ["#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4"] 
sns.barplot(
    y="cnt", 
    x="weather_desc",
    data=main_df.sort_values(by="cnt", ascending=False),
    palette=colors,
    legend=False,
    errorbar=None 
)
ax.set_title("Bike-Sharing Activity Based on Weather Situation", loc="center", fontsize=15)
ax.set_ylabel("Count")
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=12)
st.pyplot(fig)  

#User Activity
st.subheader('Bike Sharing User Activity')

col1, col2 = st.columns(2)
with col1:
    avg_casual = round(main_df.casual.mean())
    st.metric("Casual User per Hour (Average)", value=avg_casual)
 
with col1:
    avg_registered = round(main_df.registered.mean())
    st.metric("Registered User per Hour (Average)", value=avg_registered)

colors = [
    '#A4D65E',  
    '#FBBE43',  
    '#FFA07A',  
    '#8BC6E6',  
    '#4C8CDB',  
    '#D67898',  
    '#D54A29'   
]
col1, col2 = st.columns(2)
with col1:
    # Line chart for bike-sharing activity of casual user in a week
    fig1, ax1 = plt.subplots(figsize=(20, 10))
    sns.pointplot(x='hr', y='casual', hue='weekday', data=main_df, palette=colors)
    ax1.set_title('Bike-Sharing Activity of Casual User')
    ax1.set_xlabel('Hour')
    ax1.set_ylabel('User')
    st.pyplot(fig1)  
with col2:
    # Line chart for bike-sharing activity of registered user in a week
    fig2, ax2 = plt.subplots(figsize=(20, 10))
    sns.pointplot(x='hr', y='registered', hue='weekday', data=main_df, palette=colors)
    ax2.set_title('Bike-Sharing Activity of Registered User')
    ax2.set_xlabel('Hour')
    ax2.set_ylabel('User')
    st.pyplot(fig2)  

#Clustering
st.subheader('Clustering Analysis of Bike Sharing User Activity')

col1, col2 = st.columns(2)
with col1:
    #Casual user
    fig1, ax1 = plt.subplots(figsize=(15, 6))
    sns.countplot(data=main_df, x='temp_category', hue='casual_user')
    ax1.set_title('Casual User Activity by Temperature Category')
    ax1.set_xlabel('Temperature Category')
    ax1.set_ylabel('Count of Casual Users')
    st.pyplot(fig1)  

with col2:
    #Registered user
    fig2, ax2 = plt.subplots(figsize=(15, 6))
    sns.countplot(data=main_df, x='temp_category', hue='registered_user')
    ax2.set_title('Registered User Activity by Temperature Category')
    ax2.set_xlabel('Temperature Category')
    ax2.set_ylabel('Count of Registered Users')
    st.pyplot(fig2)  

st.caption('github.com/zarazannetta/Analisis-Data-Python')