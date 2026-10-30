def reverse_list(items):
    code = []
    for  i in range(len(items)- 1, - 1,- 1):
        code.append(items[i])


    return code 


print(reverse_list([1, 2, 3, 4]))
print(reverse_list(["a", "b", "c"]))

