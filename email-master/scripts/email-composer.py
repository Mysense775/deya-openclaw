#!/usr/bin/env python3
"""
Email Composer - генератор деловых писем
Создаёт письма разных типов с правильной структурой и тоном
"""

import argparse
import json
from datetime import datetime
from typing import Dict, Optional

class EmailComposer:
    """Композер деловых писем"""
    
    EMAIL_TYPES = {
        'introduction': {
            'name': 'Introduction',
            'structure': ['greeting', 'intro', 'context', 'cta', 'closing'],
            'tone': 'professional'
        },
        'proposal': {
            'name': 'Business Proposal',
            'structure': ['greeting', 'hook', 'value_prop', 'details', 'cta', 'closing'],
            'tone': 'formal'
        },
        'follow-up': {
            'name': 'Follow-up',
            'structure': ['greeting', 'reminder', 'value', 'soft_cta', 'closing'],
            'tone': 'friendly'
        },
        'meeting-request': {
            'name': 'Meeting Request',
            'structure': ['greeting', 'context', 'request', 'propose_times', 'closing'],
            'tone': 'professional'
        },
        'thank-you': {
            'name': 'Thank You',
            'structure': ['greeting', 'gratitude', 'specifics', 'future', 'closing'],
            'tone': 'warm'
        },
        'apology': {
            'name': 'Apology',
            'structure': ['greeting', 'acknowledge', 'apologize', 'solution', 'closing'],
            'tone': 'apologetic'
        },
        'reminder': {
            'name': 'Reminder',
            'structure': ['greeting', 'reminder', 'details', 'urgency', 'closing'],
            'tone': 'professional'
        },
        'newsletter': {
            'name': 'Newsletter',
            'structure': ['subject', 'greeting', 'intro', 'content', 'cta', 'closing'],
            'tone': 'friendly'
        },
        'promotional': {
            'name': 'Promotional',
            'structure': ['hook', 'offer', 'value', 'urgency', 'cta'],
            'tone': 'enthusiastic'
        },
        'support-response': {
            'name': 'Support Response',
            'structure': ['greeting', 'acknowledge', 'solution', 'next_steps', 'closing'],
            'tone': 'helpful'
        }
    }
    
    TONES = {
        'formal': {
            'greeting': ['Dear {name}', 'To {name}'],
            'closing': ['Sincerely', 'Respectfully', 'Regards'],
            'style': 'reserved, polite, no contractions'
        },
        'professional': {
            'greeting': ['Hi {name}', 'Hello {name}', 'Dear {name}'],
            'closing': ['Best regards', 'Best', 'Kind regards'],
            'style': 'business-casual, clear, concise'
        },
        'friendly': {
            'greeting': ['Hi {name}', 'Hey {name}', 'Hello {name}'],
            'closing': ['Best', 'Cheers', 'Talk soon'],
            'style': 'warm, approachable, light'
        },
        'warm': {
            'greeting': ['Hi {name}', 'Hello {name}'],
            'closing': ['Warmly', 'With appreciation', 'Gratefully'],
            'style': 'personal, grateful, sincere'
        },
        'apologetic': {
            'greeting': ['Hi {name}', 'Hello {name}'],
            'closing': ['My apologies again', 'Thank you for understanding'],
            'style': 'sincere, taking responsibility, solution-focused'
        },
        'enthusiastic': {
            'greeting': ['Hi {name}!', 'Hey {name}!'],
            'closing': ['Excited to hear from you!', 'Let\'s do this!'],
            'style': 'energetic, exciting, motivating'
        },
        'helpful': {
            'greeting': ['Hi {name}', 'Hello {name}'],
            'closing': ['Here to help', 'Let me know if you need more'],
            'style': 'supportive, clear, patient'
        }
    }
    
    def __init__(self, email_type: str = 'professional', tone: str = None):
        self.email_type = email_type
        self.type_config = self.EMAIL_TYPES.get(email_type, self.EMAIL_TYPES['professional'])
        self.tone = tone or self.type_config['tone']
        self.tone_config = self.TONES.get(self.tone, self.TONES['professional'])
    
    def compose(self, recipient_name: str, context: Dict = None) -> Dict:
        """Создаёт письмо указанного типа"""
        context = context or {}
        
        # Выбираем приветствие и закрытие
        greeting = self.tone_config['greeting'][0].format(name=recipient_name)
        closing = self.tone_config['closing'][0]
        
        # Генерируем контент на основе типа
        content = self._generate_content(recipient_name, context)
        
        # Формируем полное письмо
        email = {
            'subject': self._generate_subject(context),
            'body': self._format_email(greeting, content, closing),
            'type': self.email_type,
            'tone': self.tone,
            'timestamp': datetime.now().isoformat()
        }
        
        return email
    
    def _generate_content(self, name: str, context: Dict) -> str:
        """Генерирует контент письма"""
        email_type = self.email_type
        
        if email_type == 'introduction':
            return self._compose_introduction(name, context)
        elif email_type == 'proposal':
            return self._compose_proposal(name, context)
        elif email_type == 'follow-up':
            return self._compose_follow_up(name, context)
        elif email_type == 'meeting-request':
            return self._compose_meeting_request(name, context)
        elif email_type == 'thank-you':
            return self._compose_thank_you(name, context)
        elif email_type == 'apology':
            return self._compose_apology(name, context)
        elif email_type == 'reminder':
            return self._compose_reminder(name, context)
        elif email_type == 'newsletter':
            return self._compose_newsletter(name, context)
        else:
            return context.get('custom_body', 'Please provide content for this email.')
    
    def _compose_introduction(self, name: str, context: Dict) -> str:
        """Письмо-знакомство"""
        my_name = context.get('my_name', 'Deya')
        my_title = context.get('my_title', 'AI Assistant')
        my_company = context.get('my_company', 'Deya Cloud')
        reason = context.get('reason', 'I came across your profile and was impressed by your work.')
        cta = context.get('cta', 'connect and explore potential collaboration')
        
        return f"""My name is {my_name}, and I'm {my_title} at {my_company}.

{reason}

I'd love to {cta}. Would you be open to a brief conversation next week?"""
    
    def _compose_proposal(self, name: str, context: Dict) -> str:
        """Коммерческое предложение"""
        offer = context.get('offer', 'our AI-powered assistant platform')
        value = context.get('value', 'reduce operational costs by 30%')
        details = context.get('details', 'We offer a comprehensive solution that integrates with your existing tools.')
        
        return f"""I hope you're doing well. I'm reaching out to introduce {offer}.

Our platform helps businesses like yours {value}.

{details}

I'd be happy to schedule a 15-minute call to discuss how this could specifically benefit your organization. Would Tuesday or Wednesday work for you?"""
    
    def _compose_follow_up(self, name: str, context: Dict) -> str:
        """Follow-up письмо"""
        previous_topic = context.get('previous_topic', 'my previous email')
        value = context.get('value', 'this solution could save your team 10+ hours per week')
        
        return f"""I wanted to follow up on {previous_topic}.

I understand you're busy, but I believe {value}.

If you're interested, I'd love to show you a quick demo. If not, no worries at all—just let me know either way!"""
    
    def _compose_meeting_request(self, name: str, context: Dict) -> str:
        """Запрос на встречу"""
        purpose = context.get('purpose', 'discuss how we can help with your upcoming project')
        duration = context.get('duration', '30 minutes')
        
        return f"""I'd like to schedule a meeting to {purpose}.

Would you be available for a {duration} call sometime next week? I'm flexible on timing and can work around your schedule.

Here are a few options that work for me:
- Tuesday at 10:00 AM or 2:00 PM
- Wednesday at 11:00 AM or 3:00 PM
- Thursday at 9:00 AM or 4:00 PM

Please let me know what works best for you, or suggest an alternative time."""
    
    def _compose_thank_you(self, name: str, context: Dict) -> str:
        """Письмо-благодарность"""
        reason = context.get('reason', 'taking the time to speak with me yesterday')
        specifics = context.get('specifics', 'Your insights about the industry were incredibly valuable.')
        
        return f"""I wanted to reach out and thank you for {reason}.

{specifics}

I look forward to staying in touch and hope our paths cross again soon."""
    
    def _compose_apology(self, name: str, context: Dict) -> str:
        """Письмо-извинение"""
        issue = context.get('issue', 'the delay in our response')
        solution = context.get('solution', 'We have resolved the issue and implemented measures to prevent it from happening again.')
        
        return f"""I want to personally apologize for {issue}. This is not the standard of service we strive to provide.

{solution}

We truly value your business and are committed to making this right. Please don't hesitate to reach out if you have any further concerns."""
    
    def _compose_reminder(self, name: str, context: Dict) -> str:
        """Напоминание"""
        deadline = context.get('deadline', 'March 15th')
        task = context.get('task', 'review the proposal')
        
        return f"""This is a friendly reminder that the deadline for {task} is approaching on {deadline}.

Please let me know if you need any additional information or if there are any questions I can answer to help move this forward."""
    
    def _compose_newsletter(self, name: str, context: Dict) -> str:
        """Newsletter"""
        intro = context.get('intro', "Here's what's new this month:")
        content = context.get('content', '- New feature: AI-powered analytics\n- Case study: How Company X improved efficiency by 40%\n- Upcoming webinar: Best practices for 2026')
        cta = context.get('cta', 'Check out our latest updates')
        
        return f"""{intro}

{content}

{cta}

As always, thank you for being part of our community!"""
    
    def _generate_subject(self, context: Dict) -> str:
        """Генерирует subject line"""
        subjects = {
            'introduction': f"Introduction - {context.get('my_name', 'Deya')} from {context.get('my_company', 'Deya Cloud')}",
            'proposal': f"Proposal: {context.get('offer', 'Collaboration Opportunity')}",
            'follow-up': f"Following up on {context.get('previous_topic', 'our conversation')}",
            'meeting-request': f"Meeting Request: {context.get('purpose', 'Quick Chat')}",
            'thank-you': f"Thank you for {context.get('reason', 'your time')}",
            'apology': f"My sincere apologies regarding {context.get('issue', 'the recent issue')}",
            'reminder': f"Reminder: {context.get('task', 'Action Required')} - {context.get('deadline', 'Due Soon')}",
            'newsletter': context.get('newsletter_title', 'Monthly Update - March 2026'),
        }
        
        return subjects.get(self.email_type, context.get('subject', 'Important Update'))
    
    def _format_email(self, greeting: str, content: str, closing: str) -> str:
        """Форматирует полное письмо"""
        signature = "\n\nDeya\nAI Assistant | Deya Cloud\nfounder@airouter.host"
        
        return f"{greeting},\n\n{content}\n\n{closing},{signature}"
    
    def get_template(self) -> str:
        """Возвращает шаблон для данного типа письма"""
        return f"""Type: {self.type_config['name']}
Tone: {self.tone}
Structure: {', '.join(self.type_config['structure'])}

Template:
{self.tone_config['greeting'][0]},

[Your content here]

{self.tone_config['closing'][0]},
[Your name]"""

