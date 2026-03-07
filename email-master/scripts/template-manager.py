#!/usr/bin/env python3
"""
Template Manager - управление шаблонами писем
Создаёт, редактирует, удаляет шаблоны для быстрого использования
"""

import argparse
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List

class TemplateManager:
    """Менеджер шаблонов email"""
    
    DEFAULT_TEMPLATES = {
        'introduction': {
            'name': 'Introduction',
            'description': 'First contact with a new person',
            'subject': 'Introduction - {{sender_name}} from {{sender_company}}',
            'body': """Hi {{recipient_name}},

My name is {{sender_name}}, and I'm {{sender_title}} at {{sender_company}}.

{{context}}

I'd love to {{call_to_action}}. Would you be open to a brief conversation?

Best regards,
{{sender_name}}""",
            'variables': ['recipient_name', 'sender_name', 'sender_title', 'sender_company', 'context', 'call_to_action']
        },
        'follow-up': {
            'name': 'Follow-up',
            'description': 'Gentle reminder after no response',
            'subject': 'Following up on {{topic}}',
            'body': """Hi {{recipient_name}},

I wanted to follow up on {{topic}}.

{{value_proposition}}

If you're interested, I'd love to {{next_step}}. If not, no worries at all!

Best,
{{sender_name}}""",
            'variables': ['recipient_name', 'sender_name', 'topic', 'value_proposition', 'next_step']
        },
        'meeting-request': {
            'name': 'Meeting Request',
            'description': 'Request for a meeting or call',
            'subject': 'Meeting Request: {{purpose}}',
            'body': """Hi {{recipient_name}},

I'd like to schedule a meeting to {{purpose}}.

Would you be available for a {{duration}} call sometime next week? Here are some options:
{{time_options}}

Please let me know what works best for you.

Best regards,
{{sender_name}}""",
            'variables': ['recipient_name', 'sender_name', 'purpose', 'duration', 'time_options']
        },
        'thank-you': {
            'name': 'Thank You',
            'description': 'Expressing gratitude',
            'subject': 'Thank you for {{reason}}',
            'body': """Hi {{recipient_name}},

I wanted to reach out and thank you for {{reason}}.

{{specific_details}}

I look forward to {{future_action}}.

Warmly,
{{sender_name}}""",
            'variables': ['recipient_name', 'sender_name', 'reason', 'specific_details', 'future_action']
        },
        'project-update': {
            'name': 'Project Update',
            'description': 'Update on project status',
            'subject': 'Update: {{project_name}} - {{status}}',
            'body': """Hi {{recipient_name}},

I wanted to give you a quick update on {{project_name}}.

Status: {{status}}
{{details}}

Next steps:
{{next_steps}}

Let me know if you have any questions.

Best,
{{sender_name}}""",
            'variables': ['recipient_name', 'sender_name', 'project_name', 'status', 'details', 'next_steps']
        },
        'out-of-office': {
            'name': 'Out of Office',
            'description': 'Automatic reply when away',
            'subject': 'Out of Office: {{dates}}',
            'body': """Hi,

Thank you for your email. I'm currently out of the office from {{start_date}} to {{end_date}}.

{{message}}

For urgent matters, please contact {{alternative_contact}}.

Best regards,
{{sender_name}}""",
            'variables': ['start_date', 'end_date', 'message', 'alternative_contact', 'sender_name']
        }
    }
    
    def __init__(self, templates_dir: str = None):
        self.templates_dir = Path(templates_dir) if templates_dir else Path(__file__).parent.parent / 'templates'
        self.templates_dir.mkdir(exist_ok=True)
        self.templates_file = self.templates_dir / 'templates.json'
        self.templates = self._load_templates()
    
    def _load_templates(self) -> Dict:
        """Загружает шаблоны из файла или создаёт дефолтные"""
        if self.templates_file.exists():
            with open(self.templates_file) as f:
                return json.load(f)
        
        # Инициализируем дефолтными шаблонами
        return self.DEFAULT_TEMPLATES.copy()
    
    def _save_templates(self):
        """Сохраняет шаблоны в файл"""
        with open(self.templates_file, 'w') as f:
            json.dump(self.templates, f, indent=2)
    
    def list_templates(self) -> List[Dict]:
        """Возвращает список всех шаблонов"""
        return [
            {
                'id': key,
                'name': template['name'],
                'description': template['description'],
                'variables': template.get('variables', [])
            }
            for key, template in self.templates.items()
        ]
    
    def get_template(self, template_id: str) -> Dict:
        """Получает шаблон по ID"""
        return self.templates.get(template_id)
    
    def create_template(self, template_id: str, name: str, subject: str, 
                       body: str, description: str = '', variables: List[str] = None):
        """Создаёт новый шаблон"""
        if template_id in self.templates:
            raise ValueError(f"Template '{template_id}' already exists")
        
        # Авто-определяем переменные из шаблона
        if variables is None:
            import re
            vars_in_subject = re.findall(r'\{\{(\w+)\}\}', subject)
            vars_in_body = re.findall(r'\{\{(\w+)\}\}', body)
            variables = list(set(vars_in_subject + vars_in_body))
        
        self.templates[template_id] = {
            'name': name,
            'description': description,
            'subject': subject,
            'body': body,
            'variables': variables,
            'created': datetime.now().isoformat()
        }
        
        self._save_templates()
        return self.templates[template_id]
    
    def update_template(self, template_id: str, **kwargs):
        """Обновляет существующий шаблон"""
        if template_id not in self.templates:
            raise ValueError(f"Template '{template_id}' not found")
        
        template = self.templates[template_id]
        
        allowed_fields = ['name', 'description', 'subject', 'body', 'variables']
        for field, value in kwargs.items():
            if field in allowed_fields:
                template[field] = value
        
        template['updated'] = datetime.now().isoformat()
        
        self._save_templates()
        return template
    
    def delete_template(self, template_id: str):
        """Удаляет шаблон"""
        if template_id not in self.templates:
            raise ValueError(f"Template '{template_id}' not found")
        
        # Не удаляем дефолтные шаблоны
        if template_id in self.DEFAULT_TEMPLATES:
            raise ValueError(f"Cannot delete default template '{template_id}'")
        
        del self.templates[template_id]
        self._save_templates()
    
    def render_template(self, template_id: str, variables: Dict) -> Dict:
        """Рендерит шаблон с переменными"""
        template = self.get_template(template_id)
        
        if not template:
            raise ValueError(f"Template '{template_id}' not found")
        
        subject = template['subject']
        body = template['body']
        
        # Заменяем переменные
        for key, value in variables.items():
            placeholder = '{{' + key + '}}'
            subject = subject.replace(placeholder, str(value))
            body = body.replace(placeholder, str(value))
        
        # Проверяем незаменённые переменные
        import re
        missing_in_subject = re.findall(r'\{\{(\w+)\}\}', subject)
        missing_in_body = re.findall(r'\{\{(\w+)\}\}', body)
        missing = set(missing_in_subject + missing_in_body)
        
        return {
            'subject': subject,
            'body': body,
            'template_id': template_id,
            'missing_variables': list(missing),
            'rendered_at': datetime.now().isoformat()
        }
    
    def preview_template(self, template_id: str):
        """Показывает предпросмотр шаблона"""
        template = self.get_template(template_id)
        
        if not template:
            print(f"❌ Template '{template_id}' not found")
            return
        
        print(f"\n📄 Template: {template['name']}")
        print(f"   ID: {template_id}")
        print(f"   Description: {template.get('description', 'N/A')}")
        print(f"\n   Variables: {', '.join(template.get('variables', []))}")
        print(f"\n   Subject Template:")
        print(f"   {template['subject']}")
        print(f"\n   Body Template:")
        print(f"   {template['body'][:200]}...")

