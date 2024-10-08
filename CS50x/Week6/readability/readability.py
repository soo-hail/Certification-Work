from math import ceil


text = input("Text: ")

l = 0  # NO.OF LETTERS
w = 0  # NO.OF WORDS
s = 0  # NO.OF SENTENCES

for ch in text:
    if ch.isalpha():
        l += 1
    elif ch == ' ':
        w += 1
    elif ch in ['.', '!', '?']:
        s += 1

w += 1  # FOR LAST WORD

L = (100 / w) * l
S = (100 / w) * s

index = 0.0588 * L - 0.296 * S - 15.8

grade = ceil(index)

if grade < 1:
    print("Before Grade 1")
elif grade > 16:
    print("Grade 16+")
else:
    print(f"Grade {grade}")
