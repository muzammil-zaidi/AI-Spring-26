def fibonacci(n):
    sequence = []
    a = 0
    b = 1

    while a <= n:
        sequence.append(a)
        a, b = b, a + b

    return sequence


num = int(input("Enter a number: "))
result = fibonacci(num)
print("Fibonacci sequence up to", num, "is:")
print(result)
