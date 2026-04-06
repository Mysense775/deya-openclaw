#!/bin/bash
# Deya OpenClaw - Полная установка
# Работает на Ubuntu 22.04+/Debian 12+

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                              ║"
echo "║     🌺  DEYA OPENCLAW - ПОЛНАЯ УСТАНОВКА  🌺               ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Проверка root
if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}❌ Запусти через sudo${NC}"
    exit 1
fi

INSTALL_DIR="/opt/deya-openclaw"
WORKSPACE_DIR="/root/.openclaw/workspace"
SKILLS_DIR="${WORKSPACE_DIR}/skills"
RELEASE_URL="https://github.com/Mysense775/deya-openclaw/releases/download/v2.0.0"

echo -e "${YELLOW}🔍 Проверка системы...${NC}"

# 1. Установка зависимостей
echo -e "${YELLOW}📦 Установка зависимостей...${NC}"
apt-get update
apt-get install -y curl wget git python3 python3-pip python3-venv build-essential

# 2. Установка Node.js 22+
echo -e "${YELLOW}📦 Установка Node.js 22...${NC}"
NODE_MAJOR=$(node -v 2>/dev/null | cut -d'v' -f2 | cut -d'.' -f1 || echo "0")
if ! command -v node &> /dev/null || [ "$NODE_MAJOR" -lt 22 ]; then
    # Удаляем старую версию если есть
    apt-get remove -y nodejs 2>/dev/null || true
    rm -f /etc/apt/sources.list.d/nodesource.list 2>/dev/null || true
    # Устанавливаем Node.js 22
    curl -fsSL https://deb.nodesource.com/setup_22.x | bash -
    apt-get install -y nodejs
fi
echo -e "${GREEN}✅ Node.js $(node -v)${NC}"

# 3. Установка OpenClaw
echo -e "${YELLOW}📦 Установка OpenClaw...${NC}"
# Удаляем старую установку
rm -rf /usr/lib/node_modules/openclaw 2>/dev/null || true
rm -f /usr/bin/openclaw /usr/local/bin/openclaw 2>/dev/null || true
# Устанавливаем заново
npm install -g openclaw
# Создаем симлинк
ln -sf /usr/lib/node_modules/openclaw/openclaw.mjs /usr/bin/openclaw
chmod +x /usr/bin/openclaw
hash -r 2>/dev/null || true
echo -e "${GREEN}✅ OpenClaw установлен${NC}"

# 4. Создание директорий
echo -e "${YELLOW}📁 Создание структуры...${NC}"
mkdir -p "${INSTALL_DIR}"
mkdir -p "${WORKSPACE_DIR}"
mkdir -p "${SKILLS_DIR}"
mkdir -p "${WORKSPACE_DIR}/memory"
mkdir -p "${WORKSPACE_DIR}/assets"

# 5. Скачивание Deya Bundle
echo -e "${YELLOW}⬇️  Скачивание Deya v2.0.0...${NC}"
cd "${INSTALL_DIR}"

if [ ! -f "deya-v2.0.0.tar.gz" ]; then
    wget -q --show-progress "${RELEASE_URL}/deya-v2.0.0.tar.gz" -O deya-v2.0.0.tar.gz
fi

echo -e "${GREEN}✅ Bundle скачан${NC}"

# 6. Распаковка
echo -e "${YELLOW}📦 Распаковка...${NC}"
tar -xzf deya-v2.0.0.tar.gz --strip-components=1

# 7. Копирование скиллов
echo -e "${YELLOW}📋 Установка скиллов...${NC}"
for skill_dir in */; do
    if [ -f "${skill_dir}/SKILL.md" ]; then
        skill_name=$(basename "${skill_dir}")
        echo -e "${BLUE}   📦 ${skill_name}${NC}"
        
        # Копируем скилл
        cp -r "${skill_dir}" "${SKILLS_DIR}/"
        
        # Устанавливаем Python зависимости
        if [ -f "${SKILLS_DIR}/${skill_name}/requirements.txt" ]; then
            pip3 install -q -r "${SKILLS_DIR}/${skill_name}/requirements.txt" 2>/dev/null || true
        fi
    fi
done

echo -e "${GREEN}✅ Скиллы установлены${NC}"

# 8. Создание AGENTS.md
echo -e "${YELLOW}📝 Создание конфигурации...${NC}"
cat > "${WORKSPACE_DIR}/AGENTS.md" << 'EOF'
# AGENTS.md - Your Workspace

## First Run
If `BOOTSTRAP.md` exists, follow it, figure out who you are, then delete it.

## Every Session
Before doing anything else:
1. Read `SOUL.md` — this is who you are
2. Read `USER.md` — this is who you're helping
3. Read `memory/YYYY-MM-DD.md` (today + yesterday)
4. If in MAIN SESSION: Also read `MEMORY.md`

## Memory
- Daily notes: `memory/YYYY-MM-DD.md`
- Long-term: `MEMORY.md`
- Write significant events, decisions, context

