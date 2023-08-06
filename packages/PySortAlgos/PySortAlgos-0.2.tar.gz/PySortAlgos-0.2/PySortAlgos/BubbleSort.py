def bubble_sort(array):
    """
    Sorts a given array using bubble sort algorithm
    Complexity: O(n^2)

    Parameters:
    array (list): The array to be sorted.

    Returns:
    list: The sorted array.
    """
    
    for i in range(len(array)-1,0,-1):
        for j in range(i):
            if (array[j]>array[j+1]):
                array[j+1],array[j] = array[j],array[j+1]
    
    return array
