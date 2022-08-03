import time

import uvicorn
import requests
from fastapi import FastAPI
import re

app = FastAPI()


@app.get("/")
async def root():
    return 'Uvicorn server is running'


@app.get("/roman_to_integer/")
async def rome_to_integer(roman_number: str):
    roman_to_int = {'M': 1000, 'CM': 900, 'D': 500, 'CD': 400, 'C': 100, 'XC': 90, 'L': 50, 'XL': 40, 'X': 10, 'IX': 9,
                    'V': 5, 'IV': 4, 'I': 1}

    result, s = 0, roman_number
    while s:
        if len(s) >= 2 and s[:2:] in roman_to_int:
            result += roman_to_int[s[:2:]]
            s = s[2::]
            continue
        if len(s) >= 1 and s[0] in roman_to_int:
            result += roman_to_int[s[0]]
            s = s[1::]
    return {roman_number: result}


# @app.get("/is_roman_number/{roman_number}")
@app.get("/is_roman_number/")
def is_roman_number(roman_number: str):
    pattern = re.compile(r"""   
                                ^M{0,3}
                                (CM|CD|D?C{0,3})?
                                (XC|XL|L?X{0,3})?
                                (IX|IV|V?I{0,3})?$
            """, re.VERBOSE)

    if re.match(pattern, roman_number):
        return True
    return False


# ?section=5?task=1?answer={ANSWER}
@app.get("/check_answer/")
def check_answer(section: int, task: int, answer: str):
    time.sleep(1)
    if section == 5 and task == 1:
        if answer == '788726950':
            return 'Верно! Ты умница!'
        else:
            return 'Нет, что-то пошло не так. Проверь себя на каждом этапе'

    return 'Неверно составлен запрос'


if __name__ == "__main__":
    HOST = "127.0.0.1"
    PORT = 8005
    try:
        r = requests.get(f'http://{HOST}:{PORT}/')
        print('server is running ' if r.status_code == 200 else 'server running with errors')
    except Exception:
        print('server is not running')
        uvicorn.run(app, host=HOST, port=PORT)
