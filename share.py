import matplotlib.pyplot as plt
from matplotlib import cm
import json
import pandas as pd
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
#image = Image.open('begs.png')
#st.sidebar.image(image)

st.sidebar.title("Setelan")
left_col, mid_col, right_col = st.columns(3)

## User inputs on the control panel
st.sidebar.subheader("Setelan tampilan")
cntry=list(dict.fromkeys(nama_negara))
cntry.remove(0)
negara = st.sidebar.selectbox("Pilihlah Negara", cntry)
n_country = st.sidebar.number_input("Total Negara", min_value=1, max_value=None, value=1)
unique_year = list(dataframe['tahun'].unique())
tahun = st.sidebar.selectbox ("Tahun", unique_year)

############### lower left column ###############
left_col.subheader("Produksi Minyak Mentah Per Negara")

total_prod=[]
for i in dataframe[dataframe['nama_negara']==negara]['produksi'] :
    total_prod.append(i)

fig, ax = plt.subplots()
name_cmap = 'Pastel2'
cimap = cm.get_cmap(name_cmap)
warnawarna = cimap.warnawarna[:len(country)]
ax.bar(unique_year, total_prod, color=warnawarna)

left_col.pyplot(fig)
############### lower left column ###############

############### lower middle column ###############
mid_col.subheader("Produksi Terbesar")

df_2=dataframe.sort_values(by=['produksi'], ascending=False)
df_2 = df_2.loc[df_2['tahun']==tahun]
total_produksi = []
list_negara=[]
a=0
for i in df_2['produksi']:
    if a < n_country:
        total_produksi.append(i)
        a+=1
a=0
for i in df_2['nama_negara']:
    if a < n_country:
        list_negara.append(i)
        a+=1

fig, ax = plt.subplots()
ax.bar(list_negara, total_produksi, color=warnawarna)

plt.tight_layout()

mid_col.pyplot(fig)
############### lower middle column ###############

############### lower right column ###############
right_col.subheader("---------------")

df_3 = pd.DataFrame(dataframe, columns= ['nama_negara','produksi'])
df_3['total_prod'] =  df_3.groupby(['nama_negara'])['produksi'].transform('sum')
df_3 = df_3.drop_duplicates(subset=['nama_negara'])
df_3=df_3.sort_values(by=['total_prod'], ascending=False)
list_negara2=[]
total_prod=[]
y=0
for i in df_3['total_prod']:
    if y < n_country:
        total_prod.append(i)
        y+=1
y=0
for i in df_3['nama_negara']:
    if y < n_country:
        list_negara2.append(i)
        y+=1

fig, ax = plt.subplots()
ax.bar(list_negara2, total_prod, color=warnawarna)

plt.tight_layout()

right_col.pyplot(fig)
############### lower right column ###############
