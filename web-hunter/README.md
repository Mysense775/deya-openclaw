# Web-Hunter 🕷️

Инструменты для интеллектуального поиска, парсинга и агрегации данных из веба.

## Быстрый старт

```bash
# Поиск по множеству источников
python scripts/search-aggregator.py --query "AI breakthrough" --sources reddit,hackernews,arxiv

# Парсинг JS-сайта
python scripts/dynamic-parser.py --url "https://example.com" --wait-for "#content"

# Мониторинг изменений
python scripts/dynamic-parser.py --url "https://shop.com/price" --selector ".price" --monitor 300
```

## Установка

```bash
# Установить зависимости
pip install aiohttp playwright
playwright install chromium
```

## Инструменты

### search-aggregator.py
Агрегирует поиск из Reddit, HackerNews, arXiv.

```bash
python scripts/search-aggregator.py \
  --query "OpenAI GPT-5" \
  --sources reddit,hackernews \
  --freshness week \
  --top 10 \
  --output markdown
```

### dynamic-parser.py
Парсит JavaScript-рендеренные сайты через Playwright.

```bash
python scripts/dynamic-parser.py \
  --url "https://airbnb.com" \
  --selector ".price" \
  --screenshot \
  --output result.json
```

## Roadmap

- [x] search-aggregator.py — поиск из множества источников
- [x] dynamic-parser.py — парсинг JS-сайтов
- [ ] fact-checker.py — проверка фактов
- [ ] email-finder.py — поиск контактов
- [ ] price-monitor.py — мониторинг цен

---

*Собирай данные умно* 🕷️
