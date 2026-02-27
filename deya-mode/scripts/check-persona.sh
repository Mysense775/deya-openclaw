#!/bin/bash
# Check if Deya personality is properly configured

echo "🌺 Checking Deya Mode configuration..."

cd /root/.openclaw/workspace 2>/dev/null || {
    echo "❌ Workspace not found"
    exit 1
}

missing=0

if [ -f "SOUL.md" ]; then
    echo "✅ SOUL.md exists"
else
    echo "❌ SOUL.md missing"
    missing=$((missing + 1))
fi

if [ -f "IDENTITY.md" ]; then
    echo "✅ IDENTITY.md exists"
else
    echo "❌ IDENTITY.md missing"
    missing=$((missing + 1))
fi

if [ -f "USER.md" ]; then
    echo "✅ USER.md exists"
else
    echo "⚠️ USER.md missing (optional but recommended)"
fi

if [ $missing -eq 0 ]; then
    echo ""
    echo "🌺 Deya is fully configured and ready!"
else
    echo ""
    echo "⚠️ Run activate-deya.sh to fix missing files"
fi
