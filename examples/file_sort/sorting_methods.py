"""Module that contains a collection of sorting functions"""


def default_sort(items):
    """
    Description:
        Sort contents by using the build in sort method of the given object.

    Input:
        items: <list> or any other object that has a public sort method.
    """
    items.sort()


def quicksort_phase_two(items, low, high):
    """
    Description:
        Quicksort's function for choosing a pivot number that is placed into
        the input object in a place that has all smaller items left to it and
        all bigger items at the right.

    Input:
        items: <list> or similar object that supports access by index.
        low: <int> lower bound index
        high: <int> higher bound index
    """

    # Choose the middle item to be the pivot and swap it with the one
    # in the high position until the final position is being found.
    mid = (low + high)/2
    items[high], items[mid] = items[mid], items[high]
    next_change = low
    for i in xrange(low, high):
        if items[i] < items[high]:
            items[i], items[next_change] = items[next_change], items[i]
            next_change += 1
    items[next_change], items[high] = items[high], items[next_change]
    return next_change


def quicksort(items, low=0, high=None):
    """
    Description:
        Quicksort in place sorting algorithm.

    Input:
        items: <list> or similar object that supports access by index.
        low: <int> lower bound index
        high: <int> higher bound index
    """
    if high is None:
        high = len(items)-1
    if low < high:
        pivot = quicksort_phase_two(items, low, high)
        quicksort(items, low=low, high=pivot-1)
        quicksort(items, low=pivot+1, high=high)


def merge_sort(items):
    """
    Description:
        Merge sort algorithm for applying a stable but not in place sort

    Input:
        items: <list> - or any other similar object that also supports
                         slice operation.
    """
    length = len(items)
    if length > 1:
        mid = length/2
        left = items[:mid]
        right = items[mid:]

        # Recursively sort left and right halfs of the object.
        merge_sort(left)
        merge_sort(right)

        i_idx = 0
        l_idx = 0
        r_idx = 0
        llength = mid
        rlength = length - llength

        # Merge the left and right parts into the original one.
        while l_idx < llength and r_idx < rlength:
            if left[l_idx] <= right[r_idx]:
                items[i_idx] = left[l_idx]
                l_idx += 1
            else:
                items[i_idx] = right[r_idx]
                r_idx += 1
            i_idx += 1

        while l_idx < llength:
            items[i_idx] = left[l_idx]
            l_idx += 1
            i_idx += 1

        while r_idx < rlength:
            items[i_idx] = right[r_idx]
            r_idx += 1
            i_idx += 1
