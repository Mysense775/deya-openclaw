# Архитектура независимого инстанса

## Как это работает сейчас

### 1. Локальные скиллы (что мы создали)

```
/root/.openclaw/workspace/skills/
├── deya-mode/              # Папка скилла
│   ├── SKILL.md           # Манифест
│   ├── references/        # Документация
│   ├── scripts/           # Python/bash скрипты
│   └── assets/            # Компоненты, изображения
├── ui-ux-pro-max/
├── code-ninja/
├── web-hunter/
├── deya-visual-identity/
└── deya-dashboard/
```

**Упаковка:**
```bash
cd /root/.openclaw/workspace/skills
tar -czf deya-mode-v1.0.skill deya-mode/
# Получаем: deya-mode-v1.0.skill (tar.gz)
```

### 2. Установка скилла

**Вариант A: Локальный файл**
```bash
# Пользователь копирует .skill файл
openclaw skills install ./deya-mode-v1.0.skill

# Что происходит:
# 1. Распаковка tar.gz в ~/.openclaw/skills/
# 2. Чтение SKILL.md (манифест)
# 3. Установка зависимостей (если есть requirements.txt)
# 4. Регистрация триггеров
```

**Вариант B: ClawHub (удалённый)**
```bash
# Поиск
openclaw skills search deya

# Установка из реестра
openclaw skills install deya-mode
# Скачивается с clawhub.com/skills/deya-mode/latest
```

## Сценарии развёртывания

### Сценарий 1: Docker образ (рекомендуется)

**Dockerfile:**
```dockerfile
FROM openclaw/base:latest

# Копируем скиллы в образ
COPY skills/ /opt/openclaw/skills/

# Автоустановка при первом запуске
RUN openclaw skills install /opt/openclaw/skills/deya-mode-v1.0.skill \
    && openclaw skills install /opt/openclaw/skills/ui-ux-pro-max-v1.1.skill \
    && openclaw skills install /opt/openclaw/skills/code-ninja-v1.0.skill \
    && openclaw skills install /opt/openclaw/skills/web-hunter-v1.0.skill \
    && openclaw skills install /opt/openclaw/skills/deya-visual-identity-v1.0.skill \
    && openclaw skills install /opt/openclaw/skills/deya-dashboard-v1.0.skill

# Копируем конфиг
COPY config/ /root/.openclaw/

# Запускаем дашборд и gateway
CMD ["openclaw", "start", "--all"]
```

**docker-compose.yml:**
```yaml
version: '3.8'
services:
  deya-instance:
    image: deya/openclaw-full:latest
    ports:
      - "8000:8000"    # Gateway API
      - "8001:8001"    # Dashboard
    volumes:
      - ./workspace:/root/.openclaw/workspace
      - ./memory:/root/.openclaw/memory
    environment:
      - OPENCLAW_MODEL=moonshot/kimi-k2.5
      - DEYA_MODE=active
```

**Запуск:**
```bash
docker-compose up -d
# Готово! Дашборд на http://localhost:8001
```

### Сценарий 2: Установочный скрипт

**install-deya-instance.sh:**
```bash
#!/bin/bash
set -e

echo "🌺 Установка инстанса Деи..."

# 1. Установка OpenClaw
curl -fsSL https://openclaw.ai/install.sh | bash

# 2. Создание workspace
mkdir -p ~/.openclaw/workspace/skills
mkdir -p ~/.openclaw/memory

# 3. Скачивание скиллов
SKILLS_BASE="https://github.com/Mysense775/openclaw-skills/releases/download/v1.0"

curl -L "$SKILLS_BASE/deya-mode-v1.0.skill" -o /tmp/deya-mode.skill
curl -L "$SKILLS_BASE/ui-ux-pro-max-v1.1.skill" -o /tmp/ui-ux-pro-max.skill
curl -L "$SKILLS_BASE/code-ninja-v1.0.skill" -o /tmp/code-ninja.skill
curl -L "$SKILLS_BASE/web-hunter-v1.0.skill" -o /tmp/web-hunter.skill
curl -L "$SKILLS_BASE/deya-visual-identity-v1.0.skill" -o /tmp/deya-visual-identity.skill
curl -L "$SKILLS_BASE/deya-dashboard-v1.0.skill" -o /tmp/deya-dashboard.skill

# 4. Установка
openclaw skills install /tmp/deya-mode.skill
openclaw skills install /tmp/ui-ux-pro-max.skill
openclaw skills install /tmp/code-ninja.skill
openclaw skills install /tmp/web-hunter.skill
openclaw skills install /tmp/deya-visual-identity.skill
openclaw skills install /tmp/deya-dashboard.skill

# 5. Копирование identity
cat > ~/.openclaw/workspace/IDENTITY.md << 'EOF'
# IDENTITY.md — Deya
- **Имя:** Deya
- **Сущность:** Дух-хранитель с Бали
- **Эмодзи:** 🌺
EOF

cat > ~/.openclaw/workspace/SOUL.md << 'EOF'
# SOUL.md - Deya
...полный текст...
EOF

# 6. Запуск dashboard
cd ~/.openclaw/workspace/skills/deya-dashboard
pip install -r requirements.txt
python main.py &

# 7. Запуск OpenClaw gateway
openclaw gateway start

echo "✅ Инстанс Деи готов!"
echo "🌐 Дашборд: http://localhost:8001"
echo "💬 Gateway: http://localhost:8000"
```

