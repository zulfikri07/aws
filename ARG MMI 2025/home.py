import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timezone
import pydeck as pdk
from streamlit_option_menu import option_menu
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import matplotlib.pyplot as plt


# Konfigurasi Streamlit
st.set_page_config(page_title="AWS 2025", layout="wide")

st.title ( "AUTOMATIC WEATHER STATION 2025" )
st.sidebar.image("pages/mmi.jpg")

# Data titik koordinat
df = pd.DataFrame({
    'lat': [-6.275762],
    'lon': [106.727760],
    'label': ['AWS MMI']
})


# Buat Layer
layer = pdk.Layer(
    "ScatterplotLayer",
    df,
    get_position='[lon, lat]',
    get_color='[0, 500, 0, 200]',
    get_radius=500,
    elevation_range=[200, 1000],
    pickable=True,
    extruded=True,
)

# Set tampilan peta
view_state = pdk.ViewState(
    latitude=-2.5,  # tengah Indonesia
    longitude=118,
    zoom=4.0,
    pitch=0
)

# Render Peta
r = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip={"text": "Lokasi: {label}"}
)

st.pydeck_chart(r)

st.title ("GRAFIK SENSOR")

# Setup koneksi Google Sheets
scope = ["https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# Buka sheet
sheet = client.open("aws brin 2025").sheet1  # Ganti dengan nama sheet kamu
data = sheet.get_all_records()
df = pd.DataFrame(data)

# Gabungkan Tanggal dan Waktu jadi satu kolom datetime (jika perlu)
df['Datetime'] = pd.to_datetime(df['Tanggal'] + ' ' + df['Waktu'], format="%d-%m-%Y %H:%M:%S")

# 4. Pilih parameter yang ingin dilihat
parameter_list = ['Suhu', 'Kelembaban', 'W.Speed', 'W.Dir', 'Tekanan', 'Hujan', 'Rad', 'Signal']
selected = st.multiselect("Pilih Parameter yang Ditampilkan", parameter_list, default=['Suhu'])

# 5. Line chart
if selected:
    chart_data = df.set_index('Datetime')[selected]
    st.line_chart(chart_data)
else:
    st.warning("Silakan pilih minimal satu parameter.")

# 6. Tampilkan data mentah (opsional)
with st.expander("Lihat RAW Data"):
    st.dataframe(df)