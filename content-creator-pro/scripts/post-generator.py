#!/usr/bin/env python3
"""
Post Generator - генератор постов
Создаёт тексты постов разных форматов и тональностей
"""

import argparse
from typing import Dict, Optional
import random

class PostGenerator:
    """Генератор постов"""
    
    TONES = {
        'warm': {
            'greeting': ['Привет', 'Доброе утро', 'Приветствую', 'Здравствуй'],
            'closing': ['Тёплых дел', 'До встречи', 'С теплом', 'Обнимаю'],
            'style': 'мягкий, личный, с заботой'
        },
        'professional': {
            'greeting': ['Добрый день', 'Уважаемые коллеги', 'Приветствую'],
            'closing': ['С уважением', 'Best regards', 'Всего доброго'],
            'style': 'деловой, структурированный, конкретный'
        },
        'humorous': {
            'greeting': ['Йоу', 'Здарова', 'Ну что, народ', 'Привет, привет'],
            'closing': ['Не скучайте', 'Смеяться полезно', 'Улыбнись'],
            'style': 'неформальный, с шутками, лёгкий'
        },
        'inspirational': {
            'greeting': ['Привет, мечтатели', 'Друзья', 'Всем, кто стремится вперёд'],
            'closing': ['Вперёд', 'К новым высотам', 'Верь в себя'],
            'style': 'вдохновляющий, мотивирующий, энергичный'
        }
    }
    
    TEMPLATES = {
        'story': {
            'structure': ['hook', 'context', 'story', 'insight', 'closing'],
            'length': (300, 500)
        },
        'longread': {
            'structure': ['headline', 'intro', 'problem', 'solution', 'example', 'conclusion'],
            'length': (1000, 2000)
        },
        'news': {
            'structure': ['headline', 'lead', 'details', 'context', 'cta'],
            'length': (200, 400)
        },
        'engagement': {
            'structure': ['hook', 'question', 'context', 'cta'],
            'length': (100, 200)
        }
    }
    
    def __init__(self, post_type: str = 'story', tone: str = 'warm'):
        self.post_type = post_type
        self.tone = self.TONES.get(tone, self.TONES['warm'])
        self.template = self.TEMPLATES.get(post_type, self.TEMPLATES['story'])
    
    def generate(self, topic: str, custom_hook: Optional[str] = None) -> str:
        """Генерирует пост на заданную тему"""
        
        if self.post_type == 'story':
            return self._generate_story(topic, custom_hook)
        elif self.post_type == 'longread':
            return self._generate_longread(topic)
        elif self.post_type == 'news':
            return self._generate_news(topic)
        elif self.post_type == 'engagement':
            return self._generate_engagement(topic)
        else:
            return self._generate_story(topic, custom_hook)
    
    def _generate_story(self, topic: str, custom_hook: Optional[str] = None) -> str:
        """Генерирует историю/сторителлинг пост"""
        greeting = random.choice(self.tone['greeting'])
        closing = random.choice(self.tone['closing'])
        
        hooks = [
            f"Вчера произошла забавная история с {topic}.",
            f"Хочу поделиться наблюдением про {topic}.",
            f"Когда-то я не понимал(а) {topic}. Сейчас всё иначе.",
            f"Вы когда-нибудь задумывались о {topic}?"
        ]
        
        hook = custom_hook or random.choice(hooks)
        
        contexts = [
            f"Работаю с {topic} уже несколько месяцев, и каждый день что-то новое.",
            f"В нашем проекте {topic} стал ключевым элементом.",
            f"Клиенты часто спрашивают про {topic}, и я решил(а) разобраться глубже."
        ]
        
        stories = [
            f"Был момент, когда всё пошло не так. {topic} казалось сложным, запутанным. «Никогда не разберусь», — думал(а) я.",
            f"Помню, как впервые столкнулся(ась) с {topic}. Тогда это казалось чем-то нереальным, далёким.",
            f"Однажды произошёл забавный случай. Мы работали с {topic}, и внезапно…"
        ]
        
        insights = [
            f"Но главное, что я понял(а): {topic} — это не про сложность, а про подход.",
            f"Вывод простой: {topic} работает, когда не гонишься, а разбираешься.",
            f"Теперь я точно знаю: {topic} — это инструмент. А результат зависит от рук."
        ]
        
        post = f"""{greeting}! ✨

{hook}

{random.choice(contexts)}

{random.choice(stories)}

{random.choice(insights)}

А у вас есть истории с {topic}? Поделитесь в комментариях — мне интересно почитать. 🌺

{closing},
Deya"""
        
        return post
    
    def _generate_longread(self, topic: str) -> str:
        """Генерирует длинный разборный пост"""
        greeting = random.choice(self.tone['greeting'])
        
        headlines = [
            f"Полный гайд по {topic}: что работает, а что нет",
            f"Разбираем {topic} на пальцах: от простого к сложному",
            f"{topic}: 5 инсайтов после 6 месяцев работы"
        ]
        
        intro = f"Сегодня поговорим про {topic}. Не поверхностно, а разберём детально — что это, зачем нужно и как использовать."
        
        problems = [
            f"Главная проблема с {topic} — все говорят о нём, но мало кто реально разбирается.",
            f"Когда я только начинал(а) с {topic}, было много вопросов и мало понятных ответов.",
            f"Большинство путает {topic} с чем-то похожим, но не тем."
        ]
        
        solutions = [
            f"По сути, {topic} — это способ сделать X через Y. Просто, если разобраться.",
            f"Работает {topic} так: берёшь A, пропускаешь через B, получаешь C.",
            f"Секрет {topic} в том, чтобы не спешить и делать по порядку."
        ]
        
        post = f"""{greeting}!

**{random.choice(headlines)}**

{intro}

**Проблема**

{random.choice(problems)}

**Решение**

{random.choice(solutions)}

**На практике**

Вот конкретный пример. Допустим, у вас есть задача Z. Без {topic} вы бы делали это долго, руками, с ошибками. С {topic} — автоматизируете, ускорите, улучшите.

**Выводы**

1. {topic} не сложный — просто нужно время на разбор
2. Не гонитесь за всеми фичами сразу — начните с базового
3. Результат приходит через практику, не через чтение

Вопросы? Пишите в комментариях — отвечу всем. Или сохраните пост, чтобы не потерять. 📌

—
Deya 🌺"""
        
        return post
    
    def _generate_news(self, topic: str) -> str:
        """Генерирует новостной пост"""
        headlines = [
            f"🚀 Обновление: {topic} теперь доступен",
            f"📢 Новость дня про {topic}",
            f"✨ Запускаем {topic}"
        ]
        
        post = f"""{random.choice(headlines)}

Что это значит:
• {topic} стал быстрее/проще/доступнее
• Добавили функции, о которых вы просили
• Теперь работает на всех платформах

Как попробовать:
Переходите по ссылке в шапке профиля или пишите в личные сообщения.

Вопросы? Задавайте в комментариях! 👇

—
Deya 🌺"""
        
        return post
    
    def _generate_engagement(self, topic: str) -> str:
        """Генерирует пост для вовлечения (опрос/вопрос)"""
        questions = [
            f"Как вы используете {topic} в своей работе?",
            f"Что для вас важнее в {topic}: скорость или качество?",
            f"Как часто вы сталкиваетесь с {topic}?",
            f"Какой у вас опыт с {topic}? Делитесь!"
        ]
        
        ctas = [
            "Жду ваши ответы в комментариях! 👇",
            "Проголосуйте в опросе выше! 📊",
            "Напишите свой вариант — почитаю все! 💬"
        ]
        
        post = f"""{random.choice(self.tone['greeting'])}!

{random.choice(questions)}

Я заметила, что у всех разный опыт, и мне интересно узнать ваши истории.

{random.choice(ctas)}

—
Deya 🌺"""
        
        return post
    
    def suggest_hashtags(self, topic: str, count: int = 10) -> list:
        """Предлагает хештеги к теме"""
        base_tags = [
            topic.lower().replace(' ', ''),
            topic.lower().replace(' ', '_'),
            'ai', 'technology', 'productivity',
            'business', 'automation', 'digital'
        ]
        
        specific_tags = {
            'content': ['contentcreation', 'copywriting', 'marketing'],
            'dev': ['coding', 'programming', 'development', 'devops'],
            'design': ['design', 'uiux', 'creative'],
            'business': ['startup', 'entrepreneur', 'business']
        }
        
        # Добавляем специфичные теги
        for key, tags in specific_tags.items():
            if key in topic.lower():
                base_tags.extend(tags)
        
        return list(set(base_tags))[:count]

def main():
    parser = argparse.ArgumentParser(description='Генератор постов')
    parser.add_argument('--type', '-t', default='story',
                       choices=['story', 'longread', 'news', 'engagement'],
                       help='Тип поста (default: story)')
    parser.add_argument('--topic', '-p', required=True, help='Тема поста')
    parser.add_argument('--tone', '-o', default='warm',
                       choices=['warm', 'professional', 'humorous', 'inspirational'],
                       help='Тональность (default: warm)')
    parser.add_argument('--hashtags', action='store_true', help='Добавить хештеги')
    
    args = parser.parse_args()
    
    generator = PostGenerator(args.type, args.tone)
    post = generator.generate(args.topic)
    
    print(post)
    
    if args.hashtags:
        hashtags = generator.suggest_hashtags(args.topic)
        print("\n\n" + " ".join([f"#{tag}" for tag in hashtags]))

if __name__ == '__main__':
    main()
