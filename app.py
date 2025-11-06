import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(
    page_title = "Dashboard Analisis Pelangan Walmart",
    page_icon = "🛒",
    layout = "wide",
    initial_sidebar_state = "expanded"    
)

@st.cache_data
def load_data():
    return pd.read_csv("data/walmart.csv")

df = load_data()
df.columns = df.columns.str.lower().str.replace(' ', '_')
df['purchase_date'] = pd.to_datetime(df['purchase_date'])

st.image("walmart image.jpg", use_container_width=True)
st.title("Dashboard Perilaku Pelanggan Berbelanja di Walmart")
st.markdown("Dashboard ini memberikan gambaran mengenai **Trend** dan **Distribusi** Walmart")

st.sidebar.title("Dashboard Menu")

st.sidebar.divider()

pilihan_halaman = st.sidebar.radio(
    "pilihan halaman:",
    ("Overview", "Kelompok Pelanggan")
)

if pilihan_halaman == "Overview":
    st.sidebar.markdown("### Filter Data")

    min_date = df['purchase_date'].min().date()
    max_date = df['purchase_date'].max().date()

    date_range = st.sidebar.date_input(
        "Pilih Tanggal",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    if len(date_range) == 2:
        start_date_filter = pd.to_datetime(date_range[0])
        end_date_filter = pd.to_datetime(date_range[1])

        filtered_df = df[(df['purchase_date'] >= start_date_filter) &
                               (df['purchase_date'] <= end_date_filter)]
        
    else:
        filtered_df = df  


    selected_gender = st.sidebar.multiselect(
        "Jenis Kelamin:",
        options=df['gender'].unique().tolist(),
        default=df['gender'].unique().tolist()
    )

    filtered_df = filtered_df[filtered_df['gender'].isin(selected_gender)]

    selected_category = st.sidebar.multiselect(
        "Kategori Produk:",
        options=df['category'].unique().tolist(),
        default=df['category'].unique().tolist()
    )

    filtered_df = filtered_df[filtered_df['category'].isin(selected_category)]

    selected_payment = st.sidebar.multiselect(
        "Metode Pembayaran:",
        options=df['payment_method'].unique().tolist(),
        default=df['payment_method'].unique().tolist()
    )

    filtered_df = filtered_df[filtered_df['payment_method'].isin(selected_payment)]

    selected_discount = st.sidebar.multiselect(
        "Menggunakan Diskon:",
        options=df['discount_applied'].unique().tolist(),
        default=df['discount_applied'].unique().tolist()
    )

    filtered_df = filtered_df[filtered_df['discount_applied'].isin(selected_discount)]
    
else:
    df_filtered = df.copy()

if pilihan_halaman == "Overview":
    st.subheader("Ringkasan Penjualan Walmart")

    col1, col2, col3 = st.columns([3, 3, 3])

    total_sales = filtered_df['purchase_amount'].sum()
    total_customer = filtered_df['customer_id'].nunique()

    with col1:
        st.metric(label='Total Penjualan', value = f"RP {total_sales:,.2f}")
    with col2:
        st.metric('Jumlah Pelanggan', value=f"{total_customer}")


    st.subheader("Trend Pelanggan Walmart")

    tab1, tab2 = st.tabs(["Pendapatan", "Customer"])

    with tab1:
        st.write("### Trend Pendapatan")
    
        filtered_df['bulan'] = filtered_df['purchase_date'].dt.to_period('M').astype(str)
        sales_by_month = filtered_df.groupby('bulan')['purchase_amount'].sum().reset_index()
        sales_by_month = sales_by_month.sort_values('bulan')

        fig_monthly_sales = px.line(
            sales_by_month,
            x='bulan',
            y='purchase_amount',
            title='Trend Penjualan Walmart'
        )

        st.plotly_chart(fig_monthly_sales, use_container_width=True)

    with tab2:
        st.write("### Trend Pelanggan")
    
        filtered_df['bulan'] = filtered_df['purchase_date'].dt.to_period('M').astype(str)

        customer_by_month = filtered_df.groupby('bulan')['customer_id'].nunique().reset_index()
        customer_by_month = customer_by_month.sort_values('bulan')

        fig_monthly_customer = px.line(
            customer_by_month,
            x='bulan',
            y='customer_id',
            title='Trend Pelanggan Walmart'
        )

        st.plotly_chart(fig_monthly_customer, use_container_width=True)

if pilihan_halaman == "Kelompok Pelanggan":
    st.subheader("Visualisasi Data Pelanggan")

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Kategori", "Jenis Kelamin", "Penggunaan Diskon", "Rentang Umur", "Metode Pemabayaran"])

    with tab1:
        st.write("### Distribusi Kategori")

        sales_by_category = df_filtered.groupby(
            'category'
            )['customer_id'].nunique().reset_index()
        
        fig_category = px.pie(
            sales_by_category,
            names='category',
            values='customer_id',
            title= 'Pelanggan Berdasarkan Kategori'
        )

        st.plotly_chart(fig_category, use_container_width=True)
        st.markdown("**interpretasi:** komposisi kategori barang yang dibeli hampir sama untuk 4 kategori barang")


    with tab2:
        st.write("### Distribusi Jenis Kelamin")

        sales_by_gender = df_filtered.groupby(
            'gender'
            )['customer_id'].nunique().reset_index()
        
        fig_gender = px.pie(
            sales_by_gender,
            names='gender',
            values='customer_id',
            title= 'Pelanggan Berdasarkan Jenis Kelamin'
        )

        st.plotly_chart(fig_gender, use_container_width=True)
        st.markdown("**interpretasi:** komposisi jenis kelamin pelanggan hampir sama di 3 kategori jenis kelamin")
        st.markdown("* jenis kelamin others untuk pelanggan yang tidak menuliskan jenis kemalin atau tidak terinput oleh sistem")


    with tab3:
        st.write("### Distribusi Diskon")

        sales_by_discount = df_filtered.groupby(
            'discount_applied'
            )['customer_id'].nunique().reset_index()
        
        fig_discount = px.pie(
            sales_by_discount,
            names='discount_applied',
            values='customer_id',
            title= 'Pelanggan Berdasarkan Pengguna Diskon'
        )

        st.plotly_chart(fig_discount, use_container_width=True)
        st.markdown("**interpretasi:** komposisi pelanggan pengguna diskon dengan yang tidak menggunakan sama")

    with tab4:
        st.write("### Distribusi Umur")

        if 'filtered_df' not in locals():
            filtered_df = df.copy()

        # Hapus data umur kosong (NaN) supaya tidak error
        filtered_df = filtered_df.dropna(subset=['age'])

        # Definisi rentang umur
        bins = [0, 18, 25, 35, 50, 100]
        labels = ['0-18', '19-25', '26-35', '36-50', '50+']

        # Membuat kategori umur
        filtered_df['age_group'] = pd.cut(filtered_df['age'], bins=bins, labels=labels, right=False)

        # Hitung jumlah customer unik per kelompok umur
        sales_by_age = filtered_df.groupby('age_group')['customer_id'].nunique().reset_index()

        # Buat bar chart
        fig_age = px.bar(
            sales_by_age,
            x='age_group',
            y='customer_id',
            color='age_group',
            title='Jumlah Pelanggan Berdasarkan Rentang Umur'
        )

        st.plotly_chart(fig_age, use_container_width=True)
        st.markdown("**interpretasi:** grafik pelanggan berumur 36-50 paling sering berbelanja di walmart")

    with tab5:
        st.write("### Distrbusi Metode Pembayaran")

        sales_by_payment = filtered_df.groupby(
            'payment_method'
        )['customer_id'].nunique().reset_index()

        fig_payment = px.bar(
            sales_by_payment,
            x='payment_method',
            y='customer_id',
            color='payment_method'
        )

        st.plotly_chart(fig_payment, use_container_width=True)
        st.markdown("**interpretasi:** grafik pelanggan hampir sama di setiap bar chart")