#!/usr/bin/env python3
"""
Reply Assistant - помощник в ответах на письма
Анализирует входящее письмо и генерирует подходящий ответ
"""

import argparse
import re
from datetime import datetime
from typing import Dict, List, Optional

class ReplyAssistant:
    """Ассистент для ответов на email"""
    
    def __init__(self, tone: str = 'professional'):
        self.tone = tone
    
    def analyze_email(self, email_text: str) -> Dict:
        """Анализирует входящее письмо"""
        analysis = {
            'sentiment': self._detect_sentiment(email_text),
            'urgency': self._detect_urgency(email_text),
            'questions': self._extract_questions(email_text),
            'action_items': self._extract_action_items(email_text),
            'tone': self._detect_tone(email_text),
            'topics': self._extract_topics(email_text)
        }
        return analysis
    
    def generate_reply(self, incoming_email: str, context: Dict = None) -> Dict:
        """Генерирует ответ на письмо"""
        context = context or {}
        
        # Анализируем письмо
        analysis = self.analyze_email(incoming_email)
        
        # Извлекаем информацию об отправителе
        sender_name = self._extract_sender_name(incoming_email)
        
        # Генерируем ответ
        reply_body = self._compose_reply(analysis, sender_name, context)
        
        # Формируем полный ответ
        reply = {
            'subject': self._generate_subject(incoming_email),
            'body': reply_body,
            'tone': self.tone,
            'analysis': analysis,
            'timestamp': datetime.now().isoformat()
        }
        
        return reply
    
    def _detect_sentiment(self, text: str) -> str:
        """Определяет тональность письма"""
        positive_words = ['thank', 'great', 'excellent', 'love', 'happy', 'pleased', 'appreciate']
        negative_words = ['problem', 'issue', 'error', 'bad', 'disappointed', 'frustrated', 'complaint']
        
        text_lower = text.lower()
        pos_count = sum(1 for word in positive_words if word in text_lower)
        neg_count = sum(1 for word in negative_words if word in text_lower)
        
        if neg_count > pos_count:
            return 'negative'
        elif pos_count > neg_count:
            return 'positive'
        else:
            return 'neutral'
    
    def _detect_urgency(self, text: str) -> str:
        """Определяет срочность"""
        urgent_words = ['urgent', 'asap', 'immediately', 'deadline', 'today', 'emergency']
        text_lower = text.lower()
        
        urgency_score = sum(2 if word in text_lower else 0 for word in urgent_words)
        
        if urgency_score >= 4:
            return 'high'
        elif urgency_score >= 2:
            return 'medium'
        else:
            return 'low'
    
    def _extract_questions(self, text: str) -> List[str]:
        """Извлекает вопросы из письма"""
        # Ищем предложения со знаком вопроса
        questions = re.findall(r'[^.!?]*\?', text)
        return [q.strip() for q in questions if len(q.strip()) > 10]
    
    def _extract_action_items(self, text: str) -> List[str]:
        """Извлекает action items"""
        action_patterns = [
            r'please (\w+.*?)\.',
            r'can you (\w+.*?)\?',
            r'need to (\w+.*?)\.',
            r'should (\w+.*?)\.'
        ]
        
        actions = []
        for pattern in action_patterns:
            matches = re.findall(pattern, text.lower())
            actions.extend(matches)
        
        return actions[:5]  # Максимум 5
    
    def _detect_tone(self, text: str) -> str:
        """Определяет тон письма"""
        formal_markers = ['dear', 'sincerely', 'regards', 'would you', 'could you']
        casual_markers = ['hey', 'hi', 'thanks', 'cheers', 'btw']
        
        text_lower = text.lower()
        formal_count = sum(1 for m in formal_markers if m in text_lower)
        casual_count = sum(1 for m in casual_markers if m in text_lower)
        
        if formal_count > casual_count:
            return 'formal'
        elif casual_count > formal_count:
            return 'casual'
        else:
            return 'neutral'
    
    def _extract_topics(self, text: str) -> List[str]:
        """Извлекает основные темы"""
        # Простое извлечение по ключевым словам
        common_topics = ['meeting', 'proposal', 'project', 'question', 'issue', 'update', 'deadline']
        text_lower = text.lower()
        
        found_topics = [topic for topic in common_topics if topic in text_lower]
        return found_topics
    
    def _extract_sender_name(self, text: str) -> str:
        """Извлекает имя отправителя"""
        # Ищем подпись в конце письма
        lines = text.strip().split('\n')
        
        # Обычно имя в последних 3 строках
        for line in reversed(lines[-5:]):
            line = line.strip()
            if line and not line.startswith('>'):
                # Простая эвристика: короткая строка без спецсимволов
                if len(line) < 50 and not any(c in line for c in ['@', 'http', 'www']):
                    return line
        
        return 'there'
    
    def _generate_subject(self, incoming_email: str) -> str:
        """Генерирует subject для ответа"""
        # Ищем оригинальный subject
        lines = incoming_email.split('\n')
        for line in lines[:10]:
            if line.lower().startswith('subject:'):
                original = line.split(':', 1)[1].strip()
                if not original.startswith('Re:'):
                    return f"Re: {original}"
                return original
        
        return "Re: Your email"
    
    def _compose_reply(self, analysis: Dict, sender_name: str, context: Dict) -> str:
        """Составляет текст ответа"""
        lines = []
        
        # Приветствие
        greeting = self._get_greeting(sender_name, analysis['tone'])
        lines.append(greeting)
        lines.append("")
        
        # Благодарность (если письмо позитивное)
        if analysis['sentiment'] == 'positive':
            lines.append("Thank you for your email.")
            lines.append("")
        
        # Ответы на вопросы
        if analysis['questions']:
            lines.append("To answer your questions:")
            lines.append("")
            for i, question in enumerate(analysis['questions'], 1):
                lines.append(f"{i}. Regarding '{question}' - [Please provide your answer here]")
            lines.append("")
        
        # Подтверждение action items
        if analysis['action_items']:
            if analysis['urgency'] == 'high':
                lines.append("I understand the urgency. I'll take care of the following immediately:")
            else:
                lines.append("I'll work on the following:")
            lines.append("")
            for item in analysis['action_items']:
                lines.append(f"- {item}")
            lines.append("")
        
        # Сроки для срочных писем
        if analysis['urgency'] == 'high':
            lines.append("I'll get back to you with a complete response by end of day.")
            lines.append("")
        
        # Предложение помощи
        if context.get('offer_help', True):
            lines.append("Please let me know if you need any clarification or have additional questions.")
            lines.append("")
        
        # Закрытие
        closing = self._get_closing(analysis['tone'])
        lines.append(closing)
        lines.append("")
        lines.append("Deya")
        if context.get('signature'):
            lines.append(context['signature'])
        
        return '\n'.join(lines)
    
    def _get_greeting(self, name: str, their_tone: str) -> str:
        """Выбирает приветствие"""
        if self.tone == 'formal':
            return f"Dear {name}"
        elif self.tone == 'friendly':
            return f"Hi {name}"
        else:
            return f"Hello {name}"
    
    def _get_closing(self, their_tone: str) -> str:
        """Выбирает закрытие"""
        if self.tone == 'formal':
            return "Sincerely,"
        elif self.tone == 'friendly':
            return "Best,"
        else:
            return "Best regards,"
    
    def print_analysis(self, analysis: Dict):
        """Выводит анализ письма"""
        print("\n📊 Email Analysis:")
        print(f"  Sentiment: {analysis['sentiment']}")
        print(f"  Urgency: {analysis['urgency']}")
        print(f"  Tone: {analysis['tone']}")
        print(f"  Topics: {', '.join(analysis['topics']) if analysis['topics'] else 'None detected'}")
        print(f"  Questions found: {len(analysis['questions'])}")
        print(f"  Action items: {len(analysis['action_items'])}")
        
        if analysis['questions']:
            print("\n  Questions:")
            for q in analysis['questions'][:3]:
                print(f"    - {q[:80]}...")
        
        if analysis['action_items']:
            print("\n  Action Items:")
            for item in analysis['action_items'][:3]:
                print(f"    - {item}")

