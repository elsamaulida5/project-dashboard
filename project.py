import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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
filtered_data = data.loc[(data['dteday'] >= pd.to_datetime(start_date)) & (data['dteday'] <= pd.to_datetime(end_date))]


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
    color="#90CAF9"
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
ax.pie(proporsi_peminjam, labels=proporsi_peminjam.index, autopct='%1.1f%%', startangle=90, colors=['#b3e5fc', '#81d4fa', '#4fc3f7', '#5ba4cf'])
ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

# Menampilkan pie chart
st.pyplot(fig)

# Menambahkan header judul
st.subheader('Number of Renters by Season')

# Menghitung jumlah peminjam berdasarkan musim
proporsi_peminjam = filtered_data.groupby('season')['cnt'].sum()
proporsi_peminjam_sorted = proporsi_peminjam.sort_values(ascending=False)

# Membuat bar plot dengan data yang telah diurutkan
fig, ax = plt.subplots()
proporsi_peminjam_sorted.plot(kind='barh', ax=ax, color='skyblue')  # Mengatur warna bar menjadi biru langit

# Mengatur ukuran font label sumbu x dan sumbu y
ax.tick_params(axis='x', labelsize=10)  # Ukuran font label sumbu x
ax.tick_params(axis='y', labelsize=10)  # Ukuran font label sumbu y

# Mengatur ketebalan garis sumbu x dan sumbu y
ax.spines['bottom'].set_linewidth(0.8)  # Ketebalan garis sumbu x
ax.spines['left'].set_linewidth(0.8)    # Ketebalan garis sumbu y

# Memberi label sumbu x dan sumbu y serta judul plot
ax.set_xlabel('Number of Renters', fontsize=10)  # Label sumbu x dengan ukuran font 14
ax.set_ylabel('Season', fontsize=10)            # Label sumbu y dengan ukuran font 14

# Menampilkan bar plot
st.pyplot(fig)