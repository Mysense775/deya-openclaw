#!/usr/bin/env python3
"""
Timing Analyzer - анализатор времени публикаций
Анализирует статистику канала и определяет лучшее время для постов
"""

import argparse
import json
from datetime import datetime, timedelta
from collections import defaultdict
import statistics

class TimingAnalyzer:
    """Анализатор времени публикаций"""
    
    # Оптимальные времена по умолчанию (если нет данных)
    DEFAULT_BEST_TIMES = {
        'telegram': ['09:00', '12:00', '18:00'],
        'instagram': ['09:00', '13:00', '19:00'],
        'twitter': ['08:00', '12:00', '17:00'],
        'linkedin': ['08:00', '12:00', '17:00']
    }
    
    # Дни недели с наибольшей активностью
    BEST_DAYS = ['Tuesday', 'Wednesday', 'Thursday']
    
    def __init__(self, platform: str = 'telegram'):
        self.platform = platform
    
    def analyze_channel_stats(self, posts_data: list) -> dict:
        """
        Анализирует статистику постов канала
        posts_data: список словарей с {'date': '2026-03-01 09:30', 'views': 150, 'reactions': 12}
        """
        if not posts_data:
            return self._get_default_schedule()
        
        # Группировка по часам
        hourly_stats = defaultdict(lambda: {'views': [], 'engagement': []})
        daily_stats = defaultdict(lambda: {'views': [], 'engagement': []})
        
        for post in posts_data:
            try:
                post_time = datetime.strptime(post['date'], '%Y-%m-%d %H:%M')
                hour = post_time.hour
                day = post_time.strftime('%A')
                
                views = post.get('views', 0)
                engagement = post.get('reactions', 0) + post.get('comments', 0) + post.get('shares', 0)
                
                hourly_stats[hour]['views'].append(views)
                hourly_stats[hour]['engagement'].append(engagement)
                
                daily_stats[day]['views'].append(views)
                daily_stats[day]['engagement'].append(engagement)
            except:
                continue
        
        # Расчёт средних значений
        hourly_scores = {}
        for hour, stats in hourly_stats.items():
            if stats['views']:
                avg_views = statistics.mean(stats['views'])
                avg_engagement = statistics.mean(stats['engagement'])
                # Скор = средние просмотры + коэффициент вовлечения * 10
                hourly_scores[hour] = avg_views + (avg_engagement * 10)
        
        daily_scores = {}
        for day, stats in daily_stats.items():
            if stats['views']:
                avg_views = statistics.mean(stats['views'])
                avg_engagement = statistics.mean(stats['engagement'])
                daily_scores[day] = avg_views + (avg_engagement * 10)
        
        # Сортировка
        best_hours = sorted(hourly_scores.items(), key=lambda x: x[1], reverse=True)[:3]
        best_days = sorted(daily_scores.items(), key=lambda x: x[1], reverse=True)[:3]
        
        return {
            'best_hours': [f"{h:02d}:00" for h, _ in best_hours],
            'best_days': [day for day, _ in best_days],
            'hourly_stats': dict(hourly_stats),
            'daily_stats': dict(daily_stats),
            'data_based': True
        }
    
    def _get_default_schedule(self) -> dict:
        """Возвращает расписание по умолчанию"""
        return {
            'best_hours': self.DEFAULT_BEST_TIMES.get(self.platform, ['09:00', '12:00', '18:00']),
            'best_days': self.BEST_DAYS,
            'hourly_stats': {},
            'daily_stats': {},
            'data_based': False
        }
    
    def generate_weekly_schedule(self, content_plan: list, stats: dict = None) -> list:
        """
        Генерирует оптимальное расписание публикаций на неделю
        """
        if stats is None:
            stats = self._get_default_schedule()
        
        best_hours = stats['best_hours']
        best_days = stats['best_days']
        
        schedule = []
        
        for i, content in enumerate(content_plan):
            day = content.get('day', 'Monday')
            content_type = content.get('type', 'story')
            
            # Выбор времени в зависимости от типа контента
            if content_type == 'story':
                time_slot = best_hours[0] if best_hours else '09:00'
            elif content_type == 'longread':
                time_slot = best_hours[1] if len(best_hours) > 1 else '12:00'
            elif content_type == 'engagement':
                time_slot = best_hours[2] if len(best_hours) > 2 else '18:00'
            else:
                time_slot = best_hours[0] if best_hours else '09:00'
            
            # Проверяем, является ли день оптимальным
            is_optimal_day = day in best_days
            
            schedule.append({
                'day': day,
                'time': time_slot,
                'content_type': content_type,
                'topic': content.get('topic_angle', 'General'),
                'optimal': is_optimal_day,
                'reason': f"{day} - {'оптимальный' if is_optimal_day else 'нормальный'} день, {time_slot} - пик активности"
            })
        
        return schedule
    
    def get_posting_recommendations(self, stats: dict = None) -> str:
        """Возвращает текстовые рекомендации по времени публикаций"""
        if stats is None:
            stats = self._get_default_schedule()
        
        hours = stats['best_hours']
        days = stats['best_days']
        
        rec = f"""📊 **Рекомендации по времени публикаций ({self.platform})**

🕐 **Лучшие часы:**
"""
        
        time_descriptions = {
            '09:00': 'Утро — люди проверяют сообщения за завтраком',
            '12:00': 'Обеденный перерыв — время для чтения',
            '13:00': 'Обед — пик активности в соцсетях',
            '18:00': 'Вечер — возвращение домой, расслабленное чтение',
            '19:00': 'Вечер — пик активности после работы',
            '08:00': 'Раннее утро — первые проверки телефона',
            '17:00': 'Конец рабочего дня — последние проверки'
        }
        
        for hour in hours:
            desc = time_descriptions.get(hour, 'Хорошее время для публикации')
            rec += f"• {hour} — {desc}\n"
        
        rec += f"\n📅 **Лучшие дни:** {', '.join(days)}\n"
        
        if not stats.get('data_based'):
            rec += "\n⚠️ *Рекомендации основаны на общей статистике. Для точных данных подключите аналитику канала.*\n"
        
        return rec

def main():
    parser = argparse.ArgumentParser(description='Анализатор времени публикаций')
    parser.add_argument('--channel', '-c', help='ID или @username канала Telegram')
    parser.add_argument('--platform', '-p', default='telegram',
                       choices=['telegram', 'instagram', 'twitter', 'linkedin'],
                       help='Платформа (default: telegram)')
    parser.add_argument('--days', '-d', type=int, default=30,
                       help='Анализировать последние N дней (default: 30)')
    parser.add_argument('--export', '-e', help='Экспортировать в JSON файл')
    
    args = parser.parse_args()
    
    analyzer = TimingAnalyzer(args.platform)
    
    # Пример данных (в реальности — получить из API)
    example_data = [
        {'date': '2026-03-01 09:00', 'views': 150, 'reactions': 12},
        {'date': '2026-03-02 12:00', 'views': 230, 'reactions': 18},
        {'date': '2026-03-03 18:00', 'views': 310, 'reactions': 25},
    ]
    
    stats = analyzer.analyze_channel_stats(example_data)
    recommendations = analyzer.get_posting_recommendations(stats)
    
    print(recommendations)
    
    if args.export:
        with open(args.export, 'w', encoding='utf-8') as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)
        print(f"\n✅ Данные экспортированы в {args.export}")

if __name__ == '__main__':
    main()
