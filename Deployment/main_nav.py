from re import A
from cv2 import resize, sort
from matplotlib import image
from pyparsing import col
from requests import options
import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import seaborn as sns
import matplotlib.pyplot as plt
import pickle
df = pd.read_csv('tesimages.csv')
pageicon = Image.open('MakanKuy!.png')
side2=Image.open('side2.jpg')
side3=Image.open('side3.jpg')
home1=Image.open('home6.png')
home2=Image.open('home7.jpg')
home3=Image.open('home10.jpg')
home4=Image.open('home11.jpg')
home5=Image.open('home12.jpg')
home6=Image.open('home13.jpg')
home7=Image.open('home1.jpg')
home8=Image.open('home15.jpg')
home9=Image.open('home16.jpg')


st.set_page_config(
    page_title="MAKAN KUY!",
    page_icon=pageicon,
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.github.com/reynaldimarchiano',
        'Report a bug': "https://www.google.com",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

header = Image.open('header.png')
header2 = Image.open('welcome3.png')
# header2 = header2.resize((1300,300))
st.image('header.png', use_column_width=True)
# st.write('Makankuy! adalah sebuah aplikasi pemesanan tempat makan terdekat, yang dapat memberikan rekomendasi berdasarkan suasana yang diinginkan oleh customer serta preferensi tempat makan yang telah diketahui customer.')
st.write('-----')

# st.sidebar.title('Menu')
opsi =st.sidebar.selectbox('MENU', ['Beranda', 'Rekomendasi berdasarkan budget', 'Rekomendasi berdasarkan referensi tempat makanmu'])
st.sidebar.image('MakanKuy!2.png', width=300)
# st.sidebar.image('side2.jpg', width=300)
st.sidebar.image('side3.jpg', width=300)

# st.subheader('Apa yang sedang dicari ?')
# opsi = st.selectbox('', ['Beranda', 'Rekomendasi berdasarkan budget', 'Rekomendasi berdasarkan referensi tempat makanmu'])

# with st.container():
#     st.caption("Hacktiv8 - Batch 11 - Reynaldi Marchiano")
#     st.title("Analisa Penjualan di Myanmar")

# st.write('----')
df_percent = pd.read_csv('df_percent.csv')
df_percent.set_index('Nama Restaurant', inplace=True)
indices = pd.Series(df_percent.index)
cosdf = pd.read_csv('cos.csv',header=None)
cosine_similarities = cosdf.to_numpy()
def recommend(name, cosine_similarities = cosine_similarities):
    recommend_restaurant = []
    idx = indices[indices == name].index[0]
    score_series = pd.Series(cosine_similarities[idx]).sort_values(ascending=False)
    top30_indexes = list(score_series.iloc[0:31].index)
    for each in top30_indexes:
        recommend_restaurant.append(list(df_percent.index)[each])
    dat_for_filter = pd.DataFrame(columns=['Rating', 'Price', 'Daerah','Tipe_1', 'Tipe_2', 'Tipe_3'])
    for each in recommend_restaurant:
        dat_for_filter = dat_for_filter.append(pd.DataFrame(df_percent[['Rating', 'Price', 'Daerah','Tipe_1', 'Tipe_2', 'Tipe_3']][df_percent.index == each].sample()))
    dat_for_filter = dat_for_filter.drop_duplicates(subset=['Rating', 'Price', 'Daerah','Tipe_1', 'Tipe_2', 'Tipe_3'], keep=False)
    dat_for_filter = dat_for_filter.head(6)
    print('TOP %s TEMPAT MAKAN/RESTORAN YANG MEMILIKI REVIEW MIRIP %s : ' % (str(len(dat_for_filter)-1), name))
    return dat_for_filter[1:]

nama = (df['Nama'].sort_values()).reset_index(drop=True)
if opsi == 'Beranda':
    # st.subheader('Beranda')
    # st.header('-------------------------------------- SELAMAT DATANG DI MakanKuy! ------------------------------------------')
    st.image(header2)
    # st.write('----')
    st.subheader('Klik untuk melihat partner MakanKuy!')
    st.write('Kami bekerja sama dengan 100+ tempat makan di Jakarta Selatan untuk memberikan rekomendasi terbaik untuk kepuasan Anda')
    # st.button('Lihat Partner Kami')
    if st.button('Lihat Partner Kami'):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            for i in range (0,35):
                st.write(i+1,'. ', nama[i])
        with col2:
            for i in range (35,70):
                st.write(i+1,'. ', nama[i])
        with col3:
            for i in range (70,105):
                st.write(i+1,'. ', nama[i])
        with col4:
            for i in range (105,120):
                st.write(i+1,'. ', nama[i])
            st.subheader('...dan masih banyak lagi!')
    st.write('-------')

    st.header('Jelajahi MakanKuy!')
    col1, col2, col3 = st.columns(3)
    with col1:
        st.image(home1, use_column_width=True)
    with col2:
        st.image(home2, use_column_width=True)
    with col3:
        st.image(home3, use_column_width=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.image(home7, use_column_width=True)
    with col2:
        st.image(home8, use_column_width=True)
    with col3:
        st.image(home9, use_column_width=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.image(home4, use_column_width=True)
    with col2:
        st.image(home5, use_column_width=True)
    with col3:
        st.image(home6, use_column_width=True)
elif opsi == 'Rekomendasi berdasarkan budget':
    st.header('REKOMENDASI BERDASARKAN BUDGET')
    st.subheader('Silahkan isi sesuai dengan yang kamu mau!')
    col1, col2 = st.columns(2)
    with col1:
        daerah =  st.selectbox('Pilih Daerah : ', sorted(df['Daerah'].unique()))
    with col2:
        tipe = st.selectbox('Pilih Tipe : ', sorted(df['Tipe_1'].unique()))
    
    col1, col2 = st.columns(2)
    with col1:
        budget = st.slider('Masukkan Budget : ', min_value=0, max_value=1500000, value=100000, step=25000)
    with col2:
        rating = st.slider('Masukkan Rating : ', min_value=0.0, max_value=5.0,step=0.1,value=5.0)
    userinput = st.text_input('Yang Sedang Dicari : ')
    st.button('Cari')
else:
    st.header('>>Kami berikan rekomendasi sesuai dengan referensi tempat makanmu')
    st.subheader('Silahkan isi sesuai dengan yang kamu mau!')
    
    resto = st.selectbox('Pilih Tempat Makan Referensimu', nama)
    st.write(resto)
    rt = ' /5'
    # st.write((df.loc[df['Nama']==resto])['Images'])
    tes1=Image.open(df.loc[df['Nama']==resto]['Images'].values[0])
    tes1=tes1.resize((800,500))
    col1, col2 = st.columns((3,2))
    with col1:
        st.image(tes1)
    with col2:
        cont1 = st.container()
        cont1.header(df.loc[df['Nama']==resto]['Nama'].values[0])
        cont1.write('-----')
        cont1.subheader('DAERAH : ' +df.loc[df['Nama']==resto]['Daerah'].values[0])
        cont1.subheader('HARGA : '+ str(df.loc[df['Nama']==resto]['Price'].values[0]))
        cont1.subheader('KATEGORI : ')
        cont1.subheader('> '+ df.loc[df['Nama']==resto]['Tipe_1'].values[0] +', '+ df.loc[df['Nama']==resto]['Tipe_2'].values[0])
        cont1.subheader('RATING : ' + str(df.loc[df['Nama']==resto]['Rating'].values[0]) + str(' / 5'))
    if st.button('Cari'):
        st.header('Berikut adalah rekomendasi sesuai referensimu : ')
        st.spinner('Memuat...')
        rcmnd = recommend(resto)
        # st.write(rcmnd)
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.subheader('1.')
            res1 = Image.open(df.loc[df['Nama']==rcmnd.index[0]]['Images'].values[0])
            st.image(res1, use_column_width=True,caption=rcmnd.index[0]+', '+rcmnd['Daerah'].values[0])
        with col2:
            st.subheader('2.')
            res2 = Image.open(df.loc[df['Nama']==rcmnd.index[1]]['Images'].values[0])
            st.image(res2, use_column_width=True,caption=rcmnd.index[1]+', '+rcmnd['Daerah'].values[1])
        with col3:
            st.subheader('3.')
            res3 = Image.open(df.loc[df['Nama']==rcmnd.index[2]]['Images'].values[0])
            st.image(res3, use_column_width=True,caption=rcmnd.index[2]+', '+rcmnd['Daerah'].values[2])
        with col4:
            st.subheader('4.')
            res4 = Image.open(df.loc[df['Nama']==rcmnd.index[3]]['Images'].values[0])
            st.image(res4, use_column_width=True,caption=rcmnd.index[3]+', '+rcmnd['Daerah'].values[3])
        with col5:
            st.subheader('5.')
            res5 = Image.open(df.loc[df['Nama']==rcmnd.index[4]]['Images'].values[0])
            st.image(res5, use_column_width=True,caption=rcmnd.index[4]+', '+rcmnd['Daerah'].values[4])

# st.subheader('Media')




# pages =  {'Data Visualization':data_viz,
#           'Hypothesis Testing':hypo_test}

          

# selected=st.sidebar.selectbox("Please Select Page:",options=pages.keys())
# img= Image.open("—Pngtree—flag of the myanmar with_5297502.png")
# img2= Image.open('pngwing.png')

# st.sidebar.image(img,use_column_width=True)
# st.sidebar.image(img2,width=250)



# page=pages[selected]

# page.app()