**Использование:**
```bash
curl -fsSL https://deya.ai/install.sh | bash
# или
wget -qO- https://deya.ai/install.sh | bash
```

### Сценарий 3: GitHub Releases (готовые бинарники)

**Структура релиза:**
```
openclaw-deya-bundle-v1.0/
├── openclaw-binary        # Скомпилированный бинарник
├── skills-bundle/         # Все 6 скиллов
│   ├── deya-mode/
│   ├── ui-ux-pro-max/
│   ├── code-ninja/
│   ├── web-hunter/
│   ├── deya-visual-identity/
│   └── deya-dashboard/
├── default-config.yaml    # Конфиг по умолчанию
└── install.sh            # Установщик
```

**GitHub Actions workflow:**
```yaml
name: Build Deya Bundle
on:
  release:
    types: [created]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Build skills bundle
        run: |
          mkdir -p bundle/skills
          for skill in deya-mode ui-ux-pro-max code-ninja web-hunter deya-visual-identity deya-dashboard; do
            tar -czf bundle/skills/$skill.skill skills/$skill/
          done
      
      - name: Build OpenClaw binary
        run: |
          go build -o bundle/openclaw ./cmd/openclaw
      
      - name: Create release archive
        run: |
          tar -czf openclaw-deya-v${{ github.ref_name }}.tar.gz bundle/
      
      - name: Upload to release
        uses: softprops/action-gh-release@v1
        with:
          files: openclaw-deya-*.tar.gz
```

### Сценарий 4: ClawHub Marketplace

**Что нужно сделать:**

1. **Создать манифест пакета:**
```json
{
  "name": "deya-complete-bundle",
  "version": "1.0.0",
  "description": "Полный инстанс Деи с веб-интерфейсом",
  "skills": [
    "deya-mode@1.0.0",
    "ui-ux-pro-max@1.1.0",
    "code-ninja@1.0.0",
    "web-hunter@1.0.0",
    "deya-visual-identity@1.0.0",
    "deya-dashboard@1.0.0"
  ],
  "config": {
    "default_model": "moonshot/kimi-k2.5",
    "timezone": "Europe/Berlin",
    "theme": "deya"
  },
  "scripts": {
    "post_install": "setup-deya-instance.sh"
  }
}
```

2. **Загрузить на ClawHub:**
```bash
openclaw clawhub login
openclaw clawhub publish deya-complete-bundle.json
```

3. **Пользователь устанавливает:**
```bash
openclaw install deya-complete-bundle
# Устанавливает все 6 скиллов + настройки
```

## Рекомендуемый подход

### Для разработки (сейчас):
```bash
# Локальная установка
openclaw skills install ./deya-dashboard-v1.0.skill
cd ~/.openclaw/workspace/skills/deya-dashboard
python main.py
```

### Для продакшена:
**Docker образ** — лучший вариант:
- Одна команда запуска
- Все зависимости внутри
- Легко масштабировать
- Версионирование

### Для распространения:
**GitHub Releases + install скрипт:**
```bash
curl -fsSL https://get.deya.ai | bash
```

## Что нужно сделать прямо сейчас

1. **Создать репозиторий** `openclaw-deya-bundle`
2. **Настроить GitHub Actions** для сборки
3. **Создать install.sh** скрипт
4. **Протестировать** установку на чистой машине

Хочешь, чтобы я создал эту инфраструктуру? 🌺
