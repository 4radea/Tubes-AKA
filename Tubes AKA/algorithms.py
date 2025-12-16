"""
algorithms.py

Berisi:
- bubble_sort_iterative(arr)
- bubble_sort_recursive(arr, n=None)
- binary_search_iterative(arr, target)
- binary_search_recursive(arr, target, left=0, right=None)
"""

from typing import List, Optional

def bubble_sort_iterative(arr: List[int]) -> List[int]:
    a = arr[:]  # salin agar tidak mengubah input
    n = len(a)
    for i in range(n):
        swapped = False
        for j in range(0, n - 1 - i):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swapped = True
        if not swapped:
            break
    return a

def bubble_sort_recursive(arr: List[int], n: Optional[int] = None) -> List[int]:
    # Implementasi rekursif: lakukan satu pass lalu rekursi pada prefix
    a = arr[:]  # salin lokal agar pure
    if n is None:
        n = len(a)
    if n <= 1:
        return a
    for i in range(n - 1):
        if a[i] > a[i + 1]:
            a[i], a[i + 1] = a[i + 1], a[i]
    # rekursi pada bagian pertama
    prefix_sorted = bubble_sort_recursive(a[:n - 1], n - 1)
    return prefix_sorted + [a[n - 1]]

def binary_search_iterative(arr: List[int], target: int) -> int:
    left = 0
    right = len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

def binary_search_recursive(arr: List[int], target: int, left: int = 0, right: Optional[int] = None) -> int:
    if right is None:
        right = len(arr) - 1
    if left > right:
        return -1
    mid = (left + right) // 2
    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return binary_search_recursive(arr, target, mid + 1, right)
    else:
        return binary_search_recursive(arr, target, left, mid - 1)