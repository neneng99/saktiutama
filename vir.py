import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import os
from datetime import datetime
import matplotlib.pyplot as plt
import os
import time
from io import StringIO


# Define file paths
STOK_BARANG_FILE = 'stok_barang.csv'
PENJUALAN_FILE = 'penjualan.csv'
SUPPLIER_FILE = 'supplier.csv'
OWNER_FILE = 'owner.csv'  # Add the owner file path

# Initialize session state data if not already present
def initialize_session_state():
    if 'stok_barang' not in st.session_state:
        st.session_state.stok_barang = pd.DataFrame(columns=[
            "ID", "Nama Barang", "Merk", "Ukuran/Kemasan", "Harga", "Stok", "Persentase Keuntungan", "Waktu Input"
        ])
    if 'penjualan' not in st.session_state:
        st.session_state.penjualan = pd.DataFrame(columns=[
            "ID", "Nama Pelanggan", "Nomor Telepon", "Alamat", "Nama Barang", "Ukuran/Kemasan", "Merk", "Jumlah", "Total Harga", "Keuntungan", "Waktu"
        ])
    if 'supplier' not in st.session_state:
        st.session_state.supplier = pd.DataFrame(columns=[
            "ID", "Nama Barang", "Merk", "Ukuran/Kemasan", "Jumlah Barang", "Nama Supplier", "Tagihan", "Waktu"
        ])
    if 'owner' not in st.session_state:
        st.session_state.owner = pd.DataFrame(columns=[
            "ID", "Username", "Password"  # Adjust columns as needed
        ])

# Load data from CSV files if they exist
def load_data():
    if os.path.exists(STOK_BARANG_FILE):
        st.session_state.stok_barang = pd.read_csv(STOK_BARANG_FILE)
        # Convert 'Waktu Input' column to datetime after loading
        if 'Waktu Input' in st.session_state.stok_barang.columns:
            st.session_state.stok_barang['Waktu Input'] = pd.to_datetime(st.session_state.stok_barang['Waktu Input'])
    
    if os.path.exists(PENJUALAN_FILE):
        st.session_state.penjualan = pd.read_csv(PENJUALAN_FILE)
        # Convert 'Waktu' column to datetime after loading
        if 'Waktu' in st.session_state.penjualan.columns:
            st.session_state.penjualan['Waktu'] = pd.to_datetime(st.session_state.penjualan['Waktu'])
    
    if os.path.exists(SUPPLIER_FILE):
        st.session_state.supplier = pd.read_csv(SUPPLIER_FILE)
        # Convert 'Waktu' column to datetime after loading
        if 'Waktu' in st.session_state.supplier.columns:
            st.session_state.supplier['Waktu'] = pd.to_datetime(st.session_state.supplier['Waktu'])


# Save data to CSV files
def save_data():
    st.session_state.stok_barang.to_csv(STOK_BARANG_FILE, index=False)
    st.session_state.penjualan.to_csv(PENJUALAN_FILE, index=False)
    st.session_state.supplier.to_csv(SUPPLIER_FILE, index=False)
    st.session_state.owner.to_csv(OWNER_FILE, index=False)  # Save owner data
    st.session_state.stok_barang.to_csv("stok_barang.csv", index=False)
    st.session_state.penjualan.to_csv("penjualan.csv", index=False)
    st.session_state.supplier.to_csv("supplier.csv", index=False)
    st.session_state.piutang_konsumen.to_csv("piutang_konsumen.csv", index=False)
    st.session_state.pengeluaran.to_csv("pengeluaran.csv", index=False)
    st.session_state.historis_analisis_keuangan.to_csv("historis_analisis_keuangan.csv", index=False)
    st.session_state.historis_keuntungan_bersih.to_csv("historis_keuntungan_bersih.csv", index=False)

def save_to_excel():
    with pd.ExcelWriter("data_laporan.xlsx") as writer:
        st.session_state.stok_barang.to_excel(writer, sheet_name="Stock Barang", index=False)
        st.session_state.penjualan.to_excel(writer, sheet_name="Penjualan", index=False)
        st.session_state.supplier.to_excel(writer, sheet_name="Supplier", index=False)
        st.session_state.piutang_konsumen.to_excel(writer, sheet_name="Piutang Konsumen", index=False)
        st.session_state.pengeluaran.to_excel(writer, sheet_name="Pengeluaran", index=False)
        st.session_state.historis_analisis_keuangan.to_excel(writer, sheet_name="Historis Analisis Keuangan", index=False)
        st.session_state.historis_keuntungan_bersih.to_excel(writer, sheet_name="Historis Keuntungan Bersih", index=False)

# Function to save data to file (implement as needed)
def save_data():
    st.session_state.stok_barang.to_csv('stok_barang.csv', index=False)  # Example file path

