from math import sqrt

DESIRED_INDEX = 10_001

current_prime = 3
current_number = current_prime + 2
current_index = 2

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

while current_index < DESIRED_INDEX:
    #print(f"Testing {current_number}")
    if is_prime(current_number):
        #print(f"{current_number} is prime")
        current_prime = current_number
        current_index += 1
    current_number += 2

print(f"{DESIRED_INDEX}th prime is {current_prime}")
