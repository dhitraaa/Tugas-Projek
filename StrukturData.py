import csv
import os
from datetime import datetime
from collections import deque

# === Struktur Data ===
produk_list = []
antrian_transaksi = deque()

# === Baca Produk dari CSV ===
def load_produk():
    if os.path.exists('produk.csv'):
        with open('produk.csv', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                row['harga'] = int(row['harga'])
                row['stok'] = int(row['stok'])
                produk_list.append(row)

# === Simpan Produk ke CSV ===
def simpan_produk():
    with open('produk.csv', 'w', newline='') as file:
        fieldnames = ['id', 'nama', 'harga', 'stok', 'deskripsi']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for p in produk_list:
            writer.writerow(p)

# === Tambah Produk ===
def tambah_produk():
    id = input("ID Produk: ")
    nama = input("Nama Produk: ")
    harga = int(input("Harga: "))
    stok = int(input("Stok: "))
    deskripsi = input("Deskripsi: ")
    produk_list.append({'id': id, 'nama': nama, 'harga': harga, 'stok': stok, 'deskripsi': deskripsi})
    simpan_produk()

# === Tampilkan Produk ===
def tampilkan_produk():
    print("\nDaftar Produk:")
    for p in produk_list:
        print(f"{p['id']} | {p['nama']} | Rp{p['harga']} | Stok: {p['stok']}")

# === Tambah Transaksi ===
def transaksi(tipe):
    tampilkan_produk()
    id = input("Masukkan ID produk: ")
    jumlah = int(input("Jumlah: "))
    tanggal = datetime.now().strftime("%Y-%m-%d")

    for p in produk_list:
        if p['id'] == id:
            if tipe == "jual":
                if p['stok'] >= jumlah:
                    p['stok'] -= jumlah
                    total = jumlah * p['harga']
                    antrian_transaksi.append({'tanggal': tanggal, 'tipe': 'jual', 'id_produk': id, 'jumlah': jumlah, 'total': total})
                    print("Transaksi berhasil.")
                else:
                    print("Stok tidak cukup!")
            elif tipe == "beli":
                p['stok'] += jumlah
                total = jumlah * p['harga']
                antrian_transaksi.append({'tanggal': tanggal, 'tipe': 'beli', 'id_produk': id, 'jumlah': jumlah, 'total': total})
                print("Produk berhasil ditambah.")
            break
    simpan_produk()
    simpan_transaksi()

# === Simpan Transaksi ke CSV ===
def simpan_transaksi():
    with open('transaksi.csv', 'a', newline='') as file:
        fieldnames = ['tanggal', 'tipe', 'id_produk', 'jumlah', 'total']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if file.tell() == 0:
            writer.writeheader()
        while antrian_transaksi:
            writer.writerow(antrian_transaksi.popleft())

# === Laporan Penjualan ===
def laporan_penjualan():
    if os.path.exists('transaksi.csv'):
        print("\nLaporan Transaksi:")
        with open('transaksi.csv', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                print(f"{row['tanggal']} | {row['tipe']} | ID: {row['id_produk']} | {row['jumlah']} x Rp{row['total']}")

# === Menu Utama ===
def menu():
    load_produk()
    while True:
        print("\n--- Menu Utama ---")
        print("1. Tambah Produk")
        print("2. Tampilkan Produk")
        print("3. Transaksi Penjualan")
        print("4. Transaksi Pembelian")
        print("5. Laporan Transaksi")
        print("0. Keluar")
        pilih = input("Pilih menu: ")

        if pilih == '1':
            tambah_produk()
        elif pilih == '2':
            tampilkan_produk()
        elif pilih == '3':
            transaksi("jual")
        elif pilih == '4':
            transaksi("beli")
        elif pilih == '5':
            laporan_penjualan()
        elif pilih == '0':
            break
        else:
            print("Pilihan tidak valid.")

# === Jalankan Program ===
menu()
