# DevOps Assistant

AI-ассистент для управления инфраструктурой. Мониторит сервера, управляет Docker, делает бэкапы, анализирует логи и предупреждает о проблемах.

## Capabilities

- **Container Management**: Управление Docker контейнерами (старт, стоп, статус, логи)
- **Server Monitoring**: Мониторинг CPU, RAM, диска, сети в реальном времени
- **Backup Automation**: Автоматические бэкапы баз данных и файлов
- **Log Analysis**: Анализ логов на ошибки и аномалии
- **Alert System**: Уведомления в Telegram о критических событиях
- **Health Checks**: Проверка доступности сервисов
- **Resource Optimization**: Рекомендации по оптимизации ресурсов

## Usage

```bash
# Управление контейнерами
python scripts/container-manager.py --list
python scripts/container-manager.py --restart airouter-backend
python scripts/container-manager.py --logs airouter-frontend --tail 100

# Мониторинг сервера
python scripts/server-monitor.py --watch
python scripts/server-monitor.py --alert --threshold-cpu 80

# Бэкапы
python scripts/backup-automation.py --create --target db --dest /backup
python scripts/backup-automation.py --schedule daily --time 03:00

# Анализ логов
python scripts/log-analyzer.py --service nginx --errors-only
python scripts/log-analyzer.py --pattern "error|warning|failed"
```

## Features

### Container Management
- Список всех контейнеров со статусом
- Перезапуск, остановка, запуск
- Просмотр логов в реальном времени
- Проверка использования ресурсов контейнерами
- Автоматический рестарт при падении

### Server Monitoring
- CPU usage в реальном времени
- RAM usage с алертами
- Дисковое пространство по разделам
- Сетевой трафик
- Load average
- Температура (если доступно)

### Backup System
- PostgreSQL бэкапы с pg_dump
- Файловые бэкапы с tar
- Инкрементальные бэкапы
- Автоматическая ротация (удаление старых)
- Шифрование бэкапов
- Проверка целостности

### Log Analysis
- Поиск ошибок по паттернам
- Агрегация по типам ошибок
- Временные диапазоны
- Экспорт отчётов
- Real-time мониторинг

## Alert Conditions

- CPU > 80% в течение 5 минут
- RAM > 85%
- Диск < 10% свободного места
- Контейнер упал/не отвечает
- Сервис недоступен (HTTP check fails)
- Ошибки в логах (более 10 в минуту)

## Requirements

- Python 3.9+
- docker (CLI)
- psutil (для мониторинга)
- requests (для HTTP checks)
- python-telegram-bot (для алертов)
- cron (для расписания)

## Installation

```bash
cd skills/devops-assistant
pip install -r requirements.txt

# Настройка переменных окружения
export TELEGRAM_BOT_TOKEN=your_token
export TELEGRAM_CHAT_ID=your_chat_id
export BACKUP_DIR=/backup
```

## Integration

Интегрируется с:
- Telegram Bot API (для уведомлений)
- Docker API
- Systemd (для автозапуска)
- Cron (для расписаний)

## Security

- Не требует root для базового мониторинга
- Безопасное хранение токенов в .env
- Ограниченный доступ к docker группе
- Шифрование чувствительных бэкапов

## License

MIT