def main():
    parser = argparse.ArgumentParser(description='Email Template Manager')
    parser.add_argument('--templates-dir', help='Directory for templates')
    
    subparsers = parser.add_subparsers(dest='command', help='Command')
    
    # List command
    subparsers.add_parser('list', help='List all templates')
    
    # Get command
    get_parser = subparsers.add_parser('get', help='Get template details')
    get_parser.add_argument('template_id', help='Template ID')
    
    # Create command
    create_parser = subparsers.add_parser('create', help='Create new template')
    create_parser.add_argument('template_id', help='Template ID')
    create_parser.add_argument('--name', required=True, help='Template name')
    create_parser.add_argument('--subject', required=True, help='Subject template')
    create_parser.add_argument('--body', required=True, help='Body template')
    create_parser.add_argument('--description', help='Template description')
    
    # Render command
    render_parser = subparsers.add_parser('render', help='Render template with variables')
    render_parser.add_argument('template_id', help='Template ID')
    render_parser.add_argument('--vars', help='JSON file with variables')
    
    # Preview command
    preview_parser = subparsers.add_parser('preview', help='Preview template')
    preview_parser.add_argument('template_id', help='Template ID')
    
    # Delete command
    delete_parser = subparsers.add_parser('delete', help='Delete template')
    delete_parser.add_argument('template_id', help='Template ID')
    
    args = parser.parse_args()
    
    manager = TemplateManager(args.templates_dir)
    
    if args.command == 'list':
        templates = manager.list_templates()
        print("\n📋 Available Templates:")
        print("-" * 60)
        for t in templates:
            print(f"\n  {t['id']:<20} {t['name']}")
            print(f"  {'':20} {t['description']}")
            print(f"  {'':20} Variables: {', '.join(t['variables'])}")
    
    elif args.command == 'get':
        template = manager.get_template(args.template_id)
        if template:
            print(json.dumps(template, indent=2))
        else:
            print(f"❌ Template '{args.template_id}' not found")
    
    elif args.command == 'create':
        try:
            manager.create_template(
                args.template_id,
                args.name,
                args.subject,
                args.body,
                args.description
            )
            print(f"✅ Template '{args.template_id}' created successfully")
        except ValueError as e:
            print(f"❌ Error: {e}")
    
    elif args.command == 'render':
        variables = {}
        if args.vars:
            with open(args.vars) as f:
                variables = json.load(f)
        
        try:
            result = manager.render_template(args.template_id, variables)
            print(f"\nSubject: {result['subject']}\n")
            print(result['body'])
            
            if result['missing_variables']:
                print(f"\n⚠️  Missing variables: {', '.join(result['missing_variables'])}")
        except ValueError as e:
            print(f"❌ Error: {e}")
    
    elif args.command == 'preview':
        manager.preview_template(args.template_id)
    
    elif args.command == 'delete':
        try:
            manager.delete_template(args.template_id)
            print(f"✅ Template '{args.template_id}' deleted")
        except ValueError as e:
            print(f"❌ Error: {e}")
    
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
