# Security Guardian

AI-ассистент для мониторинга безопасности. Сканирует сервер на уязвимости, отслеживает подозрительную активность, проверяет конфигурации, предупреждает об угрозах.

## Capabilities

- **Security Audit**: Проверка конфигураций SSH, firewall, прав доступа
- **Vulnerability Scan**: Сканирование на известные уязвимости
- **Intrusion Detection**: Обнаружение подозрительной активности (brute-force, сканирование портов)
- **Log Monitoring**: Анализ auth.log, syslog на признаки атак
- **Compliance Check**: Проверка соответствия best practices (CIS benchmarks)
- **Malware Detection**: Поиск подозрительных процессов и файлов
- **Certificate Monitoring**: Отслеживание сроков действия SSL сертификатов
- **Alert System**: Уведомления о критических угрозах

## Usage

```bash
# Полный аудит безопасности
python scripts/security-audit.py --full --report html

# Проверка SSH конфигурации
python scripts/security-audit.py --check ssh

# Сканирование уязвимостей
python scripts/vulnerability-scan.py --port-range 1-65535

# Мониторинг входов
python scripts/intrusion-detection.py --watch --alert-telegram

# Проверка сертификатов
python scripts/cert-monitor.py --domain airouter.host

# Автоматический фикс базовых проблем
python scripts/security-audit.py --auto-fix
```

## Features

### Security Checks
- **SSH**: root login, password auth, port, keys
- **Firewall**: UFW/iptables статус, открытые порты
- **File Permissions**: SUID/SGID файлы, world-writable
- **Services**: Ненужные сервисы, exposed ports
- **Users**: Пустые пароли, неиспользуемые аккаунты
- **Updates**: Доступные security updates
- **Kernel**: Live patching, версия

### Vulnerability Detection
- Open ports scanning
- Service version fingerprinting
- CVE database lookup
- Weak SSL/TLS configurations
- Default credentials check

### Intrusion Detection
- Failed login attempts
- Brute-force detection
- Port scanning detection
- New user/process alerts
- File integrity monitoring
- Suspicious cron jobs

### Reports
- HTML report with recommendations
- JSON for automation
- Priority levels (Critical/High/Medium/Low)
- Remediation steps

## Alert Levels

- **CRITICAL**: Угроза компрометации системы (немедленное действие)
- **HIGH**: Серьёзная уязвимость (исправить в течение 24ч)
- **MEDIUM**: Проблема безопасности (исправить в течение недели)
- **LOW**: Рекомендация (улучшение безопасности)
- **INFO**: Информация

## Requirements

- Python 3.9+
- nmap (для сканирования портов)
- lynis (для аудита, опционально)
- ss/nc (для проверки сети)
- openssl (для проверки сертификатов)
- root/sudo для полного аудита

## Installation

```bash
cd skills/security-guardian
pip install -r requirements.txt

# Установка зависимостей системы
apt-get install -y nmap lynis openssl
```

## Automation

```bash
# Ежедневный аудит в 2:00
0 2 * * * /root/.openclaw/workspace/skills/security-guardian/scripts/security-audit.py --json /var/log/security-audit.json

# Мониторинг входов каждую минуту
* * * * * /root/.openclaw/workspace/skills/security-guardian/scripts/intrusion-detection.py --check

# Проверка сертификатов раз в неделю
0 9 * * 1 /root/.openclaw/workspace/skills/security-guardian/scripts/cert-monitor.py --check-all
```

## Safety

- Только проверки, не изменяет систему без `--auto-fix`
- Бэкап перед применением фиксов
- Логирование всех действий
- Возможность dry-run

## License

MIT
