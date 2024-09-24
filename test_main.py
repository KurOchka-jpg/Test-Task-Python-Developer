import pytest
import aiohttp
import json

from unittest.mock import patch
from aioresponses import aioresponses
from main import (input_strings, dumps_json, check_allowed_methods, check_url,
                  ENDWORD, INDENT)


@pytest.mark.asyncio
async def test_check_allowed_methods():
    # Мок для ответа сервера
    url = 'https://example.com'

    with aioresponses() as mocked:
        mocked.get(url, status=200)
        mocked.post(url, status=201)
        mocked.delete(url, status=405)
        mocked.patch(url, status=204)

        async with aiohttp.ClientSession() as session:
            result = await check_allowed_methods(url, session)

        expected_result = {
            "GET": 200,
            "POST": 201,
            "PATCH": 204  # DELETE должен отсутствовать, так как статус 405
        }

        assert result == expected_result


@pytest.mark.asyncio
async def test_check_url():
    # Тестируем функцию, которая валидирует URL
    url = 'https://example.com'

    with aioresponses() as mocked:
        mocked.get(url, status=200)
        mocked.post(url, status=201)
        mocked.delete(url, status=405)
        mocked.patch(url, status=204)

        async with aiohttp.ClientSession() as session:
            result = await check_url(url, session)

        expected_result = {
            url: {
                "GET": 200,
                "POST": 201,
                "PATCH": 204
            }
        }

        assert result == expected_result


@pytest.mark.asyncio
async def test_invalid_url():
    # Тестируем случай, когда строка не является ссылкой
    invalid_url = "not-a-url"

    async with aiohttp.ClientSession() as session:
        result = await check_url(invalid_url, session)

    assert result is None


def test_input_strings():
    # Подменяем функцию input последовательностью значений
    with patch('builtins.input', side_effect=['https://example.com',
                                              'https://test.com', ENDWORD]):
        result = input_strings()
        expected_result = ['https://example.com', 'https://test.com']
        assert result == expected_result


def test_dumps_json():
    # Тестируем функцию преобразования в JSON.
    test_string = {'food': {'horse': 'apple', 'rabbit': 'carrot'}}
    expected_json = json.dumps(test_string, indent=INDENT)
    test_json = dumps_json(test_string)
    assert test_json == expected_json
