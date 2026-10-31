"""Данные занятий 3 и 4. Без --reset загружает только пустые коллекции."""

import argparse
import os
from pathlib import Path

from bson.json_util import loads
from pymongo import MongoClient


DATASETS = {
    "catalog": [
        ("shop", "products", "shop.products.json"),
        ("sandbox", "products", "shop.products.json"),
    ],
    "logs": [("logs", "events", "logs.events.json")],
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dataset", choices=DATASETS)
    parser.add_argument("--reset", action="store_true",
                        help="пересоздать указанные коллекции, удалив их данные и индексы")
    args = parser.parse_args()
    seed = Path(__file__).resolve().parent / "seed"
    batches = [(database, collection, loads((seed / filename).read_text(encoding="utf-8")))
               for database, collection, filename in DATASETS[args.dataset]]

    with MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017"),
                     serverSelectionTimeoutMS=5000) as client:
        client.admin.command("ping")
        occupied = [f"{database}.{collection}" for database, collection, _ in batches
                    if client[database][collection].find_one() is not None]
        if occupied and not args.reset:
            parser.exit(2, "Данные уже есть: " + ", ".join(occupied)
                        + ". Для нового прогона используйте --reset.\n")
        for database, collection, documents in batches:
            target = client[database][collection]
            if args.reset:
                target.drop()
            target.insert_many(documents, ordered=True)
            print(f"{database}.{collection}: {target.count_documents({})}")


if __name__ == "__main__":
    main()
