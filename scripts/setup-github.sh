#!/bin/bash
# Initialize and push to GitHub
# Usage: ./scripts/setup-github.sh

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}"
echo "╔══════════════════════════════════════════════════════════╗"
echo "║                                                          ║"
echo "║     🌺  GITHUB SETUP FOR DEYA OPENCLAW INSTANCE  🌺     ║"
echo "║                                                          ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo -e "${RED}❌ Git не установлен${NC}"
    exit 1
fi

# Get GitHub repo info
echo -e "${YELLOW}Введите информацию о репозитории GitHub:${NC}"
read -p "GitHub username: " USERNAME
read -p "Repository name [deya-openclaw]: " REPO_NAME
REPO_NAME=${REPO_NAME:-deya-openclaw}
read -p "Repository description: " DESCRIPTION

REMOTE_URL="https://github.com/${USERNAME}/${REPO_NAME}.git"

echo ""
echo -e "${BLUE}Настройка репозитория:${NC}"
echo "  Username: $USERNAME"
echo "  Repo: $REPO_NAME"
echo "  URL: $REMOTE_URL"
echo ""

# Check if already a git repo
if [ -d ".git" ]; then
    echo -e "${YELLOW}⚠️  Git репозиторий уже существует${NC}"
    read -p "Пересоздать? (y/n): " REINIT
    if [ "$REINIT" = "y" ]; then
        rm -rf .git
    else
        echo -e "${YELLOW}Используем существующий репозиторий${NC}"
    fi
fi

# Initialize git repo
if [ ! -d ".git" ]; then
    echo -e "${BLUE}🔧 Инициализация git репозитория...${NC}"
    git init
    git branch -M main
fi

# Rename README for GitHub
echo -e "${BLUE}📝 Подготовка README.md...${NC}"
cp README-GITHUB.md README.md

# Add all files
echo -e "${BLUE}➕ Добавление файлов...${NC}"
git add README.md LICENSE .gitignore CONTRIBUTING.md Dockerfile docker-compose.yml install-deya.sh
git add config/ scripts/ .github/

# Add skill source folders (not .skill files - they're in releases)
git add deya-mode/ ui-ux-pro-max/ code-ninja/ web-hunter/ deya-visual-identity/ deya-dashboard/

# Commit
echo -e "${BLUE}💾 Создание коммита...${NC}"
git commit -m "🌺 Initial release: Deya OpenClaw Instance v1.0

Complete instance with:
- 6 skills (deya-mode, ui-ux-pro-max, code-ninja, web-hunter, deya-visual-identity, deya-dashboard)
- Web dashboard (7 pages)
- One-line installer
- Docker support
- Full documentation

Ready to use: curl -fsSL https://get.deya.ai | bash"

# Add remote
echo -e "${BLUE}🔗 Добавление remote...${NC}"
git remote add origin "$REMOTE_URL" 2>/dev/null || git remote set-url origin "$REMOTE_URL"

# Instructions for pushing
echo ""
echo -e "${GREEN}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                                                          ║${NC}"
echo -e "${GREEN}║  ✅  РЕПОЗИТОРИЙ ГОТОВ!  ✅                            ║${NC}"
echo -e "${GREEN}║                                                          ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${YELLOW}Следующие шаги:${NC}"
echo ""
echo -e "${BLUE}1. Создайте репозиторий на GitHub:${NC}"
echo "   https://github.com/new"
echo "   Название: ${REPO_NAME}"
echo "   Описание: ${DESCRIPTION}"
echo ""
echo -e "${BLUE}2. Запушьте код:${NC}"
echo -e "   ${GREEN}git push -u origin main${NC}"
echo ""
echo -e "${BLUE}3. Создайте Personal Access Token (для releases):${NC}"
echo "   https://github.com/settings/tokens"
echo "   Нужные права: repo, workflow"
echo ""
echo -e "${BLUE}4. Настройте GitHub Actions secrets:${NC}"
echo "   https://github.com/${USERNAME}/${REPO_NAME}/settings/secrets/actions"
echo "   - DOCKER_USERNAME"
echo "   - DOCKER_PASSWORD"
echo ""
echo -e "${BLUE}5. Создайте первый релиз:${NC}"
echo -e "   ${GREEN}git tag v1.0.0${NC}"
echo -e "   ${GREEN}git push origin v1.0.0${NC}"
echo ""
echo -e "${YELLOW}Или используйте GitHub CLI:${NC}"
echo -e "   ${GREEN}gh repo create ${REPO_NAME} --public --source=. --remote=origin --push${NC}"
echo -e "   ${GREEN}gh release create v1.0.0 deya-openclaw-v1.0.tar.gz --title \"v1.0.0\" --notes \"Initial release\"${NC}"
echo ""
echo -e "${GREEN}🌺 Удачи!${NC}"
echo ""
