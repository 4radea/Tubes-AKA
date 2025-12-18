"""
main.py

Interaktif:
- Menjalankan pengukuran performa Merge Sort & Binary Search sesuai pilihan user
- Menampilkan:
  1) Tabel perbandingan performa (ASCII table)
  2) Menanyakan apakah akan menampilkan grafik perbandingan; jika ya maka
     menampilkan grafik untuk keduanya (jika data tersedia) dan menyimpannya.
"""

import random
import time
import statistics
import sys
from typing import List, Tuple
import re

import matplotlib.pyplot as plt

# import dari file algoritma.py
from algoritma import (
    merge_sort_iterative,
    merge_sort_recursive,
    binary_search_iterative,
    binary_search_recursive,
)

# Default eksperimen
DEFAULT_SORT_SIZES = [100, 500, 1000]
DEFAULT_SEARCH_SIZES = [100, 1000, 5000]
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
        t_iter = time_ms(merge_sort_iterative, arr, repeats=repeats)
        t_rec = time_ms(merge_sort_recursive, arr, repeats=repeats)
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

# Cetak tabel ASCII (untuk sort dan search)
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

# Plotting: menampilkan grafik keduanya (satu subplot per algoritma yang ada)
def plot_results_both(sort_results, search_results, out_filename="compare.png"):
    subplots = 0
    if sort_results:
        subplots += 1
    if search_results:
        subplots += 1
    if subplots == 0:
        print("Tidak ada data untuk digrafikkan.")
        return

    fig, axes = plt.subplots(1, subplots, figsize=(7 * subplots, 5))
    if subplots == 1:
        axes = [axes]
    idx = 0

    if sort_results:
        x = [r[0] for r in sort_results]
        rec = [r[1] for r in sort_results]
        itr = [r[2] for r in sort_results]
        axes[idx].plot(x, itr, marker='o', color='blue', label='Iterative (bottom-up)')
        axes[idx].plot(x, rec, marker='s', color='green', linestyle='--', label='Recursive (top-down)')
        axes[idx].set_title("Merge Sort: Iteratif vs Rekursif")
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
    print(f"\nGrafik disimpan ke: {out_filename}")
    try:
        plt.show()
    except Exception:
        pass

def interactive():
    random.seed(42)
    print("=== Pengukuran Performa: Merge Sort & Binary Search ===")
    run_sort = input("Jalankan pengukuran performa Merge Sort? (y/n) [y]: ").strip().lower()
    run_sort = (run_sort == "" or run_sort == "y" or run_sort == "yes")
    run_search = input("Jalankan pengukuran performa Binary Search? (y/n) [y]: ").strip().lower()
    run_search = (run_search == "" or run_search == "y" or run_search == "yes")

    sort_sizes = []
    if run_sort:
        s = input(f"Masukkan ukuran data Merge Sort atau tekan Enter untuk default {DEFAULT_SORT_SIZES}: ")
        sort_sizes = parse_sizes(s, DEFAULT_SORT_SIZES)

    search_sizes = []
    if run_search:
        s = input(f"Masukkan ukuran data Binary Search atau tekan Enter untuk default {DEFAULT_SEARCH_SIZES}: ")
        search_sizes = parse_sizes(s, DEFAULT_SEARCH_SIZES)

    repeats = parse_positive_int(input(f"Masukkan jumlah perulangan untuk rata-rata [default {DEFAULT_REPEATS}]: "), DEFAULT_REPEATS)

    # jalankan pengukuran (tanpa mencetak per-bar)
    sort_results = benchmark_sorting(sort_sizes, repeats) if run_sort else []
    search_results = benchmark_searching(search_sizes, repeats) if run_search else []

    # Tampilkan tabel perbandingan performa
    if sort_results:
        print_table("PERBANDINGAN PERFORMA: Merge Sort (Recursif vs Iteratif)", sort_results)
    if search_results:
        print_table("PERBANDINGAN PERFORMA: Binary Search (Recursif vs Iteratif)", search_results)

    # Tanyakan ke user sebelum menampilkan grafik
    show_plot = input("\nTampilkan grafik perbandinganya? (y/n) [y]: ").strip().lower()
    show_plot = (show_plot == "" or show_plot == "y" or show_plot == "yes")

    if show_plot:
        print("\nMenampilkan grafik untuk kedua algoritma ...")
        plot_results_both(sort_results, search_results)
    else:
        print("\nGrafik tidak ditampilkan.")

    print("\nSelesai.")

def main():
    try:
        interactive()
    except KeyboardInterrupt:
        print("\nDibatalkan oleh user.")
        sys.exit(0)

if __name__ == "__main__":
    main()