# QRKot

![parser_workflow](https://github.com/kapkaevandrey/cat_charity_fund/actions/workflows/test_workflow.yml/badge.svg)

### _Описание проекта_
> ***Лу́ис Уи́льям Уэ́йн***
>>Я попытался раз и навсегда избавиться от презрения, 
> с которым кошек держали у нас в стране. Я повысил их статус с сомнительной забавы и 
> развлечения для старых дев до постоянного спутника жизни со своим местом в доме. 
> В результате многолетних исследований я обнаружил, что все люди, 
> которые держат дома кошек и ухаживают за ними, не страдают от мелких недугов, 
> которым подвержена всякая плоть. Они свободны от разного рода нервных расстройств. 
> Истерия и ревматизм им тоже неведомы. 
> Все любители кошечек — очень милые люди по свой сути.
>>
Сервис для сбора средств на реализацию различных проектов для наших милых котиков.

### _Технологии_
 - __[Python 3.10.1](https://docs.python.org/3/)__
 - __[Fast API 0.73](https://fastapi.tiangolo.com/)__
 - __[FastAPI Users 9.3](https://fastapi-users.github.io/fastapi-users/9.3/)__
 - __[SQLAlchemy 1.4.37](https://www.sqlalchemy.org/)__
 - __[Alembic 1.8.0](https://alembic.sqlalchemy.org/en/latest/)__
 - __[Pydantic 1.9.0](https://alembic.sqlalchemy.org/en/latest/)__
 - __[Uvicron 0.17.6](https://www.uvicorn.org/)__

## _Как запустить проект_:
________________________________________

Клонировать репозиторий и перейти в него в командной строке:

```bash
https://github.com/kapkaevandrey/cat_charity_fund.git
```

```bash
cd cat_charity_fund
```

Cоздать и активировать виртуальное окружение:

```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```

Установить зависимости из файла requirements.txt:

```bash
python3 -m pip install --upgrade pip
```

```bash
python3 pip install -r requirments.txt
```
☑️**_Примечание_**: если вы используете Windows то библиотека **[uvloop](https://uvloop.readthedocs.io/)** не установиться.
Вы можете установить её, используя систему **[WSL](https://docs.microsoft.com/en-us/windows/wsl/install)**.

Заполните файл .env, предварительно создав его в главной директории проекта.
Пример заполнения
```
APP_TITLE=QRKot                                 <----название приложения
DESCRIPTION=application for                     <----описание приложения
DATABASE_URL=sqlite+aiosqlite:///./fastapi.db   <---данные для подключения к БД
FIRST_SUPERUSER_EMAIL=king.arthur@camelot.bt    <---emai суперюзера который будет создан при первой инициалзации БД
FIRST_SUPERUSER_PASSWORD=guinevere              <---password суперюзера который будет создан при первой инициалзации БД
```

Выполните миграции Alembic
```shell
alembic upgrade head
```
Запустите приложение
```shell
uvicorn app.main:app
```

### _Описание работы сервиса и пользовательские роли_:
__________________________________________
Сервис позволяет создавать проекты направленные на улучшение жизни кошек. Сервис также принимает пожертвования от зарегистрированных
пользователей которые автоматически распределяются между проектами. Распределение происходит по принципу ~~"кто первый тому и тапки"~~
не до конца инвестированный проект, созданный ранее остальных, получает деньги первым.
В случае отсутствия актуальных проектов все пожертвования хранятся в фонде и распределятся также от самого раннего к самому позднему
при появлении новых проектов. Пожертвования могут быть потрачены как полностью, так и частично.
_______________________________________________________
### _Пользовательские роли в сервисе_:
1. **Аноним :alien:**
2. **Аутентифицированный пользователь :sunglasses:**
3. **Администратор (superuser) :innocent:**

**Анонимные:alien:** пользователи могут:
Просматривать все проекты которые сейчас есть.

**Аутентифицированные: sunglasses:** пользователи могут:
1. Получать данные о **своей** учётной записи;
2. Просматривать сделанные пожертвования;
3. Редактировать информацию о себе;
4. Создавать пожертвования;

☑️***Примечание***: Доступ ко всем операциям доступны только после аутентификации и получения токена.

**Администратор (superuser)  :innocent:** может:
1. Редактировать данные других пользователей;
2. Получать информацию о каждом пользователе;
3. Создавать проекты;
4. Удалять проекты в которые не внесены деньги;
5. Редактировать проекты;
6. Просматривать все пожертвования.

### _Примеры запросов_:
_________________________________
Здесь могли быть примеры запросов, но они гораздо лучше описаны в сгенерированной документации. 

[host/docs]() - Swagger 

[host/redoc]() - Redoc

При локальном запуске http://127.0.0.1:8000/docs



________________________________

### Автор проекта:
#### Андрей ***Lucky*** Капкаев
>*Улыбайтесь - это всех раздражает :relaxed:.*