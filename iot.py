from tkinter import N
import streamlit as st
import requests 
import pandas as pd
import json
#import matplotlib.pyplot as plt
import time
from PIL import Image

hide_st_style = """
<style>
footer {visibility: hidden;}
[data-testid="column"] {
    border: 1px solid #CCCCCC;
    padding: 5% 5% 5% 3%;
    border-radius: 5px;
    
    border-left: 0.5rem solid #9AD8E1 !important;
    box-shadow: 0 0.15rem 1.75rem 0 rgba(58, 59, 69, 0.15) !important;
    }
[data-testid="stMarkdownContainer"]{
    font-weight: 700 !important;
    text-transform: uppercase !important;
}

</style>
"""

st.markdown(hide_st_style, unsafe_allow_html=True)

def load(data):
    res = requests.get(f'https://blynk.cloud/external/api/get?token=a54M3HVTAnRMi0EVuVx0b1m4tqQfkM14&{data}')
    return res.text

counter = 1
def app():
    st.header("🚪 Dashboard 🚪")
    st.subheader("Pintu Kantor PT Tyotech Mandiri Jaya")

    image = Image.open('pintu1terbuka.png')
    image2 = Image.open('pintu2terbuka.png')
    image3 = Image.open('pintutertutup.png')

    data = {
        'Timestamp': [],
        'Keterangan Pintu 1': [],
        'Keterangan Pintu 2': [],
        'Akses Ruangan': [],
        'Jumlah Orang': []
    }

    placeholder = st.empty()
    if st.button("Reload"):
        st.experimental_rerun()

    for seconds in range(5):
        with placeholder.container():
            col1, col2 = st.columns(2)

            ket_pintu_1 = load("V1")
            ket_pintu_2 = load("V3")
            akses_ruangan = load("V2")
            jumlah_orang = load("V7")

            col1.metric("Keterangan Pintu 1", ket_pintu_1)
            col2.metric("Keterangan Pintu 2", ket_pintu_2)
            
            # Mengecek apakah Keterangan Pintu 1 adalah "Buka" dan memberikan notifikasi jika iya
            # if str(ket_pintu_1) == "Buka":
            #     st.warning("Pintu 1 terbuka!")
            
            # Mengecek apakah Keterangan Pintu 2 adalah "Buka" dan memberikan notifikasi jika iya
            #if str(ket_pintu_2) == "Buka":
            #    st.warning("Pintu 2 terbuka!")
            
            data['Timestamp'].append(pd.Timestamp.now())
            data['Keterangan Pintu 1'].append(str(ket_pintu_1))  
            data['Keterangan Pintu 2'].append(str(ket_pintu_2))  
            data['Akses Ruangan'].append((akses_ruangan))
            data['Jumlah Orang'].append((jumlah_orang))
        time.sleep(1)

    df = pd.DataFrame(data)
    df3=pd.read_csv('iot.csv')
    df3 = pd.concat([df3, df], ignore_index=True)
    df3.to_csv('iot.csv', index=False)

    # Mengecek apakah Keterangan Pintu 1 adalah "Buka" dan memberikan notifikasi jika iya
    if str(ket_pintu_1) == "Pintu 1 terbuka" and str(ket_pintu_2) == "Pintu 2 tertutup":
        st.image(image, caption='Pintu 1 terbuka')
    if str(ket_pintu_2) == "Pintu 2 terbuka" and str(ket_pintu_1) == "Pintu 1 tertutup":
        st.image(image2, caption='Pintu 2 terbuka')
    if ket_pintu_1 == "Pintu 1 tertutup" and ket_pintu_2 == "Pintu 2 tertutup":
        st.image(image3, caption='Pintu sedang tertutup')
        
    # if st.button("Lihat Histori Akses"):
    st.markdown("## Histori Akses Ruangan")

    df2 = pd.read_csv('iot.csv')
    st.dataframe(df2, height=300)
    # if st.button("Lihat Grafik Akses"):
    # plt.figure(figsize=(10, 6))
    # plt.plot(df2['Timestamp'], df2['Akses Ruangan'])
    # plt.xlabel('Timestamp')
    # plt.ylabel('Value')
    # plt.title('Grafik Akses Ruangan')
    # plt.legend()
    # st.pyplot(plt)

app_mode = st.sidebar.selectbox('MENU', ['Dashboard', 'Tentang Sistem'])

if app_mode == 'Dashboard':
    # while True:
    app()
        # time.sleep(1)

elif app_mode == 'Tentang Sistem':
    st.header('Rancang Bangun Sistem Pembukaan Pintu Hemat Daya Menggunakan Kombinasi Suara dan Fingerprint Serta Kontrol Bot Telegram Untuk Kantor PT Tyotech Mandiri Jaya')
    
    st.subheader('Tentang Sistem')
    long_paragraph = """
    Sistem dibuat dengan berbasis Internet of Things yang artinya sistem berjalan dengan adanya koneksi internet dan dapat dimonitor menggunakan aplikasi
    """
    st.write(long_paragraph)

    