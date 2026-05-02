from knapsack import knapsack

values = [60, 100, 120]
weights = [10, 20, 30]
capacity = 50
n = len(values)

result = knapsack(capacity, weights, values, n)

print("Maximum value that can be carried:", result)