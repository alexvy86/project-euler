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
from multiprocessing import Pool

memoized_results = {}
def number_of_new_cubes_in_layer_n(a,b,c,n):
    return 4*n*n + 4*n*(a + b + c - 3) + (a + b - 2)*(2*c - 4) + 2*a*b
    a,b,c = sorted([a,b,c]) # The orientation of the cuboid doesn't matter, consider only one for memoization purposes
    key = f"{a}_{b}_{c}_{n}"
    if key not in memoized_results:
        memoized_results[key] = 4*n*n + 4*n*(a + b + c - 3) + (a + b - 2)*(2*c - 4) + 2*a*b
    return memoized_results[key]

#a, b, c, n = [int(arg) for arg in sys.argv[1:]]
#print(f"{number_of_new_cubes_in_layer_n(a,b,c,n)} cubes in layer {n} for cuboid {a},{b},{c}")

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

#TEST_LAYER_SIZE = 22
#number_of_cuboids_with_layer_of_size = get_number_of_cuboids_with_a_layer_of_desired_size(TEST_LAYER_SIZE)
#print(f"Number of cuboids with a layer of size {TEST_LAYER_SIZE}: {number_of_cuboids_with_layer_of_size}")

DESIRED_NUMBER_OF_CUBOIDS = 10
# for layer_size in range(2, 10000, 2): # There's always an even number of cuboids in any layer, no point in checking odd-sized ones
#     cuboids_with_layers_of_this_size = get_number_of_cuboids_with_a_layer_of_desired_size(layer_size)
#     print(f"Checked layer size {layer_size}: {cuboids_with_layers_of_this_size}")
#     if cuboids_with_layers_of_this_size == DESIRED_NUMBER_OF_CUBOIDS:
#         print(f"Least value of n for which C(n) == {DESIRED_NUMBER_OF_CUBOIDS}: {layer_size}")
#         sys.exit()

MAX_SIDE_SIZE = 100
MAX_LAYERS_TO_COMPUTE = 1000

c_n_dict = {}
ns_with_value_of_1000 = set()

if __name__ == "__main__":
    print(f"Computing with MAX_SIDE_SIZE={MAX_SIDE_SIZE} and MAX_LAYERS_TO_COMPUTE={MAX_LAYERS_TO_COMPUTE}")
    for a in range(1, MAX_SIDE_SIZE + 1):
        start = time.time()
        #print(f"c_n: {c_n_dict}")
        for b in range(a, MAX_SIDE_SIZE + 1):
            for c in range(b, MAX_SIDE_SIZE + 1):
                for layer_num in range (1, MAX_LAYERS_TO_COMPUTE + 1):
                    layer_size = number_of_new_cubes_in_layer_n(a,b,c,layer_num)
                    c_n_dict[layer_size] = c_n_dict.get(layer_size, 0) + 1
                    if c_n_dict[layer_size] == 1000:
                        ns_with_value_of_1000.add(layer_size)
                    if c_n_dict[layer_size] == 1001 and layer_size in ns_with_value_of_1000:
                        ns_with_value_of_1000.remove(layer_size)
        print(f"Checked cuboids of shape {a}*b*c in {round(time.time() - start,4)} seconds")

    for s in [22, 46, 78, 118, 154]:
        print(f"C({s}) = {c_n_dict[s]}")
    print(f"First 10 values of n for with C(n) = 1000: {sorted(ns_with_value_of_1000)[0:10]}")