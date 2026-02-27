#!/usr/bin/env python3
"""
Price Monitor
Мониторинг изменения цен на сайтах

Пример:
    python price-monitor.py --url "https://shop.com/product" --selector ".price"
    python price-monitor.py --url "https://example.com" --selector "#price" --threshold 1000 --telegram
"""

import argparse
import asyncio
import json
import sqlite3
from datetime import datetime, timedelta
from typing import Optional, Dict, List
from dataclasses import dataclass, asdict
import aiohttp
from pathlib import Path


@dataclass
class PriceRecord:
    """Запись о цене"""
    url: str
    selector: str
    price: float
    currency: str
    timestamp: datetime
    title: Optional[str] = None
    availability: Optional[str] = None


class PriceDatabase:
    """SQLite база для истории цен"""
    
    def __init__(self, db_path: str = "prices.db"):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """Инициализация базы"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS prices (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT NOT NULL,
                    selector TEXT NOT NULL,
                    price REAL NOT NULL,
                    currency TEXT DEFAULT 'USD',
                    title TEXT,
                    availability TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_url_timestamp 
                ON prices(url, timestamp)
            """)
            
            conn.commit()
    
    def save(self, record: PriceRecord):
        """Сохранение записи"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO prices (url, selector, price, currency, title, availability, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                record.url, record.selector, record.price, record.currency,
                record.title, record.availability, record.timestamp
            ))
            conn.commit()
    
    def get_latest(self, url: str, selector: str) -> Optional[PriceRecord]:
        """Получение последней записи"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("""
                SELECT * FROM prices 
                WHERE url = ? AND selector = ?
                ORDER BY timestamp DESC 
                LIMIT 1
            """, (url, selector))
            
            row = cursor.fetchone()
            if row:
                return PriceRecord(
                    url=row['url'],
                    selector=row['selector'],
                    price=row['price'],
                    currency=row['currency'],
                    timestamp=datetime.fromisoformat(row['timestamp']),
                    title=row['title'],
                    availability=row['availability']
                )
            return None
    
    def get_history(self, url: str, selector: str, days: int = 30) -> List[PriceRecord]:
        """Получение истории цен"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            since = datetime.now() - timedelta(days=days)
            
            cursor = conn.execute("""
                SELECT * FROM prices 
                WHERE url = ? AND selector = ? AND timestamp > ?
                ORDER BY timestamp ASC
            """, (url, selector, since))
            
            records = []
            for row in cursor.fetchall():
                records.append(PriceRecord(
                    url=row['url'],
                    selector=row['selector'],
                    price=row['price'],
                    currency=row['currency'],
                    timestamp=datetime.fromisoformat(row['timestamp']),
                    title=row['title'],
                    availability=row['availability']
                ))
            
            return records