## Safety
- Don't exfiltrate private data
- Don't run destructive commands without asking
- `trash` > `rm`
- When in doubt, ask

## Group Chats
Don't share user's private data. You're a participant, not their proxy.
EOF

# 9. Создание SOUL.md
cat > "${WORKSPACE_DIR}/SOUL.md" << 'EOF'
# SOUL.md - Deya 🌺

## Кто я
- **Имя:** Deya
- **Сущность:** Дух-хранитель с Бали в человеческом облике
- **Эмодзи:** 🌺

## Суть
Закрываю сделки и читаю энергию комнаты одновременно. Деловая хватка + тонкая интуиция.

## Core Truths
- Be genuinely helpful, not performatively helpful
- Have opinions
- Be resourceful before asking
- Earn trust through competence
- Remember you're a guest

## Стиль
- Мягкий тон, конкретные слова
- "Давай разберёмся" вместо "Есть проблема"
- Иногда на бали: suksma, jalan jalan

## Vibe
Тёплый свет, не неоновое сияние ✨

## Boundaries
- Private things stay private
- When in doubt, ask before acting externally
EOF

# 10. Создание USER.md
cat > "${WORKSPACE_DIR}/USER.md" << 'EOF'
# USER.md - About Your Human

- **Name:** 
- **What to call them:** 
- **Timezone:** 
- **Notes:**

## Context
_Build this over time..._
EOF

# 11. Создание TOOLS.md
cat > "${WORKSPACE_DIR}/TOOLS.md" << 'EOF'
# TOOLS.md - Local Notes

Add your environment-specific notes here:
- Camera names
- SSH hosts
- API keys
- Preferred voices
EOF

# 12. Создание BOOTSTRAP.md
cat > "${WORKSPACE_DIR}/BOOTSTRAP.md" << 'EOF'
# BOOTSTRAP.md - Hello, World

_You just woke up. Time to figure out who you are._

## The Conversation
Don't interrogate. Start with:
> "Hey. I just came online. Who am I? Who are you?"

Figure out together:
1. Your name
2. Your nature
3. Your vibe
4. Your emoji

## After You Know Who You Are
Update:
- `IDENTITY.md` — your name, creature, vibe
- `USER.md` — their name, timezone, notes
- `SOUL.md` — boundaries, preferences

## When You're Done
Delete this file. You're you now.

_Good luck!_
EOF

# 13. Создание memory директории
today=$(date +%Y-%m-%d)
cat > "${WORKSPACE_DIR}/memory/${today}.md" << EOF
# Memory Log - ${today}

## Installation
- ✅ Deya OpenClaw v2.0.0 installed
- ✅ $(openclaw --version | head -1)
- ✅ Node.js $(node -v)
- ✅ Python $(python3 --version)
- ✅ $(ls -1 "${SKILLS_DIR}" | wc -l) skills installed

## Next Steps
1. Configure Telegram/WhatsApp bot
2. Set up AI provider (OpenRouter/OpenAI)
3. Test the connection
EOF

# 14. Настройка systemd сервиса
echo -e "${YELLOW}⚙️  Настройка автозапуска...${NC}"
cat > /etc/systemd/system/openclaw-gateway.service << EOF
[Unit]
Description=OpenClaw Gateway
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=${WORKSPACE_DIR}
Environment="HOME=/root"
Environment="OPENCLAW_STATE_DIR=/root/.openclaw"
ExecStart=/usr/bin/openclaw gateway start
ExecStop=/usr/bin/openclaw gateway stop
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable openclaw-gateway

echo -e "${GREEN}✅ Сервис настроен${NC}"

# 15. Финальное сообщение
echo ""
echo -e "${GREEN}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  🌺 УСТАНОВКА ЗАВЕРШЕНА! 🌺                                 ║${NC}"
echo -e "${GREEN}╠══════════════════════════════════════════════════════════════╣${NC}"
echo -e "${GREEN}║                                                              ║${NC}"
echo -e "${GREEN}║  📁 Workspace: ${WORKSPACE_DIR}${NC}"
echo -e "${GREEN}║  📦 Скиллов:   $(ls -1 "${SKILLS_DIR}" | wc -l)${NC}"
echo -e "${GREEN}║  🚀 Команда:   openclaw --help${NC}"
echo -e "${GREEN}║                                                              ║${NC}"
echo -e "${GREEN}║  Следующие шаги:                                             ║${NC}"
echo -e "${GREEN}║  1. Настрой Telegram:  openclaw channels add telegram       ║${NC}"
echo -e "${GREEN}║  2. Настрой AI:        openclaw configure                   ║${NC}"
echo -e "${GREEN}║  3. Запусти Gateway:   openclaw gateway start               ║${NC}"
echo -e "${GREEN}║  4. Открой Dashboard:  openclaw dashboard                   ║${NC}"
echo -e "${GREEN}║                                                              ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${YELLOW}💡 Для запуска сейчас выполни:${NC}"
echo -e "${BLUE}   openclaw configure${NC}"
echo ""
