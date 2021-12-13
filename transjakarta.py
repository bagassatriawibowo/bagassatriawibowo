"""
Aplikasi Streamlit untuk menggambarkan statistik penumpang TransJakarta

Sumber data berasal dari Jakarta Open Data
Referensi API Streamlit: https://docs.streamlit.io/library/api-reference
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
import streamlit as st
from PIL import Image


############### title ###############
st.set_page_config(layout="wide")  # this needs to be the first Streamlit command called
st.title("Statistik Jumlah Penumpang TransJakarta Tahun 2019")
st.markdown("*Sumber data berasal dari [Jakarta Open Data](https://data.jakarta.go.id/dataset/data-jumlah-penumpang-trans-jakarta-tahun-2019-kpi)*")
############### title ###############)

############### sidebar ###############
image = Image.open('tj_logo.png')
st.sidebar.image(image)

st.sidebar.title("Pengaturan")
left_col, mid_col, right_col = st.columns(3)

## User inputs on the control panel
st.sidebar.subheader("Pengaturan konfigurasi tampilan")
list_bulan = ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember']
bulan = st.sidebar.selectbox("Pilih bulan", list_bulan)
list_url = {'Januari': 'https://data.jakarta.go.id/dataset/50b36c4b-0aed-42a5-82e4-c3510475716a/resource/1a3bcf20-1ed0-42c9-baca-71cdabbe7fdc/download/Data-Penumpang-Bus-Transjakarta-Januari-2019.csv',
            'Februari': 'https://data.jakarta.go.id/dataset/50b36c4b-0aed-42a5-82e4-c3510475716a/resource/849e203a-ca5d-47d6-9024-1e753ca405ad/download/Data-Penumpang-Bus-Transjakarta-Februari-2019.csv', 
            'Maret': 'https://data.jakarta.go.id/dataset/50b36c4b-0aed-42a5-82e4-c3510475716a/resource/c7cea037-4306-4d3c-aabd-382798bf88ff/download/Data-Penumpang-Bus-Transjakarta-Maret-2019.csv', 
            'April': 'https://data.jakarta.go.id/dataset/50b36c4b-0aed-42a5-82e4-c3510475716a/resource/204a8676-afe3-4355-91cf-21ac866605eb/download/Data-Penumpang-Bus-Transjakarta-April-2019.csv', 
            'Mei': 'https://data.jakarta.go.id/dataset/50b36c4b-0aed-42a5-82e4-c3510475716a/resource/178a44a4-ad21-41c0-860b-67b5e1dd0175/download/Data-Penumpang-Bus-Transjakarta-Mei-2019.csv', 
            'Juni': 'https://data.jakarta.go.id/dataset/50b36c4b-0aed-42a5-82e4-c3510475716a/resource/fc49004a-2eaf-43c2-ab7d-b316ca0a6e38/download/Data-Penumpang-Bus-Transjakarta-Juni-2019.csv', 
            'Juli': 'https://data.jakarta.go.id/dataset/50b36c4b-0aed-42a5-82e4-c3510475716a/resource/ee7a387c-f0e5-4564-a17f-5e50e1137441/download/Data-Penumpang-Bus-Transjakarta-Juli-2019.csv', 
            'Agustus': 'https://data.jakarta.go.id/dataset/50b36c4b-0aed-42a5-82e4-c3510475716a/resource/d950bb97-7a49-42ff-9d22-438374404b82/download/Data-Penumpang-Bus-Transjakarta-Agustus-2019.csv', 
            'September': 'https://data.jakarta.go.id/dataset/50b36c4b-0aed-42a5-82e4-c3510475716a/resource/04e2b099-2d2c-47d5-bddd-3b0d092fbdae/download/Data-Penumpang-Bus-Transjakarta-September-2019.csv', 
            'Oktober': 'https://data.jakarta.go.id/dataset/50b36c4b-0aed-42a5-82e4-c3510475716a/resource/b37e5a6f-9b98-443b-bb5f-bdba288cf7e3/download/Data-Penumpang-Bus-Transjakarta-Oktober-2019.csv', 
            'November': 'https://data.jakarta.go.id/dataset/50b36c4b-0aed-42a5-82e4-c3510475716a/resource/14520801-0674-4334-89bc-a1f1a94257b7/download/Data-Penumpang-Bus-Transjakarta-November-2019.csv', 
            'Desember': 'https://data.jakarta.go.id/dataset/50b36c4b-0aed-42a5-82e4-c3510475716a/resource/4c3be51b-6ae9-44cc-9b42-616b4c982614/download/Data-Penumpang-Bus-Transjakarta-Desember-2019.csv'
           }

n_tampil = st.sidebar.number_input("Jumlah baris dalam tabel yang ditampilkan", min_value=1, max_value=None, value=10)
############### sidebar ###############

############### upper left column ###############
left_col.subheader("Tabel representasi data")

filepath = list_url[bulan]
df = pd.read_csv(filepath)

left_col.dataframe(df.head(n_tampil))
############### upper left column ###############

############### upper middle column ###############
mid_col.subheader("Jenis transportasi")

jenis_unik = list(df['jenis'].unique())
tulis_jenis = []
for i, jenis in enumerate(jenis_unik):
    tulis_jenis.append(f"{str(i+1)}. {jenis}\n")
tulis_jenis = ' '.join(map(str, tulis_jenis))

mid_col.markdown(tulis_jenis)
############### upper middle column ###############

############### upper right column ###############
right_col.subheader("Total penumpang perbulan")

total_perbulan = []
for i in range(len(list_bulan)):
    df_bulan = pd.read_csv(list_url[list_bulan[i]])
    df_bulan['jumlah_penumpang'] = df_bulan['jumlah_penumpang'].str.replace(",", "", regex=True)
    df_bulan['jumlah_penumpang'] = df_bulan['jumlah_penumpang'].str.replace(".", "", regex=True)
    df_bulan['jumlah_penumpang'] = pd.to_numeric(df_bulan['jumlah_penumpang'], errors='coerce')
    #jumlah_perbulan = df_bulan['jumlah_penumpang'].astype(int).sum()
    jumlah_perbulan = df_bulan['jumlah_penumpang'].sum()
    #print(f"Bulan {bulan}, total penumpang: {jumlah_perbulan}")
    total_perbulan.append(int(jumlah_perbulan))

cmap_name = 'tab20'
cmap = cm.get_cmap(cmap_name)
colors = cmap.colors[:len(list_bulan)]
fig, ax = plt.subplots()
ax.bar(list_bulan, total_perbulan, color=colors)
ax.set_xticklabels(list_bulan, rotation=45)
ax.set_xlabel("Bulan", fontsize=12)
ax.set_ylabel("Total jumlah penumpang", fontsize=12)
plt.tight_layout()

right_col.pyplot(fig)
############### upper right column ###############

############### lower left column ###############
left_col.subheader("Total penumpang")

total_penumpang = []
for jenis in jenis_unik:
    df['jumlah_penumpang'] = df['jumlah_penumpang'].str.replace(",", "", regex=True)
    df['jumlah_penumpang'] = df['jumlah_penumpang'].str.replace(".", "", regex=True)
    #df['jumlah_penumpang'] = pd.to_numeric(df['jumlah_penumpang'], errors='coerce')
    jumlah_penumpang = df[df['jenis']==jenis]['jumlah_penumpang'].astype(int)
    total_penumpang.append(jumlah_penumpang.sum())

fig, ax = plt.subplots()
ax.barh(jenis_unik, total_penumpang, color=colors)
ax.set_yticklabels(jenis_unik, rotation=0)
ax.invert_yaxis()  # labels read top-to-bottom
ax.set_xlabel("Total jumlah penumpang", fontsize=12)

left_col.pyplot(fig)
############### lower left column ###############

############### lower middle column ###############
mid_col.subheader("Jumlah trayek")

total_trayek = []
for jenis in jenis_unik:
    jumlah_trayek = df[df['jenis']==jenis].shape[0]
    total_trayek.append(jumlah_trayek)

def label_function(val):
    return f'{val / 100 * sum(total_trayek):.0f}'

colors = cmap.colors[:len(jenis_unik)]
fig, ax = plt.subplots()
patches, labels, texts = ax.pie(total_trayek, autopct=label_function, startangle=90, colors=colors, textprops={'fontsize': 11})
ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
ax.legend(patches, jenis_unik, loc="center left", bbox_to_anchor=(0.85, 0.5))

mid_col.pyplot(fig)
############### lower middle column ###############

############### lower right column ###############
right_col.subheader("Summary")
max_penumpang = np.asarray(total_penumpang).max()
max_penumpang_idx = np.asarray(total_penumpang).argmax()
right_col.markdown(f"**Jenis angkutan terpadat pada {bulan}: ** \n {jenis_unik[max_penumpang_idx]} ({max_penumpang} orang)")

max_trayek = np.asarray(total_trayek).max()
max_trayek_idx = np.asarray(total_trayek).argmax()
right_col.markdown(f"**Jenis trayek terbanyak pada {bulan}: ** \n {jenis_unik[max_trayek_idx]} ({max_trayek} trayek)")

max_perbulan = np.asarray(total_perbulan).max()
max_perbulan_idx = np.asarray(total_perbulan).argmax()
right_col.markdown(f"**Bulan tersibuk adalah: ** \n {list_bulan[max_perbulan_idx]} ({max_perbulan} orang)")
############### lower right column ###############