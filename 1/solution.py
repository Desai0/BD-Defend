import os
import sys

from pymongo import ASCENDING, DESCENDING, MongoClient
from pymongo.errors import PyMongoError


MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
products = client["shop"]["products"]


def catalog_page(category=None, page=1, per_page=5, sort_field="price", desc=True):
    """Вернуть товары одной страницы и кол-во под тем же фильтром"""
    if page < 1 or per_page < 1:
        raise ValueError("должны быть положительными")

    query = {}
    if category is not None:
        query["category"] = category

    fields = {"_id": 0, "sku": 1, "title": 1, "price": 1, "rating": 1}
    order = [(sort_field, DESCENDING if desc else ASCENDING)]
    if sort_field != "sku":
        order.append(("sku", ASCENDING))

    total = products.count_documents(query)
    items = list(
        products.find(query, fields)
        .sort(order)
        .skip((page - 1) * per_page)
        .limit(per_page)
    )
    return items, total


def show_page(title, **options):
    items, total = catalog_page(**options)
    print(f"\n{title}: показано {len(items)} из {total}")
    for item in items:
        print(
            f"{item['sku']} | {item['title']} | "
            f"{item['price']} р | рейтинг {item['rating']}"
        )


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        client.admin.command("ping")
        print("Успехх")
        show_page("Весь каталог, с 1", page=1)
        show_page("Ноутбуки, с 1", category="ноутбуки", page=1, per_page=3)
        show_page("Ноутбуки, с 9", category="ноутбуки", page=9, per_page=3)
    except PyMongoError as exc:
        raise SystemExit("Не удалось прочитать каталог") from exc
    finally:
        client.close()


if __name__ == "__main__":
    main()
