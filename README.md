# QRKot

### Технологии
Python, FastApi, SQLAlchemy, Aiogoogle

## Описание

Фонд для сбора пожертвований на различные целевые проекты: на медицинское обслуживание нуждающихся хвостатых, на обустройство кошачьей колонии в подвале, на корм оставшимся без попечения кошкам — на любые цели, связанные с поддержкой кошачьей популяции.

Каждый пользователь может сделать пожертвование и сопроводить его комментарием. Пожертвования не целевые: они вносятся в фонд, а не в конкретный проект. Каждое полученное пожертвование автоматически добавляется в первый открытый проект, который ещё не набрал нужную сумму. Если пожертвование больше нужной суммы или же в Фонде нет открытых проектов — оставшиеся деньги ждут открытия следующего проекта. При создании нового проекта все неинвестированные пожертвования автоматически вкладываются в новый проект.

## Данные для тестирования

```bash
Пользователь с праввами администратора:
Логин: admin@admin.admin
Пароль: admin

Пользователь:
Логин: user@user.user
Пароль: user
```

## Запуск проекта

Клонировать репозиторий и перейти в него в командной строке:

```bash
git clone 
```

```bash
cd cat_charity_fund
```

Cоздать и активировать виртуальное окружение:

```bash
python3 -m venv venv
```

- Если у вас Linux/macOS

    ```bash
    source venv/bin/activate
    ```

- Если у вас windows

    ```bash
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```bash
python3 -m pip install --upgrade pip
```

```bash
pip install -r requirements.txt
```

Запуск тестового сервера:

```bash
uvicorn app.main:app --reload
```

## Спецификация проекта

<http://127.0.0.1:8000/docs>

<http://127.0.0.1:8000/redoc>

## Автор

[Genek91](https://github.com/Genek91)
