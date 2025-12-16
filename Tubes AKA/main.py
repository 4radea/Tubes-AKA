"""
main.py

Interaktif:
- Jalankan pengukuran performa Bubble Sort & Binary Search
- Menampilkan:
  1) Hasil pengukuran (dipisah): PERFORMA BUBBLE SORT / PERFORMA BINARY SEARCH
  2) Kesimpulan tabel pengukurannya
  3) Tabel perbandingan performa (ASCII table)
"""

import random
import time
import statistics
import sys
from typing import List, Tuple
import re

import matplotlib.pyplot as plt

from algorithms import (
    bubble_sort_iterative,
    bubble_sort_recursive,
    binary_search_iterative,
    binary_search_recursive,
)

# Default eksperimen
DEFAULT_SORT_SIZES = [10, 20, 30, 50]
DEFAULT_SEARCH_SIZES = [10, 15, 30, 100]
DEFAULT_REPEATS = 5

# Utility
def time_ms(func, *args, repeats=1):
    times = []
    for _ in range(repeats):
        start = time.perf_counter()
        func(*args)
        end = time.perf_counter()
        times.append((end - start) * 1000.0)  # ms
    return statistics.mean(times) if times else 0.0

def parse_sizes(input_str: str, default: List[int]) -> List[int]:
    s = input_str.strip()
    if s == "" or s.lower() in ("d", "default"):
        return default
    try:
        # Terima pemisah spasi atau koma (prompt tidak menyebut koma, tapi parser toleran)
        parts = [p.strip() for p in re.split(r"[\s,]+", s) if p.strip() != ""]
        sizes = sorted({max(1, int(float(p))) for p in parts})
        return sizes
    except Exception:
        print("Input ukuran tidak valid. Menggunakan default.")
        return default

def parse_positive_int(input_str: str, default: int) -> int:
    s = input_str.strip()
    if s == "" or s.lower() in ("d", "default"):
        return default
    try:
        v = int(s)
        return max(1, v)
    except Exception:
        print("Input tidak valid. Menggunakan default.")
        return default

# Pengukuran performa (kembalikan list hasil)
def benchmark_sorting(sizes: List[int], repeats: int) -> List[Tuple[int, float, float]]:
    results: List[Tuple[int, float, float]] = []
    for n in sizes:
        arr = [random.randint(0, 1000000) for _ in range(n)]
        t_iter = time_ms(bubble_sort_iterative, arr, repeats=repeats)
        t_rec = time_ms(bubble_sort_recursive, arr, repeats=repeats)
        results.append((n, t_rec, t_iter))
    return results

def benchmark_searching(sizes: List[int], repeats: int) -> List[Tuple[int, float, float]]:
    results: List[Tuple[int, float, float]] = []
    for n in sizes:
        arr = sorted([random.randint(0, 1000000) for _ in range(n)]) if n > 0 else []
        targets = [arr[random.randrange(n)] for _ in range(repeats)] if n > 0 else []
        t_iter_list = [time_ms(binary_search_iterative, arr, t, repeats=1) for t in targets]
        t_rec_list = [time_ms(binary_search_recursive, arr, t, repeats=1) for t in targets]
        t_iter = statistics.mean(t_iter_list) if t_iter_list else 0.0
        t_rec = statistics.mean(t_rec_list) if t_rec_list else 0.0
        results.append((n, t_rec, t_iter))
    return results

# Cetak hasil terpisah sesuai permintaan
def print_separated_results(sort_results, search_results):
    if sort_results:
        print("\nPERFORMA BUBBLE SORT")
        for n, rec, itr in sort_results:
            print(f"n={n:5d}  recursive={rec:.6f} ms  iterative={itr:.6f} ms")
    if search_results:
        print("\nPERFORMA BINARY SEARCH")
        for n, rec, itr in search_results:
            print(f"n={n:5d}  recursive={rec:.6f} ms  iterative={itr:.6f} ms")

# Cetak tabel ASCII (kedua tabel: sort dan search)
def print_table(title: str, results):
    if not results:
        print(f"\n{title}: (no data)")
        return
    print(f"\n{title} [avg ms]")
    headers = ("n", "Waktu Rekursif (ms)", "Waktu Iteratif (ms)")
    col_widths = [max(len(h), 12) for h in headers]
    for r in results:
        col_widths[0] = max(col_widths[0], len(str(r[0])))
        col_widths[1] = max(col_widths[1], len(f"{r[1]:.6f}"))
        col_widths[2] = max(col_widths[2], len(f"{r[2]:.6f}"))
    line = "+".join("-" * (w + 2) for w in col_widths)
    print("+" + line + "+")
    print("| " + " | ".join(h.center(w) for h, w in zip(headers, col_widths)) + " |")
    print("+" + line + "+")
    for r in results:
        print("| " + " | ".join(
            (str(r[i]).center(col_widths[i]) if i == 0 else f"{r[i]:.6f}".center(col_widths[i]))
            for i in range(3)
        ) + " |")
    print("+" + line + "+")

