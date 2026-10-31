# Данные практических работ

`shop.products.json` и `logs.events.json` взяты без изменений из
[MaximBytecamp/mongodb-practice, коммит 00eb16b](https://github.com/MaximBytecamp/mongodb-practice/tree/00eb16bbd515c7298a799a03d15f59b8c1497682/stend/seed).

Для занятия 3 файл товаров загружается в `shop.products` и `sandbox.products`:
исходные данные этих коллекций в стенде курса одинаковы (по 21 документу).
Для занятия 4 загружается `logs.events` (1200 документов).
Даты в Extended JSON загрузчик сохраняет как BSON Date.

Загрузка из корня репозитория:

```bash
rtk proxy python stend/load_practice.py catalog
rtk proxy python stend/load_practice.py logs
```

Для чистого повторного прогона добавьте `--reset`: он удаляет данные и индексы
только выбранного набора. Остальные учебные коллекции не затрагиваются.