def main():
    parser = argparse.ArgumentParser(description='Email Reply Assistant')
    parser.add_argument('--file', '-f', help='Input email file')
    parser.add_argument('--text', '-t', help='Input email text')
    parser.add_argument('--tone', choices=['formal', 'professional', 'friendly', 'casual'],
                       default='professional', help='Reply tone')
    parser.add_argument('--analyze', '-a', action='store_true', help='Only analyze, no reply')
    parser.add_argument('--output', '-o', help='Output file for reply')
    
    args = parser.parse_args()
    
    # Получаем входящее письмо
    if args.file:
        with open(args.file, 'r') as f:
            incoming = f.read()
    elif args.text:
        incoming = args.text
    else:
        print("❌ Error: Provide either --file or --text")
        return
    
    # Создаём ассистента
    assistant = ReplyAssistant(args.tone)
    
    if args.analyze:
        # Только анализ
        analysis = assistant.analyze_email(incoming)
        assistant.print_analysis(analysis)
    else:
        # Генерируем ответ
        reply = assistant.generate_reply(incoming)
        
        # Выводим анализ
        assistant.print_analysis(reply['analysis'])
        
        # Выводим ответ
        print("\n" + "="*70)
        print("📝 SUGGESTED REPLY:")
        print("="*70)
        print(f"Subject: {reply['subject']}\n")
        print(reply['body'])
        print("="*70)
        
        # Сохраняем если нужно
        if args.output:
            with open(args.output, 'w') as f:
                f.write(f"Subject: {reply['subject']}\n\n")
                f.write(reply['body'])
            print(f"\n✅ Reply saved to: {args.output}")

if __name__ == '__main__':
    main()
