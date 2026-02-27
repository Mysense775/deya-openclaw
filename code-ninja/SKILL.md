---
name: code-ninja
description: Architecture analysis, debugging, and code refactoring assistant. Use when you need to analyze code structure, find root cause of bugs, suggest refactoring, or switch between programming languages. Includes tools for architecture analysis, debug detection, refactoring suggestions, and multi-language translation.
triggers:
  - "проанализируй код"
  - "найди баг"
  - "почему ошибка"
  - "рефакторинг"
  - "улучши код"
  - "python на javascript"
  - "структура проекта"
  - "циклический импорт"
  - "traceback"
---

# Code-Ninja 🥷

Инструменты для анализа архитектуры, отладки и рефакторинга кода.

## Быстрый старт

### Анализ архитектуры проекта

```bash
python scripts/architecture-analyzer.py /path/to/project

# Пример для AI Router
python scripts/architecture-analyzer.py /root/.openclaw/workspace/ai-router-platform/backend
```

Находит:
- Циклические импорты
- Слишком большие файлы (>500 строк)
- Высокую цикломатическую сложность
- Архитектурные "запахи"

### Детектив отладки

```bash
# Из файла с traceback
python scripts/debug-detective.py --traceback error.log

# Из текста
python scripts/debug-detective.py --text "Traceback (most recent call last): ..."

# С показом контекста кода
python scripts/debug-detective.py --traceback error.log --show-context
```

Анализирует ошибки и предлагает решения из базы знаний.

### Рекомендации по рефакторингу

```bash
# Анализ одного файла
python scripts/refactor-suggest.py /path/to/file.py

# Анализ всего проекта
python scripts/refactor-suggest.py /path/to/project --full
```

Ищет:
- Длинные функции (>50 строк)
- Глубокую вложенность (>3 уровня)
- Магические числа
- Голые except:
- print вместо logger
- И другие проблемы

### Переключение языков

```bash
# Показать паттерн на всех языках
python scripts/multi-lang-switch.py class

# Перевести с Python на Go
python scripts/multi-lang-switch.py list_comprehension --from python --to go

# Список всех паттернов
python scripts/multi-lang-switch.py --list
```

## Рабочий процесс

### 1. Есть баг — непонятно почему

```bash
# Получаем traceback из логов
docker logs container 2>&1 | tail -100 > error.log

# Анализируем
python scripts/debug-detective.py --traceback error.log --show-context
```

Вывод:
- Тип ошибки и описание
- Где в коде проблема
- Конкретное решение

### 2. Проект растёт — боюсь mess

```bash
# Анализируем архитектуру
python scripts/architecture-analyzer.py ./backend

# Получаем отчёт:
# - Файлы с циклическими импортами
# - Слишком большие модули
# - Сложные функции
```

### 3. Код работает — но грязный

```bash
# Проверяем на рефакторинг
python scripts/refactor-suggest.py ./app.py

# Получаем:
# - Что вынести в функции
# - Как упростить условия
# - Где добавить константы
```

### 4. Нужно переписать на другой язык

```bash
# Python -> JavaScript
python scripts/multi-lang-switch.py async_function --from python --to javascript

# Python -> Go
python scripts/multi-lang-switch.py error_handling --from python --to go
```

## База знаний ошибок

Debug Detective знает:

**Python ошибки:**
- ModuleNotFoundError → pip install
- ImportError → проверить циклический импорт
- AttributeError → проверить тип объекта
- KeyError → использовать .get()
- RecursionError → добавить базовый случай

**Базы данных:**
- Connection refused → проверить PostgreSQL
- IntegrityError duplicate key → проверить уникальность
- Too many connections → увеличить pool

**Web/API:**
- Pydantic validation error → проверить схемы
- Timeout → увеличить timeout или оптимизировать
- Connection reset → клиент закрыл соединение

## Паттерны для переключения языков

Доступные паттерны:
- list_comprehension — фильтрация/преобразование
- dictionary — ассоциативный массив
- class — классы с методами
- async_function — async/await
- error_handling — try/catch vs ошибки
- lambda — анонимные функции
- destructuring — множественное присваивание
- string_interpolation — f-strings/template literals
- type_annotation — типизация
- decorator — декораторы/middleware

Языки: Python 🐍, JavaScript 💛, TypeScript 💙, Go 🐹

## Структура skill

```
code-ninja/
├── SKILL.md                      # Этот файл
├── README.md                     # Документация
├── scripts/
│   ├── architecture-analyzer.py # ⭐ Анализ структуры
│   ├── debug-detective.py        # ⭐ Поиск корня проблемы
│   ├── refactor-suggest.py       # ⭐ Рекомендации по улучшению
│   └── multi-lang-switch.py      # Переключение языков
├── references/
│   └── patterns/                 # Паттерны проектирования
└── examples/                     # Примеры "до и после"
```

## Примеры использования

### Найти причину 500 ошибки

```bash
# 1. Получить логи
docker logs airouter-backend 2>&1 | grep -A 20 "ERROR" > error.log

# 2. Анализ
python scripts/debug-detective.py --traceback error.log

# 3. Результат:
# ❌ ОШИБКА: sqlalchemy.exc.OperationalError: Connection refused
# 📋 АНАЛИЗ: Нет подключения к БД
# 🛠️  ИСПРАВЛЕНИЕ: Проверьте запущен ли PostgreSQL
```

### Улучшить архитектуру

```bash
python scripts/architecture-analyzer.py ./backend

# Результат:
# 🔴 Критических: 2 (циклические импорты)
# 📏 Самые большие файлы:
#    892 строк  api/v1/proxy.py
#    756 строк  services/billing.py
# 💡 Рекомендации:
#    - Разбейте proxy.py на модули
#    - Устраните циклические импорты
```

### Рефакторинг перед релизом

```bash
python scripts/refactor-suggest.py ./critical_file.py

# Найдено:
# 🔴 process_payment: 127 строк - разбейте на функции
# 🟡 calculate_cost: сложность 15 - упростите условия
# 🟢 Магическое число 0.8 - создайте константу DISCOUNT_RATE
```

## Roadmap

- [x] architecture-analyzer.py
- [x] debug-detective.py
- [x] refactor-suggest.py
- [x] multi-lang-switch.py
- [ ] Автофикс проблем (автоматический рефакторинг)
- [ ] Интеграция с IDE (VS Code extension)
- [ ] Больше языков (Rust, Java, C#)

## Связь

- Канал: @dayanrouter
- Бот: @ai_router_support_bot
- Сайт: go.airouter.host

---

*Быстрый код — хороший код* 🥷⚡
