"""
Tried several approaches to get a formula for the total number of cubes in layer n,
and/or the number of cubes that were added on layer n. Finally went with the idea that
you can grow the initial cuboid to the sides, in 2D, with a relatively straightfoward
formula c*((a+2n)(b+2n) - 2n(n+1)). For each layer n, we add 2 cubes on the A dimension,
(1 on each side) and similarly 2 on the B dimension, compute the total area of a single
slice of that grown rectangle, then subtract the 4 corners (which grow as a triangle
for each subsequent layer), and multiply by the "height" of that shape.

Now, think of the growth of the cuboid along the C axis as we add layers. For layer 1,
we take a height-1 slice of the initial cuboid, and append two of them to the initial
cuboid, one on top and one beneath. For layer 1, those height-1 slices we added will grow
to the sides, and we will again add two height-1 slices of the initial cuboid to the very
top and the very bottom. So we can think of the growth along this axis as a sum of height-1
slices that will grow only to the sides, with the same formula we derived above. Thus
the total number of cubes of this C-axis growth for layer N is given by:

2*sum[x=0 -> x=n-1]( (a+2x)(b+2x) - 2x(x+1) )

The total number of cubes in layer N is then given by adding the two formulas above:

total_cubes(n) = c*((a+2n)(b+2n) - 2n(n+1)) + 2*sum[x=0 -> x=n-1]( (a+2x)(b+2x) - 2x(x+1) )

Now the number of cubes *added* on layer N is simply total_cubes(n) - total_cubes(n-1).

Expanding and simplifying this subtraction yields this formula for the number of cubes
*added* on layer N:

new_cubes(n) = 4*n*n + 4*n*(a + b + c - 3) + (a + b - 2)*(2*c - 4) + 2*a*b

With that closed-form formula, we can iterate all initial cuboid shapes whose total volume
is less than the layer-size we're looking for, and compute their layer sizes to see
how many of them match the desired layer-size.
"""

import sys
import time
import random
from multiprocessing import Pool

memoized_results = {}
def number_of_new_cubes_in_layer_n(a,b,c,n):
    return 4*n*n + 4*n*(a + b + c - 3) + (a + b - 2)*(2*c - 4) + 2*a*b

def get_number_of_cuboids_with_a_layer_of_desired_size(size):
    result = 0
    for a in range(1, size + 1):

        for b in range(a, size + 1):
            if a*b > size: break # pylint: disable=multiple-statements

            for c in range(b, size + 1):
                if a*b*c > size: break # pylint: disable=multiple-statements

                current_layer = 1
                current_layer_size = 0
                while current_layer_size < size:
                    current_layer_size = number_of_new_cubes_in_layer_n(a,b,c,current_layer)
                    if current_layer_size == size:
                        result += 1
                        break
                    current_layer += 1
    return result

MAX_SIDE_SIZE, MAX_LAYER_SIZE = [int(arg) for arg in sys.argv[1:]]

c_n_dict = {}
ns_with_value_of_1000 = set()

def compute_for_max_side_size(side_size):
    temp_dict = dict()
    a = side_size
    f_start = time.time()
    for b in range(1, a + 1):
        if number_of_new_cubes_in_layer_n(a,b,1,1) > MAX_LAYER_SIZE: break # pylint: disable=multiple-statements
        for c in range(1, b + 1):
            layer_num = 1
            layer_size = number_of_new_cubes_in_layer_n(a,b,c,layer_num)
            if layer_size > MAX_LAYER_SIZE: break # pylint: disable=multiple-statements
            while layer_size < MAX_LAYER_SIZE:
                temp_dict[layer_size] = temp_dict.get(layer_size, 0) + 1
                layer_num += 1
                layer_size = number_of_new_cubes_in_layer_n(a,b,c,layer_num)

    print(f"Checked cuboids of shape {a}*b*c in {round(time.time() - f_start,4)} seconds")
    return temp_dict

def compute_with_parallelism():
    with Pool() as p:
        side_size_list = list(range(1, MAX_SIDE_SIZE + 1))
        random.shuffle(side_size_list)
        result_dicts = p.map(compute_for_max_side_size, side_size_list)
        print(f"Processing {len(result_dicts)} dictionaries from multiprocessing")
        for d in result_dicts:
            for layer_size, count in d.items():
                c_n_dict[layer_size] = c_n_dict.get(layer_size, 0) + count
                if c_n_dict[layer_size] == 1000:
                    ns_with_value_of_1000.add(layer_size)
                if c_n_dict[layer_size] > 1000 and layer_size in ns_with_value_of_1000:
                    ns_with_value_of_1000.remove(layer_size)

def compute_without_parallelism():
    for a in range(1, MAX_SIDE_SIZE + 1):
        f2_start = time.time()
        for b in range(1, a+1):
            if number_of_new_cubes_in_layer_n(a,b,1,1) > MAX_LAYER_SIZE: break # pylint: disable=multiple-statements
            for c in range(1, b+1):
                layer_num = 1
                layer_size = number_of_new_cubes_in_layer_n(a,b,c,layer_num)
                if layer_size > MAX_LAYER_SIZE: break # pylint: disable=multiple-statements
                while layer_size < MAX_LAYER_SIZE:
                    c_n_dict[layer_size] = c_n_dict.get(layer_size, 0) + 1
                    if c_n_dict[layer_size] == 1000:
                        ns_with_value_of_1000.add(layer_size)
                    if c_n_dict[layer_size] > 1000 and layer_size in ns_with_value_of_1000:
                        ns_with_value_of_1000.remove(layer_size)
                    layer_num += 1
                    layer_size = number_of_new_cubes_in_layer_n(a,b,c,layer_num)
        print(f"Checked cuboids of shape {a}*b*c in {round(time.time() - f2_start,4)} seconds")

if __name__ == "__main__":
    print(f"Computing with MAX_SIDE_SIZE={MAX_SIDE_SIZE} and MAX_LAYER_SIZE={MAX_LAYER_SIZE}")
    start = time.time()
    compute_with_parallelism()
    print(f"Finished in {round(time.time() - start,4)} seconds (MAX_SIDE_SIZE={MAX_SIDE_SIZE} and MAX_LAYER_SIZE={MAX_LAYER_SIZE})")

    for s in [22, 46, 78, 118, 154]:
        print(f"C({s}) = {c_n_dict.get(s,'not present')}")
    print(f"First 10 values of n for with C(n) = 1000: {sorted(ns_with_value_of_1000)[0:10]}")

# Right answer: 18522
# Wrong answers: 18576, 20590, 21862, 22398, 25750, 26282, 26332, 26772, 26892, 27286, 30746, 31012, 31454, 31716, 32604, 33446

# 2000 500000
# [21862, 25750, 26332, 26772, 27286, 33446, 40166, 40454, 41612]
# 2000 1000000
# [21862, 25750, 26332, 26772, 27286, 33446, 40166, 40454, 41612]
# 3000 200000
# [18576, 20590, 22398, 26282, 26892, 30746, 31012, 31454, 31716, 32604]
# 5000 200000
# [18522, 18576, 18880, 22398, 26892, 28400, 32604, 34164, 45188, 47276]
# 5000 20000
# [18522, 18576, 18880]
