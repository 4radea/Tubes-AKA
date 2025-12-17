"""
algoritma.py

Implementasi algoritma:
- merge_sort_iterative(arr)  # bottom-up iterative mergesort
- merge_sort_recursive(arr)  # top-down recursive mergesort
- binary_search_iterative(arr, target)
- binary_search_recursive(arr, target, left=0, right=None)
"""

from typing import List, Optional

def merge(left: List[int], right: List[int]) -> List[int]:
    i = j = 0
    out: List[int] = []
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            out.append(left[i])
            i += 1
        else:
            out.append(right[j])
            j += 1
    if i < len(left):
        out.extend(left[i:])
    if j < len(right):
        out.extend(right[j:])
    return out

def merge_sort_recursive(arr: List[int]) -> List[int]:
    # Top-down mergesort (rekursif)
    n = len(arr)
    if n <= 1:
        return arr[:]
    mid = n // 2
    left = merge_sort_recursive(arr[:mid])
    right = merge_sort_recursive(arr[mid:])
    return merge(left, right)

def merge_sort_iterative(arr: List[int]) -> List[int]:
    # Bottom-up (iterative) mergesort
    n = len(arr)
    if n <= 1:
        return arr[:]
    a = arr[:]
    width = 1
    # temp array for merging
    while width < n:
        new_a: List[int] = []
        for i in range(0, n, 2 * width):
            left = a[i:i+width]
            right = a[i+width:i+2*width]
            new_a.extend(merge(left, right))
        a = new_a
        width *= 2
    return a

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
