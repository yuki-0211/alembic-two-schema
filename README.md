# alembic-two-schema

I want to create two schemas (inner schema and outer schema) in one DB(postgresql) and create foreign keys between schemas using alembic.

## Setting

You need to create a .env file to root directory

```.env example
DATABASE=postgresql+asyncpg
DB_USER=user
PASSWORD=user
SECRET_KEY=user
HOST=db
PORT=5432
DB_NAME=verification_db
MIN_CONNECTIONS_COUNT=10
MAX_CONNECTIONS_COUNT=10
INNER_DB_SCHEMA=inner
OUTER_DB_SCHEMA=outer

```


## Build


- Build A DB Container And Two Migration Container(Inner And Outer)

```
docker-compose up
```

- Enter the Inner Container

```
docker-compose exec inner bash
```

- Enter the Outer Container

```
docker-compose exec outer bash
```

## Migration

- Generate DB management file

```
alembic -c app/db/migration/alembic.ini revision --autogenerate -m "your comment"
```

- Update DB

```
alembic -c app/db/migration/alembic.ini upgrade head
```