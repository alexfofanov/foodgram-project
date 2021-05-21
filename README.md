# foodgram-project
![foodgram-project](https://github.com/alexfofanov/foodgram-project/workflows/foodgram_workflow/badge.svg)

Это онлайн-сервис, где пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## Установка и запуск на примере Linux

### Установите docker и docker-compose
Проверьте установлен ли docker и docker-compose

    docker -v
    docker-compose -v

В случае отсутствия установите согласно документации по установке [docker](https://docs.docker.com/engine/install/) и [docker-compose](https://docs.docker.com/compose/install/) на официальном сайте.

### Клонировать с помощью git ###

git clone https://github.com/alexfofanov/foodgram-project.git

### Создайте файл .env с переменными окружения в корне приложения и добавьте в него следующие параметры:

    SECRET_KEY=pR(vp1)y(m0h2e86c01lm+$-72i#na)*i4e3$3@663re&_wx%4 # секретный ключ Django (установите свой)
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
Сервис доступен по адресу: http://localhost

### Для остановки и удаления сервиса используйте команду
    docker-compose down

### Технологии    
+ Python3  
+ Django
+ PostgreSQL
+ Gunicorn
+ Nginx
+ Docker
+ Docker Compose
+ GitHub Actions
