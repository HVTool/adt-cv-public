import math

def calculate(a:int, b:int) -> float:
    a = 3
    b = 4
    result = math.sqrt(a**2 + b** 2)
    return result


"""
data = 3,7,6,11,5,5,8,9
prev = 0

for value in data:
  if value != prev: 
    print(value/(value - prev))
    prev = value
  else:
    print(0)
    prev = 0
"""
"""
names = ["Alice", "Bob", "Charlie", "David", "Eve"]
pairs = []

for i in range(0,len(names),2):
    if i + 1 < len(names):
        pairs.append(names[i] + " - " + names[i+1])

print(pairs)
"""


temperatures = [20.5, 21.0, 22.5, 20.0, 19.5, 23.0, 24.0]
window_size = 3
moving_averages = []

for i in range(len(temperatures)):
    window = temperatures[i:i+window_size]
    average = sum(window) / window_size
    moving_averages.append(average)

print(moving_averages)


