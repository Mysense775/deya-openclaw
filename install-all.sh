#!/bin/bash
# install-all.sh - Install all Deya v2.0 skills

echo "🌺 Deya v2.0 Installation Script"
echo "================================="
echo ""

SKILLS=(
    "content-creator-pro"
    "data-analyst"
    "devops-assistant"
    "email-master"
    "research-assistant"
    "security-guardian"
)

echo "📦 Skills to install: ${#SKILLS[@]}"
echo ""

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $python_version"

# Install skills
for skill in "${SKILLS[@]}"; do
    if [ -d "$skill" ]; then
        echo ""
        echo "🔧 Installing $skill..."
        cd "$skill" || continue
        
        if [ -f "requirements.txt" ]; then
            pip install -q -r requirements.txt
            echo "  ✓ Dependencies installed"
        fi
        
        # Make scripts executable
        if [ -d "scripts" ]; then
            chmod +x scripts/*.py 2>/dev/null
            echo "  ✓ Scripts made executable"
        fi
        
        cd .. || exit
    else
        echo "⚠️  $skill directory not found, skipping"
    fi
done

echo ""
echo "✅ Installation complete!"
echo ""
echo "📚 Quick start:"
echo "  cd content-creator-pro && ./scripts/post-generator.py --help"
echo "  cd devops-assistant && ./scripts/server-monitor.py --check"
echo "  cd data-analyst && ./scripts/data-processor.py --help"
echo ""
echo "📖 Read INSTALL-v2.md for detailed usage"
