# Быстрый старт

Репозиторий: [Desai0/BD-Defend](https://github.com/Desai0/BD-Defend).
Создан из шаблона курса с собственной историей, без связи форка.

Команды выполняются из корня `data-platform`. Перед запуском откройте
Docker Desktop и дождитесь готовности движка.

## Запуск и проверка

```bash
rtk proxy docker compose -f stend/docker-compose.yml up -d --wait
rtk proxy docker compose -f stend/docker-compose.yml ps
rtk proxy docker compose -f stend/docker-compose.yml exec -T mongo mongosh --quiet --eval 'db.adminCommand({ping:1}).ok'
```

У контейнера `hh-mongo` должен быть статус `healthy`, результат `ping` — `1`.
Порт `27017` опубликован только на `127.0.0.1`.
Данные сохраняются в Docker-томе `stend_mongo-data`.

## MongoDB Compass

Откройте сохранённое подключение **data-platform local**:

```text
mongodb://localhost:27017/
```

Пароль для локального учебного стенда не нужен. База изначально пустая:
видны только системные базы `admin`, `config`, `local`.

Первый учебный документ создаётся вручную. Затем восемь резюме из
`stend/seed/resumes.json` импортируются в `hh.resumes` через
**ADD DATA → Import JSON or CSV file**. Данные следующих занятий
загружайте по их инструкциям.

## Остановка и журнал

```bash
rtk proxy docker compose -f stend/docker-compose.yml stop
rtk proxy docker compose -f stend/docker-compose.yml logs --tail 50 mongo
```

Команда `stop` сохраняет данные; следующий `up -d --wait` снова запускает стенд.
Команда `down -v` удаляет учебную базу вместе с томом — для обычной остановки
она не нужна.

## Начало задания

Читайте `README.md` и `homework_*.md` в папке нужного занятия.
Для первого задания:

```bash
rtk git switch -c hw-01
```

После выполнения задания:

```bash
rtk git add lesson_01
rtk git commit -m "hw-01: выполнено задание"
rtk git push -u origin hw-01
```

Создайте Pull Request из `hw-01` в `main` своего репозитория.
`origin` указывает на `Desai0/BD-Defend`, `upstream` — на шаблон преподавателя.

Инструкции по установке на другом компьютере: [stend/SETUP.md](stend/SETUP.md).
