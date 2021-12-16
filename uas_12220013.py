############### UJIAN AKHIR SEMESTER ###############
# Nama  : Bagas Satria Wibowo
# NIM   : 12220013

import matplotlib.pyplot as plt
from matplotlib import cm
import json
import pandas as pd
import streamlit as st
from PIL import Image
import numpy as np
import streamlit as st

dataframe = pd.read_csv('produksi_minyak_mentah.csv')
dataframe['produksi'] = pd.to_numeric(dataframe['produksi'])
jison_f = open("kode_negara_lengkap.json")
det = json.loads(jison_f.read())

nama_negara=[]
for z in range (len(dataframe.index)):
    a=0
    indie = 0
    for k in det:
        if dataframe['kode_negara'][z] == det[a]['alpha-3'] :
            nama_negara.append(det[a]['name'])
            indie +=1
        a+=1
    if indie == 0:
        nama_negara.append(0)

dataframe['nama_negara']=nama_negara
dataframe = dataframe[dataframe.nama_negara != 0]


#JUDUL
st.set_page_config(layout="wide")  
st.title("Informasi Seputar Data Produksi Minyak Mentah dari Berbagai Negara di Seluruh Dunia")
#JUDUL

############### sidebar ###############
image = Image.open('Statistikminyakdunia.png')
st.sidebar.image(image)

st.sidebar.title("Pengaturan")
left_col, mid_col, right_col = st.columns(3)

## User inputs on the control panel
st.sidebar.subheader("Pengaturan Konfigurasi Tampilan")
cntry=list(dict.fromkeys(nama_negara))
cntry.remove(0)
negara = st.sidebar.selectbox("Pilihlah Negara", cntry)
n_country = st.sidebar.number_input("Total Negara", min_value=1, max_value=None, value=1)
unique_year = list(dataframe['tahun'].unique())
tahun = st.sidebar.selectbox ("Tahun", unique_year)

###############  left column ###############
left_col.subheader("Produksi Minyak Mentah Negara yang Dipilih")

total_prod=[]
for s in dataframe[dataframe['nama_negara']==negara]['produksi'] :
    total_prod.append(s)

figure, ax = plt.subplots()
name_cmap = 'Pastel2'
cimap = cm.get_cmap(name_cmap)
warnawarna = cimap.colors[:len(cntry)]
ax.bar(unique_year, total_prod, color=warnawarna)

left_col.pyplot(figure)

left_col.subheader("Tabel Data Produksi Minyak Mentah Negara yang Dipilih")
zasdsad = pd.DataFrame({
    'Tahun Unik':unique_year,
    'Produksi minyak mentah':total_prod
})
left_col.dataframe(zasdsad)
###############  left column ###############

###############  middle column ###############
mid_col.subheader("Produksi Terbesar")

dataframe_2=dataframe.sort_values(by=['produksi'], ascending=False)
dataframe_2 = dataframe_2.loc[dataframe_2['tahun']==tahun]
sum_produksi = []
negara_negara=[]
a=0
for s in dataframe_2['produksi']:
    if a < n_country:
        sum_produksi.append(s)
        a+=1
a=0
for s in dataframe_2['nama_negara']:
    if a < n_country:
        negara_negara.append(s)
        a+=1

figure, ax = plt.subplots()
ax.barh(negara_negara, sum_produksi, color=warnawarna)
ax.set_yticklabels(negara_negara, rotation=0)
ax.invert_yaxis()  # labels read top-to-bottom

plt.tight_layout()

mid_col.pyplot(figure)
mid_col.subheader("Tabel Data Produksi Minyak Terbesar")
zasdsadsa = pd.DataFrame({
    'Daftar Negara':negara_negara,
    'Produksi':sum_produksi
})
mid_col.dataframe(zasdsadsa)
############### middle column ###############

###############  right column ###############
right_col.subheader(" Produksi Terbesar secara Kumulatif Keseluruhan Tahun")

dataframe_3 = pd.DataFrame(dataframe, columns= ['nama_negara','produksi'])
dataframe_3['total_prod'] =  dataframe_3.groupby(['nama_negara'])['produksi'].transform('sum')
dataframe_3 = dataframe_3.drop_duplicates(subset=['nama_negara'])
dataframe_3=dataframe_3.sort_values(by=['total_prod'], ascending=False)
negara_negara2=[]
total_prod=[]
b=0
for s in dataframe_3['total_prod']:
    if b < n_country:
        total_prod.append(s)
        b+= 1
b=0
for s in dataframe_3['nama_negara']:
    if b < n_country:
        negara_negara2.append(s)
        b+=1

figure, ax = plt.subplots()
ax.bar(negara_negara2, total_prod, color=warnawarna)

plt.tight_layout()

right_col.pyplot(figure)
right_col.subheader("Tabel Data Produksi Kumulatif Minyak Terbesar")
zasdsads = pd.DataFrame({
    'Daftar Negara':negara_negara2,
    'Produksi Kumulatif':total_prod
})
right_col.dataframe(zasdsads)
############### right column ###############

left_col.subheader("SUMMARY")
for x in range(len(det)):
    if negara == det[x]['name']:
        index_negara = x
middle_col.header('Informasi Negara yang Anda Pilih')
st.write('Nama Lengkap Negara: %s' % (det[index_negara]['name']))
st.write('Kode alpha-2: %s' % (det[index_negara]['alpha-2']))
st.write('Kode alpha-3: %s' % (det[index_negara]['alpha-3']))
st.write('Kode Negara: %s' % (det[index_negara]['country-code']))
st.write('Region: %s' % (det[index_negara]['region']))
st.write('Sub-Region: %s' % (det[index_negara]['sub-region']))
st.header('Informasi Produksi Minyak Negara yang Anda Pilih')
zasdsad = zasdsad.sort_values(by='Produksi minyak mentah', ascending=False)
datanonzero = zasdsad.loc[zasdsad['Produksi minyak mentah'] > 0, 'Tahun Unik']
dat_terbesar = datanonzero.values[0]
dat_terkecil = datanonzero.values[len(datanonzero)-1]
middle_col.write(f'Produksi Terbesar Terjadi pada Tahun: {dat_terbesar}')
middle_col.write(f'Produksi Terkecil Terjadi pada Tahun: {dat_terkecil}')
sum_data = zasdsad['Produksi minyak mentah'].sum()
middle_col.write(f'Produksi Kumulatif Keseluruhan Tahun dari Negara Ini yakni Sebesar: {sum_data:.2f}')
