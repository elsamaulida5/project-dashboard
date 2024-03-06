import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px

# Fungsi untuk memuat data
data = pd.read_csv("data.csv")
datetime_columns = ["dteday"]
data.sort_values(by="dteday", inplace=True)
data.reset_index(inplace=True)

for column in datetime_columns:
    data[column] = pd.to_datetime(data[column])

# Menambahkan judul dashboard
st.title('Dashboard Bike Sharing :star:')
st.write("")

# Menambahkan sidebar untuk memilih tanggal
min_date = data['dteday'].min()
max_date = data['dteday'].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://raw.githubusercontent.com/elsamaulida5/project-dashboard/main/pngegg.png")

    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date.date(), max_value=max_date.date(), value=[min_date.date(), max_date.date()]
    )

# Filter data berdasarkan rentang waktu yang dipilih
filtered_data = data.loc[(data['dteday'] >= pd.to_datetime(start_date)) 
                         & (data['dteday'] <= pd.to_datetime(end_date))]


# Membuat sub header
st.subheader('Daily Rental Bikes')

col1, _ = st.columns([2, 1])  # Menggunakan 2 kolom untuk metrik "Total Orders"

with col1:
    total_rent = filtered_data['cnt'].sum()
    st.metric("Total rent", value=total_rent)

# Membuat line plot
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    filtered_data["dteday"],
    filtered_data["cnt"],
    marker='o', 
    linewidth=2,
    color="#145780"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
 
st.pyplot(fig)

#Membuat proporsi peminjam sepeda dengan pie chart
st.subheader('Proportion of Bicycle Rentals')

# Menghitung jumlah peminjam berdasarkan kategori
proporsi_peminjam = filtered_data.groupby('season')['cnt'].sum()

# Membuat pie chart
fig, ax = plt.subplots(figsize=(7,7))
ax.pie(proporsi_peminjam, labels=proporsi_peminjam.index, autopct='%1.1f%%', startangle=90, colors=['#145780', '#52acae', '#81acc1', '#afd3d0'])
ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

# Menampilkan pie chart
st.pyplot(fig)

# Menambahkan header judul
st.subheader('Lets take a look!!! :flushed:')
st.subheader('Relationship of several factors affecting the number of bike renters')

# Mendefinisikan data dahulu
data_scatter = { 
    'Temperature' : data['temp'],
    'Humidity' : data['hum'],
    'WindSpeed' : data['windspeed'],
    'Number_of_Renters' : data['cnt']
 }

# Membuat selectbox
col1, col2 =st.columns(2)
choice = ['Temperature', 'Humidity', 'WindSpeed', 'Number_of_Renters']
choice1 = col1.selectbox('Horizontal', options=choice)
choice2 = col2.selectbox('Vertikal', options=choice)

# Membuat tulisan korelasi antara suhu dan jumlah peminjam sepeda
correlation = np.corrcoef(data_scatter[choice1], data_scatter[choice2])[0, 1]
col1, _ = st.columns([2, 1])  

with col1:
       st.metric("Correlation", value="{:.2f}".format(correlation), delta=2)

# Membuat scatter plot
fig = px.scatter(data_scatter,
                 x=choice1,
                 y=choice2,
                 color_discrete_sequence=['#145780'],
                 title = f'Scatter Plot of {choice1.title()} and {choice2.title()}')
st.plotly_chart(fig)