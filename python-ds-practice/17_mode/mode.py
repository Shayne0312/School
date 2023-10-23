def mode(nums):
    """Return most-common number in list.
    
    For this function, there will always be a single-most-common value; 
    you do not need to worry about handling cases where more than one item
    occurs the same number of times.

    >>> mode([1, 2, 1])
    1
    
    >>> mode([2, 2, 3, 3, 2])
    2
    """

    count = {}
    max_count = 0
    mode = None

    for num in nums:
        if num in count:
            count[num] += 1
        else:
            count[num] = 1
        
        if count[num] > max_count:
            max_count = count[num]
            mode = num

    return mode