def quicksort(array):
    """
    Sorts a given array using quick sort algorithm
    Complexity: O(nLogn)

    Parameters:
    array (list): The array to be sorted.

    Returns:
    list: The sorted array.
    """
    
    if len(array) <= 1:
        return array

    pivot = array[len(array) // 2]
    left = [x for x in array if x < pivot]
    middle = [x for x in array if x == pivot]
    right = [x for x in array if x > pivot]

    return quicksort(left) + middle + quicksort(right)
