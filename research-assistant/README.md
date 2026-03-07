# Research Assistant 🔬

AI-ассистент для глубокого исследования. Собирает информацию из множества источников, анализирует темы, структурирует знания, находит инсайты.

## 🚀 Быстрый старт

```bash
# Установка
cd skills/research-assistant
pip install -r requirements.txt

# Исследование темы
./scripts/topic-researcher.py --topic "AI agents 2026" --depth deep

# Проверка фактов
./scripts/fact-checker.py --claim "GPT-5 will be released in 2026"

# Суммаризация
./scripts/summarizer.py --file article.txt --length medium
```

## 📋 Скрипты

### 1. Topic Researcher
Глубокое исследование темы из множества источников.

```bash
# Быстрое исследование
./topic-researcher.py --topic "blockchain technology" --depth quick

# Глубокое исследование
./topic-researcher.py --topic "AI agents" --depth deep --sources all

# С сохранением в файл
./topic-researcher.py -t "cloud computing" -d medium -o report.md

# JSON формат
./topic-researcher.py -t "machine learning" --format json
```

**Глубина исследования:**
- `quick` — 3-5 источников, обзор
- `medium` — 5-10 источников, детальный разбор
- `deep` — 10+ источников, полный анализ

**Источники:**
- `web` — Google, Bing, DuckDuckGo
- `news` — Google News, RSS
- `academic` — arXiv, Google Scholar
- `tech` — HackerNews, GitHub
- `social` — Reddit, Twitter
- `all` — все источники

### 2. Fact Checker
Перекрёстная проверка фактов.

```bash
# Проверка заявления
./fact-checker.py --claim "Python was created in 1991"

# С подробностями
./fact-checker.py -c "Bitcoin market cap exceeded $1T in 2026" --verbose

# Экспорт
./fact-checker.py -c "claim to verify" --json result.json
```

**Вердикты:**
- ✅ **true** — подтверждено
- 🟢 **likely_true** — скорее всего верно
- 🟡 **uncertain** — недостаточно данных
- 🟠 **likely_false** — скорее всего неверно
- ❌ **false** — опровергнуто
- ⚪ **unverified** — невозможно проверить

### 3. Summarizer
Суммаризация текстов и документов.

```bash
# Базовая суммаризация
./summarizer.py --file article.txt

# Короткий пересказ
./summarizer.py -f document.md --length short

# В формате bullet-points
./summarizer.py -f report.txt --format bullet-points

# Только ключевые тезисы
./summarizer.py -f longread.txt --key-points 5

# TL;DR (2-3 предложения)
./summarizer.py -f article.txt --tldr

# Со статистикой
./summarizer.py -f book.txt --stats --length long
```

**Форматы вывода:**
- `paragraph` — связный текст
- `bullet-points` — маркированный список
- `numbered` — нумерованный список

**Длина:**
- `short` — ~10% от оригинала
- `medium` — ~20% от оригинала
- `long` — ~30% от оригинала

## 🎯 Use Cases

### Исследование рынка перед запуском

```bash
./topic-researcher.py \
  --topic "AI assistant market 2026" \
  --depth deep \
  --sources web,news,academic \
  --output market-research.md
```

### Проверка новости перед публикацией

```bash
./fact-checker.py \
  --claim "Company X acquired Company Y for $10B" \
  --verbose
```

### Суммаризация исследовательской статьи

```bash
./summarizer.py \
  --file research-paper.pdf \
  --length medium \
  --format bullet-points \
  --key-points 7 \
  --output summary.txt
```

### Подготовка к презентации

```bash
# Собрать информацию
./topic-researcher.py -t "Quantum computing applications" -d medium -o quantum.md

# Проверить ключевые факты
./fact-checker.py -c "Quantum supremacy achieved in 2025" -v

# Сделать краткое резюме
./summarizer.py -f quantum.md --tldr
```

## 📊 Процесс исследования

1. **Query Planning** — разбиение темы на подзапросы
2. **Data Collection** — сбор из множества источников
3. **Deduplication** — удаление дубликатов
4. **Relevance Scoring** — ранжирование
5. **Extraction** — извлечение ключевой информации
6. **Synthesis** — синтез знаний
7. **Verification** — перекрёстная проверка
8. **Formatting** — оформление отчёта

## 🔗 Интеграция с другими скиллами

**Content Creator Pro:**
```bash
# Исследовать тему → создать пост
./topic-researcher.py -t "topic" -d medium --format markdown > content.md
./content-creator-pro/post-generator.py --use-content content.md
```

**Data Analyst:**
```bash
# Собрать данные → проанализировать
./topic-researcher.py -t "market data" --format json > data.json
./data-analyst/data-processor.py --file data.json --analyze
```

**Web Hunter:**
```bash
# Углубленный парсинг после первичного исследования
./topic-researcher.py -t "topic" -d quick
./web-hunter/dynamic-parser.py --url "found-url" --depth 2
```

## ⚠️ Ethics & Limits

- Уважение robots.txt при веб-скрапинге
- Rate limiting для API (не спамить)
- Обязательное цитирование источников
- Не использовать для плагиата
- Проверка фактов перед публикацией
- Уважение авторских прав

## 📄 License

MIT License

---

*Создано для глубоких исследований Deya* 🔬🌺
