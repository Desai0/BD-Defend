"""Выгрузка плана второго запроса в JSON.

Из корня репозитория:
    rtk proxy python -m pip install pymongo==4.18.2
    rtk proxy python 2/plan.py

По умолчанию MongoDB находится на localhost:27018.
Другой адрес можно задать через MONGO_URI. Имя JSON — аргумент команды.
Индексы скрипт не изменяет.
"""

from pymongo import MongoClient

# ─────────────────────────────────────────────────────────────────────────
#  ЗАПРОС. Меняете только этот блок.
# ─────────────────────────────────────────────────────────────────────────

BAZA = "logs"
KOLLEKCIYA = "events"

# Фильтр — тот же документ, что вы пишете в find({...}).
FILTR = {
    "level": "error",
}

# Сортировка: список пар «поле, направление». 1 — по возрастанию, -1 — по
# убыванию. Пустой список, если сортировки нет.
SORTIROVKA = [("duration_ms", -1)]

# Сколько документов вернуть. 0 — все.
PREDEL = 10

# Куда положить план. Файл ложится рядом с этим скриптом.
FAYL = "plan-4.json"

# ─────────────────────────────────────────────────────────────────────────
#  Дальше менять ничего не нужно.
# ─────────────────────────────────────────────────────────────────────────

import json
import os
import sys
from pathlib import Path

from bson.json_util import RELAXED_JSON_OPTIONS, dumps


def oshibka(tekst):
    print(tekst, file=sys.stderr)
    sys.exit(2)


def shagi_plana(stadiya):
    """Имена шагов снизу вверх: так же, как их рисует визуализатор."""
    imena = []
    while stadiya:
        imena.append(stadiya["stage"])
        stadiya = stadiya.get("inputStage")
    return list(reversed(imena))


def main():
    imya = sys.argv[1] if len(sys.argv) > 1 else FAYL
    if not imya.endswith(".json"):
        oshibka("Имя файла должно оканчиваться на .json, например plan-2.json")

    # Адрес отдельного учебного стенда можно заменить через MONGO_URI.
    client = MongoClient(
        os.environ.get("MONGO_URI", "mongodb://localhost:27018"),
        serverSelectionTimeoutMS=5000,
    )
    try:
        client.admin.command("ping")
    except Exception:
        oshibka(
            "Сервер не отвечает. Проверьте стенд и MONGO_URI.\n"
            "Для подготовленной среды адрес: mongodb://localhost:27018"
        )

    kollekciya = client[BAZA][KOLLEKCIYA]
    vsego = kollekciya.count_documents({})
    if vsego == 0:
        oshibka("Коллекция %s.%s пуста. Данные: docker compose run --rm reset"
                % (BAZA, KOLLEKCIYA))

    zapros = {"find": KOLLEKCIYA, "filter": FILTR}
    if SORTIROVKA:
        zapros["sort"] = dict(SORTIROVKA)
    if PREDEL:
        zapros["limit"] = PREDEL

    plan = client[BAZA].command("explain", zapros, verbosity="executionStats")
    stats = plan["executionStats"]

    # Файл кладём рядом со скриптом: студент запускает его из своей папки work.
    fayl = Path(__file__).resolve().parent / imya
    # dumps из bson пишет даты и числа BSON так, как их ждёт визуализатор.
    fayl.write_text(dumps(plan, json_options=RELAXED_JSON_OPTIONS), encoding="utf-8")

    print("Запрос к %s.%s, всего документов в коллекции: %d" % (BAZA, KOLLEKCIYA, vsego))
    print("  фильтр:                %s" % json.dumps(FILTR, ensure_ascii=False))
    print("  сортировка:            %s" % (SORTIROVKA or "нет"))
    print("  предел:                %s" % (PREDEL or "нет"))
    print()
    print("  файл с планом:         %s" % fayl.name)
    print("  возвращено:            %d" % stats["nReturned"])
    print("  документов просмотрено:%d" % stats["totalDocsExamined"])
    print("  ключей просмотрено:    %d" % stats["totalKeysExamined"])
    print("  шаги плана:            %s" % " → ".join(shagi_plana(stats["executionStages"])))
    print("  индексы коллекции:     %s"
          % ", ".join(i["name"] for i in kollekciya.list_indexes()))


if __name__ == "__main__":
    main()
