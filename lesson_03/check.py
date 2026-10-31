"""Самопроверка по требованиям practice01/check.py из mongodb-practice."""

import os
from pathlib import Path

from bson.json_util import loads
from pymongo import MongoClient


def verify(client):
    products = client["shop"]["products"]
    box = client["sandbox"]["products"]
    results = []

    def check(name, actual, expected):
        ok = actual == expected
        results.append(ok)
        print(f"{'OK' if ok else 'ОШИБКА'} | {name}: {actual!r}"
              + ("" if ok else f"; ожидалось {expected!r}"))

    print("Проверка shop.products и sandbox.products")
    check("товаров в каталоге shop.products", products.count_documents({}), 21)
    check("ноутбуков", products.count_documents({"category": "ноутбуки"}), 5)
    top = products.find_one({}, {"title": 1}, sort=[("price", -1)])
    check("самый дорогой товар", (top or {}).get("title"), "Ноутбук Apple MacBook Air 13")
    check("позиций в sandbox.products", box.count_documents({}), 22)
    check("новинка p-101", box.count_documents({"_id": "p-101"}), 1)
    check("новинка p-102", box.count_documents({"_id": "p-102"}), 1)
    check("снятый с продажи SKU-CP-018", box.count_documents({"sku": "SKU-CP-018"}), 0)
    check("аксессуаров с бесплатной доставкой", box.count_documents(
        {"category": "аксессуары", "free_shipping": True}), 5)
    for sku, quantity in [("SKU-NB-001", 5), ("SKU-PH-006", 12), ("SKU-PR-010", 3)]:
        check(f"остаток {sku}", (box.find_one({"sku": sku}) or {}).get("qty_total"), quantity)

    seed = Path(__file__).resolve().parents[1] / "stend/seed/shop.products.json"
    expected = loads(seed.read_text(encoding="utf-8"))
    check("эталонный каталог shop полностью сохранён",
          list(products.find().sort("_id", 1)) == sorted(expected, key=lambda p: p["_id"]), True)
    print(f"\nПройдено {sum(results)} из {len(results)}")
    return all(results)


def main():
    with MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017"),
                     serverSelectionTimeoutMS=5000) as client:
        client.admin.command("ping")
        return 0 if verify(client) else 1


if __name__ == "__main__":
    raise SystemExit(main())
