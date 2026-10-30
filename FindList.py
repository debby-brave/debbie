def find_number(numbers,  target):
  for i in range (len(numbers)):
     if numbers[i] == target:
       return i


print(find_number([10, 25, 30, 45 ], 30)) 
print(find_number([5, 8, 5, 9], 5))
print(find_number([10, 20, 30], 99))           

