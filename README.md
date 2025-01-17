# Aplikasi Point of Sale

Ini adalah aplikasi _point of sale_ yang digunakan untuk pencatatan transaksi kasir. Berikut daftar fitur yang ada
diaplikasi ini:

1. CRUD Produk
2. CRUD Kategori Produk
3. Authentication (Login)
4. Authorization (admin, cashier)
5. CRUD User (cashier)

Aplikasi ini dibuat dengan menggunakan _flask_ dan _mysql_. Requirement yang digunakan:

* python 3.11
* mysql 8
* docker

## Instalasi

### Flask

Instalasi paket-paket python yang dibutuhkan.
Pastikan anda berada di direktori yang berisi file **requirements.txt**.
> pip install -r requirements.txt

Jalankan flask dengan interpreter python yang sudah terinstall di laptop anda.
> python main.py

Jika berhasil maka flask akan berlajan di localhost:5000

### MySQL

MySQL akan dijalankan dengan menggunakan docker. Anda harus berada di direktori yang berisi folder db.

1. Buat image MySQL dengan cara:

> docker build -t db:1.0.0 .

2. Menjalankan dengan container

> docker run -d -p 3301:3306 db:1.0.0

Jika berhasil maka MySQL anda bisa mengakses MySQL dengan port 3301. Detail credential ada di file .env.