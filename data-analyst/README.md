# Data Analyst 📊

AI-ассистент для анализа данных. Обрабатывает CSV/JSON, строит графики, считает бизнес-метрики, находит инсайты.

## 🚀 Быстрый старт

```bash
# Установка
cd skills/data-analyst
pip install -r requirements.txt

# Анализ данных
./scripts/data-processor.py --file sales.csv --analyze

# Построить график
./scripts/visualizer.py --file users.csv --x date --y revenue --type line --output chart.png

# Расчёт метрик
./scripts/metrics-calculator.py --file customers.csv --metric ltv

# Полный отчёт
./scripts/metrics-calculator.py --file transactions.csv --all --json report.json
```

## 📋 Скрипты

### 1. Data Processor
Загрузка и очистка данных.

```bash
# Показать сводку
./data-processor.py -f data.csv --analyze

# Очистить данные
./data-processor.py -f data.csv --clean --remove-duplicates --export clean.csv

# Фильтрация
./data-processor.py -f data.csv --query "revenue > 1000"
```

**Возможности:**
- Поддержка CSV, JSON, Excel, Parquet
- Удаление дубликатов
- Заполнение пропусков (mean, median, mode)
- Удаление выбросов (Z-score)
- Оптимизация типов данных
- SQL-like фильтрация

### 2. Visualizer
Построение графиков.

```bash
# Линейный график (временной ряд)
./visualizer.py -f sales.csv --type line -x date -y revenue

# Столбчатая диаграмма
./visualizer.py -f sales.csv --type bar -x category -y amount

# Круговая диаграмма
./visualizer.py -f users.csv --type pie -x country

# Scatter plot
./visualizer.py -f customers.csv --type scatter -x age -y spending

# Гистограмма
./visualizer.py -f orders.csv --type hist -x order_value

# Тепловая карта корреляций
./visualizer.py -f data.csv --type heatmap
```

**Типы графиков:**
- line — временные ряды
- bar — сравнение категорий
- pie — распределение долей
- scatter — корреляции
- hist — распределения
- heatmap — корреляционная матрица
- box — статистика

### 3. Metrics Calculator
Расчёт бизнес-метрик.

```bash
# Все метрики
./metrics-calculator.py -f transactions.csv --all

# Только LTV
./metrics-calculator.py -f customers.csv --metric ltv

# CAC с маркетинговыми расходами
./metrics-calculator.py -f users.csv --metric cac --marketing-spend 5000

# Churn за 30 дней
./metrics-calculator.py -f activity.csv --metric churn

# Retention (day 1, 7, 30, 90)
./metrics-calculator.py -f logins.csv --metric retention

# ARPU
./metrics-calculator.py -f payments.csv --metric arpu

# MRR
./metrics-calculator.py -f subscriptions.csv --metric mrr
```

**Метрики:**
- **LTV** — Lifetime Value
- **CAC** — Customer Acquisition Cost
- **Churn** — отток пользователей
- **Retention** — удержание (cohort analysis)
- **ARPU** — Average Revenue Per User
- **MRR** — Monthly Recurring Revenue
- **Conversion** — конверсия воронки

## 📊 Примеры использования

### Анализ продаж Deya Cloud

```bash
# 1. Очистить данные
./data-processor.py -f subscriptions.csv --clean --export clean.csv

# 2. Построить график MRR
./visualizer.py -f clean.csv --type line -x month -y mrr --title "Deya Cloud MRR"

# 3. Рассчитать метрики
./metrics-calculator.py -f clean.csv --all --json metrics.json
```

### Аналитика Telegram канала

```bash
# Анализ роста подписчиков
./visualizer.py -f channel_stats.csv --type line -x date -y subscribers

# Retention аудитории
./metrics-calculator.py -f post_views.csv --metric retention
```

### Финансовая отчётность

```bash
# Очистка и анализ
./data-processor.py -f financials.csv --analyze

# График выручки по категориям
./visualizer.py -f financials.csv --type bar -x category -y revenue

# Расчёт unit-экономики
./metrics-calculator.py -f customers.csv --metric ltv
./metrics-calculator.py -f marketing.csv --metric cac --marketing-spend 10000
```

## 🔧 Форматы данных

**CSV:**
```csv
date,user_id,revenue,country
2026-03-01,123,99.00,US
2026-03-01,124,29.00,RU
```

**JSON:**
```json
[
  {"date": "2026-03-01", "user_id": 123, "revenue": 99.00},
  {"date": "2026-03-01", "user_id": 124, "revenue": 29.00}
]
```

## 📈 Поддерживаемые метрики

| Метрика | Описание | Формула |
|---------|----------|---------|
| LTV | Lifetime Value | ARPU × Margin × Lifetime |
| CAC | Acquisition Cost | Marketing / New Users |
| Churn | Отток | Users Lost / Users Start |
| Retention | Удержание | Active / Total × 100 |
| ARPU | Revenue per user | Revenue / Users |
| ARPPU | Revenue per paying | Revenue / Paying Users |
| MRR | Monthly recurring | Sum of monthly revenue |

## 🔗 Интеграция с Deya

Этот скилл может:
- Подключаться к PostgreSQL AI Router
- Генерировать отчёты по расписанию
- Отправлять графики в Telegram
- Строить дашборды для бизнес-аналитики

## 📝 License

MIT License

---

*Создано для анализа данных Deya Cloud* 🌺
