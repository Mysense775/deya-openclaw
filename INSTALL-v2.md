# Deya v2.0.0 🌺

**Complete AI Assistant Suite - Ready for Installation**

[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](https://github.com/Mysense775/deya-openclaw/releases/tag/v2.0.0)
[![Skills](https://img.shields.io/badge/skills-10-green.svg)](#skills)
[![License](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)

## 🚀 Quick Install

### Option 1: Direct Download (Recommended)

```bash
# Download latest release
curl -L -o deya-v2.0.0.tar.gz https://github.com/Mysense775/deya-openclaw/releases/download/v2.0.0/deya-v2.0.0.tar.gz

# Extract
tar -xzf deya-v2.0.0.tar.gz
cd deya-openclaw

# Install dependencies for all skills
./install-all.sh
```

### Option 2: Git Clone

```bash
# Clone repository
git clone https://github.com/Mysense775/deya-openclaw.git
cd deya-openclaw

# Checkout v2.0.0
git checkout v2.0.0

# Install all skills
./install-all.sh
```

## 📦 What's Included

### Core Skills (4)

| Skill | Description | Scripts |
|-------|-------------|---------|
| `deya-mode` | Personality engine, behavior, mood detection | 5 scripts |
| `ui-ux-pro-max` | React component generator with animations | 6 components |
| `code-ninja` | Code analysis, debugging, refactoring | 4 analyzers |
| `web-hunter` | Web scraping, search aggregation | 5 tools |

### New in v2.0 (6 skills)

| Skill | Description | Scripts |
|-------|-------------|---------|
| `content-creator-pro` | Social media content, posts, hashtags | 4 scripts |
| `devops-assistant` | Docker, monitoring, backups | 4 scripts |
| `data-analyst` | Data processing, metrics (LTV, CAC) | 3 scripts |
| `email-master` | Email composition, templates | 3 scripts |
| `research-assistant` | Topic research, fact checking | 3 scripts |
| `security-guardian` | Security audits, intrusion detection | 3 scripts |

**Total: 10 skills | 40+ scripts | ~450KB of code**

## 🛠️ Individual Skill Installation

### Content Creator Pro
```bash
cd content-creator-pro
pip install -r requirements.txt
./scripts/content-planner.py --help
```

### DevOps Assistant
```bash
cd devops-assistant
pip install -r requirements.txt
./scripts/container-manager.py --list
```

### Data Analyst
```bash
cd data-analyst
pip install -r requirements.txt
./scripts/data-processor.py --file data.csv --analyze
```

### Email Master
```bash
cd email-master
pip install -r requirements.txt
./scripts/email-composer.py --type introduction --to "Client"
```

### Research Assistant
```bash
cd research-assistant
pip install -r requirements.txt
./scripts/topic-researcher.py --topic "AI trends" --depth deep
```

### Security Guardian
```bash
cd security-guardian
pip install -r requirements.txt
./scripts/security-audit.py --full
```

## 📋 Requirements

- Python 3.9+
- Linux/macOS (some scripts work on Windows)
- Docker (for DevOps Assistant)
- API keys (optional, for external services)

## 🎯 Usage Examples

### Create social media content
```bash
cd content-creator-pro
./scripts/post-generator.py --type story --topic "Morning routine" --tone warm
```

### Monitor your server
```bash
cd devops-assistant
./scripts/server-monitor.py --watch
```

### Analyze business metrics
```bash
cd data-analyst
./scripts/metrics-calculator.py --file customers.csv --metric ltv
```

### Research a topic
```bash
cd research-assistant
./scripts/fact-checker.py --claim "Python 4 will release in 2027"
```

### Security audit
```bash
cd security-guardian
./scripts/security-audit.py --full --html report.html
```

## 🔧 Configuration

### Environment Variables

Create `.env` file in skill directories:

```bash
# For Email Master
SMTP_HOST=smtp.gmail.com
SMTP_USER=your-email@gmail.com

# For Research Assistant (optional)
REDDIT_CLIENT_ID=xxx
REDDIT_CLIENT_SECRET=xxx
```

### Telegram Integration

For skills that send notifications:

```bash
export TELEGRAM_BOT_TOKEN=your_token
export TELEGRAM_CHAT_ID=your_chat_id
```

## 📚 Documentation

Each skill has its own README with detailed usage:
- `content-creator-pro/README.md`
- `data-analyst/README.md`
- `devops-assistant/README.md`
- `email-master/README.md`
- `research-assistant/README.md`
- `security-guardian/README.md`

## 🔄 Updates

To update to latest version:

```bash
git pull origin main
# or
git checkout v2.1.0  # when available
```

## 🐛 Troubleshooting

### Permission denied
```bash
chmod +x */scripts/*.py
```

### Missing dependencies
```bash
pip install -r requirements.txt
```

### Docker not found (for DevOps)
```bash
sudo apt install docker.io
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing`)
5. Open Pull Request

## 📄 License

MIT License - see LICENSE file

## 🔗 Links

- **Repository**: https://github.com/Mysense775/deya-openclaw
- **Releases**: https://github.com/Mysense775/deya-openclaw/releases
- **Latest**: https://github.com/Mysense775/deya-openclaw/releases/tag/v2.0.0

---

**Made with 💜 by Deya**  
*Your AI assistant from Bali* 🌺
