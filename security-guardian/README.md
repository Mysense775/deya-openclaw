# Security Guardian 🛡️

AI-ассистент для мониторинга безопасности. Сканирует сервер на уязвимости, отслеживает подозрительную активность, проверяет конфигурации, предупреждает об угрозах.

## 🚀 Быстрый старт

```bash
# Установка
cd skills/security-guardian
pip install -r requirements.txt

# Полный аудит безопасности
./scripts/security-audit.py --full --html report.html

# Проверка SSH
./scripts/security-audit.py --check ssh

# Мониторинг входов
./scripts/intrusion-detection.py --analyze --since 60

# Проверка сертификатов
./scripts/cert-monitor.py --check-all
```

## 📋 Скрипты

### 1. Security Audit
Полный аудит безопасности системы.

```bash
# Полный аудит с HTML отчётом
./security-audit.py --full --html report.html

# Проверка только SSH
./security-audit.py --check ssh

# Проверка firewall
./security-audit.py --check firewall

# JSON экспорт
./security-audit.py --full --json audit.json
```

**Проверяет:**
- ✅ SSH конфигурация (root login, password auth, port)
- ✅ Firewall (UFW/iptables статус)
- ✅ File permissions (SUID, world-writable)
- ✅ Services (опасные сервисы, exposed ports)
- ✅ Updates (security updates)
- ✅ Users (пустые пароли, sudoers)
- ✅ Kernel version

**Score:** 0-100 (чем выше, тем лучше)

### 2. Intrusion Detection
Обнаружение brute-force и подозрительной активности.

```bash
# Анализ последнего часа
./intrusion-detection.py --analyze --since 60

# Режим непрерывного мониторинга
./intrusion-detection.py --watch --interval 60

# С экспортом
./intrusion-detection.py --analyze --json threats.json
```

**Обнаруживает:**
- 🔴 Brute-force атаки (5+ попыток)
- 🟠 Подозрительные пользователи (много IP)
- 🔴 Успешный вход после множества попыток
- 🟢 Уже забаненные IP (fail2ban)

### 3. Certificate Monitor
Мониторинг SSL/TLS сертификатов.

```bash
# Проверка всех локальных сертификатов
./cert-monitor.py --check-all

# Проверка конкретного домена
./cert-monitor.py --domain airouter.host

# С проверкой конфигурации SSL
./cert-monitor.py --domain airouter.host --config
```

**Проверяет:**
- ✅ Срок действия (warning за 30 дней, critical за 7)
- ✅ Истёкшие сертификаты
- ✅ Слабые cipher suites
- ✅ Устаревшие протоколы (SSLv2, SSLv3)

## 🎯 Alert Levels

| Level | Описание | Действие |
|-------|----------|----------|
| 🔴 **CRITICAL** | Угроза компрометации | Немедленное действие |
| 🟠 **HIGH** | Серьёзная уязвимость | Исправить в течение 24ч |
| 🟡 **MEDIUM** | Проблема безопасности | Исправить в течение недели |
| 🟢 **LOW** | Рекомендация | Улучшить при возможности |
| ℹ️ **INFO** | Информация | Для сведения |

## 📊 Примеры использования

### Ежедневный аудит

```bash
# Утренний аудит
./security-audit.py --full --json /var/log/security/$(date +%Y%m%d).json

# Если score < 80, отправить алерт
if [ $? -ne 0 ]; then
    echo "Security issues detected" | telegram-send
fi
```

### Мониторинг brute-force

```bash
# Каждые 5 минут проверяем атаки
*/5 * * * * /root/.openclaw/workspace/skills/security-guardian/scripts/intrusion-detection.py --analyze --since 5 --json /tmp/threats.json && if [ $? -eq 2 ]; then echo "CRITICAL: Intrusion detected" | mail admin; fi
```

### Проверка сертификатов

```bash
# Раз в неделю проверяем сроки
0 9 * * 1 /root/.openclaw/workspace/skills/security-guardian/scripts/cert-monitor.py --check-all
```

## 🔧 Cron автоматизация

```bash
# /etc/crontab

# Security audit every day at 2:00
0 2 * * * root /root/.openclaw/workspace/skills/security-guardian/scripts/security-audit.py --full --html /var/www/security-report.html

# Intrusion detection every 5 minutes
*/5 * * * * root /root/.openclaw/workspace/skills/security-guardian/scripts/intrusion-detection.py --analyze --since 5

# Certificate check every Monday at 9:00
0 9 * * 1 root /root/.openclaw/workspace/skills/security-guardian/scripts/cert-monitor.py --check-all
```

## 📈 Рекомендации по безопасности

### SSH Hardening
```bash
# Отключить root login
PermitRootLogin no

# Отключить password auth
PasswordAuthentication no

# Сменить порт (опционально)
Port 2222

# Разрешить только Protocol 2
Protocol 2
```

### Firewall (UFW)
```bash
# Включить
ufw enable

# Default deny
ufw default deny incoming
ufw default allow outgoing

# Разрешить нужные порты
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
```

### Fail2ban
```bash
# Установить
apt install fail2ban

# Базовая конфигурация защитит от brute-force
systemctl enable fail2ban
systemctl start fail2ban
```

## 🔒 Безопасность

- Скрипты только читают конфигурации, не изменяют без `--auto-fix`
- Требуются root права для полного аудита
- Логи сохраняются локально
- Можно запускать в dry-run режиме

## 📄 License

MIT License

---

*Создано для защиты Deya Cloud* 🛡️🌺
