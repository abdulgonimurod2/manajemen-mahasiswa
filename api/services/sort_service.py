def get_val(item, field: str):
    val = getattr(item, f"_{field}", "")
    if isinstance(val, str):
        return val.lower()
    return val

def compare(val1, val2, order: str) -> bool:
    if order == "asc":
        return val1 > val2
    return val1 < val2

def bubble_sort(data: list, field: str, order: str) -> list:
    arr = data.copy()
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if compare(get_val(arr[j], field), get_val(arr[j+1], field), order):
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

def selection_sort(data: list, field: str, order: str) -> list:
    arr = data.copy()
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            if compare(get_val(arr[min_idx], field), get_val(arr[j], field), order):
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr

def insertion_sort(data: list, field: str, order: str) -> list:
    arr = data.copy()
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and compare(get_val(arr[j], field), get_val(key, field), order):
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

def merge_sort(data: list, field: str, order: str) -> list:
    if len(data) <= 1:
        return data
    mid = len(data) // 2
    left = merge_sort(data[:mid], field, order)
    right = merge_sort(data[mid:], field, order)
    
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if not compare(get_val(left[i], field), get_val(right[j], field), order):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def shell_sort(data: list, field: str, order: str) -> list:
    arr = data.copy()
    n = len(arr)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and compare(get_val(arr[j - gap], field), get_val(temp, field), order):
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
        gap //= 2
    return arr

def sort_data(data: list, method: str, field: str, order: str) -> list:
    method = method.lower()
    order = order.lower()
    if method == "selection":
        return selection_sort(data, field, order)
    elif method == "insertion":
        return insertion_sort(data, field, order)
    elif method == "merge":
        return merge_sort(data, field, order)
    elif method == "shell":
        return shell_sort(data, field, order)
    else:
        return bubble_sort(data, field, order)
