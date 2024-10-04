import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt
import plotly.express as px

# Mengumpulkan data-data yang akan digunakan
df = pd.read_csv("hour.csv", delimiter = ",")  # Pastikan path file sesuai

# Memeriksa data awal
st.title('Bike Sharing Data Analysis')
st.write("Data Awal:")
st.write(df.head())
st.write("Info Data:")
st.write(df.info())
st.write("Deskripsi Data:")
st.write(df.describe())

# Mengidentifikasi Missing Values
st.write("Missing Values:")
st.write(df.isna().sum())

# Mengidentifikasi duplicate data
st.write("Duplicate Data:")
st.write(df.duplicated().sum())

# Menghitung total penyewaan sepeda oleh pengguna casual dan registered
total_casual = df['casual'].sum()
total_registered = df['registered'].sum()

# Membuat data untuk bar plot
categories = ['Casual Users', 'Registered Users']
totals = [total_casual, total_registered]

# Membuat bar plot
plt.figure(figsize=(8, 6))
plt.bar(categories, totals, color=['orange', 'blue'])
plt.title('Total Bike Rentals by Casual and Registered Users', fontsize=16)
plt.ylabel('Total Rentals', fontsize=12)
st.pyplot(plt)  # Menampilkan bar plot di Streamlit

# Hitung dan tampilkan total hari libur dan hari kerja
total_holiday_days = df[df['holiday'] == 1].shape[0]
total_working_days = df[df['workingday'] == 1].shape[0]

# Data untuk visualisasi jumlah hari (holiday vs workingday)
categories_days = ['Holiday Days', 'Working Days']
total_days = [total_holiday_days, total_working_days]

# Data untuk visualisasi total penyewaan (holiday vs workingday)
total_holiday_rentals = df[df['holiday'] == 1]['cnt'].sum()
total_workingday_rentals = df[df['workingday'] == 1]['cnt'].sum()
categories_rentals = ['Holiday Rentals', 'Workingday Rentals']
total_rentals = [total_holiday_rentals, total_workingday_rentals]

# Membuat figure dan axes untuk plot
plt.figure(figsize=(12, 6))

# Bar plot untuk total hari
plt.subplot(1, 2, 1)  # Membuat subplot 1 dari 2
plt.bar(categories_days, total_days, color=['green', 'purple'])
plt.title('Total Holiday vs Working Days', fontsize=16)
plt.ylabel('Total Days', fontsize=12)

# Bar plot untuk total penyewaan
plt.subplot(1, 2, 2)  # Membuat subplot 2 dari 2
plt.bar(categories_rentals, total_rentals, color=['green', 'purple'])
plt.title('Total Rentals on Holiday vs Working Days', fontsize=16)
plt.ylabel('Total Rentals', fontsize=12)

# Menyesuaikan layout agar rapi
plt.tight_layout()
st.pyplot(plt)  # Menampilkan visualisasi di Streamlit

# Membuat data untuk analisis time series
# Analisis time series per bulan
monthly_data = df.groupby(df['dteday'].dt.to_period('M')).agg(
    total_rentals=('cnt', 'sum'),
    avg_rentals=('cnt', 'mean'),
    min_rentals=('cnt', 'min'),
    max_rentals=('cnt', 'max')
).reset_index()

# Analisis time series per tahun
yearly_data = df.groupby(df['dteday'].dt.year).agg(
    total_rentals=('cnt', 'sum'),
    avg_rentals=('cnt', 'mean'),
    min_rentals=('cnt', 'min'),
    max_rentals=('cnt', 'max')
).reset_index()

# Analisis time series per hari
daily_data = df.groupby(df['dteday']).agg(
    total_rentals=('cnt', 'sum'),
    avg_rentals=('cnt', 'mean'),
    min_rentals=('cnt', 'min'),
    max_rentals=('cnt', 'max')
).reset_index()

# Tambahkan debug output untuk memastikan data terdefinisi
st.write("Monthly Data:")
st.write(monthly_data)
st.write("Yearly Data:")
st.write(yearly_data)
st.write("Daily Data:")
st.write(daily_data)

# Visualisasi Time Series per Bulan
plt.figure(figsize=(15, 5))

# Bar plot untuk total penyewaan per bulan
plt.subplot(1, 3, 1)  # Membuat subplot 1 dari 3
plt.bar(monthly_data['dteday'].astype(str), monthly_data['total_rentals'], color='orange')
plt.title('Total Rentals per Month', fontsize=16)
plt.xlabel('Month', fontsize=12)
plt.ylabel('Total Rentals', fontsize=12)
plt.xticks(rotation=45)

# Visualisasi Time Series per Tahun
plt.subplot(1, 3, 2)  # Membuat subplot 2 dari 3
plt.bar(yearly_data['dteday'], yearly_data['total_rentals'], color='blue')
plt.title('Total Rentals per Year', fontsize=16)
plt.xlabel('Year', fontsize=12)
plt.ylabel('Total Rentals', fontsize=12)
plt.xticks(rotation=45)

# Visualisasi Time Series per Hari
plt.subplot(1, 3, 3)  # Membuat subplot 3 dari 3
plt.bar(daily_data['dteday'].astype(str), daily_data['total_rentals'], color='green')
plt.title('Total Rentals per Day', fontsize=16)
plt.xlabel('Date', fontsize=12)
plt.ylabel('Total Rentals', fontsize=12)
plt.xticks(rotation=45)

# Menyesuaikan layout agar rapi
plt.tight_layout()
st.pyplot(plt)  # Menampilkan visualisasi di Streamlit
