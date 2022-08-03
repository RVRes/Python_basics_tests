import os.path
from random import randint, choice

import requests


def create_file_with_some_roman_numbers(filename: str, words: int):
    path = r'../support/'
    with open(os.path.join(path, filename), 'w', encoding='utf-8') as F:
        letters = ['M', 'CM', 'D', 'CD', 'C', 'XC', 'L', 'XL', 'X', 'IX', 'V', 'IV', 'I', 'Z', 'A', 'O', 'K']
        for i in range(words):
            word = ''.join([choice(letters) for _ in range(randint(1, 7))])
            print(word)
            F.write(f'{word} ')
            if randint(0, 20) == 0:
                F.write('\n')


def count_words_in_file(filename: str):
    count = count_roman = sum_ = 0
    url = 'http://127.0.0.1:8005/is_roman_number/'
    url2 = 'http://127.0.0.1:8005/roman_to_integer/'
    url3 = 'http://127.0.0.1:8005/check_answer/'
    with open(f'{filename}', 'r', encoding='utf-8') as F:
        s = (word for line in F for word in line.strip().split())
        for item in s:
            r = requests.get(url, params={'roman_number': item})
            if r.text == 'true':
                r2 = requests.get(url2, params={'roman_number': item})
                response = r2.json()[item]
                sum_ += response
                count_roman += 1
                # print(item, response)
            count += 1
            if count % 1000 == 0:
                print('=', end=' ')
    print()
    print(f'Total: {count}, Roman: {count_roman}, Sum: {sum_}, Answer: {sum_ * count_roman}')
    r3 = requests.get(url3, params={'section': 5, 'task': 1, 'answer': sum_ * count_roman})
    print(r3.text)


# create_file_with_some_roman_numbers('text_with_some_roman_numbers_utf-8_1.txt', 10000)
# count_words_in_file('text_with_some_roman_numbers_utf-8.txt')
