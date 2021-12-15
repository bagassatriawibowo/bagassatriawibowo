import matplotlib.pyplot as plt
from matplotlib import cm
import json
import pandas as pd
import streamlit as st
from PIL import Image
import numpy as np

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
image = Image.open('Oildrop.png')
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

############### lower left column ###############
left_col.subheader("Produksi Minyak Mentah Per Negara")

total_prod=[]
for s in dataframe[dataframe['nama_negara']==negara]['produksi'] :
    total_prod.append(s)

figure, ax = plt.subplots()
name_cmap = 'Pastel2'
cimap = cm.get_cmap(name_cmap)
warnawarna = cimap.colors[:len(cntry)]
ax.bar(unique_year, total_prod, color=warnawarna)

left_col.pyplot(figure)

zasdsad = pd.DataFrame({
    'Tahun Unik':unique_year,
    'Produksi minyak mentah':total_prod
})
st.table(zasdsad)
############### lower left column ###############

############### lower middle column ###############
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

zasdsadsa = pd.DataFrame({
    'Daftar Negara':negara_negara,
    'Produksi':sum_produksi
})
st.table(zasdsadsa)
############### lower middle column ###############

############### lower right column ###############
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
        b+=1
b=0
for s in dataframe_3['nama_negara']:
    if b < n_country:
        negara_negara2.append(s)
        b+=1

figure, ax = plt.subplots()
ax.bar(negara_negara2, total_prod, color=warnawarna)

plt.tight_layout()

right_col.pyplot(figure)

zasdsads = pd.DataFrame({
    'Daftar Negara':negara_negara2,
    'Produksi Kumulatif':total_prod
})
st.table(zasdsads)
############### lower right column ###############
right_col.subheader("Summary")
max_produksi = np.asarray(total_prod).max()
max_produksi_idx = np.asarray(total_prod).argmax()
right_col.markdown(f"**Negara dengan total produksi terbanyak adalah : {negara_negara2[max_produksi_idx]} ({max_produksi}). Pada tahun {tahun} produksi terbanyaknya yakni sebesar:**\n {negara_negara2[sum_produksi]}")

