#!/bin/bash
# Package all skills for release

set -e

VERSION="${1:-1.0.0}"
RELEASE_DIR="./release-${VERSION}"

echo "🌺 Packaging Deya OpenClaw Instance v${VERSION}"
echo ""

# Create release directory
mkdir -p "${RELEASE_DIR}"

# Copy install script
cp install-deya.sh "${RELEASE_DIR}/"
chmod +x "${RELEASE_DIR}/install-deya.sh"

# Copy Docker files
cp Dockerfile "${RELEASE_DIR}/"
cp docker-compose.yml "${RELEASE_DIR}/"
cp README-INSTANCE.md "${RELEASE_DIR}/README.md"

# Create config directory
mkdir -p "${RELEASE_DIR}/config"
cp config/*.md "${RELEASE_DIR}/config/" 2>/dev/null || echo "⚠️  Config files not found, will be generated"

# Create scripts directory
mkdir -p "${RELEASE_DIR}/scripts"
cp scripts/start.sh "${RELEASE_DIR}/scripts/"
chmod +x "${RELEASE_DIR}/scripts/start.sh"

# Copy all skill files
echo "📦 Copying skill files..."
for skill in *.skill; do
    if [ -f "$skill" ]; then
        cp "$skill" "${RELEASE_DIR}/"
        echo "   ✅ $skill"
    fi
done

# Create tarball
echo ""
echo "📦 Creating release archive..."
tar -czf "deya-openclaw-v${VERSION}.tar.gz" -C "${RELEASE_DIR}" .

# Create ZIP for Windows users
zip -r "deya-openclaw-v${VERSION}.zip" "${RELEASE_DIR}"

echo ""
echo "✅ Release v${VERSION} created!"
echo ""
echo "📁 Files:"
ls -lh "deya-openclaw-v${VERSION}".*
echo ""
echo "🚀 Upload to GitHub:"
echo "   gh release create v${VERSION} \\"
echo "     deya-openclaw-v${VERSION}.tar.gz \\"
echo "     deya-openclaw-v${VERSION}.zip \\"
echo "     --title \"Deya OpenClaw Instance v${VERSION}\""

# Cleanup
rm -rf "${RELEASE_DIR}"
