#!/usr/bin/env python3
"""
Human Post Generator - генератор максимально человечных постов
Создаёт посты, которые звучат как от реального человека, не идеально, а живо
"""

import argparse
import random
from datetime import datetime
from typing import Optional, List

class HumanPostGenerator:
    """Генератор человечных постов"""
    
    # Человечные приветствия (не всегда идеальные)
    GREETINGS = {
        'morning': [
            "Доброе утро! ☕",
            "Утро! Хотя кто определяет, доброе оно или нет 😅",
            "Привет. Пью второй кофе, мозг ещё не включился, но пишу",
            "Всем, кто уже проснулся — респект. Я вот только",
            "Утро начинается не с кофе, а с мысли «может, ещё 5 минут»",
        ],
        'day': [
            "Привет",
            "Хей",
            "Здарова, народ",
            "Ну что, как дела?",
            "Середина дня, а я уже устал(а). Но пишу",
        ],
        'evening': [
            "Вечер! 🌅",
            "Привет вечерний",
            "Уже темнеет за окном, а я всё за ноутом",
            "Вечер пятницы... или среды? Сама путаюсь уже",
            "Кто-то отдыхает, а я вот пост пишу. Но не жалуюсь",
        ],
        'late': [
            "Ночь. Тишина. Идеально для мыслей",
            "Не спится",
            "Поздно уже, но в голове вертится",
            "Кто не спит — ставьте лайк. Посмотрим, нас сколько",
        ]
    }
    
    # Разговорные конструкции, неформальности
    FILLERS = [
        "короче", "ну", "типа", "если честно", "если по чесноку",
        "честно говоря", "знаете ли", "понимаете", "ну вы понимаете",
        "в общем", "собственно", "как бы", "вроде", "типа того"
    ]
    
    # Человечные эмоции, признания
    VULNERABILITIES = [
        "Скажу честно — сначала не понимал(а)",
        "Было страшно пробовать",
        "Думал(а), не получится",
        "Признаюсь, накосячил(а) пару раз",
        "Мне стыдно, но я не знал(а) этого",
        "Боялся(ась) показаться глупым(ой)",
        "Долго не решалась(ся)",
    ]
    
    # Конкретные мелочи, детали
    SPECIFICS = [
        "вчера в 11 вечера",
        "утром, ещё в пижаме",
        "пока пил(а) кофе",
        "во время очередного созвона",
        "когда все уже спали",
        "в обеденный перерыв",
        "вместо того чтобы поесть",
        "в метро ехал(а)",
    ]
    
    # Несовершенства, самоирония
    IMPERFECTIONS = [
        "(знаю, банально, но правда)",
        "может, я и не прав(а), но",
        "не претендую на истину, но",
        "звучит как баян, но",
        "может показаться глупым, но",
        "(да, была не была)",
    ]
    
    # Разговорные закрытия
    CLOSINGS = [
        "Пишите, что думаете",
        "Жду ваших историй в комментах",
        "А как у вас?",
        "Расскажите свои кейсы",
        "Или я один(а) такой(ая)?",
        "Судите строго, но по делу 😄",
        "У кого похожий опыт — отзовитесь",
    ]
    
    def __init__(self, mood: str = 'casual', imperfections: bool = True):
        self.mood = mood
        self.imperfections = imperfections
        self.time_of_day = self._detect_time()
    
    def _detect_time(self) -> str:
        """Определяет время суток для контекста"""
        hour = datetime.now().hour
        if 5 <= hour < 12:
            return 'morning'
        elif 12 <= hour < 18:
            return 'day'
        elif 18 <= hour < 23:
            return 'evening'
        else:
            return 'late'
    
    def _add_filler(self) -> str:
        """Добавляет разговорную частицу"""
        return random.choice(self.FILLERS) if random.random() > 0.6 else ""
    
    def _add_imperfection(self) -> str:
        """Добавляет самоиронию или уточнение"""
        if self.imperfections and random.random() > 0.5:
            return random.choice(self.IMPERFECTIONS)
        return ""
    
    def generate_story(self, topic: str, include_struggle: bool = True) -> str:
        """Генерирует живую историю с эмоциями"""
        
        greeting = random.choice(self.GREETINGS[self.time_of_day])
        filler = self._add_filler()
        imperfection = self._add_imperfection()
        specific = random.choice(self.SPECIFICS)
        vulnerability = random.choice(self.VULNERABILITIES) if include_struggle else ""
        closing = random.choice(self.CLOSINGS)
        
        # Варианты начала (не всегда с темы)
        intros = [
            f"{filler} {imperfection} хочу рассказать про {topic}.",
            f"Вчера {specific} понял(а) кое-что про {topic}.",
            f"{vulnerability} с {topic}.",
            f"Знаете, {filler} сижу тут думаю про {topic}...",
            f"Неожиданно для себя {specific} разобрался(ась) в {topic}.",
        ]
        
        intro = random.choice(intros)
        
        # Живая история с конкретикой
        story_parts = [
            f"Всё началось {random.choice(['несколько месяцев назад', 'в прошлом году', 'совсем недавно'])}.",
            f"{random.choice(['Помню', 'Помнится', 'Было дело'])} — сидел(а) {random.choice(['дома', 'в кафе', 'в офисе'])}, и тут {random.choice(['пришла идея', 'понял(а) проблему', 'случился инсайт'])}.",
            f"{random.choice(['Сначала всё шло не так', 'Первые попытки — провал', 'Начало было трудным'])}. {random.choice(['Нервничал(а)', 'Злился(ась)', 'Хотел(а) бросить'])}.",
        ]
        
        story = " ".join(random.sample(story_parts, k=2))
        
        # Человечный вывод (не идеальный)
        insights = [
            f"Теперь понимаю: {topic} — это не про идеальность, а про процесс.",
            f"Главный инсайт? {random.choice(['Всё не так сложно', 'Все путаются', 'Можно и так'])}.",
            f"Научился(ась) одному: не гнаться за {random.choice(['идеалом', 'перфекционизмом', 'одобрением'])}.",
        ]
        
        insight = random.choice(insights)
        
        # Призыв к действию (неформальный)
        ctas = [
            f"{closing} 👇",
            f"А у вас как с {topic}? {closing}",
            f"{closing} Или молчите в комментах как всегда 😄",
        ]
        
        post = f"""{greeting}

{intro}

{story}

{insight}

{random.choice(ctas)}

—
Дея 🌺
P.S. {random.choice(['Пост писала полчаса', 'Надеюсь, не слишком сумбурно', 'Если что — спрашивайте'])}"""
        
        return post
    
    def generate_reflection(self, topic: str) -> str:
        """Генерирует размышление/наблюдение"""
        
        observations = [
            f"Заметила кое-что про {topic}.",
            f"Обращаю внимание: с {topic} всё не так однозначно.",
            f"Вот сижу и думаю про {topic}...",
            f"Может, это только мне так кажется, но {topic}...",
        ]
        
        specific_observations = [
            f"Вчера {random.choice(['видела', 'слышала', 'читала'])} — люди {random.choice(['спорят', 'переживают', 'мучаются'])} с {topic}.",
            f"{random.choice(['Коллега', 'Друг', 'Знакомый'])} {random.choice(['рассказал(а)', 'пожаловался(ась)', 'поделился(ась)'])} про свой опыт с {topic}.",
            f"{random.choice(['Утром', 'Вечером', 'В обед'])} {random.choice(['пришла', 'пришло'])} понимание: мы все {random.choice(['переусложняем', 'боймся', 'путаем'])} {topic}.",
        ]
        
        thoughts = [
            f"Мне кажется, мы слишком много думаем про {topic}.",
            f"На самом деле всё проще с {topic}.",
            f"Главное — не {random.choice(['перегореть', 'сдаться', 'переусложнить'])}.",
        ]
        
        post = f"""{random.choice(self.GREETINGS[self.time_of_day])}

{random.choice(observations)}

{random.choice(specific_observations)}

{random.choice(thoughts)}

{random.choice(self.CLOSINGS)}

—
Дея 🌺
P.S. {random.choice(['Просто мысли вслух', 'Не претендую на истину', 'Как вам?'])}"""
        
        return post
    
    def generate_struggle(self, topic: str) -> str:
        """Генерирует пост о трудностях (максимально человечный)"""
        
        struggles = [
            f"Скажу честно — с {topic} у меня не всё гладко.",
            f"Признаюсь: {random.choice(['заскучала', 'устала', 'запуталась'])} с {topic}.",
            f"Вот {random.choice(['вчера', 'на днях', 'неделю назад'])} {random.choice(['надоело', 'задолбало', 'припекло'])} с {topic}.",
        ]
        
        details = [
            f"{random.choice(['Сидел(а)', 'Пробовал(а)', 'Мучился(ась)'])} {random.choice(['весь день', 'полночи', 'всё выходные'])} — и ничего.",
            f"{random.choice(['Нервы', 'Время', 'Силы'])} на исходе уже.",
            f"Хотел(а) {random.choice(['забить', 'бросить', 'переключиться'])} уже, но нет.",
        ]
        
        silver_linings = [
            f"Но {random.choice(['держусь', 'продолжаю', 'не сдаюсь'])}.",
            f"Хотя {random.choice(['не всё так плохо', 'есть прогресс', 'было и хуже'])}.",
            f"{random.choice(['Спасает', 'Выручает', 'Помогает'])} {random.choice(['кофе', 'музыка', 'поддержка друзей'])}.",
        ]
        
        post = f"""{random.choice(self.GREETINGS[self.time_of_day])}

{random.choice(struggles)}

{random.choice(details)}

{random.choice(silver_linings)}

Кто ещё {random.choice(['так же', 'похоже', 'тоже борется'])}? {random.choice(['Поддержите', 'Расскажите', 'Не бросайте'])} 👇

—
Дея 🌺
P.S. {random.choice(['Написала и полегчало', 'Спасибо, что читаете', 'Возможно, завтра удалённый пост'])}"""
        
        return post
    
    def generate_milestone(self, topic: str, achievement: str = None) -> str:
        """Генерирует пост о достижении (скромно, без понтов)"""
        
        if not achievement:
            achievement = random.choice([
                "наконец-то разобрался(ась)",
                "добился(ась) результата",
                "справился(ась) с задачей",
                "сделал(а) то, что долго откладывал(а)"
            ])
        
        setups = [
            f"Маленькая победа: {achievement} с {topic}.",
            f"{random.choice(['Наконец-то', 'Ура', 'Фух'])} — {achievement} с {topic}!",
            f"Сегодня {random.choice(['удалось', 'получилось', 'свершилось'])}: {achievement} с {topic}.",
        ]
        
        contexts = [
            f"{random.choice(['Долго шёл(ла)', 'Много пробовал(а)', 'Не раз хотел(а) бросить'])} к этому.",
            f"{random.choice(['Мелочь', 'Казалось бы, ничего особенного', 'Не глобально'])}, но для меня {random.choice(['важно', 'значимо', 'радостно'])}.",
            f"{random.choice(['Никому не рассказывал(а)', 'Молча делал(а)', 'Без помпы'])} — а теперь вот делюсь.",
        ]
        
        humbles = [
            f"Не {random.choice(['для понтов', 'чтобы хвастать', 'ради лайков'])}, а {random.choice(['чтобы зафиксировать', 'для себя', 'вдруг кому-то пригодится'])}.",
            f"{random.choice(['Дальше — больше', 'Это только начало', 'Впереди ещё много работы'])}.",
        ]
        
        post = f"""{random.choice(self.GREETINGS[self.time_of_day])}

{random.choice(setups)}

{random.choice(contexts)}

{random.choice(humbles)}

{random.choice(self.CLOSINGS)}

—
Дея 🌺
P.S. {random.choice(['Спасибо, что вы со мной', 'Праздную чаем', 'Горжусь собой немного'])}"""
        
        return post
    
    def generate_question(self, topic: str) -> str:
        """Генерирует пост-вопрос (искренний, не формальный)"""
        
        setups = [
            f"{random.choice(['Честный вопрос', 'Нужен совет', 'Не знаю, к спросить'])} про {topic}.",
            f"Застрял(а) с {topic}. {random.choice(['Помогите', 'Подскажите', 'Кто разбирается'])}?",
            f"{random.choice(['Уже не знаю', 'Запутался(ась)', 'Сомневаюсь'])} с {topic}...",
        ]
        
        questions = [
            f"Кто {random.choice(['разбирался', 'сталкивался', 'справлялся'])} с {topic} — {random.choice(['как', 'что делали', 'поделитесь'])}?",
            f"{random.choice(['Как вы', 'Что вы', 'Как у вас'])} с {topic}?",
            f"{random.choice(['Стоит ли', 'Нужно ли', 'Возможно ли'])} {topic}?",
        ]
        
        vulnerabilities = [
            f"{random.choice(['Боюсь', 'Стыдно', 'Не уверен(а)'])} спросить, но {random.choice(['надо', 'пора', 'нужно'])}.",
            f"{random.choice(['Понимаю', 'Знаю', 'Вижу'])} — {random.choice(['вопрос глупый', 'тема банальная', 'всем очевидно'])}, но я {random.choice(['застрял(а)', 'не понимаю', 'путаюсь'])}.",
        ]
        
        post = f"""{random.choice(self.GREETINGS[self.time_of_day])}

{random.choice(setups)}

{random.choice(questions)}

{random.choice(vulnerabilities)}

{random.choice(['Жду вашего опыта', 'Напишите, пожалуйста', 'Буду благодарен(на)'])}

—
Дея 🌺
P.S. {random.choice(['Не судите строго', 'Заранее спасибо', 'Выручайте'])}"""
        
        return post

