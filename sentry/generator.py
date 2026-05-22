import random

lower_alpha = [
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
]
upper_alpha = [
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
    "M",
    "N",
    "O",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "U",
    "V",
    "W",
    "X",
    "Y",
    "Z",
]
symbols_set = ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")"]
numbers_set = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]


def generate_password(
    len=16, include_symbols=False, include_numbers=False, include_uppercase=False
) -> str:
    password = ""
    charset = lower_alpha

    if include_symbols:
        charset.extend(symbols_set)
    if include_numbers:
        charset.extend(numbers_set)
    if include_uppercase:
        charset.extend(upper_alpha)

    for i in range(len):
        password += random.choice(charset)

    return password
