# memes_api
CRUD-операции для приложения с мемами. Включает два сервиса - публичный API с CRUD-операциями и сервис для интеграции с S3.
Сервисы Postgre, S3 и два сервиса API объединены в docker-compose.

# запуск приложения

```bash
   docker compose up
   ```
Можно установить параметр -d для того, чтобы контейнеры работали в фоновом режиме и не показывали логи