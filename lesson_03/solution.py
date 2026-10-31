import os
import sys

from pymongo import ASCENDING, DESCENDING, MongoClient
from pymongo.errors import BulkWriteError, PyMongoError


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


def receive_delivery():
    """Поставка в песочнице и результаы"""
    box = client["sandbox"]["products"]
    print("\nПриемка поставки в sandbox.products")

    arrived = {"SKU-NB-001": 5, "SKU-PH-006": 12, "SKU-PR-010": 3}
    for sku, quantity in arrived.items():
        result = box.update_one({"sku": sku}, {"$inc": {"qty_total": quantity}})
        print(
            f"Остаток {sku}: +{quantity}, найдено {result.matched_count}, "
            f"изменено {result.modified_count}"
        )

    new_products = [
        {
            "_id": "p-101",
            "sku": "SKU-AC-101",
            "title": "Подставка для ноутбука Ugreen",
            "brand": "Ugreen",
            "category": "аксессуары",
            "price": 2490,
            "specs": ["алюминий", "регулируемый угол"],
            "stock": [{"warehouse": "Москва-1", "qty": 14}],
            "rating": 4.4,
            "reviews": 0,
        },
        {
            "_id": "p-102",
            "sku": "SKU-AC-102",
            "title": "Док-станция Baseus 6 в 1",
            "brand": "Baseus",
            "category": "аксессуары",
            "price": 5890,
            "specs": ["USB-C", "HDMI 4K", "SD"],
            "stock": [
                {"warehouse": "Москва-2", "qty": 7},
                {"warehouse": "Екатеринбург", "qty": 3},
            ],
            "rating": 4.2,
            "reviews": 0,
        },
    ]
    try:
        inserted_count = len(box.insert_many(new_products, ordered=False).inserted_ids)
    except BulkWriteError as exc:
        errors = exc.details.get("writeErrors", [])
        if any(error.get("code") != 11000 for error in errors):
            raise
        inserted_count = exc.details.get("nInserted", 0)
        print(f"Существующих позиций: {len(errors)}")
    print(f"Новых позиций добавлено: {inserted_count}")

    discontinued = {"sku": {"$in": ["SKU-CP-018"]}}
    before_delete = box.count_documents(discontinued)
    print(f"Позиций под снятие с продажи: {before_delete}")
    for item in box.find(discontinued, {"_id": 0, "sku": 1, "title": 1}):
        print(f"  {item['sku']} | {item['title']}")
    deleted = box.delete_many(discontinued)
    print(f"Удалено позиций: {deleted.deleted_count}")

    accessories = {"category": "аксессуары"}
    accessories_before = box.count_documents(accessories)
    shipping = box.update_many(accessories, {"$set": {"free_shipping": True}})
    print(
        f"Аксессуаров до обновления: {accessories_before}, "
        f"найдено {shipping.matched_count}, изменено {shipping.modified_count}"
    )
    print(f"Позиций после приемки: {box.count_documents({})}")


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        client.admin.command("ping")
        print("Успехх")
        show_page("Весь каталог, с 1", page=1)
        show_page("Ноутбуки, с 1", category="ноутбуки", page=1, per_page=3)
        show_page("Ноутбуки, с 9", category="ноутбуки", page=9, per_page=3)
        receive_delivery()
    except PyMongoError as exc:
        raise SystemExit("Операция с MongoDB не выполнена") from exc
    finally:
        client.close()


if __name__ == "__main__":
    main()
