# Используем официальный образ PostgreSQL с поддержкой PostGIS
FROM postgis/postgis:15-3.3

# Устанавливаем переменные окружения для пользователя и пароля
ENV POSTGRES_USER=admin1
ENV POSTGRES_PASSWORD=admin
ENV POSTGRES_DB=cdn

# Копируем SQL-скрипт в контейнер
COPY init.sql /docker-entrypoint-initdb.d/

# expose порт
EXPOSE 5432