# Function for Stock Barang page
def halaman_stock_barang():
    st.markdown('<h1 style="text-align: center;">Stock Barang</h1>', unsafe_allow_html=True)
    
    # Form input barang baru dan edit barang
    st.markdown('<h2 style="text-align: center;">Tambah/Edit Barang</h2>', unsafe_allow_html=True)
    
    # Pilih barang yang akan diedit atau pilih "Tambah Baru"
    selected_action = st.selectbox("Pilih Aksi", ["Tambah Barang", "Edit Barang"], key='action_select')
    
    if selected_action == "Edit Barang":
        # Pilih ID Barang untuk Diedit
        selected_id = st.selectbox("Pilih ID Barang untuk Diedit", st.session_state.stok_barang["ID"].tolist() + ["Tambah Baru"], key='id_select')
        
        if selected_id != "Tambah Baru":
            barang_dipilih = st.session_state.stok_barang[st.session_state.stok_barang["ID"] == selected_id]
            default_values = {
                "Nama Barang": barang_dipilih["Nama Barang"].values[0],
                "Merk": barang_dipilih["Merk"].values[0],
                "Ukuran/Kemasan": barang_dipilih["Ukuran/Kemasan"].values[0],
                "Harga": barang_dipilih["Harga"].values[0],
                "Stok": barang_dipilih["Stok"].values[0],
                "Kode Warna": barang_dipilih["Kode Warna"].values[0] if "Kode Warna" in barang_dipilih.columns else ""
            }
        else:
            default_values = {
                "Nama Barang": "",
                "Merk": "",
                "Ukuran/Kemasan": "",
                "Harga": 0,
                "Stok": 0,
                "Kode Warna": ""
            }

    else:
        # Untuk tambah barang baru, set default values kosong
        selected_id = "Tambah Baru"
        default_values = {
            "Nama Barang": "",
            "Merk": "",
            "Ukuran/Kemasan": "",
            "Harga": 0,
            "Stok": 0,
            "Kode Warna": ""
        }

    with st.form("input_barang"):
        nama_barang = st.text_input("Nama Barang", value=default_values["Nama Barang"])
        merk = st.text_input("Merk", value=default_values["Merk"])
        ukuran = st.text_input("Ukuran/Kemasan", value=default_values["Ukuran/Kemasan"])
        harga = st.number_input("Harga", min_value=0, value=int(default_values["Harga"]))
        stok = st.number_input("Stok Barang", min_value=0, value=int(default_values["Stok"]))
        kode_warna = st.text_input("Kode Warna/Base", value=default_values["Kode Warna"], placeholder="Opsional")
        
        # Calculate the selling price as 15% more than the base price
        selling_price = harga * 1.15
        
        submit = st.form_submit_button("Simpan Barang")

        if submit:
            # Check if an item with the same attributes exists
            existing_item = st.session_state.stok_barang[
                (st.session_state.stok_barang["Nama Barang"] == nama_barang) &
                (st.session_state.stok_barang["Merk"] == merk) &
                (st.session_state.stok_barang["Ukuran/Kemasan"] == ukuran) &
                (st.session_state.stok_barang["Kode Warna"] == kode_warna)
            ]

            if not existing_item.empty:
                # Update existing item
                existing_id = existing_item["ID"].values[0]
                st.session_state.stok_barang.loc[
                    st.session_state.stok_barang["ID"] == existing_id,
                    ["Stok", "Harga Jual"]
                ] = [existing_item["Stok"].values[0] + stok, selling_price]
                st.success("Stok barang berhasil diperbarui!")
            else:
                # Add new item
                new_id = st.session_state.stok_barang["ID"].max() + 1 if not st.session_state.stok_barang.empty else 1
                new_data = pd.DataFrame({
                    "ID": [new_id],
                    "Nama Barang": [nama_barang],
                    "Merk": [merk],
                    "Ukuran/Kemasan": [ukuran],
                    "Harga": [harga],
                    "Stok": [stok],
                    "Kode Warna": [kode_warna],
                    "Harga Jual": [selling_price],
                    "Waktu Input": [datetime.now()]
                })
                st.session_state.stok_barang = pd.concat([st.session_state.stok_barang, new_data], ignore_index=True)
                st.success("Barang berhasil ditambahkan!")

            save_data()  # Save data after adding or updating item

    # Tabel stok barang
    st.markdown('<h2 style="text-align: center;">Daftar Stok Barang</h2>', unsafe_allow_html=True)
    df_stok_barang = st.session_state.stok_barang.copy()
    
    # Hapus kolom "Harga" dari tabel jika ada
    if "Harga" in df_stok_barang.columns:
        df_stok_barang = df_stok_barang.drop(columns=["Harga"])
    
    # Pencarian nama barang atau merk
    search_text = st.text_input("Cari Nama Barang atau Merk", key='search_text')
    if search_text:
        df_stok_barang = df_stok_barang[
            (df_stok_barang["Nama Barang"].str.contains(search_text, case=False, na=False)) |
            (df_stok_barang["Merk"].str.contains(search_text, case=False, na=False))
        ]
    
    st.dataframe(df_stok_barang)
    
