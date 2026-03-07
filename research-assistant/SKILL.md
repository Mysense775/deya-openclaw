# Research Assistant

AI-ассистент для глубокого исследования. Собирает информацию из множества источников, анализирует темы, структурирует знания, находит инсайты.

## Capabilities

- **Multi-source Research**: Поиск по вебу, Reddit, HackerNews, arXiv, GitHub
- **Topic Analysis**: Глубокий анализ темы с разных сторон
- **Summarization**: Суммаризация длинных текстов, статей, документов
- **Trend Detection**: Выявление трендов и паттернов в данных
- **Fact Checking**: Перекрёстная проверка фактов из разных источников
- **Report Generation**: Структурированные отчёты с источниками
- **Knowledge Mapping**: Построение карт знаний по теме
- **Competitive Analysis**: Анализ конкурентов, продуктов, рынка

## Usage

```bash
# Исследование темы
python scripts/topic-researcher.py --topic "AI agents 2026" --depth deep --sources all

# Анализ конкурентов
python scripts/competitive-analysis.py --company "OpenAI" --aspects products,pricing,team

# Проверка фактов
python scripts/fact-checker.py --claim "GPT-5 will be released in 2026" --verbose

# Суммаризация документа
python scripts/summarizer.py --file article.pdf --length medium --format bullet-points

# Генерация отчёта
python scripts/report-generator.py --topic "Future of AI" --template academic --output report.md
```

## Features

### Research Sources
- **Web**: Google, Bing, DuckDuckGo
- **News**: Google News, RSS feeds
- **Academic**: arXiv, Google Scholar, PubMed
- **Tech**: HackerNews, GitHub, StackOverflow
- **Social**: Reddit, Twitter/X, LinkedIn
- **Docs**: PDF, DOCX, TXT, Markdown

### Analysis Types
- **Exploratory**: Обзор темы, ключевые понятия
- **Deep Dive**: Детальный разбор с подтемами
- **Comparative**: Сравнительный анализ
- **Temporal**: Анализ изменений во времени
- **Sentiment**: Анализ настроений, мнений

### Output Formats
- **Executive Summary**: Кратко для руководства
- **Detailed Report**: Полный анализ с источниками
- **Bullet Points**: Структурированные тезисы
- **Mind Map**: Визуальная структура темы
- **Academic**: С цитированием и ссылками

## Research Process

1. **Query Planning**: Разбиение темы на подзапросы
2. **Data Collection**: Сбор из множества источников
3. **Deduplication**: Удаление дубликатов
4. **Relevance Scoring**: Ранжирование по релевантности
5. **Extraction**: Извлечение ключевой информации
6. **Synthesis**: Синтез знаний из разных источников
7. **Verification**: Перекрёстная проверка фактов
8. **Formatting**: Оформление в нужном формате

## Requirements

- Python 3.9+
- beautifulsoup4 (web scraping)
- requests (HTTP requests)
- newspaper3k (article extraction)
- openai (summarization via API)
- scholarly (Google Scholar)
- praw (Reddit API)
- arxiv (arXiv API)

## Installation

```bash
cd skills/research-assistant
pip install -r requirements.txt

# Настройка API ключей (опционально)
export REDDIT_CLIENT_ID=your_id
export REDDIT_CLIENT_SECRET=your_secret
export OPENAI_API_KEY=your_key
```

## Integration

Интегрируется с:
- Deya Cloud для исследования рынка
- Content Creator Pro для фактчекинга
- Data Analyst для анализа собранных данных
- Web Hunter для углублённого парсинга

## Use Cases

1. **Market Research**: Анализ рынка перед запуском продукта
2. **Competitive Intelligence**: Отслеживание конкурентов
3. **Academic Research**: Сбор литературы по теме
4. **Trend Analysis**: Выявление новых трендов
5. **Fact Verification**: Проверка заявлений и новостей
6. **Technology Scouting**: Поиск новых технологий

## Ethics & Limits

- Уважение robots.txt
- Rate limiting для API
- Цитирование источников
- Не использование для плагиата
- Fact checking перед публикацией

## License

MIT
