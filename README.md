# foodgram-project
![api_yamdb](https://github.com/alexfofanov/yamdb_final/workflows/api_yamdb_workflow/badge.svg)

Это онлайн-сервис, где пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## Установка и запуск

### Установите docker и docker-compose
Проверьте установлен ли docker и docker-compose

    docker -v
    docker-compose -v

В случае отсутствия установите согласно документации по установке [docker](https://docs.docker.com/engine/install/) и [docker-compose](https://docs.docker.com/compose/install/) на официальном сайте.


### Создайте файл .env с переменными окружения для работы с БД в корне приложения и добавьте в него следующие параметры:

    DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
    DB_NAME=postgres # имя базы данных
    POSTGRES_USER=postgres # логин для подключения к базе данных
    POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
    DB_HOST=db # название сервиса (контейнера)
    DB_PORT=5432 # порт для подключения к БД

### Запустите docker-compose
    docker-compose up -d

### Выплните миграцию
    docker-compose exec web python manage.py migrate

### Для загрузки исходных данных используйте команды
    docker-compose exec web python manage.py collectstatic
    docker-compose exec web python manage.py load_ingredients
    docker-compose exec web python manage.py load_tags

### Создайте суперпользователя Django
    docker-compose run web python manage.py createsuperuser
Сервис доступен по адресу http://localhost:8000

### Для остановки и удаления сервиса используйте команду
    docker-compose down
