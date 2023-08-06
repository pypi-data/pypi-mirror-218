def selection_sort(array):
    """
    Sorts a given array using selection sort algorithm
    Complexity: O(n^2)

    Parameters:
    array (list): The array to be sorted.

    Returns:
    list: The sorted array.
    """
    for i in range(len(array)):
        min_index = i
        for j in range(i + 1, len(array)):
            if array[j] < array[min_index]:
                min_index = j
        array[i], array[min_index] = array[min_index], array[i]
    return array