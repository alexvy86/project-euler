from math import sqrt

def is_prime(number):
    if number & 1 == 0:
        return False
    if number in [2,3,5,7,11,13]:
        return True
    upper_limit = round(sqrt(number))
    for i in range(3, upper_limit + 3, 2):
        if number % i == 0:
            return False
    return True
