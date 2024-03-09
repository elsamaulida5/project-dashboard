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

# Membuat aplikasi Streamlit
st.title("Bicycle Rental Visualization")

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


# Line Plot Penyewa Harian
st.subheader("Daily Counts")

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
# Label sumbu x dan y
ax.set_xlabel('Date', fontsize=20)
ax.set_ylabel('Count', fontsize=20)
# Judul plot
ax.set_title('Daily Counts', fontsize=25)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
# Menampilkan Plot
st.pyplot(fig)

# Pie Chart Musim
st.subheader("Proportion of Bicycle Rental by Season")
# Mengelompokkan data musim
data_musim = filtered_data.groupby(by=["season"]).agg({
    "cnt": "sum",
})
# Membuat plot
fig, ax = plt.subplots(figsize=(8, 6))
ax.pie(data_musim['cnt'], labels=data_musim.index, autopct='%1.1f%%', colors=['#145780', '#52acae', '#81acc1', '#afd3d0'])
ax.axis('equal') 
# Membuat Judul
ax.set_title('Proportion of Bicycle Rental by Season', fontsize=15)
# Menampilkan plot
st.pyplot(fig)


# Bar Chart Cuaca
st.subheader("Counts by Weather Situation")
# Mengelompokkan data cuaca
data_cuaca = filtered_data.groupby(by=["weathersit"]).agg({
    "cnt": "sum",
})
# Membuat plot
fig, ax = plt.subplots(figsize=(10, 6))
data_cuaca.plot(kind='bar', color='#52acae', ax=ax)
# Membuat label
ax.set_xlabel('Weather Situation', fontsize=12)
ax.set_ylabel('Count', fontsize=12)
ax.set_xticklabels(data_cuaca.index, rotation=45)
# Membuat Judul Plot
ax.set_title('Counts by Weather Situation', fontsize=15)
# Tampilkan plot dengan st.pyplot()
st.pyplot(fig)



