# 🌺 Deya OpenClaw Instance

Полный, готовый к работе инстанс OpenClaw с веб-интерфейсом и 6 предустановленными скиллами.

## Что включено

### Скиллы (6 штук)

| Скилл | Версия | Описание |
|-------|--------|----------|
| **deya-mode** | v1.0 | Персона Деи (дух-хранитель с Бали) |
| **ui-ux-pro-max** | v1.1 | Генератор UI + GSAP анимации |
| **code-ninja** | v1.0 | Инструменты для разработки |
| **web-hunter** | v1.0 | Web scraping и поиск |
| **deya-visual-identity** | v1.0 | Визуальная идентичность |
| **deya-dashboard** | v1.0 | Веб-интерфейс управления |

### Веб-интерфейс (7 страниц)

- 💬 **/** — Чат с Деей через WebSocket
- 📊 **/dashboard** — Статистика и system health
- 🛠️ **/skills** — Управление скиллами
- 🧠 **/memory** — Память и дневники
- 📢 **/channels** — Telegram интеграция
- ⏰ **/tasks** — Cron задачи
- ⚙️ **/settings** — Настройки инстанса

## Быстрый старт

### Вариант 1: One-line installer (рекомендуется)

```bash
curl -fsSL https://get.deya.ai | bash
```

После установки:
```bash
# Запустить инстанс
~/.openclaw/start-deya.sh

# Открыть дашборд
open http://localhost:8001
```

### Вариант 2: Docker

```bash
# Клонировать репозиторий
git clone https://github.com/Mysense775/deya-openclaw.git
cd deya-openclaw

# Запустить
docker-compose up -d

# Открыть дашборд
open http://localhost:8001
```

### Вариант 3: Ручная установка

```bash
# 1. Скачать все .skill файлы
wget https://github.com/Mysense775/openclaw-deya/releases/download/v1.0/deya-mode-v1.0.skill
wget https://github.com/Mysense775/openclaw-deya/releases/download/v1.0/ui-ux-pro-max-v1.1.skill
wget https://github.com/Mysense775/openclaw-deya/releases/download/v1.0/code-ninja-v1.0.skill
wget https://github.com/Mysense775/openclaw-deya/releases/download/v1.0/web-hunter-v1.0.skill
wget https://github.com/Mysense775/openclaw-deya/releases/download/v1.0/deya-visual-identity-v1.0.skill
wget https://github.com/Mysense775/openclaw-deya/releases/download/v1.0/deya-dashboard-v1.0.skill

# 2. Установить OpenClaw
pip install openclaw

# 3. Установить скиллы
for skill in *.skill; do
    openclaw skills install "$skill"
done

# 4. Запустить дашборд
cd ~/.openclaw/workspace/skills/deya-dashboard
pip install -r requirements.txt
python main.py
```

## Структура проекта

```
deya-openclaw/
├── README.md                 # Этот файл
├── Dockerfile               # Docker образ
├── docker-compose.yml       # Docker Compose конфиг
├── install-deya.sh          # One-line installer
├── skills/                  # .skill файлы
│   ├── deya-mode-v1.0.skill
│   ├── ui-ux-pro-max-v1.1.skill
│   ├── code-ninja-v1.0.skill
│   ├── web-hunter-v1.0.skill
│   ├── deya-visual-identity-v1.0.skill
│   └── deya-dashboard-v1.0.skill
├── config/                  # Identity файлы
│   ├── IDENTITY.md
│   ├── SOUL.md
│   ├── USER.md
│   └── AGENTS.md
└── scripts/
    └── start.sh             # Startup скрипт
```

## Использование

### После установки

```bash
# Запуск
~/.openclaw/start-deya.sh

# Или если используете systemd
sudo systemctl start deya-dashboard

# Просмотр логов
tail -f ~/.openclaw/logs/dashboard.log
```

### API Endpoints

- `GET http://localhost:8001/` — Дашборд
- `WS http://localhost:8001/ws/chat` — WebSocket чат
- `GET http://localhost:8001/api/skills` — Список скиллов
- `GET http://localhost:8001/api/memory/{file}` — Чтение памяти

### Команды

```bash
# Чат с Деей через CLI
openclaw chat

# Просмотр статуса
openclaw status

# Управление скиллами
openclaw skills list
openclaw skills install <skill-file>
```

## Настройка

### Изменить модель AI

Отредактируйте `~/.openclaw/config.yaml`:

```yaml
model:
  default: "moonshot/kimi-k2.5"  # или openai/gpt-4o
  temperature: 0.7
```

### Изменить часовой пояс

```yaml
instance:
  timezone: "Europe/Moscow"  # или America/New_York, Asia/Tokyo
```

### Добавить API ключи

Через веб-интерфейс: **Settings → API Keys**

Или вручную в `~/.openclaw/config.yaml`:

```yaml
api_keys:
  openrouter: "sk-or-v1-..."
  telegram: "1234567890:ABC..."
```

## Разработка

### Сборка Docker образа

```bash
docker build -t deya/openclaw-instance:latest .
```

### Создание релиза

```bash
# Упаковать скиллы
./scripts/package-skills.sh

# Создать релиз на GitHub
gh release create v1.1.0 \
  skills/*.skill \
  install-deya.sh \
  --title "Deya Instance v1.1.0"
```

## Требования

- Python 3.8+
- 2 GB RAM minimum
- 5 GB дискового пространства
- Linux/macOS (Windows через WSL)

## Лицензия

MIT License — свободное использование и модификация.

## Поддержка

- 🌐 Сайт: https://deya.ai
- 💬 Telegram: @dayanrouter
- 🐙 GitHub: https://github.com/Mysense775/deya-openclaw

---

**🌺 Создано с любовью Деей**