# Function for Penjualan page
def halaman_penjualan():
    st.header("Penjualan")

    # Initialize session state variables if they don't exist
    if 'penjualan' not in st.session_state:
        st.session_state.penjualan = pd.DataFrame(columns=[
            "ID", "Nama Pelanggan", "Nomor Telepon", "Alamat", 
            "Nama Barang", "Ukuran/Kemasan", "Merk", "Kode Warna", 
            "Jumlah", "Total Harga", "Keuntungan", "Waktu"
        ])

    if 'stok_barang' not in st.session_state:
        st.session_state.stok_barang = pd.DataFrame(columns=[
            "Nama Barang", "Ukuran/Kemasan", "Merk", "Harga", "Harga Jual", "Persentase Keuntungan", "Stok", "Kode Warna"
        ])

    # Form for adding/editing sales
    st.subheader("Tambah/Edit Penjualan")

    if not st.session_state.penjualan.empty:
        id_penjualan = st.selectbox("Pilih ID Penjualan untuk Diedit", st.session_state.penjualan["ID"].tolist() + ["Tambah Baru"])

        if id_penjualan != "Tambah Baru":
            penjualan_edit = st.session_state.penjualan[st.session_state.penjualan["ID"] == id_penjualan].iloc[0]
            default_values = {
                "Nama Pelanggan": penjualan_edit["Nama Pelanggan"],
                "Nomor Telepon": penjualan_edit["Nomor Telepon"],
                "Alamat": penjualan_edit["Alamat"],
                "Nama Barang": penjualan_edit["Nama Barang"],
                "Ukuran/Kemasan": penjualan_edit["Ukuran/Kemasan"],
                "Merk": penjualan_edit["Merk"],
                "Kode Warna": penjualan_edit["Kode Warna"] if "Kode Warna" in penjualan_edit.index else "",
                "Jumlah": penjualan_edit["Jumlah"]
            }
        else:
            default_values = {
                "Nama Pelanggan": "",
                "Nomor Telepon": "",
                "Alamat": "",
                "Nama Barang": st.session_state.stok_barang["Nama Barang"].tolist()[0] if not st.session_state.stok_barang.empty else "",
                "Ukuran/Kemasan": st.session_state.stok_barang["Ukuran/Kemasan"].tolist()[0] if not st.session_state.stok_barang.empty else "",
                "Merk": st.session_state.stok_barang["Merk"].tolist()[0] if not st.session_state.stok_barang.empty else "",
                "Kode Warna": "",
                "Jumlah": 1
            }
    else:
        id_penjualan = "Tambah Baru"
        default_values = {
            "Nama Pelanggan": "",
            "Nomor Telepon": "",
            "Alamat": "",
            "Nama Barang": st.session_state.stok_barang["Nama Barang"].tolist()[0] if not st.session_state.stok_barang.empty else "",
            "Ukuran/Kemasan": st.session_state.stok_barang["Ukuran/Kemasan"].tolist()[0] if not st.session_state.stok_barang.empty else "",
            "Merk": st.session_state.stok_barang["Merk"].tolist()[0] if not st.session_state.stok_barang.empty else "",
            "Kode Warna": "",
            "Jumlah": 1
        }

    with st.form("input_penjualan"):
        nama_pelanggan = st.text_input("Nama Pelanggan", value=default_values["Nama Pelanggan"])
        nomor_telpon = st.text_input("Nomor Telepon", value=default_values["Nomor Telepon"])
        alamat = st.text_area("Alamat", value=default_values["Alamat"])
        nama_barang_options = st.session_state.stok_barang["Nama Barang"].tolist()
        nama_barang = st.selectbox("Pilih Barang", nama_barang_options, index=nama_barang_options.index(default_values["Nama Barang"]) if default_values["Nama Barang"] in nama_barang_options else 0)

        ukuran_options = st.session_state.stok_barang[st.session_state.stok_barang["Nama Barang"] == nama_barang]["Ukuran/Kemasan"].tolist()
        ukuran = st.selectbox("Ukuran/Kemasan", ukuran_options, index=ukuran_options.index(default_values["Ukuran/Kemasan"]) if default_values["Ukuran/Kemasan"] in ukuran_options else 0)

        merk_options = st.session_state.stok_barang[
            (st.session_state.stok_barang["Nama Barang"] == nama_barang) &
            (st.session_state.stok_barang["Ukuran/Kemasan"] == ukuran)
        ]["Merk"].tolist()
        merk = st.selectbox("Merk", merk_options, index=merk_options.index(default_values["Merk"]) if default_values["Merk"] in merk_options else 0)

        kode_warna = st.text_input("Kode Warna", value=default_values["Kode Warna"], placeholder="Opsional")
        jumlah = st.number_input("Jumlah Orderan", min_value=1, value=int(default_values["Jumlah"]))

        submit = st.form_submit_button("Simpan Penjualan")

        if submit:
            stok_barang_filter = st.session_state.stok_barang[
                (st.session_state.stok_barang["Nama Barang"] == nama_barang) &
                (st.session_state.stok_barang["Ukuran/Kemasan"] == ukuran) &
                (st.session_state.stok_barang["Merk"] == merk)
            ]

            if not stok_barang_filter.empty:
                harga_jual = stok_barang_filter["Harga Jual"].values[0]  # Use Harga Jual
                persentase_keuntungan = stok_barang_filter["Persentase Keuntungan"].values[0]
                total_harga = harga_jual * jumlah
                keuntungan = total_harga * (persentase_keuntungan / 100)
                waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                new_penjualan = pd.DataFrame({
                    "ID": [st.session_state.penjualan["ID"].max() + 1 if not st.session_state.penjualan.empty else 1],
                    "Nama Pelanggan": [nama_pelanggan],
                    "Nomor Telepon": [nomor_telpon],
                    "Alamat": [alamat],
                    "Nama Barang": [nama_barang],
                    "Ukuran/Kemasan": [ukuran],
                    "Merk": [merk],
                    "Kode Warna": [kode_warna if "Kode Warna" in st.session_state.stok_barang.columns else ""],
                    "Jumlah": [jumlah],
                    "Total Harga": [total_harga],
                    "Keuntungan": [keuntungan],
                    "Waktu": [waktu]
                })

                if id_penjualan == "Tambah Baru":
                    st.session_state.penjualan = pd.concat([st.session_state.penjualan, new_penjualan], ignore_index=True)
                else:
                    st.session_state.penjualan.loc[st.session_state.penjualan["ID"] == id_penjualan, 
                        ["Nama Pelanggan", "Nomor Telepon", "Alamat", "Nama Barang", "Ukuran/Kemasan", "Merk", "Kode Warna", "Jumlah", "Total Harga", "Keuntungan", "Waktu"]] = \
                        [nama_pelanggan, nomor_telpon, alamat, nama_barang, ukuran, merk, kode_warna, jumlah, total_harga, keuntungan, waktu]

                st.session_state.stok_barang.loc[
                    (st.session_state.stok_barang["Nama Barang"] == nama_barang) &
                    (st.session_state.stok_barang["Ukuran/Kemasan"] == ukuran) &
                    (st.session_state.stok_barang["Merk"] == merk),
                    "Stok"
                ] -= jumlah

                st.success(f"Penjualan untuk {nama_pelanggan} berhasil disimpan!")
                save_data()
            else:
                st.error("Kombinasi Nama Barang, Ukuran/Kemasan, dan Merk tidak ditemukan di stok.")
    
    search_barang = st.text_input("Cari Barang")
    if search_barang:
        hasil_pencarian = st.session_state.stok_barang[st.session_state.stok_barang["Nama Barang"].str.contains(search_barang, case=False)]
        st.write("Hasil Pencarian:")
        if not hasil_pencarian.empty:
            st.dataframe(hasil_pencarian, use_container_width=True, hide_index=False)

    st.subheader("Stok Barang Terupdate")
    df_stok_barang = st.session_state.stok_barang.copy()
    if "Persentase Keuntungan" in df_stok_barang.columns:
        df_stok_barang = df_stok_barang.drop(columns=["Persentase Keuntungan"])
    if "Harga" in df_stok_barang.columns:
        df_stok_barang = df_stok_barang.drop(columns=["Harga"])  # Hapus kolom Harga dari tabel
    st.dataframe(df_stok_barang, use_container_width=True, hide_index=False)

    st.subheader("Data Penjualan")
    if not st.session_state.penjualan.empty:
        st.session_state.penjualan["Nomor Telepon"] = st.session_state.penjualan["Nomor Telepon"].astype(str)
        if "Keuntungan" in st.session_state.penjualan.columns:
            st.session_state.penjualan = st.session_state.penjualan.drop(columns=["Keuntungan"])  # Hapus kolom Keuntungan dari tabel
        st.dataframe(st.session_state.penjualan, use_container_width=True, hide_index=False)

    st.subheader("Cari Data Penjualan")
    search_nama_pelanggan = st.text_input("Cari Nama Pelanggan")
    search_nomor_telpon = st.text_input("Cari Nomor Telepon")

    # Dropdown untuk memilih ID penjualan
    if not st.session_state.penjualan.empty:
        id_pilihan = st.selectbox("Pilih ID Penjualan untuk Detail", st.session_state.penjualan["ID"].tolist())
        if id_pilihan:
            penjualan_detail = st.session_state.penjualan[st.session_state.penjualan["ID"] == id_pilihan]
            st.write("Detail Penjualan:")
            st.dataframe(penjualan_detail, use_container_width=True, hide_index=False)

    # Dropdown untuk memilih ID penjualan untuk Download Struk
    if not st.session_state.penjualan.empty:
        id_penjualan = st.selectbox("Pilih ID Penjualan untuk Download Struk", st.session_state.penjualan["ID"].unique())
        
        if st.button("Download Struk Penjualan"):
            selected_sale = st.session_state.penjualan[st.session_state.penjualan["ID"] == id_penjualan].iloc[0]
            struk = StringIO()
            struk.write("=== STRUK PENJUALAN SAKTI UTAMA ===\n")
            struk.write(f"Nama Pelanggan: {selected_sale['Nama Pelanggan']}\n")
            struk.write(f"Nomor Telepon: {selected_sale['Nomor Telepon']}\n")
            struk.write(f"Alamat: {selected_sale['Alamat']}\n")
            struk.write(f"Nama Barang: {selected_sale['Nama Barang']}\n")
            struk.write(f"Ukuran/Kemasan: {selected_sale['Ukuran/Kemasan']}\n")
            struk.write(f"Merk: {selected_sale['Merk']}\n")
            if "Kode Warna" in selected_sale.index:
                struk.write(f"Kode Warna: {selected_sale['Kode Warna']}\n")
            struk.write(f"Jumlah: {selected_sale['Jumlah']}\n")
            struk.write(f"Total Harga: {selected_sale['Total Harga']}\n")
            struk.write(f"Waktu: {selected_sale['Waktu']}\n")
            struk.write("============ TERIMA KASIH ============\n")

            # Menyediakan file untuk di-download
            struk_file = 'struk_pembelian.txt'
            with open(struk_file, 'w') as f:
                f.write(struk.getvalue())
            
            with open(struk_file, 'r') as f:
                st.download_button(label="Download Struk Penjualan", data=f, file_name=struk_file, mime="text/plain")


