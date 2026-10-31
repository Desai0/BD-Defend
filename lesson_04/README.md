# Домашнее задание № 4 · План запроса и индексы

Колобов Евгений Денисович · 9РПО1 · 31.10.2026

MongoDB 7.0.43, `logs.events` — 1200 документов.

| План | Индекс | nReturned | totalDocsExamined | totalKeysExamined | Шаги снизу вверх |
|---|---|---|---|---|---|
| [plan-1.json](plan-1.json) | Только `_id_` | 33 | 1200 | 0 | COLLSCAN → SORT |
| [plan-2.json](plan-2.json) | `{"service": 1, "level": 1, "ts": -1, "duration_ms": 1}` | 33 | 33 | 43 | IXSCAN → FETCH |
| [plan-3a.json](plan-3a.json) | `{"duration_ms": 1, "service": 1, "level": 1, "ts": -1}` | 33 | 33 | 378 | IXSCAN → SORT → FETCH |
| [plan-3b.json](plan-3b.json) | `{"service": 1, "level": 1, "duration_ms": 1, "ts": -1}` | 33 | 33 | 33 | IXSCAN → SORT → FETCH |
| [plan-4-bez.json](plan-4-bez.json) | Только `_id_` | 10 | 1200 | 0 | COLLSCAN → SORT |
| [plan-4.json](plan-4.json) | `{"level": 1, "duration_ms": -1}` | 10 | 10 | 10 | IXSCAN → FETCH → LIMIT |

## Задача 1

```javascript
db.events.find({service: "payments", level: "error", duration_ms: {$gt: 500}}).sort({ts: -1})
```

Найдено 33 записи. Подходящего индекса нет, поэтому сервер проверил все 1200 документов и отсортировал результат в памяти. Разбор в MongoPilot подтвердил полный перебор и сортировку в памяти.

