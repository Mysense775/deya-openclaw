# DevOps Assistant 🛠️

AI-ассистент для управления инфраструктурой. Мониторит сервера, управляет Docker, делает бэкапы, анализирует логи.

## 🚀 Быстрый старт

```bash
# Установка
cd skills/devops-assistant
pip install -r requirements.txt

# Список контейнеров
./scripts/container-manager.py --list

# Перезапустить контейнер
./scripts/container-manager.py --restart airouter-backend

# Мониторинг сервера
./scripts/server-monitor.py --watch

# Бэкап базы данных
./scripts/backup-automation.py --db ai_router --db-user postgres

# Анализ логов
./scripts/log-analyzer.py /var/log/nginx/error.log --errors-only
```

## 📋 Скрипты

### 1. Container Manager
Управление Docker контейнерами.

```bash
# Список запущенных
./container-manager.py -l

# Перезапуск
./container-manager.py -r airouter-backend

# Логи в реальном времени
./container-manager.py --logs airouter-frontend --follow

# Статистика ресурсов
./container-manager.py --stats

# Авто-исправление нездоровых контейнеров
./container-manager.py --auto-heal
```

### 2. Server Monitor
Мониторинг системных ресурсов.

```bash
# Одна проверка
./server-monitor.py --check

# Наблюдение в реальном времени
./server-monitor.py --watch --interval 5

# Только алерты
./server-monitor.py --watch --alerts-only

# Экспорт в JSON
./server-monitor.py --json report.json

# Кастомные пороги
./server-monitor.py --threshold-cpu 70 --threshold-ram 80
```

**Алерты:**
- CPU > 80%
- RAM > 85%
- Disk > 90%
- Load average > 4

### 3. Backup Automation
Автоматизация бэкапов.

```bash
# PostgreSQL бэкап
./backup-automation.py --db ai_router --db-user postgres

# Файловый бэкап
./backup-automation.py --files /var/www --backup-name website

# Docker volumes
./backup-automation.py --all-volumes

# С ротацией (оставить последние 7)
./backup-automation.py --db ai_router --rotate "*.sql.gz" --keep 7

# Список бэкапов
./backup-automation.py --list

# Проверка целостности
./backup-automation.py --verify /backup/databases/ai_router_20260307_120000.sql.gz
```

### 4. Log Analyzer
Анализ логов на ошибки.

```bash
# Анализ ошибок
./log-analyzer.py /var/log/nginx/error.log --errors-only

# Поиск по паттерну
./log-analyzer.py app.log --pattern "timeout|connection refused"

# Последние 100 строк
./log-analyzer.py /var/log/syslog --tail 100

# Следить за логом
./log-analyzer.py app.log --follow

# Экспорт в JSON
./log-analyzer.py nginx.log --json report.json
```

**Поддерживаемые форматы:**
- Nginx/Apache access logs
- Syslog
- Docker logs
- Python application logs

## 🔧 Интеграция с Deya

Примеры использования:

```bash
# Проверить здоровье системы перед деплоем
./server-monitor.py --check || echo "❌ System not healthy"

# Перезапустить упавшие контейнеры
./container-manager.py --auto-heal

# Ежедневный бэкап базы
./backup-automation.py --db ai_router --rotate "*.sql.gz" --keep 7

# Проверить логи на ошибки за ночь
./log-analyzer.py /var/log/nginx/error.log --errors-only
```

## ⚙️ Автоматизация

### Cron задачи

```bash
# Ежедневный бэкап в 3:00
0 3 * * * /root/.openclaw/workspace/skills/devops-assistant/scripts/backup-automation.py --db ai_router --rotate "*.sql.gz" --keep 7

# Проверка контейнеров каждые 5 минут
*/5 * * * * /root/.openclaw/workspace/skills/devops-assistant/scripts/container-manager.py --auto-heal

# Мониторинг каждую минуту с алертами
* * * * * /root/.openclaw/workspace/skills/devops-assistant/scripts/server-monitor.py --check || echo "Alert" | mail -s "Server Alert" admin@example.com
```

## 📊 Мониторинг

**Что отслеживается:**
- CPU usage и load average
- RAM и swap использование
- Дисковое пространство по разделам
- Сетевой трафик
- Docker контейнеры (статус, ресурсы)
- HTTP health checks
- Логи на ошибки

**Алерты:**
- Telegram уведомления
- Email notifications
- Exit codes для CI/CD
- JSON экспорт для внешних систем

## 🔒 Безопасность

- Не требует root для базового мониторинга
- Пользователь должен быть в группе docker
- Бэкапы можно шифровать
- Безопасное хранение паролей в env vars
- Ограниченный доступ к системным путям

## 📝 License

MIT License

---

*Создано для автоматизации инфраструктуры Deya Cloud* 🌺
