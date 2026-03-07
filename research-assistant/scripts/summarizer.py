#!/usr/bin/env python3
"""
Summarizer - суммаризация документов и текстов
Создаёт краткие пересказы разной длины и формата
"""

import argparse
from pathlib import Path
from typing import List, Dict
import re

class Summarizer:
    """Инструмент суммаризации"""
    
    def __init__(self, text: str = None, file_path: str = None):
        self.text = text
        self.file_path = file_path
        
        if file_path and not text:
            self._load_file()
    
    def _load_file(self):
        """Загружает текст из файла"""
        path = Path(self.file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {self.file_path}")
        
        suffix = path.suffix.lower()
        
        if suffix == '.txt':
            with open(path, 'r', encoding='utf-8') as f:
                self.text = f.read()
        elif suffix == '.md':
            with open(path, 'r', encoding='utf-8') as f:
                self.text = f.read()
        elif suffix == '.pdf':
            # В реальности - используем PyPDF2 или pdfplumber
            self.text = "[PDF content would be extracted here]"
        else:
            with open(path, 'r', encoding='utf-8') as f:
                self.text = f.read()
        
        print(f"📄 Loaded: {len(self.text)} characters from {path.name}")
    
    def summarize(self, length: str = 'medium', format: str = 'paragraph') -> str:
        """Создаёт summary текста"""
        
        if not self.text:
            return "No text to summarize"
        
        # Определяем длину summary
        length_ratios = {
            'short': 0.1,    # 10% от оригинала
            'medium': 0.2,   # 20% от оригинала
            'long': 0.3      # 30% от оригинала
        }
        
        ratio = length_ratios.get(length, 0.2)
        
        # Разбиваем на предложения
        sentences = self._split_sentences(self.text)
        
        # Оцениваем важность предложений
        scored_sentences = self._score_sentences(sentences)
        
        # Выбираем топ-N предложений
        target_count = max(1, int(len(sentences) * ratio))
        top_sentences = scored_sentences[:target_count]
        
        # Сортируем по порядку в оригинальном тексте
        top_sentences.sort(key=lambda x: x['index'])
        
        # Форматируем вывод
        if format == 'paragraph':
            summary = ' '.join(s['text'] for s in top_sentences)
        elif format == 'bullet-points':
            summary = '\n'.join(f"• {s['text']}" for s in top_sentences)
        elif format == 'numbered':
            summary = '\n'.join(f"{i+1}. {s['text']}" for i, s in enumerate(top_sentences))
        else:
            summary = ' '.join(s['text'] for s in top_sentences)
        
        return summary
    
    def _split_sentences(self, text: str) -> List[str]:
        """Разбивает текст на предложения"""
        # Простое разбиение по знакам окончания предложения
        sentences = re.split(r'(?<=[.!?])\s+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def _score_sentences(self, sentences: List[str]) -> List[Dict]:
        """Оценивает важность предложений"""
        # Простой алгоритм на основе:
        # 1. Длины предложения (не слишком короткие, не слишком длинные)
        # 2. Наличия ключевых слов
        # 3. Позиции (начало и конец важнее)
        
        # Извлекаем ключевые слова (наиболее частые слова)
        words = re.findall(r'\b[a-zA-Z]{4,}\b', self.text.lower())
        word_freq = {}
        for word in words:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        # Топ-10 ключевых слов
        key_words = set(sorted(word_freq, key=word_freq.get, reverse=True)[:10])
        
        scored = []
        for i, sentence in enumerate(sentences):
            score = 0
            
            # Позиция (начало и конец важнее)
            if i < 2:
                score += 3
            elif i > len(sentences) - 3:
                score += 2
            else:
                score += 1
            
            # Длина (оптимальная 10-30 слов)
            word_count = len(sentence.split())
            if 10 <= word_count <= 30:
                score += 2
            elif 5 <= word_count < 10 or 30 < word_count <= 40:
                score += 1
            
            # Ключевые слова
            sentence_words = set(re.findall(r'\b[a-zA-Z]{4,}\b', sentence.lower()))
            key_matches = sentence_words & key_words
            score += len(key_matches)
            
            # Цифры и даты (часто важны)
            if re.search(r'\d{4}|\d+%|\d+ million|\d+ billion', sentence):
                score += 1
            
            scored.append({
                'index': i,
                'text': sentence,
                'score': score,
                'word_count': word_count
            })
        
        # Сортируем по score
        scored.sort(key=lambda x: x['score'], reverse=True)
        
        return scored
    
    def extract_key_points(self, count: int = 5) -> List[str]:
        """Извлекает ключевые тезисы"""
        sentences = self._split_sentences(self.text)
        scored = self._score_sentences(sentences)
        
        # Берём топ-N
        top = scored[:count]
        
        # Сортируем по порядку в тексте
        top.sort(key=lambda x: x['index'])
        
        return [s['text'] for s in top]
    
    def generate_tldr(self) -> str:
        """Создаёт TL;DR (2-3 предложения)"""
        return self.summarize(length='short', format='paragraph')
    
    def get_stats(self) -> Dict:
        """Возвращает статистику текста"""
        words = len(self.text.split())
        sentences = len(self._split_sentences(self.text))
        paragraphs = len([p for p in self.text.split('\n\n') if p.strip()])
        
        return {
            'characters': len(self.text),
            'words': words,
            'sentences': sentences,
            'paragraphs': paragraphs,
            'avg_words_per_sentence': round(words / sentences, 1) if sentences > 0 else 0
        }

def main():
    parser = argparse.ArgumentParser(description='Text Summarization Tool')
    parser.add_argument('--file', '-f', help='Input file to summarize')
    parser.add_argument('--text', '-t', help='Input text to summarize')
    parser.add_argument('--length', '-l', default='medium',
                       choices=['short', 'medium', 'long'],
                       help='Summary length')
    parser.add_argument('--format', default='paragraph',
                       choices=['paragraph', 'bullet-points', 'numbered'],
                       help='Output format')
    parser.add_argument('--key-points', '-k', type=int, help='Extract N key points')
    parser.add_argument('--tldr', action='store_true', help='Generate TL;DR')
    parser.add_argument('--stats', '-s', action='store_true', help='Show text statistics')
    parser.add_argument('--output', '-o', help='Output file')
    
    args = parser.parse_args()
    
    # Проверяем входные данные
    if not args.file and not args.text:
        print("❌ Error: Provide either --file or --text")
        return
    
    # Создаём суммаризатор
    summarizer = Summarizer(text=args.text, file_path=args.file)
    
    # Статистика
    if args.stats:
        stats = summarizer.get_stats()
        print("\n📊 Text Statistics:")
        for key, value in stats.items():
            print(f"   {key}: {value}")
        print()
    
    # Генерация summary
    if args.tldr:
        summary = summarizer.generate_tldr()
        print("\n📝 TL;DR:")
        print(summary)
    
    elif args.key_points:
        points = summarizer.extract_key_points(args.key_points)
        print(f"\n🔑 Key Points ({len(points)}):")
        for i, point in enumerate(points, 1):
            print(f"{i}. {point}")
    
    else:
        summary = summarizer.summarize(length=args.length, format=args.format)
        print(f"\n📄 Summary ({args.length}, {args.format}):")
        print(summary)
    
    # Сохранение
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            if args.tldr:
                f.write(summarizer.generate_tldr())
            elif args.key_points:
                points = summarizer.extract_key_points(args.key_points)
                f.write('\n'.join(points))
            else:
                f.write(summarizer.summarize(length=args.length, format=args.format))
        print(f"\n✅ Saved to: {args.output}")

if __name__ == '__main__':
    main()
