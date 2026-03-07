#!/usr/bin/env python3
"""
Hashtag Research - исследователь хештегов
Подбирает релевантные хештеги для разных платформ
"""

import argparse
import json
from typing import List, Dict
import random

class HashtagResearch:
    """Исследователь хештегов"""
    
    # База хештегов по категориям
    HASHTAG_DB = {
        'ai': {
            'general': ['ai', 'artificialintelligence', 'machinelearning', 'deeplearning', 'neuralnetworks'],
            'tools': ['chatgpt', 'openai', 'claude', 'ai tools', 'aiassistant'],
            'business': ['aibusiness', 'ai automation', 'ai solutions', 'enterprise ai'],
            'trending': ['ai2026', 'futureofai', 'aitrends', 'generativeai']
        },
        'technology': {
            'general': ['tech', 'technology', 'innovation', 'digital', 'futuretech'],
            'dev': ['programming', 'coding', 'developer', 'software', 'opensource'],
            'infrastructure': ['cloud', 'docker', 'kubernetes', 'devops', 'serverless']
        },
        'business': {
            'general': ['business', 'entrepreneur', 'startup', 'founder', 'smallbusiness'],
            'marketing': ['marketing', 'digitalmarketing', 'contentmarketing', 'growth'],
            'productivity': ['productivity', 'efficiency', 'automation', 'workflow']
        },
        'content': {
            'general': ['content', 'contentcreation', 'contentcreator', 'copywriting'],
            'social': ['socialmedia', 'instagram', 'telegram', 'twitter', 'linkedin'],
            'strategy': ['contentstrategy', 'contentmarketing', 'editorial', 'publishing']
        },
        'lifestyle': {
            'general': ['lifestyle', 'life', 'daily', 'routine', 'balance'],
            'work': ['worklife', 'remotework', 'freelance', 'digitalnomad'],
            'mindset': ['mindset', 'growthmindset', 'productivity', 'selfimprovement']
        }
    }
    
    # Популярные универсальные хештеги
    UNIVERSAL_TAGS = ['follow', 'like', 'share', 'viral', 'trending', 'instagood', 'photooftheday']
    
    # Специфичные для платформ
    PLATFORM_SPECIFIC = {
        'telegram': ['telegram', 'tg', 'telegramchannel', 'телеграм'],
        'instagram': ['instagram', 'insta', 'instadaily', 'instalike', 'photooftheday'],
        'twitter': ['twitter', 'tweet', 'trending', 'viral', 'thread'],
        'linkedin': ['linkedin', 'professional', 'networking', 'career', 'b2b']
    }
    
    def __init__(self, platform: str = 'telegram'):
        self.platform = platform
    
    def research(self, topic: str, count: int = 15) -> List[str]:
        """
        Исследует и подбирает хештеги для темы
        """
        hashtags = []
        
        # 1. Находим релевантные категории
        topic_lower = topic.lower()
        relevant_categories = []
        
        for category, subcats in self.HASHTAG_DB.items():
            if category in topic_lower:
                relevant_categories.append(category)
            else:
                # Проверяем ключевые слова в подкатегориях
                for subcat, tags in subcats.items():
                    if any(word in topic_lower for word in tags[:3]):
                        relevant_categories.append(category)
                        break
        
        # Если категорий не нашлось, используем все
        if not relevant_categories:
            relevant_categories = list(self.HASHTAG_DB.keys())
        
        # 2. Собираем хештеги из категорий
        for category in relevant_categories[:2]:  # Берём 2 лучшие категории
            cat_data = self.HASHTAG_DB[category]
            
            # Берём из general
            hashtags.extend(cat_data.get('general', [])[:2])
            
            # Берём из trending или business (если есть)
            for subcat in ['trending', 'business', 'tools', 'marketing']:
                if subcat in cat_data:
                    hashtags.extend(cat_data[subcat][:2])
                    break
        
        # 3. Добавляем хештеги из темы
        topic_words = topic_lower.replace('-', ' ').replace('_', ' ').split()
        for word in topic_words[:3]:
            clean_word = word.strip('.,!?;:')
            if len(clean_word) > 3:
                hashtags.append(clean_word)
        
        # 4. Добавляем платформенные
        platform_tags = self.PLATFORM_SPECIFIC.get(self.platform, [])
        hashtags.extend(platform_tags[:2])
        
        # 5. Удаляем дубликаты и ограничиваем количество
        hashtags = list(set(hashtags))
        random.shuffle(hashtags)
        
        # Форматируем с #
        formatted = [f"#{tag}" for tag in hashtags[:count]]
        
        return formatted
    
    def generate_sets(self, topic: str) -> Dict[str, List[str]]:
        """
        Генерирует наборы хештегов для разных целей
        """
        return {
            'minimal': self.research(topic, 5),
            'optimal': self.research(topic, 10),
            'maximum': self.research(topic, 20),
            'engagement': self._get_engagement_tags(topic),
            'niche': self._get_niche_tags(topic)
        }
    
    def _get_engagement_tags(self, topic: str) -> List[str]:
        """Хештеги для вовлечения"""
        engagement = ['follow', 'like', 'comment', 'share', 'discover', 'explore']
        return [f"#{tag}" for tag in engagement[:5]]
    
    def _get_niche_tags(self, topic: str) -> List[str]:
        """Нишевые хештеги"""
        # Создаём комбинации
        niche = [
            topic.lower().replace(' ', ''),
            topic.lower().replace(' ', '_'),
            f"{topic.lower().replace(' ', '')}tips",
            f"{topic.lower().replace(' ', '')}community"
        ]
        return [f"#{tag}" for tag in niche[:4]]
    
    def analyze_competition(self, hashtag: str) -> Dict:
        """
        Анализирует конкуренцию по хештегу (имитация)
        В реальности — API запросы к соцсетям
        """
        # Имитация данных
        base_count = random.randint(1000, 1000000)
        
        return {
            'hashtag': hashtag,
            'posts_count': base_count,
            'competition_level': self._get_competition_level(base_count),
            'reach_potential': self._get_reach_potential(base_count),
            'recommendation': self._get_recommendation(base_count)
        }
    
    def _get_competition_level(self, count: int) -> str:
        if count < 10000:
            return 'low'
        elif count < 100000:
            return 'medium'
        else:
            return 'high'
    
    def _get_reach_potential(self, count: int) -> str:
        if count < 10000:
            return 'high'  # Мало конкуренции
        elif count < 100000:
            return 'medium'
        else:
            return 'low'  # Слишком много постов
    
    def _get_recommendation(self, count: int) -> str:
        if count < 10000:
            return 'Используйте — низкая конкуренция'
        elif count < 100000:
            return 'Хороший баланс охвата и конкуренции'
        else:
            return 'Избегайте или используйте редко — слишком высокая конкуренция'

def main():
    parser = argparse.ArgumentParser(description='Исследователь хештегов')
    parser.add_argument('--topic', '-t', required=True, help='Тема для поиска хештегов')
    parser.add_argument('--count', '-c', type=int, default=15, help='Количество (default: 15)')
    parser.add_argument('--platform', '-p', default='telegram',
                       choices=['telegram', 'instagram', 'twitter', 'linkedin'],
                       help='Платформа (default: telegram)')
    parser.add_argument('--sets', '-s', action='store_true', help='Сгенерировать наборы')
    parser.add_argument('--analyze', '-a', help='Анализировать конкретный хештег')
    
    args = parser.parse_args()
    
    researcher = HashtagResearch(args.platform)
    
    if args.analyze:
        analysis = researcher.analyze_competition(args.analyze)
        print(json.dumps(analysis, ensure_ascii=False, indent=2))
    elif args.sets:
        sets = researcher.generate_sets(args.topic)
        for set_name, tags in sets.items():
            print(f"\n{set_name.upper()} ({len(tags)} tags):")
            print(" ".join(tags))
    else:
        hashtags = researcher.research(args.topic, args.count)
        print(" ".join(hashtags))

if __name__ == '__main__':
    main()
