# ChronoCrypt v2.0

**Deskripsi Singkat**

ChronoCrypt adalah aplikasi web yang dirancang untuk melakukan enkripsi dan dekripsi teks menggunakan kombinasi algoritma Caesar Cipher dan teknik kuantum sederhana. Aplikasi ini juga menyertakan fitur steganografi untuk menyisipkan pesan terenkripsi ke dalam gambar.

Ini adalah pengembangan dari Program Enkripsi dan Dekripsi Kuantum Caesar Cipher (QCC) v1.0, yang bertujuan untuk memberikan antarmuka pengguna yang lebih baik, fitur yang lebih lengkap, serta tampilan yang lebih menarik dan responsif dengan tema yang menggabungkan waktu dan enkripsi.


**Fitur Utama**

*   **Enkripsi Teks:** Mengenkripsi teks menggunakan Caesar Cipher, kemudian dilanjutkan dengan enkripsi kuantum sederhana (berbasis gerbang X dan pengukuran).
*   **Dekripsi Teks:** Mendekripsi teks yang telah dienkripsi menggunakan metode yang sama.
*   **Penyimpanan dan Pembukaan File Teks:** Menyimpan hasil enkripsi dan dekripsi ke dalam file teks, dan juga membuka file teks untuk dekripsi.
*   **Steganografi Gambar:** Menyisipkan pesan terenkripsi ke dalam gambar PNG, JPG, atau JPEG menggunakan teknik LSB (Least Significant Bit).
*   **Ekstraksi Pesan dari Gambar:** Mengambil pesan terenkripsi dari gambar.
*   **Penyimpanan dan Pembukaan File Gambar:** Menyimpan gambar setelah penyisipan, dan menyimpan pesan terdekripsi ke dalam file teks.
*   **Tampilan Interaktif:** Antarmuka pengguna yang responsif, sederhana, dan menarik dengan animasi latar belakang partikel kuantum.
*  **Opsi Input dan Output Kunci:** Input kunci dapat berupa text manual atau file, begitu juga dengan output untuk enkripsi pesan.


**Teknologi yang Digunakan**

*   **Python:** Bahasa pemrograman utama.
*   **Flask:** Framework web untuk backend.
*   **Cirq:** Library untuk simulasi rangkaian kuantum.
*   **Pillow (PIL):** Library untuk manipulasi gambar.
*   **HTML/CSS:** Untuk tampilan antarmuka pengguna (frontend).


**Instalasi**

Berikut adalah langkah-langkah untuk menginstal dan menjalankan aplikasi:

1.  **Pastikan Python Terinstal:**
    Pastikan Python (versi 3.6 atau lebih tinggi) dan `pip` (package installer for Python) telah terinstal di sistem Anda. Anda dapat mengunduhnya dari situs resmi Python [https://www.python.org/downloads/](https://www.python.org/downloads/).

2.  **Clone Repositori GitHub:**
    Clone repositori GitHub ke komputer Anda menggunakan perintah berikut di terminal atau command prompt:

    ```bash
    git clone [URL_Repositori_Anda]
    ```

    Ganti `[URL_Repositori_Anda]` dengan URL repositori GitHub Anda.

3.  **Masuk ke Direktori Proyek:**
    Pindah ke direktori proyek menggunakan perintah:

    ```bash
    cd nama_folder_proyek
    ```

4.  **Instal Dependensi:**
    Instal semua package atau library Python yang dibutuhkan dengan perintah:

    ```bash
    pip install Flask cirq pillow werkzeug
    ```

5.  **Jalankan Aplikasi:**
    Jalankan aplikasi dengan perintah:

    ```bash
    python app.py
    ```

    Aplikasi akan berjalan pada server Flask dan dapat diakses melalui browser di alamat `http://127.0.0.1:5000/`.

**Struktur Folder**

```
your_project/
├── app.py
├── templates/
│   ├── index.html
│   ├── crypto.html
│   ├── steganography.html
│   ├── encrypt.html
│   ├── decrypt.html
│   ├── insert.html
│   ├── extract.html
│   └── base.html
├── static/
│   ├── style.css
│   └── uploads/
└── README.md

```

**Penggunaan**

1.  Buka aplikasi pada browser melalui `http://127.0.0.1:5000/`.
2.  Pilih menu **crypto** untuk melakukan enkripsi/dekripsi teks atau **steganography** untuk menyisipkan/mengekstraksi pesan dari gambar.
3.  Ikuti petunjuk pada setiap halaman untuk menginput data yang dibutuhkan.

**Catatan Tambahan**

*   Pastikan folder `static/uploads/` ada di direktori proyek Anda.
*   Untuk meng-upload file, ukuran maksimum yang direkomendasikan adalah 20MB.

**Kontribusi**

Jika Anda ingin berkontribusi pada proyek ini, ikuti langkah-langkah berikut:

1.  Fork repositori ini.
2.  Buat branch baru untuk fitur Anda.
3.  Lakukan perubahan pada branch tersebut.
4.  Buat pull request ke repositori asli.

**Penutup**

Terima kasih telah menggunakan ChronoCrypt. Jika Anda memiliki pertanyaan atau masukan, jangan ragu untuk menghubungi saya.

