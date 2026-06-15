def get_val(item, field: str):
    val = getattr(item, f"_{field}", "")
    if isinstance(val, str):
        return val.lower()
    return val

def linear_search(data: list, keyword: str, field: str) -> list:
    keyword = keyword.lower()
    results = []
    for item in data:
        val = str(get_val(item, field)).lower()
        if keyword in val:
            results.append(item)
    return results

def sequential_search(data: list, keyword: str, field: str) -> list:
    keyword = keyword.lower()
    for item in data:
        val = str(get_val(item, field)).lower()
        if keyword in val:
            return [item]
    return []

def binary_search(data: list, keyword: str, field: str) -> list:
    # Binary Search on a sorted array
    sorted_data = sorted(data, key=lambda x: str(get_val(x, field)).lower())
    keyword = keyword.lower()
    
    left = 0
    right = len(sorted_data) - 1
    match_index = -1
    
    while left <= right:
        mid = (left + right) // 2
        mid_val = str(get_val(sorted_data[mid], field)).lower()
        
        if mid_val == keyword:
            match_index = mid
            break
        elif mid_val < keyword:
            left = mid + 1
        else:
            right = mid - 1
            
    if match_index == -1:
        return []
        
    results = [sorted_data[match_index]]
    
    # scan left
    l = match_index - 1
    while l >= 0 and str(get_val(sorted_data[l], field)).lower() == keyword:
        results.append(sorted_data[l])
        l -= 1
        
    # scan right
    r = match_index + 1
    while r < len(sorted_data) and str(get_val(sorted_data[r], field)).lower() == keyword:
        results.append(sorted_data[r])
        r += 1
        
    return results

def search_data(data: list, method: str, keyword: str, field: str) -> list:
    method = method.lower()
    if method == "binary":
        return binary_search(data, keyword, field)
    elif method == "sequential":
        return sequential_search(data, keyword, field)
    else:
        return linear_search(data, keyword, field)
