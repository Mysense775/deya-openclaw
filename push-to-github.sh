#!/bin/bash
# Push Deya OpenClaw to GitHub
# Run this to publish the repository

cd /root/.openclaw/workspace/skills

echo "🌺 ПУБЛИКАЦИЯ НА GITHUB"
echo ""
echo "Репозиторий: https://github.com/Mysense775/deya-openclaw"
echo ""

# Check if we have credentials
if ! git config --global user.name &>/dev/null; then
    echo "Настройка git identity..."
    git config --global user.name "Mysense775"
    git config --global user.email "your@email.com"
fi

echo "📤 Отправка кода на GitHub..."
git push -u origin main --force

echo ""
echo "🏷️  Отправка тега v1.0.0..."
git push origin v1.0.0

echo ""
echo "✅ Код опубликован!"
echo ""
echo "🌐 Проверь: https://github.com/Mysense775/deya-openclaw"
echo ""

# Create release with file if gh is available
if command -v gh &> /dev/null; then
    echo "📦 Создание релиза через GitHub CLI..."
    gh release create v1.0.0 \
        deya-openclaw-v1.0.tar.gz \
        --title "🌺 Deya OpenClaw v1.0" \
        --notes "Complete instance with 6 skills and web dashboard"
    echo "✅ Релиз создан!"
else
    echo "⚠️  GitHub CLI не установлен"
    echo "📦 Загрузи файл deya-openclaw-v1.0.tar.gz вручную:"
    echo "   https://github.com/Mysense775/deya-openclaw/releases/new"
fi

echo ""
echo "🎉 ГОТОВО!"
echo ""
echo "🔗 Ссылки:"
echo "   Репозиторий: https://github.com/Mysense775/deya-openclaw"
echo "   Релизы: https://github.com/Mysense775/deya-openclaw/releases"