[Разбор без индекса](https://dfrancour.dev/tools/mongodb-paste-the-plan#v1:zVXbbiM3DP0XYh-nwUx8zbwljt0GG9dpJu1isSgKRuJMVGukWUnj2Gv43wvK8SV7SRZboOiTxyQPKR4eSmugZaNRmT_IeWUN5JBBAh9bcqsbjcaQg3wNBmvyDQqCHLSt_AktyAQPCSgjaTlROpArKEBeovaUQIPOk_yN0zD-DRoJ-Yc1aFqQjhb6CDmQc9bBZpOswZNbKC6w8zW4qmOR6Jatw6Cs-av2MaQKkPfSdLP5c_N03F_QP0AOo4us2xsPLyGBRqMZoXigt7R67rFNULX6FDPeqZqmSmvlIU8TqHF5xT2RnLnC6pZD_C1xGrlv7xB0buRLUYVA4-_seNloK-nzgEdljDIVE81N-YAVM1zMbu8gAW9duMEQyEVv8JD_lG0SqKm-VrUKkGdpd9gb9NM0gbBqGOpV3WiKc2naUGwTHjKPZtfXxej8V0igjDP7D4YjlSPBXsihtO4RnWQUOPqbRCDJ3XvIP3AsLUlELouA3O_6yNIKQd5DHlxLCZhbCq0zTGancwT8bJrBBtRvaeXHS6xVDN9ZL604smanzOJx_Yr8V4byet2xD6rGQLHSo3Vzz9k7vQRQLtCIHdQQSUbF2tn2_3tFentEjwtiEtjNXPlg3ZFB-fFsEr_-lUq2RGDAQn2iwrrAhzvLhlkCrSd5qfx8L1bfKK23rMZPkhEYrMOKGB9d_x_d_eikeBbfnFTWH_zwpL62CAnIL2S44e0Qtq4jP2soFf_C_so9MLin58BLsmPzicbk2yRttfNMNG_k_dMND-wmtyB3ZUrLQQ_WB8ihg9gd9lD001LwHRtTnA7SbJDAYv-IDE7Sk24HEqhUODwtVPZwIDvdYXrfOysJKevIXr_bGfSz07NSdAUR9bPB4FD8Bh3WFMjFsyvDMkcd35UJCgoXbVmSY_VdrAIv7JHYv4ye4nLWhqYNl1a8jLm2dt42UcdXbKpJKgx0aUXLPE9x-TJ-F1jY1gn62dm2meJySrV1q1dOOsXlhbZirkzFG7nF_O6xeq3FG2cf1L0KO_SUXEUzM7WmssXTcj6vcy7lnS0ofG8fBYV3ykj7OGH1--_taMIz5P0aWROcZXGW1gkaafReibGplCGeuZ1Dnp2km38A).

## Задача 2

E — `service`, `level`; S — `ts`; R — `duration_ms`.

```javascript
db.events.createIndex({service: 1, level: 1, ts: -1, duration_ms: 1})
```

Просмотрено 33 документа вместо 1200 — в 36,36 раза меньше. `SORT` исчез: индекс уже задаёт порядок по `ts` для выбранных сервиса и уровня. В MongoPilot также получены 33 документа и 43 ключа, полный перебор отсутствует.

[Разбор с ESR](https://dfrancour.dev/tools/mongodb-paste-the-plan#v1:7VZLc9s2EP4rnp0cekA8pCVZNm_Wq_G4ipXQ6WMcj2YNLGXEJEADoExFw__eAfR2WzvHdqYnEov99oUPu1gC1WWOUv1KxkqtIIEYGDxVZBaTHJUiA8kSFBZkS-QECeR6Zo9pTspZYCCVoHokc0cmJQdJhrklBiUaS-KTN-Px71AJSG6XkNOc8iChJ0iAjNEGmoYtwZKZS-9gs1fioghOwraoDDqp1bSwQWXmIOlEUdPcNetwP6B9gAT6vbjdGZ4NgEGZo-ojf6ArWkACg1EvjuNhDxjo0slCfg8Wb2RBY5nn0kISMSiwvvQ5kbg2qc4rr2I_kzcjtuntlC6UeE0r5ajsjR7WZa4FvVR4lkpJNfOF9klZhzNf4dHwpv8h1LasXLoS7nYvf0_7Fx-BwSMtJugcmRV4U7-YbaocM3AWkvcxOyxf3KzP7SMW3uIaOo2nATiNp85O38fTPdDUs0LacZU7Gaq5SXEtmKB7sAdh3N5t4_C_PhD_PQjk1h-etF-UfKpoa1PaNNBnTzBB4yTmO4mPfkvZEwZCGuLeLiSQafOMRmzI2dOVEi9ig9uvW359BXa0v7qDvci9YiDpSmv9G1RCRnA7xvqKFuxoLNUVLcLOYY7wUyeK2JFU2XF0B3dN0zAw9I24I-FPflMHqokHHqUOve3lnqTinKyFxJmKGKjP5CqjPJFarT3gCyY77TC_ooUd1ljIoN5urcUDzffEB1YC4ezf8fFtv0PrZIGOgv9nbR7tyieKOSq-ASoi4TGQnK8Wf0jKRcBYnJPPf2XBkHXa7AmkHV6PArHFXxLA3BAK3wau77-ttF-_P_-mdP6_y__JuxwO7sX9skSeJ3HkwaW9Iev81no5MLoswzo0Aq6LIszGJWTSf2E7WbMwVA9y3c3EbVbrEcr-eUAysNo4L1sRqGHwTtyvBzn4bTJzMpcq017pQVsHCbQQ22cd5KdRxv0oDSZOulHcZTDfvhW6x9FxuwUMZtLtXhCUdbArWu2z6L5znhFS3BKd03arexqfnGe8zYnoNO52d84naLAgRybELpW_CJiH58MIOblelWVkUvmdegvnm1Mctc863dMo3PKX2mOsrytXVm6g-euYX7R-rMrQIi69qCAh0dFA88rXeYz16_iNYqorw-lno6tyjPWYCm0Wb0Q6xrqXa_4o1SzVxq0wXyzO3kpxYvSDvJdugx6TmdG1Gms10-m67x36uRDiRqfkfjSPlNxvUgn9PPKNzP5oRiN_hr5L9rVyRntyZtpw6udoreRDNZOK_JnrR0ji46j5Ew).

## Задача 3

Вариант А (R–E–S) просмотрел 378 ключей: диапазон стоит первым и захватывает события всех сервисов и уровней.

В варианте Б (E–R–S) просмотрено 33 ключа, но остался `SORT`: диапазон `duration_ms` стоит перед `ts`, поэтому общего порядка по времени нет.

Оставил бы ESR из задачи 2: он сокращает чтение и не требует отдельной сортировки.

## Задача 4

```javascript
db.events.find({level: "error"}).sort({duration_ms: -1}).limit(10)
db.events.createIndex({level: 1, duration_ms: -1})
```

E — `level`, S — `duration_ms`, диапазона нет. Сначала отбираются ошибки, затем они идут по длительности от большей к меньшей.

Без индекса прочитано 1200 документов, с индексом — 10 документов и 10 ключей. Всего ошибок 180, но индекс сразу отдаёт самые долгие, а `limit(10)` останавливает чтение после десятой.

[Разбор второго запроса с индексом](https://dfrancour.dev/tools/mongodb-paste-the-plan#v1:7VXJcts4EP2VVFeOjIu0Noc3a5uoHMZKqEwy5bhcbaApIQYBGgBlKSn9-xSgNfKMnVkOc5gTicbr_aH7O9CikijUr2Ss0ApSSCCC-5rMcixRKTKQfgeFJdkKGUEKUk_tCc1JOQsRCMVpMRTSkcnJQVqgtBRBhcYSf-_NeH1Jc5L-5yXdQwpkjDawWm0cvUE7gxRag9N2o9kaQASVRNVDNqMLWkIK3cag3z1r9yECXTlRim_ohFYTUVImpBQW0jiCEhcjHw3xS5NrWXuI_UDeDN8FtgedK_4UKmeo7EQPFpXUnI4BD0Ipoaa-RD4t63Dqa_N2lI0mEIEUpXDnpa6VgzSJfZmq2uVr1B4-HEx6b-DPbkef8975O4jgjpZjdI6MOqhlEgGvTajDTWkhfZWsNt14h2Xok8fdJDcHqJtXvrnCZrV0IpR2m-9GMEY3swdOrq6PvFxdey_2oxL3Ne3Uhc1Dww8EYzROoNxLfGQ7kp1GwIUh5u1CCoU2D2j4lk5dXSv-Qxhw9WVNmi8Qvdj9XsOj8OAqw8UFLaMXmVAXtLyG69XKE83QV2KOuO_YNg9aEAv9zx264G8vqRkjayF1pqYI1AdytVGeAL6bO9gRA512KC9oaQcLLMUOHsR9zY7Eh-6nZP-IR8_7HVgnSnQU_D9oc2chTZIIkM9Rsa2iIuJeJ6D84TdBkoeTxTn5_Nd3hqzT5kAg7OByGNj2Fzn9N0OP__XQ4wj4o9qjNITcT57L269r9NNv8L-Uzv_z4B_Ng1DAIz5YotAvr1_ZCVnnbzx16sr2ja6qcF7PEqbLEhX3ARXCf2G3DouwCQ9C3e66CKw2zl887lJ4Wes4XvLbzYoNKmTmZEaq0F5xpq2DFBqIzbMWsnZcML8qg9nTTpx0IpjvtnjnJD5pNiCCqXD73U5FCzu80TyLb1uvC0JKGrzVbjY67eT0dcGajIjaSaezdz5GgyU5MqH-QnnWoQyLfYiMXLcuCjK5-EbdpfNDLImbZ61OOw5P6hid4eKydlXt-po9rfNW67u6Cu9x5EUlcYGO-prVJSlv6Gn9LTDXtWH0i9F1leEio1Kb5TORZrjoSs3uhJrm2ri1zkeL0-dSHBs9E7fCbbUzMlO6VJlWU51vhsyPfs45n-ic3M_mkZP7JBTXD0M_NezPZjT0PfQjqaeVM9rTstCGUU-itYIN1FQo8j3Xd5AmJ_Hqdw).
