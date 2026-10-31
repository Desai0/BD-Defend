# Занятие 3 · Каталог товаров

Программа каталога и приёмки поставки: [solution.py](solution.py).
Результаты и ответы на вопросы: [homework_03.md](homework_03.md).

## Запуск

Из корня репозитория:

```bash
rtk proxy docker compose -f stend/docker-compose.yml up -d --wait
rtk proxy python -m pip install -r requirements.txt
rtk proxy python stend/load_practice.py catalog --reset
rtk proxy python -X utf8 lesson_03/solution.py
```

Загрузка с `--reset` восстанавливает исходные товары в `shop.products`
и `sandbox.products`. Приёмка изменяет только песочницу.

Проверка результата:

```bash
rtk proxy python -X utf8 lesson_03/check.py
```
