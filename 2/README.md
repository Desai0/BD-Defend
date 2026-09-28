# Домашнее задание № 4

Сделана задача 1. Остальные пока не выполнены.

| План | Индекс | nReturned | totalDocsExamined | totalKeysExamined | Шаги выполнения |
| --- | --- | --- | --- | --- | --- |
| plan-1.json | Только `_id_` | 33 | 1200 | 0 | COLLSCAN → SORT |
| plan-2.json | `{ service: 1, level: 1, ts: -1, duration_ms: 1 }` | — | — | — | — |
| plan-3a.json | `{ duration_ms: 1, service: 1, level: 1, ts: -1 }` | — | — | — | — |
| plan-3b.json | `{ service: 1, level: 1, duration_ms: 1, ts: -1 }` | — | — | — | — |
| plan-4-bez.json | Только `_id_` | — | — | — | — |
| plan-4.json | Подобрать в задаче 4 | — | — | — | — |

## Задача 1

Подходящего индекса нет, поэтому MongoDB проверила все 1200 документов и отсортировала 33 найденные записи в памяти.

[Разбор плана](https://dfrancour.dev/tools/mongodb-paste-the-plan#v1:zVXbbiM3DP0XYh-ngSe-xfOWOHYbbFynmbSLxaIoGIkzUa2RZiWOM17D_15Iji_ZS7LYAkWfPCZ5SPHwUFoDtbVGZf4g55U1kEEKCXxsyK1uNBpDDrI1GKzI1ygIMtC29Ce0JMMeElBGUjtVmsnlxJAVqD0lUKPzJH8LaQL-DRoJ2Yc1aFqSjhb6CBmQc9bBZpOswZNbqlBg56txVcUi0S0bh6ys-avyMaRkyPqdzmbz5-bpuL-gf4AMxhdprz85u4QEao1mjOKB3tLqucfWrCr1KWa8UxXNlNbKQ9ZJoML2KvREcu5yq5sQ4m8ppJH79g5B50a-FJULNP7OTtpaW0mfBzwqY5QpA9GhKc9YBobz-e0dJOCt4xtkJhe97CH7Kd0kUFF1rSrFkKWd3ll_OOh0EuBVHaBeVbWmOJe64Xyb8JB5PL--zsfnv0ICRZzZfzAcqRwJ3mqrsO4RnQwocPQ3CSYZuveQfQix1JKIXOaMHHMdLI0Q5D1k7BpKwNwSN84EMrvdI-Bn02TLqN_Syk9arFQM31kvrTiypqeBxeP6JfmvDOX1uhPPqkKmWOnRuoUP2bv9BFAu0Ygd1BDJgIq10-3_94r09ogelxRICO7AlWfrjgzKT-bT-PWvVLIlAhlz9Yly6zgcbpSepQk0nuSl8ou9WH2ttN6yGj9JRiBbhyUFfHT9f3T3o5MKs_jmpNLB8Icn9bVFSEB-IcNN2A5hqyrys4ZChV_YX7kHBvf0HHhJdmw-0Zh8m6Stdp6J5o28f7rhIbjJLcldmcKGoAfrGTIYjIqiczoSUsgi3LExxemwkw4TWO4fkeFJ56TXhQRKxYenhYo-DmW3d9a5748KQkq7sj_odYeD9HRUiJ4gokE6HB6K36DDiphcPLsyQeao47syRUF80RQFuaC-ixWHhT0S-5fRM2znDdcNX1rxMuba2kVTRx1fBVNFUiHTpRVN4HmG7cv4XWBuGyfoZ2ebeobtjCrrVq-cdIbthbZioUwZNnKL-d1j-VqLN84-qHvFO_SMXElzM7OmtPnTcj6vcy7lnc2Jv7ePnPidMtI-ToP6_fd2NA0zDPs1toad1Vv9Cxpr9F6JiSmVoTBzu4As3fwD).
