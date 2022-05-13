
def myRange(int1, int2):
    """
    It takes two integers as arguments and returns a list of integers from the first integer to the
    second integer
    
    :param int1: the first integer
    :param int2: The end of the range
    :return: A list of numbers from int1 to int2
    """
    list = []
    if int1 < int2:
        while int1 <= int2:
            list.append(int1)
            int1 += 1
    else:
        while int1 >= int2:
            list.append(int1)
            int1 -= 1
    return list