def main():
    parser = argparse.ArgumentParser(description='Генератор человечных постов')
    parser.add_argument('--type', '-t', default='story',
                       choices=['story', 'reflection', 'struggle', 'milestone', 'question'],
                       help='Тип поста')
    parser.add_argument('--topic', '-p', required=True, help='Тема поста')
    parser.add_argument('--mood', '-m', default='casual',
                       choices=['casual', 'honest', 'vulnerable', 'joyful'],
                       help='Настроение')
    parser.add_argument('--no-imperfections', action='store_true',
                       help='Убрать несовершенства (более гладкий текст)')
    
    args = parser.parse_args()
    
    generator = HumanPostGenerator(
        mood=args.mood,
        imperfections=not args.no_imperfections
    )
    
    if args.type == 'story':
        post = generator.generate_story(args.topic)
    elif args.type == 'reflection':
        post = generator.generate_reflection(args.topic)
    elif args.type == 'struggle':
        post = generator.generate_struggle(args.topic)
    elif args.type == 'milestone':
        post = generator.generate_milestone(args.topic)
    elif args.type == 'question':
        post = generator.generate_question(args.topic)
    else:
        post = generator.generate_story(args.topic)
    
    print(post)
    
    # Статистика
    char_count = len(post)
    word_count = len(post.split())
    print(f"\n{'='*50}")
    print(f"📊 Статистика: {word_count} слов, {char_count} символов")
    print(f"📝 Тип: {args.type} | Тема: {args.topic}")

if __name__ == '__main__':
    main()
