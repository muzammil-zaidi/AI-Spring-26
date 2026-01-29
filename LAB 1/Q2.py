numbers = []

print("Enter 10 integers:")
for i in range(10):
    num = int(input("Enter number: "))
    numbers.append(num)

print("\nPrime number check:")
for num in numbers:
    if num <= 1:
        print(num, "is NOT a Prime number")
    else:
        prime = True
        for i in range(2, num):
            if num % i == 0:
                prime = False
                break

        if prime:
            print(num, "is a Prime number")
        else:
            print(num, "is NOT a Prime number")
