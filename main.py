import aiohttp
import asyncio
import validators
import json

from tqdm.asyncio import tqdm


HTTP_METHODS = ['GET', 'POST', 'DELETE', 'PATCH']
UNAVAILIBLE_STATUS = 405
ENDWORD = 'end'
TIMEOUT = 5
INDENT = 3


def input_strings():
    # Функция для ввода строк

    strings = []

    while True:
        string = input(f'Введите ссылку или {ENDWORD}: ')
        if string == ENDWORD:
            return strings
        else:
            strings.append(string)


def dumps_json(result):
    # Функция для преобразования результата в JSON

    return json.dumps(result, indent=INDENT)


async def check_allowed_methods(url, session):
    # Функция для проверки доступных методов по ссылкам

    allowed_methods = {}
    try:
        for method in HTTP_METHODS:
            async with session.request(method, url,
                                       timeout=TIMEOUT, ssl=False) as response:
                if response.status != UNAVAILIBLE_STATUS:
                    allowed_methods[method] = response.status
        return allowed_methods

    except Exception as ex:
        print(ex)


async def check_url(url, session):
    # Функция для провери строки. Является ли URL?

    if validators.url(url):
        allowed_methods = await check_allowed_methods(url, session)
        return {url: allowed_methods}
    else:
        print(f'Строка {url[:10]}... не является ссылкой!')


async def main():
    # Точка входа

    strings = input_strings()
    results = {}
    tasks = []
    async with aiohttp.ClientSession() as session:
        for string in strings:
            tasks.append(check_url(string, session))
        responses = await tqdm.gather(*tasks)

    for response in responses:
        if response:
            results.update(response)

    json_result = dumps_json(results)
    print(json_result)


if __name__ == '__main__':
    asyncio.run(main())