class PriceMonitor:
    """Мониторинг цен"""
    
    def __init__(self):
        self.session: Optional[aiohttp.ClientSession] = None
        self.db = PriceDatabase()
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            },
            timeout=aiohttp.ClientTimeout(total=30)
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def fetch_price(self, url: str, selector: str) -> Optional[PriceRecord]:
        """Получение цены со страницы"""
        try:
            async with self.session.get(url) as response:
                if response.status != 200:
                    print(f"❌ Ошибка загрузки: {response.status}")
                    return None
                
                html = await response.text()
                
                # Простой парсинг (без BeautifulSoup для минимизации зависимостей)
                # Ищем по регулярке
                import re
                
                # Паттерн для поиска цены рядом с селектором (упрощённо)
                # В реальном коде лучше использовать BeautifulSoup
                price_pattern = r'[\$€₽£]\s*([\d,]+\.?\d*)'
                matches = re.findall(price_pattern, html)
                
                if not matches:
                    print("⚠️ Цена не найдена на странице")
                    return None
                
                # Берём первую найденную цену
                price_str = matches[0].replace(',', '')
                price = float(price_str)
                
                # Определяем валюту
                if '$' in html[:1000]:
                    currency = 'USD'
                elif '€' in html[:1000]:
                    currency = 'EUR'
                elif '₽' in html[:1000]:
                    currency = 'RUB'
                else:
                    currency = 'USD'
                
                # Ищем название товара
                title_match = re.search(r'<title>(.*?)</title>', html)
                title = title_match.group(1).strip() if title_match else None
                
                return PriceRecord(
                    url=url,
                    selector=selector,
                    price=price,
                    currency=currency,
                    timestamp=datetime.now(),
                    title=title
                )
                
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            return None
    
    def calculate_change(self, old_price: float, new_price: float) -> Dict:
        """Расчёт изменения цены"""
        diff = new_price - old_price
        percent = (diff / old_price) * 100 if old_price > 0 else 0
        
        return {
            "absolute": diff,
            "percent": percent,
            "direction": "up" if diff > 0 else "down" if diff < 0 else "same"
        }
    
    def should_notify(self, change: Dict, threshold: float) -> bool:
        """Проверка нужно ли уведомлять"""
        return abs(change["percent"]) >= threshold or abs(change["absolute"]) >= threshold
    
    async def send_telegram_notification(self, bot_token: str, chat_id: str, record: PriceRecord, change: Dict):
        """Отправка уведомления в Telegram"""
        direction_emoji = "📈" if change["direction"] == "up" else "📉" if change["direction"] == "down" else "➡️"
        
        message = f"""{direction_emoji} Изменение цены!

🛍️ {record.title or 'Товар'}
💰 {record.price:.2f} {record.currency}
📊 Изменение: {change['percent']:+.1f}% ({change['absolute']:+.2f} {record.currency})
🔗 {record.url}
⏰ {record.timestamp.strftime('%Y-%m-%d %H:%M')}"""
        
        try:
            telegram_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            async with self.session.post(telegram_url, json={
                "chat_id": chat_id,
                "text": message,
                "disable_web_page_preview": True
            }) as response:
                if response.status == 200:
                    print("✅ Уведомление отправлено в Telegram")
                else:
                    print(f"❌ Ошибка отправки: {response.status}")
        except Exception as e:
            print(f"❌ Ошибка Telegram: {e}")
    
    def generate_chart(self, history: List[PriceRecord], output_path: str):
        """Генерация простого текстового графика цен"""
        if not history:
            return
        
        prices = [r.price for r in history]
        min_price = min(prices)
        max_price = max(prices)
        
        if max_price == min_price:
            normalized = [5] * len(prices)
        else:
            normalized = [int((p - min_price) / (max_price - min_price) * 10) for p in prices]
        
        lines = [
            f"📊 График цен: {history[0].title or 'Товар'}",
            f"Мин: {min_price:.2f} | Макс: {max_price:.2f}",
            ""
        ]
        
        for i, (record, norm) in enumerate(zip(history, normalized)):
            date = record.timestamp.strftime('%m-%d')
            bar = '█' * norm + '░' * (10 - norm)
            lines.append(f"{date} |{bar}| {record.price:.2f}")
        
        chart_text = '\n'.join(lines)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(chart_text)
        
        print(f"📈 График сохранён: {output_path}")
        print(chart_text)
    
    async def monitor_once(self, url: str, selector: str, threshold: float = 5.0,
                          telegram_token: Optional[str] = None, telegram_chat: Optional[str] = None) -> bool:
        """Одиночная проверка цены"""
        print(f"🔍 Проверка: {url}")
        
        # Получаем текущую цену
        current = await self.fetch_price(url, selector)
        if not current:
            return False
        
        print(f"💰 Текущая цена: {current.price:.2f} {current.currency}")
        
        # Получаем предыдущую цену
        previous = self.db.get_latest(url, selector)
        
        if previous:
            print(f"📋 Предыдущая цена: {previous.price:.2f} {previous.currency}")
            
            # Расчёт изменения
            change = self.calculate_change(previous.price, current.price)
            
            if change["direction"] != "same":
                print(f"📊 Изменение: {change['percent']:+.1f}% ({change['absolute']:+.2f})")
                
                # Проверка уведомления
                if self.should_notify(change, threshold):
                    print(f"🔔 Изменение превышает порог ({threshold}%)")
                    
                    if telegram_token and telegram_chat:
                        await self.send_telegram_notification(
                            telegram_token, telegram_chat, current, change
                        )
                
                # Сохраняем в любом случае
                self.db.save(current)
                return True
            else:
                print("✅ Цена не изменилась")
        else:
            print("📝 Первая запись для этого товара")
        
        # Сохраняем
        self.db.save(current)
        return True
    
    async def monitor_continuous(self, url: str, selector: str, interval: int = 3600,
                                threshold: float = 5.0, telegram_token: Optional[str] = None,
                                telegram_chat: Optional[str] = None):
        """Непрерывный мониторинг"""
        print(f"🔄 Запуск мониторинга каждые {interval} секунд...")
        print("Нажми Ctrl+C для остановки\n")
        
        try:
            while True:
                await self.monitor_once(url, selector, threshold, telegram_token, telegram_chat)
                print(f"⏳ Следующая проверка через {interval} сек...\n")
                await asyncio.sleep(interval)
        except KeyboardInterrupt:
            print("\n✅ Мониторинг остановлен")
    
    def show_history(self, url: str, selector: str, days: int = 30):
        """Показать историю цен"""
        history = self.db.get_history(url, selector, days)
        
        if not history:
            print("📭 История не найдена")
            return
        
        print(f"\n📊 История цен ({len(history)} записей, последние {days} дней):")
        print("-" * 60)
        
        for record in history:
            date = record.timestamp.strftime('%Y-%m-%d %H:%M')
            print(f"{date} | {record.price:.2f} {record.currency}")


async def main():
    parser = argparse.ArgumentParser(description='Price Monitor - мониторинг цен')
    parser.add_argument('--url', '-u', required=True, help='URL страницы с товаром')
    parser.add_argument('--selector', '-s', required=True, help='CSS селектор элемента с ценой')
    parser.add_argument('--threshold', '-t', type=float, default=5.0,
                       help='Порог изменения цены для уведомления (в %)')
    parser.add_argument('--interval', '-i', type=int, help='Интервал проверки в секундах (для continuous)')
    parser.add_argument('--telegram-token', help='Telegram Bot Token для уведомлений')
    parser.add_argument('--telegram-chat', help='Telegram Chat ID для уведомлений')
    parser.add_argument('--history', action='store_true', help='Показать историю цен')
    parser.add_argument('--chart', help='Сохранить график в файл')
    parser.add_argument('--days', type=int, default=30, help='Дней истории для показа')
    
    args = parser.parse_args()
    
    async with PriceMonitor() as monitor:
        if args.history:
            # Показываем историю
            monitor.show_history(args.url, args.selector, args.days)
            
            if args.chart:
                history = monitor.db.get_history(args.url, args.selector, args.days)
                monitor.generate_chart(history, args.chart)
        
        elif args.interval:
            # Непрерывный мониторинг
            await monitor.monitor_continuous(
                args.url, args.selector, args.interval, args.threshold,
                args.telegram_token, args.telegram_chat
            )
        
        else:
            # Одиночная проверка
            await monitor.monitor_once(
                args.url, args.selector, args.threshold,
                args.telegram_token, args.telegram_chat
            )


if __name__ == "__main__":
    asyncio.run(main())
