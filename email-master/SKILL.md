# Email Master

AI-ассистент для работы с электронной почтой. Пишет деловые письма, управляет рассылками, отвечает на типовые запросы, организует inbox.

## Capabilities

- **Email Composition**: Написание деловых писем разных типов
- **Template Management**: Шаблоны для частых сценариев
- **Reply Assistant**: Генерация ответов на входящие
- **Campaign Management**: Управление email-рассылками
- **Inbox Organization**: Автоматическая сортировка и метки
- **Follow-up Reminders**: Напоминания о неотвеченных письмах
- **Tone Adjustment**: Адаптация тона (формальный, дружелюбный, строгий)
- **Multilingual**: Поддержка нескольких языков

## Usage

```bash
# Написать письмо
python scripts/email-composer.py --to client@example.com --subject "Proposal" --type proposal

# Ответить на письмо
python scripts/reply-assistant.py --incoming email.txt --tone professional

# Создать рассылку
python scripts/campaign-manager.py --template newsletter --recipients list.csv

# Управление шаблонами
python scripts/template-manager.py --list
python scripts/template-manager.py --create --name "Follow-up" --file template.txt
```

## Email Types

### Business Emails
- **Introduction**: Представление, знакомство
- **Proposal**: Коммерческие предложения
- **Follow-up**: Напоминания, продолжение разговора
- **Meeting Request**: Запрос на встречу
- **Thank You**: Благодарности
- **Apology**: Извинения, объяснения
- **Reminder**: Напоминания о сроках
- **Update**: Обновления статуса

### Marketing Emails
- **Newsletter**: Регулярные рассылки
- **Product Launch**: Запуск продукта
- **Promotional**: Акции, скидки
- **Onboarding**: Приветствие новых пользователей
- **Re-engagement**: Возвращение неактивных
- **Survey**: Опросы, сбор feedback

### Support Emails
- **Ticket Response**: Ответы на обращения
- **FAQ Auto-reply**: Автоответы на частые вопросы
- **Escalation**: Эскалация сложных случаев
- **Resolution**: Решение проблем

## Features

### Smart Composition
- Автоматическое определение типа письма
- Генерация subject line
- Оптимальная длина и структура
- Призыв к действию (CTA)

### Personalization
- Имя получателя
- Контекст предыдущих писем
- История взаимодействия
- Персональные рекомендации

### Tone & Style
- **Formal**: Для бизнеса, незнакомых людей
- **Professional**: Стандартный деловой
- **Friendly**: Коллеги, знакомые клиенты
- **Casual**: Внутренняя коммуникация
- **Apologetic**: При проблемах
- **Urgent**: Срочные вопросы

### Email Analytics
- Open rates
- Click rates
- Reply rates
- Best sending times
- A/B testing

## Templates

### Introduction Email
```
Subject: Introduction - [Your Name] from [Company]

Hi [Name],

I hope this email finds you well. My name is [Your Name], and I'm [Title] at [Company].

I came across your [work/profile/company] and was impressed by [specific detail].

[Reason for reaching out - 1-2 sentences]

Would you be open to [specific call to action]?

Looking forward to hearing from you.

Best regards,
[Your Name]
```

### Follow-up Email
```
Subject: Following up on [Topic]

Hi [Name],

I wanted to follow up on my previous email about [topic].

[Reminder of value proposition]

[Soft CTA]

Best,
[Your Name]
```

## Requirements

- Python 3.9+
- smtplib (отправка email)
- imaplib (получение email)
- email (обработка MIME)
- jinja2 (шаблоны)
- pandas (работа с контактами)

## Installation

```bash
cd skills/email-master
pip install -r requirements.txt

# Настройка SMTP
export SMTP_HOST=smtp.gmail.com
export SMTP_PORT=587
export SMTP_USER=your-email@gmail.com
export SMTP_PASSWORD=your-app-password
```

## Security

- App passwords для Gmail (не основной пароль)
- TLS/SSL шифрование
- Не хранить credentials в коде
- Rate limiting для отправки
- DKIM/SPF проверки

## Integration

- Gmail API
- Outlook/Exchange
- SendGrid
- Mailgun
- AWS SES

## Use Cases

1. **Sales Outreach**: Холодные письма потенциальным клиентам
2. **Customer Support**: Быстрые ответы на типовые вопросы
3. **Marketing Campaigns**: Email-рассылки для @dayanrouter
4. **Networking**: Поддержка контактов, follow-ups
5. **Internal Comms**: Корпоративные коммуникации

## Best Practices

- Отправлять в оптимальное время (вторник-четверг, 10:00-14:00)
- Длина: 50-125 слов для лучшей конверсии
- Один CTA на письмо
- Персонализация увеличивает открываемость на 26%
- A/B тестировать subject lines

## License

MIT
