# Проектное задание: Сервис авторизации

## Запуск

Запустить все сервисы разом можно следующей командой:

```bash
COMPOSE_PROFILES=infra,etl,movies-api,movies-admin docker-compose -f docker-compose.yml -f docker-compose.override.yml up -d
```

Для остановки выполнить:

```bash
COMPOSE_PROFILES=infra,etl,movies-api,movies-admin docker-compose -f docker-compose.yml -f docker-compose.override.yml down
```

## Запуск (Production)

Запустить все сервисы разом можно следующей командой:

```bash
COMPOSE_PROFILES=infra,etl,movies-api docker-compose up -d
```

Для остановки выполнить:

```bash
COMPOSE_PROFILES=infra,etl,movies-api docker-compose down
```

## Сервисы

| Название сервиса     | Внешний адрес (localhost)                            | Внутренний адрес (docker network)                          |
|----------------------|------------------------------------------------------|------------------------------------------------------------|
| Movies API           | http://127.0.0.1:8000/api/docs                       | http://movies-api:8000/api/docs                            |
| Movies API (Nginx)   | http://127.0.0.1:7000/api/docs                       | http://movies-api-nginx/api/docs                           |
| Movies PostgreSQL    | postgres://app:123qwe@localhost:5432/movies_database | postgres://app:123qwe@movies-postgres:5432/movies_database |
| Movies Redis         | redis://localhost:6379                               | redis://movies-redis:6379                                  |
| Movies Admin         | http://127.0.0.1:8001/admin                          | http://movies-admin:8000/admin                             |
| Movies Admin (Nginx) | http://127.0.0.1:7001/admin                          | http://movies-admin-nginx:80/admin                         |
