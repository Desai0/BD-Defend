# Занятие 3 · Каталог товаров

Решение на Python: [solution.py](solution.py). Заполненный отчёт:
[homework_03.md](homework_03.md). Оригинал задания:
[homework_03.md преподавателя](https://github.com/MaximBytecamp/data-platform-template/blob/main/lesson_03/homework_03.md).

## Workflow для скриншотов

Из корня репозитория:

```bash
rtk proxy docker compose -f stend/docker-compose.yml up -d --wait
rtk proxy python -m pip install -r requirements.txt
rtk proxy python -X utf8 lesson_03/workflow.py --reset
```

Программа проходит шесть этапов и после каждого ждёт Enter.
Сделай снимок терминала и сохрани под именем, которое она показывает.
Точные действия и ожидаемые результаты — в [screens/README.md](screens/README.md).
Снимки программа не создаёт.

`--reset` заново загружает `shop.products` и `sandbox.products`; остальные
коллекции не затрагиваются. Это нужно перед каждым полным прогоном:
приёмка поставки прибавляет остатки, поэтому запуск без сброса повторяет поставку.

## Проверка без пауз

```bash
rtk proxy python -X utf8 lesson_03/workflow.py --reset --no-pause
```

Проверить уже полученный результат, не меняя данные:

```bash
rtk proxy python -X utf8 lesson_03/check.py
```

Ожидается **12 из 12**. Проверяются данные в MongoDB: количество товаров,
новые позиции, снятый с продажи артикул, доставка и остатки. Дополнительно
каталог `shop.products` целиком сравнивается с исходными данными.
Основа проверок — [самопроверка преподавателя](https://github.com/MaximBytecamp/mongodb-practice/blob/00eb16bbd515c7298a799a03d15f59b8c1497682/practice01/check.py).

## Сдача

Ветка `hw-03`. Текст отчёта и ответы заполнены; осталось добавить свои
шесть снимков по подготовленным ссылкам и завершить Pull Request в `main`.
Предыдущие снимки сохранены отдельно в `screens/archive-2026-09-27/`.
