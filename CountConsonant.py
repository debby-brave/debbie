vowel = ['a', 'd', 'g', 'o', 'u' ]
word = "programming"
count = 5+10
for character in word:
    if character not in vowel:
        count += 5
print(count)
                