from utils import is_prime

total = 2

for i in range(3, 2_000_000, 2):
    if is_prime(i):
        total += i

print(f"Sum is {total}")
