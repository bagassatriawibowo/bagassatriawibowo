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
mid_col.subheader("Tabel Data Produksi Minyak Terbesar")
zasdsadsa = pd.DataFrame({
    'Daftar Negara':negara_negara,
    'Produksi':sum_produksi
})
mid_col.dataframe(zasdsadsa)
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
############### lower right column ###############
ch_ = csvHandler('produksi_minyak_mentah.csv')
jh_ = jsonHandler('kode_negara_lengkap.json')
st.write()
st.write()
st.header('Bagian D COKK')
T_ = st.sidebar.number_input("Summary Tahun Produksi", min_value=1971, max_value=2015)
df = ch_.dataFrame
dfJ = jh_.dataFrame
tahun = list(dict.fromkeys(df['tahun'].tolist()))
dic_maks = {'negara':[],
            'kode_negara':[],
            'region':[],
            'sub_region':[],
            'produksi':[],
            'tahun':tahun}
dic_min = {'negara':[],
           'kode_negara':[],
           'region':[],
           'sub_region':[],
           'produksi':[],
           'tahun':tahun}
dic_zero = {'negara':[],
           'kode_negara':[],
           'region':[],
           'sub_region':[],
           'produksi':[],
           'tahun':tahun}
for t in tahun:
    df_per_tahun = df[df['tahun']==t]
    produksi = np.array(df_per_tahun['produksi'].tolist())
    maks_prod = max(produksi)
    min_prod = min([p for p in produksi if p != 0])
    zero_prod = min([p for p in produksi if p == 0])
# maksimum
    kode_negara = df_per_tahun[df_per_tahun['produksi']==maks_prod]
['kode_negara'].tolist()[0]
if kode_negara == 'WLD':
    kode_negara = 'WLF'
dic_maks['negara'].append(dfJ[dfJ['alpha-3']==kode_negara]['name'].tolist()[0])
dic_maks['kode_negara'].append(kode_negara)
dic_maks['region'].append(dfJ[dfJ['alpha-3']==kode_negara]['region'].tolist()[0])
dic_maks['sub_region'].append(dfJ[dfJ['alpha-3']==kode_negara]['sub-region'].tolist()
[0])
dic_maks['produksi'].append(maks_prod)
    # minimum != 0
kode_negara = df_per_tahun[df_per_tahun['produksi']==min_prod]
['kode_negara'].tolist()[0]
if kode_negara == 'WLD':
    kode_negara = 'WLF'
dic_min['negara'].append(dfJ[dfJ['alpha-3']==kode_negara]['name'].tolist()[0])
dic_min['kode_negara'].append(kode_negara)
dic_min['region'].append(dfJ[dfJ['alpha-3']==kode_negara]['region'].tolist()[0])
dic_min['sub_region'].append(dfJ[dfJ['alpha-3']==kode_negara]['sub-region'].tolist()
[0])
dic_min['produksi'].append(min_prod)
    # zero == 0
kode_negara = df_per_tahun[df_per_tahun['produksi']==zero_prod]
['kode_negara'].tolist()[0]
if kode_negara == 'WLD':
    kode_negara = 'WLF'
dic_zero['negara'].append(dfJ[dfJ['alpha-3']==kode_negara]['name'].tolist()[0])
dic_zero['kode_negara'].append(kode_negara)
dic_zero['region'].append(dfJ[dfJ['alpha-3']==kode_negara]['region'].tolist()[0])
dic_zero['sub_region'].append(dfJ[dfJ['alpha-3']==kode_negara]['sub-region'].tolist()
[0])
dic_zero['produksi'].append(zero_prod)
    
df_maks = pd.DataFrame(dic_maks)
df_min = pd.DataFrame(dic_min)
df_zero = pd.DataFrame(dic_zero)

st.write('Info Produksi Maksimum Tahun ke-{}'.format(T_))
st.write(df_maks[df_maks['tahun']==T_])

st.write('Tabel Maks per Tahun')
st.write(df_maks)

st.write('Info Produksi Minimum (Not Zero) Tahun ke-{}'.format(T_))
st.write(df_min[df_min['tahun']==T_])

st.write('Tabel Min (Not Zero) per Tahun')
st.write(df_min)

st.write('Info Produksi Zero Tahun ke-{}'.format(T_))
st.write(df_zero[df_zero['tahun']==T_])

st.write('abel Zero per Tahun')
st.write(df_zero)
