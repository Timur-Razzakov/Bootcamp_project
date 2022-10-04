# Nexign_bootcamp_project
## Описание проекта

Сервис по Рассылке нотификаций для стажировки в Nexign

### Стек технологий

- Django
- schedule
- PostgresSQL
- Jinja2
- RabbitMQ
---

### Установка
Перед запуском проекта убедитесь, что у вас установлен python, docker и docker-compose.

```bash
python --version
```

```
docker --version
```

```
docker-compose --version
```
Установливаем зависимости.

```
pip install -r requirements.txt
```

Выполним миграции

```
python manage.py migrate
```

Загрузка Данных из Json файла

```
python manage.py loaddata  dumped_data.json
```

Создаём .env файл и добавляем следующие настройки

- Настройки сервера
  - `SERVER_HOST=`... (поумолчанию 0.0.0.0)
  - `SERVER_PORT=`... (поумолчанию 8000)
  
- Настройки базы данных 
  - `POSTGRES_HOST=`... (поумолчанию 0.0.0.0)
  - `POSTGRES_PORT=`... (поумолчанию 5432)
  - `POSTGRES_DB=`... (обязательное поле)
  - `POSTGRES_USER=`... (обязательное поле)
  - `POSTGRES_PASSWORD=`... (обязательное поле)
 
- Настройка Email 
  - `EMAIL_HOST=`... (поумолчанию smtp.gmail.com)
  - `EMAIL_PORT=`... (поумолчанию 587)
  - `EMAIL_HOST_USER=`... (обязательное поле)
  - `EMAIL_HOST_PASSWORD=`... (обязательное поле)
  
- Секретный ключ
  - `SECRET_KEY=`... (обязательное поле)
  
Запускаем проект на компьютере

```
python manage.py runserver 127.0.0.1:8800
```

Запускаем проект в docker (но для этого обязательно укажите в вашем env-файле: **POSTGRES_HOST=db**)

```
docker-compose up
```
Запуск скрипта, для заполнения формы "Result". Перейдите в директорию "cd result_create" 

```
python get_result.py
```

Запуск скриптов, для отправки по телеграмму и по почте.  Перейдите в директорию "cd sending_notifications"

```
python send_email.py
```

```
python send_to_tg.py
```

---
