def move_zeros(numbers):
    code = []
    count = 0 

    for number in numbers:
        if number == 0:
            count += 1
        else:
            code.append(number)
    for a in range(count):
        code.append(0)

    return code


print(move_zeros([0, 1, 0, 3, 12]))
print(move_zeros([1, 2, 3]))
print(move_zeros([0, 0, 5]))