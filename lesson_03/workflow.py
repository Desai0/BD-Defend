"""Шесть этапов практики с паузами для самостоятельных скриншотов."""

import argparse
import subprocess
import sys
from pathlib import Path

from pymongo.errors import PyMongoError

import solution
from check import verify


SHOTS = [
    ("Подключение к MongoDB", "01-program-start.png"),
    ("Загрузка исходных товаров", "02-products-created.png"),
    ("Чтение каталога", "03-catalog-result.png"),
    ("Поиск по категории", "04-search-result.png"),
    ("Приёмка поставки", "05-update-or-delete-result.png"),
    ("Проверка данных в MongoDB", "06-database-check.png"),
]


def begin(number):
    title, filename = SHOTS[number - 1]
    print("\n" + "=" * 68)
    print(f"Шаг {number}/6. {title}")
    print(f"Скриншот: lesson_03/screens/{filename}")
    print("=" * 68)


def finish(no_pause):
    if not no_pause:
        input("\nСделай скриншот. Нажми Enter для продолжения... ")


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reset", action="store_true",
                        help="пересоздать только shop.products и sandbox.products")
    parser.add_argument("--no-pause", action="store_true",
                        help="пройти все этапы без ожидания Enter")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]

    try:
        begin(1)
        solution.client.admin.command("ping")
        print("Подключение к MongoDB установлено.")
        print(f"Python {sys.version.split()[0]}, MongoDB {solution.client.server_info()['version']}")
        print("Учебные коллекции: shop.products, sandbox.products")
        if args.reset:
            print("На шаге 2 эти две коллекции будут загружены заново.")
        finish(args.no_pause)

        begin(2)
        command = [sys.executable, "-X", "utf8", str(root / "stend/load_practice.py"), "catalog"]
        if args.reset:
            command.append("--reset")
        subprocess.run(command, check=True)
        print("Исходные товары загружены. Количество показано выше.")
        finish(args.no_pause)

        begin(3)
        print("Коллекция shop.products; сортировка: price по убыванию, sku по возрастанию.")
        solution.show_page("Первая страница каталога", page=1, per_page=5)
        finish(args.no_pause)

        begin(4)
        print('Коллекция shop.products; фильтр: {"category": "ноутбуки"}')
        solution.show_page("Найденные ноутбуки", category="ноутбуки", page=1, per_page=5)
        solution.show_page("Несуществующая страница 9", category="ноутбуки", page=9, per_page=3)
        finish(args.no_pause)

        begin(5)
        solution.receive_delivery()
        finish(args.no_pause)

        begin(6)
        passed = verify(solution.client)
        finish(args.no_pause)
        if passed:
            print("\nПрактика завершена. Добавь свои шесть снимков в lesson_03/screens/.")
        return 0 if passed else 1
    except (PyMongoError, subprocess.CalledProcessError) as exc:
        print(f"\nЭтап не выполнен: {type(exc).__name__}. Проверь MongoDB и учебные данные.",
              file=sys.stderr)
        return 1
    except (KeyboardInterrupt, EOFError):
        print("\nWorkflow остановлен. Для чистого прогона запусти снова с --reset.")
        return 130
    finally:
        solution.client.close()


if __name__ == "__main__":
    raise SystemExit(main())