# (opsional) plotting fungsi (sama seperti sebelumnya)
def plot_results(sort_results, search_results, out_filename="compare.png"):
    subplots = 0
    if sort_results:
        subplots += 1
    if search_results:
        subplots += 1
    if subplots == 0:
        return
    fig, axes = plt.subplots(1, subplots, figsize=(7 * subplots, 5))
    if subplots == 1:
        axes = [axes]
    idx = 0
    if sort_results:
        x = [r[0] for r in sort_results]
        rec = [r[1] for r in sort_results]
        itr = [r[2] for r in sort_results]
        axes[idx].plot(x, itr, marker='o', color='blue', label='Iterative')
        axes[idx].plot(x, rec, marker='s', color='green', linestyle='--', label='Recursive')
        axes[idx].set_title("Bubble Sort: Iteratif vs Rekursif")
        axes[idx].set_xlabel("Data Size (n)")
        axes[idx].set_ylabel("Execution Time (ms)")
        axes[idx].legend()
        axes[idx].grid(True)
        idx += 1
    if search_results:
        x = [r[0] for r in search_results]
        rec = [r[1] for r in search_results]
        itr = [r[2] for r in search_results]
        axes[idx].plot(x, itr, marker='o', color='blue', label='Iterative')
        axes[idx].plot(x, rec, marker='s', color='green', linestyle='--', label='Recursive')
        axes[idx].set_title("Binary Search: Iteratif vs Rekursif")
        axes[idx].set_xlabel("Data Size (n)")
        axes[idx].set_ylabel("Execution Time (ms)")
        axes[idx].legend()
        axes[idx].grid(True)
    plt.tight_layout()
    plt.savefig(out_filename, dpi=150)
    try:
        plt.show()
    except Exception:
        pass

def interactive():
    random.seed(42)
    print("=== Pengukuran Performa: Bubble Sort & Binary Search ===")
    run_sort = input("Jalankan pengukuran performa Bubble Sort? (y/n) [y]: ").strip().lower()
    run_sort = (run_sort == "" or run_sort == "y" or run_sort == "yes")
    run_search = input("Jalankan pengukuran performa Binary Search? (y/n) [y]: ").strip().lower()
    run_search = (run_search == "" or run_search == "y" or run_search == "yes")

    sort_sizes = []
    if run_sort:
        s = input(f"Masukkan ukuran data Bubble Sort (pisahkan angka dengan spasi) atau tekan Enter untuk default {DEFAULT_SORT_SIZES}: ")
        sort_sizes = parse_sizes(s, DEFAULT_SORT_SIZES)

    search_sizes = []
    if run_search:
        s = input(f"Masukkan ukuran data Binary Search (pisahkan angka dengan spasi) atau tekan Enter untuk default {DEFAULT_SEARCH_SIZES}: ")
        search_sizes = parse_sizes(s, DEFAULT_SEARCH_SIZES)

    repeats = parse_positive_int(input(f"Masukkan jumlah repeats untuk rata-rata [default {DEFAULT_REPEATS}]: "), DEFAULT_REPEATS)

    print("\nMulai pengukuran performa...\n")
    sort_results = benchmark_sorting(sort_sizes, repeats) if run_sort else []
    search_results = benchmark_searching(search_sizes, repeats) if run_search else []

    # 1) Tampilkan hasil terpisah terlebih dahulu (seperti format yang Anda minta)
    print_separated_results(sort_results, search_results)

    # 2) Tambahkan keterangan sebelum tabel
    print("\nKESIMPULAN TABEL PENGUKURAN:")

    # 3) Tampilkan tabel perbandingan performa (tetap ditampilkan setelah keterangan)
    if sort_results:
        print_table("PERBANDINGAN PERFORMA: Bubble Sort (Recursive vs Iterative)", sort_results)
    if search_results:
        print_table("PERBANDINGAN PERFORMA: Binary Search (Recursive vs Iterative)", search_results)

    # opsi: simpan/tampilkan grafik
    save_plot = input("\nSimpan dan tampilkan grafik? (y/n) [y]: ").strip().lower()
    if save_plot == "" or save_plot == "y" or save_plot == "yes":
        plot_results(sort_results, search_results)
        print("Grafik disimpan sebagai 'compare.png' (jika ada data).")

    print("\nSelesai.")

def main():
    try:
        interactive()
    except KeyboardInterrupt:
        print("\nDibatalkan oleh user.")
        sys.exit(0)

if __name__ == "__main__":
    main()