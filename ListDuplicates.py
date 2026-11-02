def has_duplicate(numbers):
    seen = set()

    for number in numbers:
        if number in seen:
            return True
       
        seen.add(number)

    return False

print(has_duplicate([1, 2, 3, 2]))
print(has_duplicate([1, 2, 3, 4]))
print(has_duplicate([]))