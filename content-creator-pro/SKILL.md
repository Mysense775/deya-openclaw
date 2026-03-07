# Content Creator Pro

AI-ассистент для создания контента. Генерирует идеи, пишет посты, планирует публикации, анализирует эффективность.

## Capabilities

- **Content Planning**: Создание контент-планов на неделю/месяц
- **Post Generation**: Написание постов разных форматов (сторис, лонгриды, карусели)
- **Hashtag Research**: Подбор релевантных хештегов
- **Timing Optimization**: Анализ лучшего времени для публикаций
- **Analytics**: Оценка эффективности контента
- **Multi-platform**: Адаптация под Telegram, Instagram, Twitter/X, LinkedIn

## Usage

```bash
# Создать контент-план на неделю
python scripts/content-planner.py --topic "AI tools" --days 7 --platform telegram

# Написать пост
python scripts/post-generator.py --type story --topic "Утренние ритуалы" --tone warm

# Анализ лучшего времени
python scripts/timing-analyzer.py --channel @dayanrouter --days 30

# Подобрать хештеги
python scripts/hashtag-research.py --topic "AI technology" --count 15
```

## Features

### Content Types
- **Story** (300-500 chars): Короткие истории, наблюдения
- **Longread** (1000+ chars): Глубокие статьи, разборы
- **Carousel** (5-10 слайдов): Инструкции, чеклисты
- **News** (200-400 chars): Быстрые новости
- **Engagement** (вопросы, опросы): Для вовлечения аудитории

### Tone of Voice
- warm — тёплый, личный (как Дея)
- professional — деловой
- humorous — с юмором
- inspirational — вдохновляющий
- educational — образовательный

## Requirements

- Python 3.9+
- aiogram (для Telegram API)
- pandas (для аналитики)
- python-dateutil (для работы с датами)

## Installation

```bash
cd skills/content-creator-pro
pip install -r requirements.txt
```

## API Integration

Использует Telegram Bot API для:
- Получения статистики канала
- Анализа времени публикаций
- Отправки тестовых постов

## License

MIT
