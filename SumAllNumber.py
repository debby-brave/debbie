def list_sum(numbers):
    if not numbers:
        return None

    sum = 0

    for number in numbers:
         sum += number

    return sum


print(list_sum([2, 4, 6, 8]))
print(list_sum([-5, 10, -2]))
print(list_sum([0, 0, 0]))


        