# Fungsi untuk halaman Supplier
def halaman_supplier():
    st.header("Data Supplier")

    # Memilih ID Supplier untuk diedit atau menambah baru
    supplier_ids = st.session_state.supplier["ID"].tolist()
    supplier_ids.insert(0, "Tambah Baru")  # Opsi untuk menambah data baru
    selected_supplier_id = st.selectbox("Pilih ID Supplier untuk Diedit atau Tambah Baru", supplier_ids)

    # Jika 'Tambah Baru' dipilih, buat default nilai kosong
    if selected_supplier_id == "Tambah Baru":
        selected_supplier = None
        default_values = {
            "Nama Barang": "",
            "Merk": "",
            "Ukuran/Kemasan": "",
            "Jumlah Barang": 0,
            "Nama Supplier": "",
            "Tagihan": 0,
            "Jatuh Tempo": datetime.today()
        }
    else:
        # Ambil data dari supplier berdasarkan ID yang dipilih
        selected_supplier = st.session_state.supplier[st.session_state.supplier["ID"] == selected_supplier_id].iloc[0]
        default_values = {
            "Nama Barang": selected_supplier["Nama Barang"],
            "Merk": selected_supplier["Merk"],
            "Ukuran/Kemasan": selected_supplier["Ukuran/Kemasan"],
            "Jumlah Barang": selected_supplier["Jumlah Barang"],
            "Nama Supplier": selected_supplier["Nama Supplier"],
            "Tagihan": selected_supplier["Tagihan"],
            "Jatuh Tempo": selected_supplier["Jatuh Tempo"]
        }

    # Form input data supplier baru atau edit data supplier
    with st.form("supplier_form"):
        nama_barang = st.text_input("Nama Barang", value=default_values["Nama Barang"])
        merk = st.text_input("Merk", value=default_values["Merk"])
        ukuran = st.text_input("Ukuran/Kemasan", value=default_values["Ukuran/Kemasan"])
        jumlah_barang = st.number_input("Jumlah Barang", min_value=0, value=int(default_values["Jumlah Barang"]))
        nama_supplier = st.text_input("Nama Supplier", value=default_values["Nama Supplier"])
        tagihan = st.number_input("Tagihan", min_value=0, value=int(default_values["Tagihan"]))
        jatuh_tempo = st.date_input("Tanggal Jatuh Tempo", value=default_values["Jatuh Tempo"])
        submit = st.form_submit_button("Simpan Data Supplier")
        
        if submit:
            if selected_supplier is None:
                # Tambah data baru
                new_id = st.session_state.supplier["ID"].max() + 1 if not st.session_state.supplier.empty else 1
                new_data = pd.DataFrame({
                    "ID": [new_id],
                    "Nama Barang": [nama_barang],
                    "Merk": [merk],
                    "Ukuran/Kemasan": [ukuran],
                    "Jumlah Barang": [jumlah_barang],
                    "Nama Supplier": [nama_supplier],
                    "Tagihan": [tagihan],
                    "Waktu": [datetime.now()],
                    "Jatuh Tempo": [jatuh_tempo]
                })
                st.session_state.supplier = pd.concat([st.session_state.supplier, new_data], ignore_index=True)
                st.success("Data supplier baru berhasil ditambahkan!")
            else:
                # Update data supplier
                st.session_state.supplier.loc[st.session_state.supplier["ID"] == selected_supplier_id, 
                    ["Nama Barang", "Merk", "Ukuran/Kemasan", "Jumlah Barang", "Nama Supplier", "Tagihan", "Jatuh Tempo"]] = \
                    [nama_barang, merk, ukuran, jumlah_barang, nama_supplier, tagihan, jatuh_tempo]
                st.success(f"Data supplier ID {selected_supplier_id} berhasil diupdate!")
            
            save_data()  # Simpan data setelah menambah atau mengedit supplier

    # Pencarian berdasarkan Nama Barang atau Merk
    search_input = st.text_input("Cari Nama Barang atau Merk")
    
    if search_input:
        filtered_supplier = st.session_state.supplier[
            (st.session_state.supplier["Nama Barang"].str.contains(search_input, case=False)) |
            (st.session_state.supplier["Merk"].str.contains(search_input, case=False))
        ]
        st.write("Hasil Pencarian:")
        st.dataframe(filtered_supplier)
    else:
        # Tabel data supplier tanpa filter
        st.subheader("Daftar Data Supplier")
        st.dataframe(st.session_state.supplier)



# Fungsi untuk menyimpan semua data ke file Excel
def save_to_excel():
    with pd.ExcelWriter('data_laporan.xlsx', engine='openpyxl') as writer:
        # Simpan stok barang
        st.session_state.stok_barang.to_excel(writer, sheet_name='Stok Barang', index=False)
        
        # Simpan penjualan
        st.session_state.penjualan.to_excel(writer, sheet_name='Penjualan', index=False)
        
        # Simpan supplier
        st.session_state.supplier.to_excel(writer, sheet_name='Supplier', index=False)
        
        # Simpan pengeluaran
        st.session_state.pengeluaran.to_excel(writer, sheet_name='Pengeluaran', index=False)
        
        # Simpan piutang konsumen
        if "piutang_konsumen" in st.session_state:
            st.session_state.piutang_konsumen.to_excel(writer, sheet_name='Piutang Konsumen', index=False)

        # Simpan histori analisis keuangan
        if "historis_analisis_keuangan" in st.session_state:
            st.session_state.historis_analisis_keuangan.to_excel(writer, sheet_name='Histori Analisis Keuangan', index=False)
        
        # Simpan keuntungan bersih
        total_penjualan = st.session_state.penjualan["Total Harga"].sum()
        total_pengeluaran = st.session_state.pengeluaran["Jumlah Pengeluaran"].sum()
        total_keuntungan_bersih = total_penjualan - total_pengeluaran
        df_keuntungan_bersih = pd.DataFrame({
            "Total Penjualan": [total_penjualan],
            "Total Pengeluaran": [total_pengeluaran],
            "Keuntungan Bersih": [total_keuntungan_bersih]
        })
        df_keuntungan_bersih.to_excel(writer, sheet_name='Keuntungan Bersih', index=False)