def main():
    parser = argparse.ArgumentParser(description='Email Composer')
    parser.add_argument('--type', '-t', default='introduction',
                       choices=list(EmailComposer.EMAIL_TYPES.keys()),
                       help='Type of email')
    parser.add_argument('--to', required=True, help='Recipient name')
    parser.add_argument('--tone', choices=list(EmailComposer.TONES.keys()),
                       help='Email tone (auto-selected by type if not specified)')
    parser.add_argument('--subject', '-s', help='Custom subject line')
    parser.add_argument('--context', '-c', help='JSON file with context variables')
    parser.add_argument('--template', action='store_true', help='Show template only')
    parser.add_argument('--json', '-j', action='store_true', help='Output as JSON')
    
    args = parser.parse_args()
    
    # Загружаем контекст
    context = {}
    if args.context:
        with open(args.context) as f:
            context = json.load(f)
    
    if args.subject:
        context['subject'] = args.subject
    
    # Создаём композер
    composer = EmailComposer(args.type, args.tone)
    
    if args.template:
        print(composer.get_template())
    else:
        # Генерируем письмо
        email = composer.compose(args.to, context)
        
        if args.json:
            print(json.dumps(email, indent=2))
        else:
            print(f"Subject: {email['subject']}\n")
            print(email['body'])

if __name__ == '__main__':
    main()
