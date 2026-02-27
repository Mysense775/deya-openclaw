---
name: web-hunter
description: Intelligent web search, scraping, and data aggregation assistant. Use when you need to find information from multiple sources, parse websites, monitor prices, or aggregate data from the web.
triggers:
  - "найди в интернете"
  - "спарси сайт"
  - "мониторинг цен"
  - "поиск контактов"
  - "агрегация данных"
  - "собери информацию"
  - "web scraping"
  - "проверь факты"
---

# Web-Hunter 🕷️

Инструменты для интеллектуального поиска, парсинга и агрегации данных из веба.

## Быстрый старт

### Поиск из множества источников
```bash
python scripts/search-aggregator.py --query "AI news 2025" --sources "reddit,hackernews,arxiv"
```

### Парсинг динамического сайта
```bash
python scripts/dynamic-parser.py --url "https://example.com" --wait-for "#content"
```

### Проверка фактов
```bash
python scripts/fact-checker.py --claim "NVIDIA bought Groq for $20B"
```

### Поиск email контактов
```bash
python scripts/email-finder.py --domain "company.com" --pattern "firstname.lastname"
```

### Мониторинг цен
```bash
python scripts/price-monitor.py --url "https://shop.com/product" --threshold "1000"
```

## Инструменты

### 1. search-aggregator.py 🔍
Агрегирует результаты поиска из нескольких источников одновременно:
- Reddit (r/artificial, r/MachineLearning, r/singularity)
- HackerNews
- arXiv
- Google News
- Twitter/X
- LinkedIn
- GitHub

**Особенности:**
- Устранение дубликатов
- Ранжирование по релевантности
- Фильтрация по дате
- Анализ настроений (sentiment analysis)
- Автоматическое summary топ-N результатов

### 2. dynamic-parser.py 🌐
Парсит JavaScript-рендеренные сайты:
- Headless Chrome/Selenium
- Ожидание загрузки элементов
- Обход защит (Cloudflare, DataDome)
- Кэширование результатов
- Поддержка куки и сессий

**Использование:**
```bash
# Простой парсинг
python scripts/dynamic-parser.py --url "https://example.com"

# С ожиданием элемента
python scripts/dynamic-parser.py --url "https://example.com" --wait-for ".content" --timeout 10

# С сохранением скриншота
python scripts/dynamic-parser.py --url "https://example.com" --screenshot
```

### 3. fact-checker.py ✅
Перекрёстная проверка фактов:
- Поиск подтверждений в авторитетных источниках
- Выявление противоречий
- Оценка надёжности (confidence score)
- Цитирование источников
- Проверка дат и контекста

### 4. email-finder.py 📧
Поиск контактов компаний:
- Перебор паттернов (firstname.lastname@, flast@, etc.)
- Проверка валидности (MX lookup, SMTP verify)
- Поиск на страницах "About", "Team", "Contact"
- Интеграция с Hunter.io API (опционально)
- Экспорт в CSV/JSON

### 5. price-monitor.py 💰
Мониторинг изменения цен:
- Отслеживание CSS-селекторов
- Уведомления при изменении (Telegram, Email)
- История изменений (графики)
- Сравнение цен между магазинами
- Поддержка капчи (2captcha, Anti-Captcha)

## Рабочие процессы

### 1. Ежедневный дайджест новостей
```bash
# Каждое утро в 9:00
python scripts/search-aggregator.py \
  --query "AI artificial intelligence breakthrough" \
  --sources "reddit,hackernews,arxiv" \
  --freshness "24h" \
  --top 10 \
  --output-format "telegram"
```

### 2. Мониторинг конкурентов
```bash
# Раз в неделю
python scripts/dynamic-parser.py \
  --url "https://competitor.com/pricing" \
  --selector ".price" \
  --compare-with-last \
  --notify-telegram
```

### 3. Проверка перед публикацией
```bash
# Проверить факт перед постом
python scripts/fact-checker.py \
  --claim "Meta bought Manus AI startup" \
  --min-confidence 0.8 \
  --output-format "markdown"
```

### 4. Поиск leads для продаж
```bash
# Найти контакты потенциальных клиентов
python scripts/email-finder.py \
  --domain "target-company.com" \
  --validate \
  --output "leads.csv"
```

## База знаний

### Надёжные источники
- `references/trusted-sources.md` — список проверенных источников
- `references/blacklist.md` — ненадёжные/спам-сайты
- `sources/` — сохранённые статьи и данные

### Примеры использования
- `examples/research-example.md` — как провести исследование темы
- `examples/monitoring-example.md` — настройка мониторинга
- `examples/lead-generation.md` — поиск клиентов

## Ограничения и этика

**✅ Можно:**
- Парсить публичные данные
- Мониторить цены для личного использования
- Искать контакты из публичных источников
- Агрегировать новости с указанием источников

**❌ Нельзя:**
- DDoS атаки
- Парсить приватные данные
- Обходить CAPTCHA массово
- Нарушать Terms of Service
- Спамить найденные email

## Конфигурация

Создай `.env` файл:
```
# API Keys (опционально)
HUNTER_API_KEY=your_key
SERPER_API_KEY=your_key
TWITTER_BEARER_TOKEN=your_token

# Настройки
DEFAULT_TIMEOUT=30
MAX_RETRIES=3
USER_AGENT="Web-Hunter Bot 1.0"

# Прокси (если нужно)
HTTP_PROXY=http://proxy:8080
HTTPS_PROXY=http://proxy:8080
```

## Установка

```bash
# Клонировать
openclaw skills install web-hunter

# Установить зависимости
cd skills/web-hunter
pip install -r requirements.txt

# Установить playwright для динамического парсинга
playwright install chromium
```

## Roadmap

- [x] search-aggregator.py
- [x] dynamic-parser.py
- [x] fact-checker.py
- [x] email-finder.py
- [x] price-monitor.py
- [ ] RSS-aggregator
- [ ] Social media tracker
- [ ] Change detection (визуальное сравнение страниц)
- [ ] Автоматические отчёты (PDF/HTML)

---

*Собирай данные умно, проверяй факты, уважай источники* 🕷️✨
