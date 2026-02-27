# 🚀 Публикация на GitHub

## 📋 Что готово

Структура репозитория подготовлена!

```
deya-openclaw/
├── .github/
│   └── workflows/
│       └── release.yml        # GitHub Actions для релизов
├── config/
│   ├── AGENTS.md              # Инструкции для агента
│   ├── IDENTITY.md            # Кто такая Дея
│   ├── SOUL.md               # Глубинная суть
│   └── USER.md               # О пользователе
├── scripts/
│   ├── setup-github.sh        # Настройка GitHub
│   ├── package-release.sh     # Упаковка релиза
│   └── start.sh              # Запуск инстанса
├── deya-mode/                 # Исходники скиллов
├── ui-ux-pro-max/
├── code-ninja/
├── web-hunter/
├── deya-visual-identity/
├── deya-dashboard/
├── .gitignore                 # Исключения
├── CHANGELOG.md              # История версий
├── CONTRIBUTING.md           # Как контрибьютить
├── Dockerfile                # Docker образ
├── docker-compose.yml        # Docker Compose
├── install-deya.sh           # One-line installer
├── LICENSE                   # MIT License
├── README.md                 # Главный README
└── SKILL-ROADMAP.md          # Дорожная карта
```

## 🚀 Быстрая публикация

### Вариант 1: GitHub CLI (быстрее)

```bash
cd /root/.openclaw/workspace/skills

# Установить gh если нет
# https://cli.github.com/

# Авторизоваться
gh auth login

# Создать и запушить репо
gh repo create deya-openclaw \
  --public \
  --description "Полный инстанс OpenClaw с веб-интерфейсом и персоной Деи" \
  --source=. \
  --remote=origin \
  --push

# Создать релиз
gh release create v1.0.0 \
  deya-openclaw-v1.0.tar.gz \
  --title "🌺 Deya OpenClaw v1.0" \
  --notes "Initial release with 6 skills and web dashboard"
```

### Вариант 2: Вручную через сайт

```bash
# 1. Запустить setup скрипт
cd /root/.openclaw/workspace/skills
./scripts/setup-github.sh

# 2. Следовать инструкциям скрипта:
#    - Создать репо на github.com/new
#    - Запушить код
#    - Настроить secrets
```

## 📝 Пошаговая инструкция

### Шаг 1: Создать репозиторий

1. Открой https://github.com/new
2. Repository name: `deya-openclaw`
3. Description: `Полный инстанс OpenClaw с веб-интерфейсом и персоной Деи`
4. Public ✅
5. НЕ создавай README (у нас уже есть)
6. НЕ добавляй .gitignore (у нас уже есть)
7. НЕ добавляй license (у нас уже есть)
8. Create repository

### Шаг 2: Запушить код

```bash
cd /root/.openclaw/workspace/skills

git init
git branch -M main
git add .
git commit -m "🌺 Initial release: Deya OpenClaw Instance v1.0"

git remote add origin https://github.com/ТВОЙ_USERNAME/deya-openclaw.git
git push -u origin main
```

### Шаг 3: Добавить релиз

1. На GitHub перейди в раздел Releases
2. Click "Create a new release"
3. Tag: `v1.0.0`
4. Title: `🌺 Deya OpenClaw v1.0`
5. Описание:
```markdown
## Что включено

### 🛠️ 6 Скиллов
- deya-mode v1.0 — Персона Деи
- ui-ux-pro-max v1.1 — UI генератор + GSAP
- code-ninja v1.0 — Инструменты разработки
- web-hunter v1.0 — Web scraping
- deya-visual-identity v1.0 — Визуальная айдентика
- deya-dashboard v1.0 — Веб-интерфейс

### 🚀 Установка

**One-line:**
```bash
curl -fsSL https://raw.githubusercontent.com/ТВОЙ_USERNAME/deya-openclaw/main/install.sh | bash
```

**Docker:**
```bash
docker-compose up -d
```

### 📦 Файлы
- `deya-openclaw-v1.0.tar.gz` — Полный архив
```
6. Загрузи файл `deya-openclaw-v1.0.tar.gz`
7. Publish release

### Шаг 4: Настроить GitHub Actions (опционально)

Для автоматической сборки релизов:

1. Settings → Secrets and variables → Actions
2. New repository secret:
   - Name: `DOCKER_USERNAME`
   - Value: твой логин на Docker Hub
3. New repository secret:
   - Name: `DOCKER_PASSWORD`
   - Value: твой пароль или token

Теперь при создании тега `v*` будет автоматически:
- Собираться Docker образ
- Создаваться релиз
- Пушиться образ на Docker Hub

## 📊 После публикации

### Проверь:

```bash
# Клонировать свежий репо
cd /tmp
git clone https://github.com/ТВОЙ_USERNAME/deya-openclaw.git
cd deya-openclaw

# Проверить структуру
ls -la

# Проверить install.sh
./install-deya.sh
```

### Проверь веб-интерфейс:

1. Открой http://localhost:8001
2. Убедись, что все 7 страниц работают
3. Проверь чат с Деей

## 🔗 Полезные ссылки

- Репозиторий: https://github.com/ТВОЙ_USERNAME/deya-openclaw
- Релизы: https://github.com/ТВОЙ_USERNAME/deya-openclaw/releases
- Документация: https://github.com/ТВОЙ_USERNAME/deya-openclaw#readme

## 🎨 Кастомизация

### Изменить логотип:
1. Замени эмодзи 🌺 на свой в README.md
2. Добавь скриншоты в README

### Добавить badges:
```markdown
![Version](https://img.shields.io/badge/version-1.0.0-purple.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
```

### Настроить домен:
1. Купи домен deya.ai
2. Настрой GitHub Pages или Vercel
3. Обнови ссылки в README

## 🆘 Проблемы?

Если что-то не работает:

1. Проверь права доступа к файлам
2. Убедись, что все скрипты исполняемые: `chmod +x *.sh`
3. Проверь .gitignore — не игнорируются ли нужные файлы
4. Посмотри логи: `git log --oneline`

---

**Готово! Твой инстанс Деи теперь на GitHub! 🌺**
