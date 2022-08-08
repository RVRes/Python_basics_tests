from random import randint, choice
from getpass import getpass


def user_input() -> tuple:
    first_len = tuple(map(int, input('Длина первого числа (от до): ').split()))
    if len(first_len) == 1:
        first_len = (first_len[0], first_len[0])
    second_len = tuple(map(int, input('Длина второго числа (от до): ').split()))
    if len(second_len) == 1:
        second_len = (second_len[0], second_len[0])
    signs = input('Знаки: ')
    columns = int(input('Количество столбцов: '))
    raws = int(input('примеров в столбце: '))
    return first_len, second_len, signs, columns, raws


def get_expression(n1_len: tuple, n2_len: tuple, signs: str) -> tuple:
    def get_random(nl: tuple) -> int:
        a = 10 ** (nl[0] - 1)
        b = 10 ** randint(nl[0], nl[1]) - 1
        result = None
        while not result or result in [0, 1]:
            result = randint(a, b)
        return result

    def solve(a, b, sign):
        return {
            '+': a + b,
            '-': a - b,
            '*': a * b,
            '/': round(a / b)
        }[sign]

    sign = choice(signs)
    if sign == '/':
        result_len = (max(n1_len[0] - n2_len[0], 1), max(n1_len[1] - n2_len[1], n1_len[0] - n2_len[0], 1))
        n1 = n2 = None
        while not n1 or not (n1_len[0] <= len(str(n1 * n2)) <= n1_len[1]):
            n1 = get_random(result_len)
            n2 = get_random(n2_len)
        n1 = n1 * n2
    else:
        n1, n2 = get_random(n1_len), get_random(n2_len)
    if sign == '-':
        while n2 > n1:
            n1, n2 = get_random(n1_len), get_random(n2_len)
    return n1, n2, sign, solve(n1, n2, sign)


def create_test(n1_len, n2_len, sign, columns, raws):
    test_ = []
    for _ in range(raws):
        line = []
        for _ in range(columns):
            for _ in range(10000):
                expression = get_expression(n1_len, n2_len, sign)
                if all(expression not in line_ for line_ in test_) and expression not in line:
                    line.append(expression)
                    break
            else:
                if line:
                    test_.append(line)
                return test_
        test_.append(line)
    return test_


def render_test(data, need_answers=False) -> str:
    def get_max_len(data_, item_num):
        return max(len(str(value[item_num])) for row_ in data_ for value in row_)

    n1_len = get_max_len(data, 0)
    n2_len = get_max_len(data, 1)
    answer_len = get_max_len(data, 3)
    output = ''
    for raw in data:
        for n1, n2, sign, answer in raw:
            output += f'   {n1:{n1_len}} {sign} {n2:{n2_len}} = {answer if need_answers else "":{answer_len}}   '
        output += '\n'
    return output


def print_test(data, need_answers=False) -> None:
    output = render_test(data, need_answers)
    print(output)


def write_test_to_file(data, need_answers=False) -> None:
    tests_file = 'math_1_grade_answers.txt'
    output = render_test(data, need_answers)
    with open(tests_file, 'w') as file:
        file.write(output)


# settings = ((3, 3), (1, 3), '+-*/', 4, 10)
settings = user_input()
test = create_test(*settings)
print_test(test)
if input('Нужны ответы? (y / n): ') in ['y', 'Y', 'д', 'Д']:
    write_test_to_file(test, need_answers=True)
while True:
    if input('Выход? (y / n): ') in ['y', 'Y', 'д', 'Д']:
        break
