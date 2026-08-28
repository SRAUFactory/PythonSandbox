result = ["", "Fizz", "Buzz", "FizzBuzz"]
fmt = ["{0:d}", "", "", ""]
for num in range(1, 101):
    idx = (num - 1) % 3 // 2 + (num - 1) % 5 // 4 * 2
    print(result[idx] + fmt[idx].format(num))
