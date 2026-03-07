# Data Analyst

AI-ассистент для анализа данных. Обрабатывает CSV/JSON, строит графики, считает бизнес-метрики, находит инсайты.

## Capabilities

- **Data Processing**: Загрузка и очистка CSV, JSON, Excel
- **Visualization**: Построение графиков (линии, бары, pie, heatmap)
- **Business Metrics**: Расчёт CAC, LTV, Churn, Retention, ARPU
- **Segmentation**: Сегментация пользователей по поведению
- **Trend Analysis**: Выявление трендов и паттернов
- **Report Generation**: Автоматические отчёты в PDF/HTML
- **Anomaly Detection**: Поиск аномалий в данных

## Usage

```bash
# Анализ CSV файла
python scripts/data-processor.py --file sales.csv --analyze

# Построить график
python scripts/visualizer.py --file users.csv --x date --y revenue --type line

# Расчёт бизнес-метрик
python scripts/metrics-calculator.py --file customers.csv --metric ltv --cohort monthly

# Сегментация пользователей
python scripts/segmentation.py --file users.csv --method rfm

# Полный отчёт
python scripts/report-generator.py --data-dir ./data --output report.html
```

## Features

### Data Processing
- Автоматическое определение формата (CSV, JSON, Excel)
- Очистка данных (пропуски, дубликаты, выбросы)
- Нормализация и трансформация
- Слияние нескольких источников
- Фильтрация и агрегация

### Visualization Types
- **Line**: Временные ряды, тренды
- **Bar**: Сравнение категорий
- **Pie**: Распределение долей
- **Scatter**: Корреляции
- **Heatmap**: Плотность, матрицы
- **Histogram**: Распределение значений
- **Cohort**: Когортный анализ retention

### Business Metrics
- **CAC**: Customer Acquisition Cost
- **LTV**: Lifetime Value
- **Churn Rate**: Отток пользователей
- **Retention**: Удержание (day 1, 7, 30, 90)
- **ARPU**: Average Revenue Per User
- **MRR/ARR**: Monthly/Annual Recurring Revenue
- **Conversion**: Конверсия воронки
- **Payback Period**: Срок окупаемости

### Segmentation Methods
- **RFM**: Recency, Frequency, Monetary
- **Cohort**: По дате первого действия
- **Behavioral**: По поведению
- **Demographic**: По demographics

## Output Formats

- **Charts**: PNG, SVG, interactive HTML
- **Reports**: PDF, HTML, Markdown
- **Data**: CSV, JSON, Excel
- **Dashboards**: Single-file HTML dashboards

## Requirements

- Python 3.9+
- pandas (data processing)
- matplotlib/seaborn (static charts)
- plotly (interactive charts)
- numpy (calculations)
- jinja2 (report templates)
- fpdf2 (PDF generation)

## Installation

```bash
cd skills/data-analyst
pip install -r requirements.txt
```

## Integration

Этот скилл может:
- Получать данные из PostgreSQL (AI Router база)
- Экспортировать отчёты в Telegram
- Строить дашборды для анализа бизнеса
- Генерировать отчёты по расписанию

## Use Cases

1. **Анализ продаж Deya Cloud**: выручка, подписки, отток
2. **Аналитика канала @dayanrouter**: рост, engagement, лучшие посты
3. **Мониторинг AI Router**: использование API, расходы клиентов
4. **Финансовая отчётность**: P&L, прогнозы

## License

MIT
