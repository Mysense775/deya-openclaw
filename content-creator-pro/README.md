# Content Creator Pro 🎨

AI-ассистент для создания контента. Генерирует идеи, пишет посты, планирует публикации, анализирует эффективность.

## 🚀 Быстрый старт

```bash
# Установка
cd skills/content-creator-pro
pip install -r requirements.txt

# Создать контент-план
./scripts/content-planner.py --topic "AI инструменты" --days 7 --platform telegram

# Написать пост
./scripts/post-generator.py --type story --topic "Утренние ритуалы" --tone warm

# Подобрать хештеги
./scripts/hashtag-research.py --topic "AI technology" --count 15

# Получить рекомендации по времени
./scripts/timing-analyzer.py --platform telegram
```

## 📋 Возможности

### 1. Content Planner
Создаёт структурированные контент-планы на неделю или месяц.

**Форматы:**
- Story (300-500 символов) — короткие истории
- Longread (1000+) — глубокие разборы
- News (200-400) — быстрые новости
- Engagement — вовлекающие вопросы

**Пример:**
```bash
./scripts/content-planner.py --topic "Deya Cloud" --days 7 --format markdown
```

### 2. Post Generator
Пишет посты разных форматов и тональностей.

**Типы:**
- `story` — личные истории
- `longread` — подробные гайды
- `news` — новостные анонсы
- `engagement` — вопросы и опросы

**Тона:**
- `warm` — тёплый, личный (как Дея)
- `professional` — деловой
- `humorous` — с юмором
- `inspirational` — вдохновляющий

**Пример:**
```bash
./scripts/post-generator.py --type story --topic "Запуск продукта" --tone warm --hashtags
```

### 2.1 Human Post Generator 🆕
**Максимально человечные посты** — с эмоциями, несовершенствами, живым языком.

**Что делает:**
- ✅ Разговорные приветствия (не всегда идеальные)
- ✅ Признания в трудностях и неуверенности
- ✅ Конкретные детали («вчера в 11 вечера», «в пижаме»)
- ✅ Самоирония и несовершенства
- ✅ Живые эмоции без фильтра

**Типы постов:**
- `story` — история с личным опытом
- `reflection` — размышление/наблюдение
- `struggle` — признание о трудностях (максимально человечно!)
- `milestone` — скромное достижение без понтов
- `question` — честный вопрос, а не формальный

**Пример:**
```bash
# Признание о трудностях (супер-человечно)
./scripts/human-post-generator.py --type struggle --topic "прокрастинацию"

# Скромное достижение
./scripts/human-post-generator.py --type milestone --topic "запуск продукта"

# Честный вопрос
./scripts/human-post-generator.py --type question --topic "монетизацию"
```

**Пример вывода:**
```
Вечер пятницы... или среды? Сама путаюсь уже

Вот неделю назад надоело с прокрастинацию.
Хотела бросить уже, но нет.
Помогает музыка.

Кто ещё тоже борется? Поддержите 👇

—
Дея 🌺
P.S. Спасибо, что читаете
```

### 3. Hashtag Research
Подбирает релевантные хештеги для любой темы.

**Функции:**
- База из 100+ категоризированных хештегов
- Автоматическая генерация по теме
- Наборы: minimal (5), optimal (10), maximum (20)
- Анализ конкуренции

**Пример:**
```bash
# Базовый поиск
./scripts/hashtag-research.py --topic "AI automation"

# Генерация наборов
./scripts/hashtag-research.py --topic "AI automation" --sets

# Анализ конкуренции
./scripts/hashtag-research.py --analyze "#artificialintelligence"
```

### 4. Timing Analyzer
Определяет лучшее время для публикаций.

**Возможности:**
- Анализ статистики канала
- Рекомендации по дням и часам
- Оптимизация под тип контента
- Экспорт расписаний

**Пример:**
```bash
./scripts/timing-analyzer.py --platform telegram --days 30
```

## 🎯 Use Cases

### Для @dayanrouter
```bash
# План на неделю
./content-planner.py -t "Жизнь с AI" -d 7 -p telegram -f markdown > plan.md

# Пост на сегодня
./post-generator.py -t story -p "Субботнее утро" -o warm

# Хештеги
./hashtag-research.py -t "AI lifestyle" -c 10
```

### Для бизнес-канала
```bash
# План контента
./content-planner.py -t "SaaS продукт" -d 30 -p telegram

# Профессиональный пост
./post-generator.py -t longread -p "Обновление платформы" -o professional

# Лучшее время
./timing-analyzer.py -p telegram -c @mychannel
```

## 🔧 Интеграция с Deya

Этот скилл интегрируется с основной системой Deya и может:

1. **Автоматически генерировать посты** по расписанию
2. **Анализировать эффективность** прошлых публикаций
3. **Предлагать темы** на основе трендов
4. **Адаптировать стиль** под конкретную аудиторию

## 📊 Roadmap

- [x] Базовый генератор постов
- [x] Планировщик контента
- [x] Исследователь хештегов
- [x] Анализ времени публикаций
- [x] **Human Post Generator** — максимально человечные посты 🆕
- [ ] Интеграция с Telegram API
- [ ] Автоматический анализ эффективности
- [ ] A/B тестирование постов
- [ ] Генерация визуалов (через Fal.ai)

## 📝 License

MIT License - свободное использование и модификация.

---

*Создано с любовью для Deya Cloud* 🌺
