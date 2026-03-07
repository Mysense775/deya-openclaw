#!/usr/bin/env python3
"""
Content Planner - генератор контент-планов
Создаёт структуру публикаций на основе темы и платформы
"""

import argparse
import json
from datetime import datetime, timedelta
from typing import List, Dict

class ContentPlanner:
    """Планировщик контента"""
    
    CONTENT_TYPES = {
        'telegram': ['story', 'longread', 'news', 'engagement'],
        'instagram': ['story', 'carousel', 'reel', 'engagement'],
        'twitter': ['thread', 'tweet', 'poll'],
        'linkedin': ['article', 'post', 'document']
    }
    
    TEMPLATES = {
        'story': {
            'name': 'История/Наблюдение',
            'length': '300-500 символов',
            'best_time': '09:00-11:00',
            'engagement': 'high'
        },
        'longread': {
            'name': 'Длинный пост/Разбор',
            'length': '1000+ символов',
            'best_time': '12:00-14:00',
            'engagement': 'medium'
        },
        'news': {
            'name': 'Новость/Анонс',
            'length': '200-400 символов',
            'best_time': 'Any',
            'engagement': 'high'
        },
        'engagement': {
            'name': 'Вовлечение (вопрос/опрос)',
            'length': '100-200 символов',
            'best_time': '18:00-20:00',
            'engagement': 'very_high'
        },
        'carousel': {
            'name': 'Карусель/Чеклист',
            'slides': '5-10',
            'best_time': '10:00-12:00',
            'engagement': 'high'
        }
    }
    
    def __init__(self, topic: str, platform: str = 'telegram'):
        self.topic = topic
        self.platform = platform
        self.content_types = self.CONTENT_TYPES.get(platform, ['story', 'longread'])
    
    def generate_weekly_plan(self, days: int = 7) -> List[Dict]:
        """Генерирует план на неделю"""
        plan = []
        today = datetime.now()
        
        # Распределение типов контента по дням
        content_schedule = [
            'story',      # Понедельник - мягкий старт
            'longread',   # Вторник - глубокий контент
            'engagement', # Среда - вовлечение
            'news',       # Четверг - новости
            'story',      # Пятница - лёгкий контент
            'engagement', # Суббота - общение
            'story'       # Воскресенье - размышления
        ]
        
        for i in range(min(days, 7)):
            date = today + timedelta(days=i)
            content_type = content_schedule[i]
            
            plan.append({
                'day': date.strftime('%A'),
                'date': date.strftime('%Y-%m-%d'),
                'type': content_type,
                'type_name': self.TEMPLATES[content_type]['name'],
                'topic_angle': self._generate_topic_angle(content_type),
                'best_time': self.TEMPLATES[content_type]['best_time'],
                'estimated_length': self.TEMPLATES[content_type].get('length', 'N/A'),
                'status': 'planned'
            })
        
        return plan
    
    def _generate_topic_angle(self, content_type: str) -> str:
        """Генерирует угол подачи темы"""
        angles = {
            'story': [
                f'Личный опыт работы с {self.topic}',
                f'История ошибки и уроки от {self.topic}',
                f'Наблюдение за трендами в {self.topic}',
                f'Разговор с клиентом про {self.topic}'
            ],
            'longread': [
                f'Полный гайд по {self.topic}',
                f'Разбор мифов о {self.topic}',
                f'Как мы внедряли {self.topic}',
                f'Будущее {self.topic}: прогнозы'
            ],
            'news': [
                f'Обновление в {self.topic}',
                f'Новый инструмент для {self.topic}',
                f'Запуск функции {self.topic}'
            ],
            'engagement': [
                f'Вопрос: как вы используете {self.topic}?',
                f'Опрос: что важнее в {self.topic}?',
                f'Обсуждение проблемы с {self.topic}'
            ]
        }
        
        import random
        return random.choice(angles.get(content_type, ['Общий пост']))
    
    def export_plan(self, plan: List[Dict], format: str = 'json') -> str:
        """Экспортирует план в разных форматах"""
        if format == 'json':
            return json.dumps(plan, ensure_ascii=False, indent=2)
        elif format == 'markdown':
            return self._to_markdown(plan)
        else:
            return str(plan)
    
    def _to_markdown(self, plan: List[Dict]) -> str:
        """Конвертирует план в Markdown"""
        md = f"# Контент-план: {self.topic}\n\n"
        md += f"**Платформа:** {self.platform}\n"
        md += f"**Период:** {plan[0]['date']} - {plan[-1]['date']}\n\n"
        
        for item in plan:
            md += f"## {item['day']} ({item['date']})\n\n"
            md += f"**Тип:** {item['type_name']}\n\n"
            md += f"**Тема:** {item['topic_angle']}\n\n"
            md += f"**Время публикации:** {item['best_time']}\n\n"
            md += f"**Длина:** {item['estimated_length']}\n\n"
            md += "---\n\n"
        
        return md

def main():
    parser = argparse.ArgumentParser(description='Генератор контент-планов')
    parser.add_argument('--topic', '-t', required=True, help='Основная тема')
    parser.add_argument('--days', '-d', type=int, default=7, help='Количество дней (default: 7)')
    parser.add_argument('--platform', '-p', default='telegram', 
                       choices=['telegram', 'instagram', 'twitter', 'linkedin'],
                       help='Платформа (default: telegram)')
    parser.add_argument('--format', '-f', default='markdown',
                       choices=['json', 'markdown'],
                       help='Формат вывода (default: markdown)')
    
    args = parser.parse_args()
    
    planner = ContentPlanner(args.topic, args.platform)
    plan = planner.generate_weekly_plan(args.days)
    
    output = planner.export_plan(plan, args.format)
    print(output)

if __name__ == '__main__':
    main()
