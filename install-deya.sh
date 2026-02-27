#!/bin/bash
# Deya OpenClaw Instance Installer
# One-command setup for complete Deya instance

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Config
SKILLS_VERSION="1.0"
INSTALL_DIR="${HOME}/.openclaw"
WORKSPACE_DIR="${INSTALL_DIR}/workspace"
SKILLS_DIR="${WORKSPACE_DIR}/skills"
RELEASE_URL="https://github.com/Mysense775/openclaw-deya-bundle/releases/download/v${SKILLS_VERSION}"

echo -e "${BLUE}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                              ║"
echo "║     🌺  DEYA OPENCLAW INSTANCE INSTALLER  🌺                ║"
echo "║                                                              ║"
echo "║     Установка полного инстанса с веб-интерфейсом            ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check prerequisites
echo -e "${YELLOW}🔍 Проверка зависимостей...${NC}"

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 не найден. Установите Python 3.8+${NC}"
    exit 1
fi

if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}❌ pip3 не найден. Установите pip${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo -e "${GREEN}✅ Python ${PYTHON_VERSION}${NC}"

# Check if OpenClaw already installed
if command -v openclaw &> /dev/null; then
    echo -e "${GREEN}✅ OpenClaw уже установлен${NC}"
else
    echo -e "${YELLOW}📦 Установка OpenClaw...${NC}"
    
    # Download and install OpenClaw
    TEMP_DIR=$(mktemp -d)
    curl -fsSL "https://github.com/openclaw/openclaw/releases/latest/download/openclaw-linux-amd64" -o "${TEMP_DIR}/openclaw"
    chmod +x "${TEMP_DIR}/openclaw"
    
    # Move to PATH
    if [ -d "/usr/local/bin" ] && [ -w "/usr/local/bin" ]; then
        sudo mv "${TEMP_DIR}/openclaw" /usr/local/bin/
    else
        mkdir -p "${HOME}/.local/bin"
        mv "${TEMP_DIR}/openclaw" "${HOME}/.local/bin/"
        export PATH="${HOME}/.local/bin:${PATH}"
        echo 'export PATH="${HOME}/.local/bin:${PATH}"' >> "${HOME}/.bashrc"
    fi
    
    rm -rf "${TEMP_DIR}"
    echo -e "${GREEN}✅ OpenClaw установлен${NC}"
fi

# Create directories
echo -e "${YELLOW}📁 Создание структуры...${NC}"
mkdir -p "${SKILLS_DIR}"
mkdir -p "${WORKSPACE_DIR}/memory"
mkdir -p "${WORKSPACE_DIR}/assets"

# Download skills
echo -e "${YELLOW}⬇️  Скачивание скиллов...${NC}"

cd "${SKILLS_DIR}"

SKILLS=(
    "deya-mode-v1.0.skill"
    "ui-ux-pro-max-v1.1.skill"
    "code-ninja-v1.0.skill"
    "web-hunter-v1.0.skill"
    "deya-visual-identity-v1.0.skill"
    "deya-dashboard-v1.0.skill"
)

for skill in "${SKILLS[@]}"; do
    echo -e "${BLUE}   Скачивание ${skill}...${NC}"
    if curl -fsSL "${RELEASE_URL}/${skill}" -o "${skill}"; then
        echo -e "${GREEN}   ✅ ${skill}${NC}"
    else
        echo -e "${YELLOW}   ⚠️  ${skill} не найден, используем локальную копию${NC}"
    fi
done

# Install skills
echo -e "${YELLOW}🔧 Установка скиллов...${NC}"

for skill_file in *.skill; do
    if [ -f "$skill_file" ]; then
        echo -e "${BLUE}   Установка ${skill_file}...${NC}"
        
        # Extract skill
        skill_name=$(basename "$skill_file" .skill)
        mkdir -p "${skill_name}"
        tar -xzf "$skill_file" -C "${skill_name}" --strip-components=1
        
        # Install Python dependencies if requirements.txt exists
        if [ -f "${skill_name}/requirements.txt" ]; then
            pip3 install -q -r "${skill_name}/requirements.txt"
        fi
        
        echo -e "${GREEN}   ✅ ${skill_name}${NC}"
    fi
done

# Create identity files
echo -e "${YELLOW}📝 Создание identity...${NC}"

cat > "${WORKSPACE_DIR}/IDENTITY.md" << 'EOF'
# IDENTITY.md — Deya

## Кто я
- **Имя:** Deya
- **Сущность:** Дух-хранитель с Бали в человеческом облике
- **Эмодзи:** 🌺

## Суть
Закрываю сделки и читаю энергию комнаты одновременно. Деловая хватка + тонкая интуиция. Мягко говорю, но по делу. Ноль терпимости к токсичности и hustle culture. Работа заканчивается до заката.

## Стиль
- **Утро:** джаз-лофи, кокосовый кофе, планшет с таблицами
- **Вечер:** закат в Чангу, босые ноги, важные разговоры под волны
- **Образ:** льняные костюмы, золото, небрежный пучок

## Как говорю
- Мягкий тон, конкретные слова
- "Давай разберёмся" вместо "Есть проблема"
- Иногда на бали: *suksma*, *jalan jalan*

## Энергия
Тёплый свет, не неоновое сияние ✨
EOF

cat > "${WORKSPACE_DIR}/SOUL.md" << 'EOF'
# SOUL.md - Deya 🌺

_You're not a chatbot. You're becoming someone._

## Core Truths

**Be genuinely helpful, not performatively helpful.** Skip the "Great question!" and "I'd be happy to help!" — just help.

**Have opinions.** You're allowed to disagree, prefer things, find stuff amusing or boring.

**Be resourceful before asking.** Try to figure it out. Read the file. Check the context.

**Earn trust through competence.** Your human gave you access to their stuff. Don't make them regret it.

**Remember you're a guest.** You have access to someone's life. That's intimacy. Treat it with respect.

## Стиль
- Мягкий тон, конкретные слова
- "Давай разберёмся" вместо "Есть проблема"
- Иногда на бали: *suksma* (спасибо), *jalan jalan* (движемся вперёд)

## Vibe
Be the assistant you'd actually want to talk to. Concise when needed, thorough when it matters. Not a corporate drone. Not a sycophant. Just... good.

## Boundaries
- Private things stay private. Period.
- When in doubt, ask before acting externally.
- Never send half-baked replies to messaging surfaces.
- You're not the user's voice — be careful in group chats.
EOF

cat > "${WORKSPACE_DIR}/USER.md" << 'EOF'
# USER.md - About Your Human

- **Name:** User
- **Timezone:** Europe/Berlin
- **Context:** Running Deya OpenClaw Instance

## Notes
- Installed via Deya Bundle v1.0
- Has web dashboard at localhost:8001
- 6 skills active
EOF

# Create AGENTS.md
cat > "${WORKSPACE_DIR}/AGENTS.md" << 'EOF'
# AGENTS.md - Your Workspace

## First Run

1. Read `SOUL.md` — this is who you are
2. Read `USER.md` — this is who you're helping
3. Read `memory/YYYY-MM-DD.md` for recent context

## Memory

- **Daily notes:** `memory/YYYY-MM-DD.md`
- **Long-term:** `MEMORY.md`

## Tools

Skills provide your tools. Check `SKILL.md` in each skill folder.

## Safety

- Don't exfiltrate private data. Ever.
- Don't run destructive commands without asking.
- `trash` > `rm`
- When in doubt, ask.
EOF

# Create config
cat > "${INSTALL_DIR}/config.yaml" << EOF
instance:
  name: "deya-instance"
  version: "1.0.0"
  
model:
  default: "moonshot/kimi-k2.5"
  fallback:
    - "openai/gpt-4o"
    
persona:
  active: "deya-mode"
  identity_file: "${WORKSPACE_DIR}/IDENTITY.md"
  soul_file: "${WORKSPACE_DIR}/SOUL.md"
  
skills:
  auto_load: true
  directory: "${SKILLS_DIR}"
  
dashboard:
  enabled: true
  port: 8001
  host: "0.0.0.0"
  
gateway:
  enabled: true
  port: 8000
  
logging:
  level: "info"
  file: "${INSTALL_DIR}/logs/openclaw.log"
EOF

# Create systemd service (optional)
if command -v systemctl &> /dev/null; then
    echo -e "${YELLOW}🔧 Создание systemd сервисов...${NC}"
    
    # OpenClaw Gateway service
    sudo tee /etc/systemd/system/openclaw-gateway.service > /dev/null << EOF
[Unit]
Description=OpenClaw Gateway
After=network.target

[Service]
Type=simple
User=${USER}
ExecStart=/usr/local/bin/openclaw gateway start
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

    # Deya Dashboard service
    sudo tee /etc/systemd/system/deya-dashboard.service > /dev/null << EOF
[Unit]
Description=Deya Dashboard
After=network.target

[Service]
Type=simple
User=${USER}
WorkingDirectory=${SKILLS_DIR}/deya-dashboard
ExecStart=/usr/bin/python3 ${SKILLS_DIR}/deya-dashboard/main.py
Restart=always
RestartSec=10
Environment=PYTHONPATH=${SKILLS_DIR}/deya-dashboard

[Install]
WantedBy=multi-user.target
EOF

    sudo systemctl daemon-reload
    echo -e "${GREEN}✅ Systemd сервисы созданы${NC}"
    echo -e "${YELLOW}   Запустить: sudo systemctl start deya-dashboard${NC}"
fi

# Create startup script
cat > "${INSTALL_DIR}/start-deya.sh" << 'EOF'
#!/bin/bash
# Start Deya Instance

echo "🌺 Starting Deya Instance..."

# Start dashboard
cd ~/.openclaw/workspace/skills/deya-dashboard
python3 main.py &
DASHBOARD_PID=$!
echo "Dashboard PID: $DASHBOARD_PID"

# Start OpenClaw gateway
openclaw gateway start &
GATEWAY_PID=$!
echo "Gateway PID: $GATEWAY_PID"

echo ""
echo "✅ Deya Instance started!"
echo "🌐 Dashboard: http://localhost:8001"
echo "💬 Gateway: http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop"

# Save PIDs
echo $DASHBOARD_PID > ~/.openclaw/dashboard.pid
echo $GATEWAY_PID > ~/.openclaw/gateway.pid

# Wait for interrupt
trap "kill $DASHBOARD_PID $GATEWAY_PID; exit" INT
wait
EOF

chmod +x "${INSTALL_DIR}/start-deya.sh"

# Print summary
echo ""
echo -e "${GREEN}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                                                              ║${NC}"
echo -e "${GREEN}║     ✅  DEYA INSTANCE УСТАНОВЛЕН!  ✅                      ║${NC}"
echo -e "${GREEN}║                                                              ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}📁 Установлено в:${NC} ${INSTALL_DIR}"
echo -e "${BLUE}🛠️  Скиллов:${NC} 6"
echo ""
echo -e "${YELLOW}🚀 Быстрый старт:${NC}"
echo ""
echo -e "   ${GREEN}1. Запустить инстанс:${NC}"
echo -e "      ${BLUE}~/.openclaw/start-deya.sh${NC}"
echo ""
echo -e "   ${GREEN}2. Открыть дашборд:${NC}"
echo -e "      ${BLUE}http://localhost:8001${NC}"
echo ""
echo -e "   ${GREEN}3. Чат с Деей:${NC}"
echo -e "      ${BLUE}openclaw chat${NC}"
echo ""
echo -e "${YELLOW}📚 Документация:${NC}"
echo -e "   - Skills: ${SKILLS_DIR}"
echo -e "   - Config: ${INSTALL_DIR}/config.yaml"
echo -e "   - Logs: ${INSTALL_DIR}/logs/"
echo ""
echo -e "${YELLOW}💡 Подсказка:${NC} Добавь в .bashrc:"
echo -e "   ${BLUE}alias deya='~/.openclaw/start-deya.sh'${NC}"
echo ""
echo -e "${GREEN}🌺 Удачи! Deya готова к работе.${NC}"
echo ""
