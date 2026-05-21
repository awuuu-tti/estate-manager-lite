# EstateManager Lite

Учебный Django-проект для лабораторной работы №2: базовый сайт агентства недвижимости.

## Что уже есть

- каталог объектов недвижимости;
- фильтрация по типу сделки и цене;
- карточка объекта;
- форма заявки на просмотр;
- админ-панель Django;
- экспорт заявок в CSV;
- базовая структура проекта, `.gitignore`, README.
- Административная панель защищена логином и паролем Django.

## Как запустить

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Откройте сайт: http://127.0.0.1:8000/

Админ-панель: http://127.0.0.1:8000/admin/

Экспорт CSV доступен только администратору: http://127.0.0.1:8000/admin/export-requests/

## Что нужно доделать самостоятельно для защиты

1. Создать репозиторий GitHub и загрузить проект.
2. Сделать минимум две ветки: `main` и, например, `feature/user-authentication`.
3. Добавить 3–5 тестовых объектов через админ-панель.
4. Сделать скриншоты: каталог, карточка, админ-панель, CSV-файл.
5. При желании добавить фильтр отчета по датам.

## Пример команд Git

```bash
git init
git add .
git commit -m "Initial commit: project structure"
git branch -M main
git remote add origin https://github.com/username/estate-manager-lite.git
git push -u origin main

git checkout -b feature/viewing-requests
git add .
git commit -m "Add viewing request form"
git checkout main
git merge feature/viewing-requests
git push origin main
```
## CI/CD с GitHub Actions

В этом проекте настроены следующие автоматические проверки:

| Workflow | Статус |
|----------|--------|
| Тесты с покрытием | [![Test](https://github.com/Дарья Майорова/EstateManager/actions/workflows/test.yml/badge.svg)](https://github.com/Дарья Майорова/EstateManager/actions/workflows/test.yml) |
| Качество кода (линтер) | [![Lint](https://github.com/Дарья Майорова/EаstateManager/actions/workflows/lint.yml/badge.svg)](https://github.com/Дарья Майорова/EstateManager/actions/workflows/lint.yml) |
| Имитация деплоя | [![Deploy](https://github.com/Дарья Майорова/EstateManager/actions/workflows/deploy.yml/badge.svg)](https://github.com/Дарья Майорова/EstateManager/actions/workflows/deploy.yml) |

**Что они делают:**
- **Тесты** — запускают `coverage run manage.py test`, требуют покрытия ≥90%
- **Линтер** — проверяют стиль кода и наличие немигрированных изменений
- **Деплой** — имитируют развёртывание (миграции + статика)