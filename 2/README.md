# Домашнее задание № 4

Все четыре задачи выполнены.

| План | Индекс | nReturned | totalDocsExamined | totalKeysExamined | Шаги выполнения |
| --- | --- | --- | --- | --- | --- |
| plan-1.json | Только `_id_` | 33 | 1200 | 0 | COLLSCAN → SORT |
| plan-2.json | `{ service: 1, level: 1, ts: -1, duration_ms: 1 }` | 33 | 33 | 43 | IXSCAN → FETCH |
| plan-3a.json | `{ duration_ms: 1, service: 1, level: 1, ts: -1 }` | 33 | 33 | 378 | IXSCAN → SORT → FETCH |
| plan-3b.json | `{ service: 1, level: 1, duration_ms: 1, ts: -1 }` | 33 | 33 | 33 | IXSCAN → SORT → FETCH |
| plan-4-bez.json | Только `_id_` | 10 | 1200 | 0 | COLLSCAN → SORT |
| plan-4.json | `{ level: 1, duration_ms: -1 }` | 10 | 10 | 10 | IXSCAN → FETCH → LIMIT |

## Задача 1

Подходящего индекса нет, поэтому MongoDB проверила все 1200 документов и отсортировала 33 найденные записи в памяти.

[Разбор плана](https://dfrancour.dev/tools/mongodb-paste-the-plan#v1:zVXbbiM3DP0XYh-ngSe-xfOWOHYbbFynmbSLxaIoGIkzUa2RZiWOM17D_15Iji_ZS7LYAkWfPCZ5SPHwUFoDtbVGZf4g55U1kEEKCXxsyK1uNBpDDrI1GKzI1ygIMtC29Ce0JMMeElBGUjtVmsnlxJAVqD0lUKPzJH8LaQL-DRoJ2Yc1aFqSjhb6CBmQc9bBZpOswZNbqlBg56txVcUi0S0bh6ys-avyMaRkyPqdzmbz5-bpuL-gf4AMxhdprz85u4QEao1mjOKB3tLqucfWrCr1KWa8UxXNlNbKQ9ZJoML2KvREcu5yq5sQ4m8ppJH79g5B50a-FJULNP7OTtpaW0mfBzwqY5QpA9GhKc9YBobz-e0dJOCt4xtkJhe97CH7Kd0kUFF1rSrFkKWd3ll_OOh0EuBVHaBeVbWmOJe64Xyb8JB5PL--zsfnv0ICRZzZfzAcqRwJ3mqrsO4RnQwocPQ3CSYZuveQfQix1JKIXOaMHHMdLI0Q5D1k7BpKwNwSN84EMrvdI-Bn02TLqN_Syk9arFQM31kvrTiypqeBxeP6JfmvDOX1uhPPqkKmWOnRuoUP2bv9BFAu0Ygd1BDJgIq10-3_94r09ogelxRICO7AlWfrjgzKT-bT-PWvVLIlAhlz9Yly6zgcbpSepQk0nuSl8ou9WH2ttN6yGj9JRiBbhyUFfHT9f3T3o5MKs_jmpNLB8Icn9bVFSEB-IcNN2A5hqyrys4ZChV_YX7kHBvf0HHhJdmw-0Zh8m6Stdp6J5o28f7rhIbjJLcldmcKGoAfrGTIYjIqiczoSUsgi3LExxemwkw4TWO4fkeFJ56TXhQRKxYenhYo-DmW3d9a5748KQkq7sj_odYeD9HRUiJ4gokE6HB6K36DDiphcPLsyQeao47syRUF80RQFuaC-ixWHhT0S-5fRM2znDdcNX1rxMuba2kVTRx1fBVNFUiHTpRVN4HmG7cv4XWBuGyfoZ2ebeobtjCrrVq-cdIbthbZioUwZNnKL-d1j-VqLN84-qHvFO_SMXElzM7OmtPnTcj6vcy7lnc2Jv7ePnPidMtI-ToP6_fd2NA0zDPs1toad1Vv9Cxpr9F6JiSmVoTBzu4As3fwD).

## Задача 2

E — `service`, `level`; S — `ts`; R — `duration_ms`.

```javascript
db.events.createIndex({ service: 1, level: 1, ts: -1, duration_ms: 1 })
```

Документов просмотрено в 36,36 раза меньше (1200 / 33). `SORT` исчез, потому что индекс уже даёт нужный порядок по `ts`.

[Разбор плана с индексом](https://dfrancour.dev/tools/mongodb-paste-the-plan#v1:7VZLc9s4DP4rGUwPe2AzUmzHiW7xa5vJunardB-TZjwICTlsJFIhKUduxv99h5Sf2d2kx92ZPUkEARAf-AHgM1Bd5ijVr2Ss1AoSiIHBY0VmOc1RKTKQPIPCgmyJnCCBXM_tMS1IOQsMpBJUj2TuyKTkIMkwt8SgRGNJfPJuvP07VAKSm2fIaUF5kNAjJEDGaAOrFXsGS2Yh_QGbvRKXRTgkbIvKoJNazQobVOYOkk4UrVa3q3W4H9DeQwL9XtzuDM8GwKDMUfWR39MVLSGBwagXx_GwBwx06WQhvweP17KgscxzaSGJGBRYX3pMJCYm1XnlVexn8m7EFt5O6UKJ17RSjspe62Fd5lrQS4UnqZRUc59oD8o6nPsMj4bX_Q8ht2Xl0ka42738Pe1ffAQGD7SconNkGuNN_mK2yXLMwFlI3sfsMH3xan1vH7HwHtems3gWDGfxzNnZ-3i2ZzTzrJB2XOVOhmxuIK4FU3T39iCMm9ttHP7XB-K_B4Hc-MuT9ouSjxVtfUqbBvrsCaZonMR8J_HRbyl7wkBIQ9w1BM60eUIjNuTs6UqJF7HBzdctv74CO9pf3cJe5F4xkLTRWv8GlYAIbsZYX9GSHY2luqJl2DnECD91oogdSZUdR7dwu1qtGBj6RtyR8De_yQPVxAOPUocuxLuTVJyTtZA4UxED9ZlcZZQnUqu1Z7jPZH_32mF-RUs7rLGQQb3dWosHmu-JD7wEwtm_4-Pb5w6tkwU6CpX0pM2Dbc5EsUDFN4aKSHgbSM6bxR-SchFsLC7I4288GLJOmz2BtMPJKIATfwGAuSEUvg1M7r412q_Xz78Jzv-1_J-s5XBxL-rLEnmexJE3Lu01WUcNG_xyYHRZhnVoBFwXRZiNz5BJ_4XtZM3CUD3AupuJW1TrEcr-eUAysNo4L2sItGLwTtytBzn4bTILMpcq017pXlsHCZyeZ1l0cs4FF5kfpcHFSTeKuwwW27dC9zg6breAwVy63QuCsg52Rat9Ft11zjNCiluic9pudU_jk_OMtzkRncbd7u7wKRosyJEJsUvlCwHz8HwYISfXq7KMTCq_U2_pKGS3fdbpnkahyl9qj7GeVK6s3EDz121-0fqhKkOLuPSigoRERwPNK5_nMdav228UU10ZTj8bXZVjrMdUaLN8I9Ix1r1c8wep5qk2rrH5YnH-FsSp0ffyTrqN9ZjMnCZqrNVcp-u-d3jOhRDXOiX3ozhScr9JJfTTyDcy-6OIRv4OfZfsa-WMzpvy5dTP0VrJh2ouFfk71w--b_0J).

## Задача 3

Вариант А (R–E–S) просмотрел 378 ключей: диапазон стоит первым и захватывает события разных сервисов и уровней.

В варианте Б (E–R–S) остался `SORT`, потому что диапазон `duration_ms` стоит перед полем сортировки `ts`.

Оставил бы индекс ESR из задачи 2: он сокращает чтение и сразу даёт нужную сортировку.

## Задача 4

E — `level`, S — `duration_ms`. Диапазона нет.

```javascript
db.events.createIndex({ level: 1, duration_ms: -1 })
```

Из 180 ошибок сервер прочитал только 10: индекс отдаёт самые долгие первыми, а `limit(10)` останавливает чтение.

[Разбор второго запроса с индексом](https://dfrancour.dev/tools/mongodb-paste-the-plan#v1:7VXJcts4EP2VVFeOjEvUavNmWdJE5TBSQmWWclSuNtCUEYMADYAylZT-fQqQtUSesTPLYQ5zktB8jV7eQ_c3oLqUKNTPZKzQChKIIYL7isxqKlEpMpB8A4UF2RIZQQJSL-wJLUk5CxEIxakeCenIZOQgyVFaiqBEY4l_8Nd4f0lLkv7Pa7qHBMgYbWC9fgz0Fu0tJNAZNrutdmcIEZQS1QWyW7qkFSTQbw0H_dPuACLQpROF-IpOaDUTBaVCSmEhaURQYD322RCfmEzLykPsR_LX8F1ie9C54s-hMobKzvSwLqXmdAx4EEoJtfAt8mVZhwvfm3fjdDyDCKQohDsvdKUcJHHDt6msXLZB7eGj4eziLfzZ1_Gv2cX5e4jgjlZTdI6MOuhlHAGvTOjDdWEheROvH9l4j0XgyeOu4-sD1PUbT66waSWdCK3d1vtomKK7tQdBruZHUa7mPor9pMR9RTt3YbNA-IFhisYJlHuLz2wnsmYEXBhibiO5XJsHNHwrp76uFP8uDbj6vBHNZ4he7f7O4Ul6cJVifUmr6FUq1CWt5jBfr73QDH0h5oh7xrZ1UE0s8J85dCHe3lIxRtZC4kxFEaiP5CqjvAA8mzvYkQKddigvaWWHNRZiBw_mgWZH5sPwC7J_pKOX4w6tEwU6CvEftLmzkMRxBMiXqNjWURFx7xNQ_vCbIMnDyeKSfP2bb4as0-bAIOxwMgpq-4ua_pupN_711BsR8Ce9R2kIuZ88k5svG_Tzb_C_VM7_8-AfzYPQwCM9WKLAl_cv7Yysow0p_jgwuizDeTNLmC4KVNwnlAv_C7t1mIdNeJDqdtdFYLVx_sNTlsLL2uTxmt88rtjgQmZJZqxy7R1vtXWQQPcszxvNM8YZz_2qDNc2e424F8Fyt8V7J42TdgsiWAi33-2Ud7DHW-3Txk3nLCekuMU73Xar142bZzlrMyLqxr3ePvgUDRbkyIT-C-VVhzIs9hEycv0qz8lk4iv1V46C5NunnV63EZ7UMTrFelK5snIDzZ73eaf1XVWG9zj2poK4QEcDzaqClL_oef8tMNOVYfST0VWZYp1Soc3qhUxTrPtSszuhFpk2buPzyeLipRKnRt-KG-G23imZBU1UqtVCZ49D5vs455zPdEbuR-vIyP0iFNcPIz817I9WNPIc-pF0oZUzWm6eGKMLidYKNlQLochzru8gide_Aw).

MongoDB 7.0.43, `logs.events` — 1200 записей. Скрипт выгрузки — `plan.py`. Планы без индекса и с ESR дополнительно сверены в MongoPilot.
