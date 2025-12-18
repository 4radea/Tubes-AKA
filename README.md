# Analisis Pengukuran Performa: Merge Sort & Binary Search (Iteratif vs Rekursif)

Deskripsi singkat
-----------------
Study case ini bertujuan untuk membandingkan performa (waktu eksekusi rata‑rata) antara dua pendekatan implementasi untuk algoritma sorting dan searching: implementasi rekursif (top‑down) dan iteratif (bottom‑up). Pada bagian sorting digunakan Merge Sort (dua varian: rekursif dan iteratif), sedangkan pada bagian searching digunakan Binary Search (rekursif vs iteratif). Eksperimen dijalankan pada beberapa ukuran data, misalkan (n = 10, 20, 30) dengan pengukuran diulang beberapa kali untuk memperoleh nilai rata‑rata (dalam milidetik). Tujuan study case ini adalah melihat perbedaan waktu eksekusi dan mempelajari sejauh mana overhead rekursi memengaruhi performa pada berbagai ukuran input

Program ini melakukan pengukuran performa (kecepatan eksekusi) untuk:
- Merge Sort (dua varian): iteratif (bottom-up) dan rekursif (top-down)
- Binary Search: iteratif dan rekursif

Program menampilkan:
1. Tabel perbandingan performa (ASCII table) — waktu rata-rata dalam ms (milidetik).
2. Grafik perbandingan (disimpan sebagai `compare.png` dan ditampilkan jika environment mendukung).

Contoh interaksi singkat:
- Program akan menanyakan apakah Anda ingin menjalankan pengukuran Merge Sort dan/atau Binary Search.
- Lalu minta input ukuran data (pisahkan angka dengan spasi atau koma (,) atau tekan Enter untuk menggunakan default.
- Masukkan jumlah repeats (pengulangan) untuk mengambil rata‑rata waktu, lalu program menampilkan tabel dan menanyakan apakah akan membuat grafik.
- Saat memilih membuat grafik, Anda dapat memilih grafik Merge Sort, Binary Search, atau keduanya.

Format keluaran
---------------
- Tabel ASCII per algoritma:
  - Kolom `n` (ukuran data), `Waktu Rekursif (ms)`, `Waktu Iteratif (ms)` — nilai adalah rata‑rata dari beberapa pengulangan.
- Grafik:
  - Disimpan di `compare.png` (format PNG). Grafik menampilkan garis untuk varian iteratif dan rekursif.

Penjelasan satuan waktu (ms)
----------------------------
- `ms` = millisecond (milidetik) = 1/1000 detik.
- Contoh: `0.018340 ms` ≈ 18.34 mikrodetik (μs).
- Untuk operasi sangat cepat (microsecond-level), hasil sangat sensitif terhadap noise (proses lain, scheduling CPU). Gunakan repeats besar atau akumulasi panggilan jika perlu hasil lebih stabil.

Mengapa Merge Sort direkomendasikan
---------------------------------------------
- Merge Sort: kompleksitas O(n log n) — efisien untuk data berukuran sedang sampai besar.
- Binary Search memerlukan data terurut; menggunakan algoritma pengurutan efisien untuk pra‑proses.

Tips untuk pengukuran yang valid
-------------------------------
- Naikkan `repeats` (mis. 50 atau 100) untuk mengurangi variabilitas hasil.
- Untuk operasi singkat (binary search), akumulasikan banyak panggilan dalam satu pengukuran agar waktu total cukup besar dibanding noise.
- Uji beberapa ukuran `n` yang relevan (mis. untuk Merge Sort: 100, 1k, 5k, 10k).
- Tampilkan juga `stddev` (standar deviasi) jika ingin melihat kestabilan pengukuran — program bisa dimodifikasi untuk menampilkan ini.

