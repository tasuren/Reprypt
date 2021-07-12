# Benchmark test

from reprypt import encrypt, decrypt
from decimal import Decimal
from time import time


start = time()
result = encrypt("I wanna be the guy!", "Ohk")
speed = Decimal(time() - start)
print("Result\t:", result + "\nSpeed\t:", speed)
