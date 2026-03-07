# Email Master ✉️

AI-ассистент для работы с электронной почтой. Пишет деловые письма, управляет рассылками, отвечает на типовые запросы, организует inbox.

## 🚀 Быстрый старт

```bash
# Установка
cd skills/email-master
pip install -r requirements.txt

# Написать письмо
./scripts/email-composer.py --type introduction --to "John" --tone professional

# Ответить на письмо
./scripts/reply-assistant.py --file incoming.txt --tone friendly

# Управление шаблонами
./scripts/template-manager.py list
```

## 📋 Скрипты

### 1. Email Composer
Генератор деловых писем разных типов.

```bash
# Знакомство
./email-composer.py --type introduction --to "Alice" \
  --context '{"my_name":"Deya","my_company":"Deya Cloud"}'

# Коммерческое предложение
./email-composer.py --type proposal --to "CTO" \
  --context '{"offer":"AI assistant","value":"save 30% time"}'

# Follow-up
./email-composer.py --type follow-up --to "Bob" \
  --context '{"previous_topic":"our demo","value":"10h/week savings"}'

# Запрос встречи
./email-composer.py --type meeting-request --to "Client"

# Письмо-благодарность
./email-composer.py --type thank-you --to "Speaker"
```

**Типы писем:**
- `introduction` — знакомство
- `proposal` — коммерческое предложение
- `follow-up` — напоминание
- `meeting-request` — запрос встречи
- `thank-you` — благодарность
- `apology` — извинения
- `reminder` — напоминание о сроках
- `newsletter` — рассылка
- `promotional` — промо
- `support-response` — ответ поддержки

**Тоны:**
- `formal` — официальный
- `professional` — деловой
- `friendly` — дружелюбный
- `casual` — неформальный
- `warm` — тёплый
- `apologetic` — извиняющийся

### 2. Reply Assistant
Помощник в ответах на входящие письма.

```bash
# Анализ + ответ
./reply-assistant.py --file incoming-email.txt --tone professional

# Только анализ
./reply-assistant.py --file email.txt --analyze

# Ответ на текст
./reply-assistant.py --text "Hi, can we meet tomorrow?" --tone friendly
```

**Анализирует:**
- Тональность (positive/negative/neutral)
- Срочность (high/medium/low)
- Вопросы
- Action items
- Тон отправителя

### 3. Template Manager
Управление шаблонами писем.

```bash
# Список шаблонов
./template-manager.py list

# Просмотр шаблона
./template-manager.py preview introduction

# Рендер шаблона
./template-manager.py render introduction --vars vars.json

# Создание шаблона
./template-manager.py create my-template \
  --name "My Template" \
  --subject "Hello {{name}}" \
  --body "Hi {{name}},..."
```

**Встроенные шаблоны:**
- `introduction` — знакомство
- `follow-up` — напоминание
- `meeting-request` — запрос встречи
- `thank-you` — благодарность
- `project-update` — обновление проекта
- `out-of-office` — автоответчик

## 📝 Примеры использования

### Холодное письмо потенциальному клиенту

```bash
./email-composer.py \
  --type introduction \
  --to "Alex" \
  --tone professional \
  --context '{
    "my_name": "Deya",
    "my_title": "AI Assistant",
    "my_company": "Deya Cloud",
    "reason": "I noticed your company is expanding and might need automation",
    "call_to_action": "schedule a 15-min call to discuss AI solutions"
  }'
```

### Ответ на запрос информации

```bash
# Сохраняем входящее письмо
echo "Hi, I'm interested in your AI assistant. What are the pricing plans?" > inquiry.txt

# Генерируем ответ
./reply-assistant.py --file inquiry.txt --tone friendly
```

### Использование шаблона

```bash
# Создаём файл с переменными
cat > vars.json << 'EOF'
{
  "recipient_name": "John",
  "sender_name": "Deya",
  "sender_company": "Deya Cloud",
  "context": "I saw your presentation at the conference",
  "call_to_action": "connect and explore collaboration"
}
EOF

# Рендерим шаблон
./template-manager.py render introduction --vars vars.json
```

## 🎯 Best Practices

### Тайминг отправки
- Лучшее время: вторник-четверг, 10:00-14:00
- Избегать: понедельники утром, пятницы вечером

### Длина письма
- Оптимально: 50-125 слов
- Максимум: 200 слов для холодных писем
- Subject: 30-50 символов

### Персонализация
- Использовать имя получателя
- Упоминать конкретные детали
- Один CTA на письмо

### Follow-up стратегия
- Первый follow-up: через 3-4 дня
- Второй: через неделю
- Третий: через 2 недели
- Далее: раз в месяц

## 📊 Email Analytics (планируется)

- Open rates
- Click rates
- Reply rates
- Best sending times
- A/B testing

## 🔗 Интеграция с другими скиллами

**Content Creator Pro:**
```bash
# Сгенерировать пост → отправить email
./content-creator-pro/post-generator.py --topic "AI" > content.txt
./email-master/email-composer.py --type newsletter --context "$(cat content.txt)"
```

**Research Assistant:**
```bash
# Исследовать → написать по результатам
./research-assistant/topic-researcher.py -t "market" -o research.md
./email-composer.py --type proposal --context "$(cat research.md)"
```

## 🔐 Безопасность

- Не хранить пароли в коде
- Использовать App Passwords для Gmail
- TLS/SSL для отправки
- Rate limiting (не спамить)

## 📄 License

MIT License

---

*Создано для эффективной коммуникации Deya* ✉️🌺
