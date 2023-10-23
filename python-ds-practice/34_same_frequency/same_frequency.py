def same_frequency(num1, num2):
    """Do these nums have same frequencies of digits?
    
    >>> same_frequency(551122, 221515)
    True
    
    >>> same_frequency(321142, 3212215)
    False
    
    >>> same_frequency(1212, 2211)
    True
    """

    str1 = str(num1)
    str2 = str(num2)

    if len(str1) != len(str2):
        return False

    count1 = {}
    count2 = {}

    for i in range(len(str1)):
        digit1 = str1[i]
        digit2 = str2[i]

        if digit1 in count1:
            count1[digit1] += 1
        else:
            count1[digit1] = 1

        if digit2 in count2:
            count2[digit2] += 1
        else:
            count2[digit2] = 1

    return count1 == count2
