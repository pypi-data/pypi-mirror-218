def insertion_sort(array):
    """
    Sorts a given array using insertion sort algorithm
    Complexity: O(n^2)

    Parameters:
    array (list): The array to be sorted.

    Returns:
    list: The sorted array.
    """
    for i in range(1, len(array)):
        key = array[i]
        j = i - 1
        while j >= 0 and array[j] > key:
            array[j + 1] = array[j]
            j -= 1
        array[j + 1] = key

    return array