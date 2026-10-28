# subcut — подкожные тесты на Python

Учебный проект к практической работе «Подкожные тесты на Python»
(дисциплина «Поддержка и тестирование программных модулей», Лисевич Арсений, Исп/п23-09.2).

Маленькая система регистрации пользователей: бизнес-логика в `users.py`, тонкий вход
в `api.py` и клиент внешнего сервиса баллов в `loyalty.py`. Задача — показать, что
подкожный тест проверяет сценарий целиком и его побочные эффекты, а unit-тест одной
функции этого не делает.

## Структура

| Файл | Назначение |
| --- | --- |
| `users.py` | `hash_password`, `InMemoryUserRepository`, `UserService.register` |
| `api.py` | `register_endpoint`: запрос → вызов сервиса → HTTP-код и тело |
| `loyalty.py` | клиент внешнего сервиса бонусных баллов (`requests` + `raise_for_status`) |
| `tests/test_users.py` | unit-тест хеша и подкожные тесты сценария регистрации |
| `tests/test_api.py` | smoke-тест `register_endpoint` (201 и тело ответа) |
| `tests/test_loyalty.py` | `responses`: успешный ответ 200 и ошибка 500 |
| `logs/` | вывод всех прогонов pytest, на нём построен отчёт |
| `screenshots/` | 16 скриншотов для отчёта |

## Запуск

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install pytest requests responses

python -m pytest -q .                          # 8 passed
python -m pytest -q tests\test_users.py tests\test_api.py
python -m pytest tests\test_loyalty.py -v
```

Тесты запускаются из корня проекта и именно как `python -m pytest`: так корень попадает
в путь поиска модулей и работают импорты `from users import ...`.

## Что показывают опыты с багами

| Баг в `users.py` | 2 стартовых теста | Полный набор |
| --- | --- | --- |
| нет `self.repository.add(user)` | 1 failed, 1 passed | 2 failed, 4 passed |
| нет `self.mailer.send(...)` | 1 failed, 1 passed | 2 failed, 4 passed |

В обоих случаях падает подкожный тест сценария, а unit-тест `hash_password` остаётся
зелёным: он проверяет функцию, а не сценарий. На полном наборе к нему присоединяется
тест на дубликат email, который сторожит и запись в хранилище, и единственное письмо.
Smoke-тест `api.py` остаётся зелёным — он проверяет контракт контроллера, а не хранилище.

## Мок внешнего API

`responses` перехватывает `requests` на уровне сети, поэтому код `loyalty.py` не меняется,
а тесты проходят без интернета. Проверено запуском с нерабочим прокси
`HTTPS_PROXY=http://127.0.0.1:1`: результат тот же — 2 passed.

## CI

GitHub Actions на каждый push: Python 3.12, установка `pytest requests responses`,
затем `python -m pytest -q`.

Отчёт по ГОСТ — в сдаваемой папке рядом с проектом
(`Отчёт_Практическая_работа_подкожные_тесты.docx`).
