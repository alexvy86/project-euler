from math import sqrt

MIN_DIVISORS = 500

memoized_divisors = {
    1: [1],
    2: [1,2],
    3: [1,3]
}

def get_divisors(number):
    if number in memoized_divisors:
        return memoized_divisors[number]

    divisors = set() # pylint: disable=redefined-outer-name
    for i in range(round(sqrt(number))+1, 0, -1):
        if i in divisors:
            continue
        if number % i == 0:
            divisors.add(i)
            divisors.add(number / i)
            #print(f"getting subdivisors of {i}")
            subdivisors = get_divisors(i)
            divisors = divisors.union(subdivisors)
            divisors = divisors.union([number / s for s in subdivisors])

    memoized_divisors[number] = divisors
    return divisors

def get_nth_triangle_number(index):
    return index * (index + 1) / 2

divisors = []
current_index = 0
triangle_number = 1

while len(divisors) < MIN_DIVISORS:
    current_index += 1
    triangle_number = get_nth_triangle_number(current_index)
    #print(triangle_number)
    divisors = get_divisors(triangle_number)
    if current_index % 100 == 0:
        print(f"Checking index {current_index} - {triangle_number} - {len(divisors)}")
    #print(divisors)

print(f"{triangle_number} has {len(divisors)} divisors")
    