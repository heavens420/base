'''

'''


def bindary_search(arr, target):
    min_index,max_index = 0, len(arr) - 1

    while min_index <= max_index:
        mid_index = (min_index + max_index) // 2
        if target == arr[mid_index]:
            return mid_index
        elif target > arr[mid_index]:
            min_index = mid_index + 1
        elif target < arr[mid_index]:
            max_index = mid_index - 1

    return -1


if __name__ == '__main__':
    arr = [1, 2, 3, 4, 5]
    target = 5
    print(bindary_search(arr, target))