# Fungsi untuk halaman Owner dengan pengaman password
def halaman_owner():
    st.header("Halaman Owner - Analisa Keuangan")

    # Login form
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        with st.form("login_form"):
            password = st.text_input("Masukkan Password", type="password")
            submit = st.form_submit_button("Login")
            
            if submit and password == "Jayaselalu123":  # Ganti dengan password yang Anda inginkan
                st.session_state.authenticated = True
                st.success("Login berhasil!")
            elif submit:
                st.error("Password salah!")
        return


    # Form input barang baru dan edit barang
    st.header("Stock Barang")
    
    # Tambahkan opsi untuk "Tambah Baru" di selectbox
    barang_ids = st.session_state.stok_barang["ID"].tolist()
    barang_ids.insert(0, "Tambah Baru")  # Opsi untuk menambah barang baru
    selected_row = st.selectbox("Pilih ID Barang untuk Diedit atau Tambah Baru", barang_ids)
    
    if selected_row == "Tambah Baru":
        barang_dipilih = None
        default_values = {
            "Nama Barang": "",
            "Merk": "",
            "Ukuran/Kemasan": "",
            "Harga": 0,
            "Stok": 0,
            "Persentase Keuntungan": 0,
            "Kode Warna": ""
        }
    else:
        barang_dipilih = st.session_state.stok_barang[st.session_state.stok_barang["ID"] == selected_row]
        default_values = {
            "Nama Barang": barang_dipilih["Nama Barang"].values[0],
            "Merk": barang_dipilih["Merk"].values[0],
            "Ukuran/Kemasan": barang_dipilih["Ukuran/Kemasan"].values[0],
            "Harga": barang_dipilih["Harga"].values[0] if pd.notna(barang_dipilih["Harga"].values[0]) else 0,
            "Stok": barang_dipilih["Stok"].values[0] if pd.notna(barang_dipilih["Stok"].values[0]) else 0,
            "Persentase Keuntungan": barang_dipilih["Persentase Keuntungan"].values[0] if pd.notna(barang_dipilih["Persentase Keuntungan"].values[0]) else 0,
            "Kode Warna": barang_dipilih["Kode Warna"].values[0] if "Kode Warna" in barang_dipilih.columns else ""
        }
    
    with st.form("edit_barang"):
        nama_barang = st.text_input("Nama Barang", value=default_values["Nama Barang"])
        merk = st.text_input("Merk", value=default_values["Merk"])
        ukuran = st.text_input("Ukuran/Kemasan", value=default_values["Ukuran/Kemasan"])
        
        harga = st.number_input("Harga", min_value=0, value=int(default_values["Harga"]))
        stok = st.number_input("Stok Barang", min_value=0, value=int(default_values["Stok"]))
        persentase_keuntungan = st.number_input("Persentase Keuntungan (%)", min_value=0, max_value=100, value=int(default_values["Persentase Keuntungan"]))
        kode_warna = st.text_input("Kode Warna/Base", value=default_values["Kode Warna"], placeholder="Opsional")
        
        # Calculate the selling price as base price plus profit percentage
        selling_price = harga * (1 + (persentase_keuntungan / 100))
        
        submit = st.form_submit_button("Simpan Barang")
    
        if submit:
            if barang_dipilih is None:
                # Tambah barang baru
                new_id = st.session_state.stok_barang["ID"].max() + 1 if not st.session_state.stok_barang.empty else 1
                new_data = pd.DataFrame({
                    "ID": [new_id],
                    "Nama Barang": [nama_barang],
                    "Merk": [merk],
                    "Ukuran/Kemasan": [ukuran],
                    "Harga": [harga],
                    "Stok": [stok],
                    "Persentase Keuntungan": [persentase_keuntungan],
                    "Kode Warna": [kode_warna],
                    "Harga Jual": [selling_price],
                    "Waktu Input": [datetime.now()]
                })
                st.session_state.stok_barang = pd.concat([st.session_state.stok_barang, new_data], ignore_index=True)
                st.success("Barang baru berhasil ditambahkan!")
            else:
                # Update barang yang ada
                st.session_state.stok_barang.loc[st.session_state.stok_barang["ID"] == selected_row, 
                    ["Nama Barang", "Merk", "Ukuran/Kemasan", "Harga", "Stok", "Persentase Keuntungan", "Kode Warna", "Harga Jual"]] = \
                    [nama_barang, merk, ukuran, harga, stok, persentase_keuntungan, kode_warna, selling_price]
                st.success(f"Barang ID {selected_row} berhasil diupdate!")
            
            save_data()  # Simpan data setelah menambah atau mengedit barang
    
    # Tabel stok barang
    st.subheader("Daftar Stok Barang")
    df_stok_barang = st.session_state.stok_barang.copy()
    
    # Hapus kolom "Persentase Keuntungan" dan "Harga" dari tabel jika ada
    if "Persentase Keuntungan" in df_stok_barang.columns:
        df_stok_barang = df_stok_barang.drop(columns=["Persentase Keuntungan"])
    
    if "Harga" in df_stok_barang.columns:
        df_stok_barang = df_stok_barang.drop(columns=["Harga"])
    
    # Pencarian nama barang atau merk
    search_text = st.text_input("Cari Nama Barang atau Merk", key='search_text')
    if search_text:
        df_stok_barang = df_stok_barang[
            (df_stok_barang["Nama Barang"].str.contains(search_text, case=False, na=False)) |
            (df_stok_barang["Merk"].str.contains(search_text, case=False, na=False))
        ]
    
    st.dataframe(df_stok_barang)
    
    # Tombol untuk hapus barang (jika ID bukan 'Tambah Baru')
    if selected_row != "Tambah Baru" and st.button("Hapus Barang"):
        st.session_state.stok_barang = st.session_state.stok_barang[st.session_state.stok_barang["ID"] != selected_row]
        st.success(f"Barang ID {selected_row} berhasil dihapus!")
        save_data()  # Simpan data setelah menghapus barang
        
    # Check if 'penjualan' DataFrame exists and has required columns
    if 'penjualan' not in st.session_state:
        st.error("Data penjualan tidak ditemukan.")
    else:
        # Analisa keuangan dengan grafik pemasaran
        st.subheader("Analisa Keuangan")
    
        # Perhitungan total penjualan
        if "Total Harga" in st.session_state.penjualan.columns:
            total_penjualan = st.session_state.penjualan["Total Harga"].sum()
            st.write(f"Total Penjualan: Rp {total_penjualan:,.0f}")
        else:
            st.error("Kolom 'Total Harga' tidak ditemukan dalam data penjualan.")
        
        # Grafik total penjualan per barang dan merk
        if not st.session_state.penjualan.empty and "Nama Barang" in st.session_state.penjualan.columns and "Merk" in st.session_state.penjualan.columns:
            st.subheader("Grafik Penjualan Per Barang dan Merk")
    
            # Group by "Nama Barang" and "Merk" and sum the "Total Harga"
            sales_per_item_and_brand = st.session_state.penjualan.groupby(["Nama Barang", "Merk"])["Total Harga"].sum().reset_index()
    
            # Create a bar plot
            plt.figure(figsize=(14, 8))
            for key, grp in sales_per_item_and_brand.groupby(['Nama Barang']):
                plt.bar(grp['Merk'] + ' (' + grp['Nama Barang'] + ')', grp['Total Harga'], label=key)
    
            # Customize the plot
            plt.title("Total Penjualan per Barang dan Merk", fontsize=16)
            plt.xlabel("Barang dan Merk", fontsize=14)
            plt.ylabel("Total Penjualan (Rp)", fontsize=14)
            plt.xticks(rotation=45, ha="right", fontsize=12)
            plt.legend(title='Nama Barang', bbox_to_anchor=(1.05, 1), loc='upper left')
    
            # Display the plot in Streamlit
            st.pyplot(plt)
        else:
            st.write("Data penjualan kosong atau kolom 'Nama Barang' atau 'Merk' tidak ditemukan.")
    
    # Perhitungan tagihan supplier bulanan
    current_month = datetime.now().strftime("%Y-%m")
    st.session_state.supplier['Waktu'] = pd.to_datetime(st.session_state.supplier['Waktu'])
    monthly_supplier_bills = st.session_state.supplier[st.session_state.supplier["Waktu"].dt.strftime("%Y-%m") == current_month]["Tagihan"].sum()
    st.write(f"Total Tagihan Supplier Bulan Ini: Rp {monthly_supplier_bills}")
    
    # Menghitung total penjualan
    total_penjualan = st.session_state.penjualan["Total Harga"].sum()

    # Menghitung total tagihan supplier
    if not st.session_state.supplier.empty:
        monthly_supplier_bills = st.session_state.supplier["Tagihan"].sum()
    else:
        monthly_supplier_bills = 0

    # Menghitung selisih antara total penjualan dan tagihan supplier
    selisih = total_penjualan - monthly_supplier_bills

    # Menampilkan hasil perbandingan
    st.write(f"Total Penjualan: Rp {total_penjualan:,.0f}")
    st.write(f"Total Tagihan Supplier: Rp {monthly_supplier_bills:,.0f}")
    st.write(f"Selisih antara Total Penjualan dan Tagihan Supplier: Rp {selisih:,.0f}")

    # Membuat DataFrame untuk analisis keuangan
    analisis_keuangan_df = pd.DataFrame({
        "Tanggal": [datetime.now().strftime("%Y-%m-%d")],
        "Total Penjualan": [total_penjualan],
        "Total Tagihan Supplier": [monthly_supplier_bills],
        "Selisih": [selisih]
    })

    # Menampilkan tabel analisis keuangan
    st.subheader("Tabel Analisis Keuangan")
    st.dataframe(analisis_keuangan_df)

    # Menyimpan histori analisis keuangan ke file CSV
    if "historis_analisis_keuangan" not in st.session_state:
        st.session_state.historis_analisis_keuangan = pd.DataFrame(columns=["Tanggal", "Total Penjualan", "Total Tagihan Supplier", "Selisih"])

    st.session_state.historis_analisis_keuangan = pd.concat([st.session_state.historis_analisis_keuangan, analisis_keuangan_df], ignore_index=True)

    # Menampilkan tabel data supplier dengan pencarian
    st.subheader("Data Supplier")
    
    search_input = st.text_input("Cari Nama Barang atau Merk")
    
    if search_input:
        filtered_supplier = st.session_state.supplier[
            (st.session_state.supplier["Nama Barang"].str.contains(search_input, case=False)) |
            (st.session_state.supplier["Merk"].str.contains(search_input, case=False))
        ]
        st.write("Hasil Pencarian:")
        st.dataframe(filtered_supplier)
    else:
        st.dataframe(st.session_state.supplier)

        # Inisialisasi piutang konsumen jika belum ada
    if 'piutang_konsumen' not in st.session_state:
        st.session_state.piutang_konsumen = pd.DataFrame(columns=[
            "Nama Konsumen", "Alamat", "Nomor Telepon", "Nama Barang", "Merk", 
            "Kode Warna", "Ukuran/Kemasan", "Jumlah", "Total Tagihan", 
            "Cicilan Tagihan", "Sisa Tagihan", "Janji Bayar"
        ])

    # Form Piutang Konsumen
    st.subheader("Form Piutang Konsumen")

    with st.form("form_piutang"):
        nama_konsumen = st.text_input("Nama Konsumen")
        alamat = st.text_input("Alamat")
        nomor_telepon = st.text_input("Nomor Telepon")
        nama_barang = st.text_input("Nama Barang")
        merk = st.text_input("Merk")
        kode_warna = st.text_input("Kode Warna (opsional)")
        ukuran = st.text_input("Ukuran/Kemasan")
        jumlah = st.number_input("Jumlah", min_value=1)
        total_tagihan = st.number_input("Total Tagihan", min_value=0)
        cicilan_tagihan = st.number_input("Cicilan Tagihan (opsional)", min_value=0, value=0)
        janji_bayar = st.date_input("Janji Bayar")

        # Menghitung Sisa Tagihan
        sisa_tagihan = total_tagihan - cicilan_tagihan

        # Tombol submit untuk menambahkan atau mengedit data piutang
        submit_piutang = st.form_submit_button("Tambah/Edit Piutang")

        if submit_piutang:
            new_piutang = {
                "Nama Konsumen": nama_konsumen,
                "Alamat": alamat,
                "Nomor Telepon": nomor_telepon,
                "Nama Barang": nama_barang,
                "Merk": merk,
                "Kode Warna": kode_warna if kode_warna else "",
                "Ukuran/Kemasan": ukuran,
                "Jumlah": jumlah,
                "Total Tagihan": total_tagihan,
                "Cicilan Tagihan": cicilan_tagihan if cicilan_tagihan else 0,
                "Sisa Tagihan": sisa_tagihan,
                "Janji Bayar": janji_bayar
            }

            # Tambah data piutang ke session state
            st.session_state.piutang_konsumen = st.session_state.piutang_konsumen.append(new_piutang, ignore_index=True)
            st.success("Piutang konsumen berhasil ditambahkan!")
            save_data()  # Panggil fungsi untuk menyimpan data

    # Tabel Piutang Konsumen
    st.subheader("Tabel Piutang Konsumen")

    # Tampilkan tabel piutang dengan fitur edit dan hapus
    if not st.session_state.piutang_konsumen.empty:
        st.dataframe(st.session_state.piutang_konsumen)

        # Pilih piutang yang akan diedit
        selected_row = st.selectbox("Pilih Nama Konsumen untuk Diedit", st.session_state.piutang_konsumen["Nama Konsumen"])

        piutang_dipilih = st.session_state.piutang_konsumen[st.session_state.piutang_konsumen["Nama Konsumen"] == selected_row]

        # Form untuk edit piutang konsumen
        with st.form("edit_piutang"):
            nama_konsumen_edit = st.text_input("Nama Konsumen", value=piutang_dipilih["Nama Konsumen"].values[0])
            alamat_edit = st.text_input("Alamat", value=piutang_dipilih["Alamat"].values[0])
            nomor_telepon_edit = st.text_input("Nomor Telepon", value=piutang_dipilih["Nomor Telepon"].values[0])
            nama_barang_edit = st.text_input("Nama Barang", value=piutang_dipilih["Nama Barang"].values[0])
            merk_edit = st.text_input("Merk", value=piutang_dipilih["Merk"].values[0])
            kode_warna_edit = st.text_input("Kode Warna (opsional)", value=piutang_dipilih["Kode Warna"].values[0])
            ukuran_edit = st.text_input("Ukuran/Kemasan", value=piutang_dipilih["Ukuran/Kemasan"].values[0])
            jumlah_edit = st.number_input("Jumlah", min_value=1, value=int(piutang_dipilih["Jumlah"].values[0]))
            total_tagihan_edit = st.number_input("Total Tagihan", min_value=0, value=int(piutang_dipilih["Total Tagihan"].values[0]))
            cicilan_tagihan_edit = st.number_input("Cicilan Tagihan (opsional)", min_value=0, value=int(piutang_dipilih["Cicilan Tagihan"].values[0]))
            janji_bayar_edit = st.date_input("Janji Bayar", value=pd.to_datetime(piutang_dipilih["Janji Bayar"].values[0]))

            sisa_tagihan_edit = total_tagihan_edit - cicilan_tagihan_edit

            submit_edit_piutang = st.form_submit_button("Update Piutang")

            if submit_edit_piutang:
                st.session_state.piutang_konsumen.loc[st.session_state.piutang_konsumen["Nama Konsumen"] == selected_row, [
                    "Nama Konsumen", "Alamat", "Nomor Telepon", "Nama Barang", "Merk", 
                    "Kode Warna", "Ukuran/Kemasan", "Jumlah", "Total Tagihan", 
                    "Cicilan Tagihan", "Sisa Tagihan", "Janji Bayar"
                ]] = [nama_konsumen_edit, alamat_edit, nomor_telepon_edit, nama_barang_edit, merk_edit, 
                      kode_warna_edit, ukuran_edit, jumlah_edit, total_tagihan_edit, cicilan_tagihan_edit, 
                      sisa_tagihan_edit, janji_bayar_edit]
                st.success("Piutang konsumen berhasil diupdate!")
                save_data()  # Simpan perubahan data

        # Tombol hapus piutang
        if st.button("Hapus Piutang"):
            st.session_state.piutang_konsumen = st.session_state.piutang_konsumen[st.session_state.piutang_konsumen["Nama Konsumen"] != selected_row]
            st.success("Piutang konsumen berhasil dihapus!")
            save_data()  # Simpan setelah hapus
    else:
        st.write("Tidak ada data piutang konsumen.")

    # Initialize session state variables if they don't exist
    if 'historis_analisis_keuangan' not in st.session_state:
        st.session_state.historis_analisis_keuangan = pd.DataFrame(columns=[
            "Waktu", "Keuntungan Bersih", "Bulan"
        ])
    
    if 'penjualan' not in st.session_state:
        st.session_state.penjualan = pd.DataFrame(columns=[
            "ID", "Nama Pelanggan", "Nomor Telepon", "Alamat", "Nama Barang",
            "Ukuran/Kemasan", "Merk", "Kode Warna", "Jumlah", "Total Harga",
            "Keuntungan", "Waktu"
        ])
    
    if 'pengeluaran' not in st.session_state:
        st.session_state.pengeluaran = pd.DataFrame(columns=[
            "Jenis Pengeluaran", "Jumlah Pengeluaran", "Keterangan", "Waktu"
        ])
    
    if 'historis_keuntungan_bersih' not in st.session_state:
        st.session_state.historis_keuntungan_bersih = pd.DataFrame(columns=[
            "Waktu", "Keuntungan Bersih", "Bulan"
        ])
    
        # Initialize the session state if not already initialized
        if 'historis_analisa_pendapatan' not in st.session_state:
            st.session_state.historis_analisa_pendapatan = pd.DataFrame(columns=['Bulan', 'Total Penjualan', 'Total Tagihan Supplier', 'Keuntungan Bersih'])
        
        # Current date and month
        current_month = datetime.now().strftime("%Y-%m")
        
        # Calculate `total_penjualan`, `total_tagihan_supplier`, and `keuntungan_bersih`
        total_penjualan = total_keuntungan  # or use your existing logic for total penjualan
        total_tagihan_supplier = ...  # your logic to calculate total tagihan supplier
        keuntungan_bersih = total_penjualan - total_tagihan_supplier
        
        # Check if there's already data for the current month
        if not st.session_state.historis_analisa_pendapatan.empty:
            latest_record = st.session_state.historis_analisa_pendapatan.iloc[-1]  # Get the latest record
            latest_month = latest_record['Bulan']
            
            # Update the record if it's the same month, otherwise create a new one
            if latest_month == current_month:
                st.session_state.historis_analisa_pendapatan.iloc[-1] = {
                    'Bulan': current_month,
                    'Total Penjualan': total_penjualan,
                    'Total Tagihan Supplier': total_tagihan_supplier,
                    'Keuntungan Bersih': keuntungan_bersih
                }
            else:
                # Add a new record for a different month
                st.session_state.historis_analisa_pendapatan = st.session_state.historis_analisa_pendapatan.append({
                    'Bulan': current_month,
                    'Total Penjualan': total_penjualan,
                    'Total Tagihan Supplier': total_tagihan_supplier,
                    'Keuntungan Bersih': keuntungan_bersih
                }, ignore_index=True)
        else:
            # First-time entry
            st.session_state.historis_analisa_pendapatan = st.session_state.historis_analisa_pendapatan.append({
                'Bulan': current_month,
                'Total Penjualan': total_penjualan,
                'Total Tagihan Supplier': total_tagihan_supplier,
                'Keuntungan Bersih': keuntungan_bersih
            }, ignore_index=True)
        
        # Display the financial analysis history (last updated entry only)
        st.subheader("Histori Analisa Pendapatan")
        st.dataframe(st.session_state.historis_analisa_pendapatan)
    
    
    # Menambahkan tabel pengeluaran dan fitur edit
    st.subheader("Pengeluaran")
    
    # Menampilkan tabel pengeluaran
    st.dataframe(st.session_state.pengeluaran)
    
    # Form untuk menambah pengeluaran
    with st.form("tambah_pengeluaran"):
        st.write("Tambah Pengeluaran Baru")
        jenis_pengeluaran = st.selectbox("Jenis Pengeluaran", ["Biaya Gaji", "Biaya Operasional", "Biaya Lainnya"])
        jumlah_pengeluaran = st.number_input("Jumlah Pengeluaran (Rp)", min_value=0)
        keterangan_pengeluaran = st.text_input("Keterangan Pengeluaran")
        submit_pengeluaran = st.form_submit_button("Tambah Pengeluaran")
        
        if submit_pengeluaran:
            new_data = pd.DataFrame({
                "Jenis Pengeluaran": [jenis_pengeluaran],
                "Jumlah Pengeluaran": [jumlah_pengeluaran],
                "Keterangan": [keterangan_pengeluaran],
                "Waktu": [datetime.now()]
            })
            st.session_state.pengeluaran = pd.concat([st.session_state.pengeluaran, new_data], ignore_index=True)
            st.success("Pengeluaran berhasil ditambahkan!")
            save_data()  # Simpan data setelah penambahan pengeluaran
    
    # Tabel historis pengeluaran
    st.subheader("Historis Pengeluaran")
    st.dataframe(st.session_state.pengeluaran)
    
    # Analisa Keuangan - Total Keuntungan Bersih
    st.subheader("Analisa Keuangan - Total Keuntungan Bersih")
    
    # Ensure that the required columns are present
    if 'Harga Jual' in st.session_state.stok_barang.columns and 'Harga' in st.session_state.stok_barang.columns:
        merged_df = st.session_state.penjualan.merge(
            st.session_state.stok_barang[['Nama Barang', 'Harga', 'Harga Jual']], 
            on='Nama Barang', 
            how='left'
        )
        # Calculate total selling price and total cost
        total_selling_price = (merged_df["Jumlah"] * merged_df["Harga Jual"]).sum()
        total_cost = (merged_df["Jumlah"] * merged_df["Harga"]).sum()
        total_keuntungan = total_selling_price - total_cost
        # Calculate total expenses
        total_pengeluaran = st.session_state.pengeluaran["Jumlah Pengeluaran"].sum()
    
        st.write(f"Total Keuntungan (Harga Jual): Rp {total_keuntungan}")
    
        # Debug prints
        st.write(f"Debug - Total Keuntungan (Harga Jual): Rp {total_keuntungan}")
    
        # Update data historis keuntungan bersih
        current_month = datetime.now().strftime("%Y-%m")
    
        # Check if 'Bulan' column exists before filtering
        if 'Bulan' in st.session_state.historis_keuntungan_bersih.columns:
            st.session_state.historis_keuntungan_bersih = st.session_state.historis_keuntungan_bersih[
                st.session_state.historis_keuntungan_bersih["Bulan"] != current_month
            ]
    
        # Add the new data for the current month
        new_historis = pd.DataFrame({
            "Waktu": [datetime.now()],
            "Keuntungan Bersih": [total_keuntungan - total_pengeluaran],
            "Bulan": [current_month]
        })
        st.session_state.historis_keuntungan_bersih = pd.concat([st.session_state.historis_keuntungan_bersih, new_historis], ignore_index=True)
    
        # Tabel historis keuntungan bersih
        st.subheader("Historis Keuntungan Bersih")
        st.dataframe(st.session_state.historis_keuntungan_bersih)
    else:
        st.write("Kolom 'Harga Jual' atau 'Harga' tidak ditemukan di data stok.")
    
    # Tabel ringkasan keuangan
    st.subheader("Ringkasan Keuangan")
    current_date = datetime.now()
    
    # Format the values with commas and without decimals
    summary_data = {
        "Keterangan": ["Total Keuntungan", "Total Pengeluaran", "Total Keuntungan Bersih"],
        "Jumlah (Rp)": [
            f"{total_keuntungan:,.0f}",  # Format with thousand separator and no decimals
            f"{total_pengeluaran:,.0f}",  # Format with thousand separator and no decimals
            f"{(total_keuntungan - total_pengeluaran):,.0f}"  # Format with thousand separator and no decimals
        ],
        "Waktu": [current_date.strftime("%d-%m-%Y %H:%M:%S")] * 3,
        "Bulan": [current_date.strftime("%Y-%m")] * 3
    }
    
    # Convert the summary data to a DataFrame
    data_ringkasan = pd.DataFrame(summary_data)
    
    # Display the table
    st.table(data_ringkasan)
    
    # Sales Report
    st.subheader("Laporan Penjualan")
    
    # Merge sales data with stock data to get 'Harga Jual'
    if 'Harga Jual' in st.session_state.stok_barang.columns:
        merged_df = st.session_state.penjualan.merge(
            st.session_state.stok_barang[['Nama Barang', 'Harga', 'Harga Jual']], 
            on='Nama Barang', 
            how='left'
        )
        # Calculate 'Total Harga' and 'Keuntungan'
        merged_df["Total Harga"] = merged_df["Jumlah"] * merged_df["Harga Jual"]
        # Calculate profit (assuming profit calculation is based on 'Harga' from stock)
        merged_df["Keuntungan"] = merged_df["Total Harga"] - (merged_df["Jumlah"] * merged_df["Harga"])
        
        st.dataframe(merged_df)
    else:
        st.write("Kolom 'Harga Jual' tidak ditemukan di data stok.")

    # Tombol untuk mendownload semua data ke file Excel
    if st.button("Download Semua Data (Excel)"):
        save_to_excel()
        with open("data_laporan.xlsx", "rb") as file:
            st.download_button(
                label="Download Excel",
                data=file,
                file_name="data_laporan.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
# Define the pages and their content
def page_admin():
    st.header("Halaman Admin")
    halaman_stock_barang()  # Call the stock barang function here

def page_penjualan():
    st.header("Penjualan")
    st.write("halaman Penjualan")  

def page_supplier():
    st.header("Halaman Supplier")
    st.write("Data Supplier")  # Add functionality for supplier management

def page_owner():
    st.header("Halaman Owner")
    st.write("Konten untuk halaman Owner")  # Add functionality for owner content

# Custom CSS for navigation box and menu items
st.markdown("""
    <style>
    /* Style for the navigation container */
    .css-1d391kg {
        background-color: #8967B3; /* Background color of the navigation box */
        padding: 10px; /* Padding around the menu */
        border-radius: 10px; /* Rounded corners for the menu */
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1); /* Light shadow for a subtle 3D effect */
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .css-1d391kg .css-1g7kjm0 {
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .css-1d391kg .css-1l7zdkv {
        margin: 0;
        padding: 0;
        border: none;
        background: none;
    }
    /* Style for the menu items */
    .css-1d391kg .css-1l7zdkv .css-1t8dhd0 {
        font-size: 16px;
        text-align: center;
        color: #333;
        padding: 10px;
        border-radius: 5px;
        background-color: #f8f9fa; /* Background color of the menu item */
        transition: background-color 0.3s, color 0.3s;
    }
    .css-1d391kg .css-1l7zdkv .css-1t8dhd0:hover {
        background-color: #007bff; /* Hover background color */
        color: white; /* Hover text color */
    }
    .css-1d391kg .css-1l7zdkv .css-1t8dhd0.css-1i6g40i {
        background-color: #007bff; /* Active menu item background */
        color: white; /* Active menu item text color */
    }
            
    </style>
    """, unsafe_allow_html=True)

# Create a sidebar with navigation options
with st.sidebar:
    selected_page = option_menu(
        menu_title="Toko Sakti Utama",
        options=["Stock Barang", "Penjualan", "Supplier", "Owner"],
        icons=["box", "receipt", "truck", "person"],
        menu_icon="cast",
        default_index=0
    )

# Page routing
if selected_page == "Stock Barang":
    initialize_session_state()
    load_data()
    halaman_stock_barang()
elif selected_page == "Penjualan":
    initialize_session_state()
    load_data()
    halaman_penjualan()  # Ensure this is called correctly
elif selected_page == "Supplier":
    initialize_session_state()
    load_data()
    halaman_supplier()
elif selected_page == "Owner":
    initialize_session_state()
    load_data()
    halaman_owner()

