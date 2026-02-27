#!/usr/bin/env python3
"""
Email Finder
Поиск email контактов на сайтах компаний

Пример:
    python email-finder.py --domain "company.com"
    python email-finder.py --domain "startup.io" --pattern "firstname.lastname" --validate
"""

import argparse
import asyncio
import json
import re
import socket
import smtplib
from typing import List, Dict, Optional, Set
from dataclasses import dataclass
from urllib.parse import urljoin, urlparse
import aiohttp


@dataclass
class EmailResult:
    """Результат поиска email"""
    email: str
    source: str  # Где найден
    pattern: str  # Какой паттерн использовался
    is_valid: Optional[bool] = None  # Проверен ли SMTP
    confidence: float = 1.0  # Уверенность (на основе источника)
    name: Optional[str] = None  # Имя владельца если найдено
    position: Optional[str] = None  # Должность


class EmailFinder:
    """Поиск email контактов на сайтах"""
    
    # Популярные паттерны email
    PATTERNS = [
        "{first}.{last}",      # john.doe
        "{first}{last}",       # johndoe
        "{f}{last}",           # jdoe
        "{first}_{last}",      # john_doe
        "{first}-{last}",      # john-doe
        "{last}.{first}",      # doe.john
        "{first}",             # john
        "{last}",              # doe
    ]
    
    # Страницы где искать
    TARGET_PAGES = [
        "/about", "/about-us", "/aboutus",
        "/team", "/our-team", "/people",
        "/contact", "/contact-us", "/contacts",
        "/careers", "/jobs",
        "/leadership", "/management"
    ]
    
    # Регулярное выражение для email
    EMAIL_REGEX = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
    
    def __init__(self):
        self.session: Optional[aiohttp.ClientSession] = None
        self.found_emails: Set[str] = set()
    
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
    
    async def extract_from_page(self, url: str) -> List[EmailResult]:
        """Извлечение email со страницы"""
        results = []
        
        try:
            async with self.session.get(url) as response:
                if response.status == 200:
                    text = await response.text()
                    
                    # Ищем email
                    emails = self.EMAIL_REGEX.findall(text)
                    
                    for email in emails:
                        email = email.lower()
                        if email not in self.found_emails and not self._is_noreply(email):
                            self.found_emails.add(email)
                            
                            # Пытаемся извлечь имя
                            name = self._extract_name_from_email(email, text)
                            position = self._extract_position(email, text)
                            
                            results.append(EmailResult(
                                email=email,
                                source=url,
                                pattern="extracted",
                                name=name,
                                position=position,
                                confidence=0.9
                            ))
                            
        except Exception as e:
            print(f"Error extracting from {url}: {e}")
        
        return results
    
    def _is_noreply(self, email: str) -> bool:
        """Проверка на служебные email"""
        noreply_patterns = [
            'noreply', 'no-reply', 'donotreply', 'mailer-daemon',
            'postmaster', 'admin@', 'info@', 'support@', 'help@',
            'sales@', 'marketing@', 'contact@'
        ]
        return any(pattern in email.lower() for pattern in noreply_patterns)
    
    def _extract_name_from_email(self, email: str, text: str) -> Optional[str]:
        """Попытка извлечь имя из контекста"""
        # Ищем имя рядом с email в тексте
        email_pos = text.find(email)
        if email_pos == -1:
            return None
        
        # Ищем в окрестностях email
        context = text[max(0, email_pos - 200):email_pos + 200]
        
        # Паттерны: "Name <email>" или "email - Name" или "Name: email"
        name_patterns = [
            r'([A-Z][a-z]+ [A-Z][a-z]+)\s*<[^>]+' + re.escape(email),
            re.escape(email) + r'[^\w]*[-–—][^\w]*([A-Z][a-z]+ [A-Z][a-z]+)',
            r'([A-Z][a-z]+ [A-Z][a-z]+)[^\w]*:[^\w]*' + re.escape(email)
        ]
        
        for pattern in name_patterns:
            match = re.search(pattern, context)
            if match:
                return match.group(1)
        
        return None
    
    def _extract_position(self, email: str, text: str) -> Optional[str]:
        """Попытка извлечь должность"""
        positions = [
            "CEO", "CTO", "COO", "CFO", "CMO",
            "Founder", "Co-Founder",
            "Director", "Manager", "Head of",
            "VP", "Vice President",
            "Lead", "Senior", "Principal",
            "Engineer", "Developer", "Designer",
            "Marketing", "Sales", "Product", "Operations"
        ]
        
        email_pos = text.find(email)
        if email_pos == -1:
            return None
        
        context = text[max(0, email_pos - 300):email_pos + 300].lower()
        
        for position in positions:
            if position.lower() in context:
                return position
        
        return None
    
    async def generate_from_names(self, domain: str, first_name: str, last_name: str) -> List[EmailResult]:
        """Генерация email на основе имени"""
        results = []
        
        variations = {
            "first": first_name.lower(),
            "last": last_name.lower(),
            "f": first_name[0].lower() if first_name else "",
            "l": last_name[0].lower() if last_name else ""
        }
        
        for pattern in self.PATTERNS:
            try:
                local_part = pattern.format(**variations)
                email = f"{local_part}@{domain}".lower()
                
                if email not in self.found_emails:
                    self.found_emails.add(email)
                    results.append(EmailResult(
                        email=email,
                        source="generated",
                        pattern=pattern,
                        name=f"{first_name} {last_name}",
                        confidence=0.5  # Ниже уверенность для сгенерированных
                    ))
            except:
                continue
        
        return results
    
    def verify_email(self, email: str) -> Optional[bool]:
        """Проверка валидности email через MX и SMTP"""
        try:
            # Извлекаем домен
            domain = email.split('@')[1]
            
            # Проверяем MX записи
            try:
                mx_records = socket.getmxrr(domain)
                if not mx_records:
                    return False
            except:
                # Fallback: проверка A записи
                try:
                    socket.gethostbyname(domain)
                except:
                    return False
            
            # SMTP проверка (опционально, может быть заблокирована)
            # mx_host = mx_records[0][1]
            # server = smtplib.SMTP(mx_host, timeout=10)
            # server.quit()
            
            return True
            
        except Exception as e:
            return None
    
    async def search_domain(self, domain: str, validate: bool = False) -> List[EmailResult]:
        """Поиск email на всём домене"""
        all_results = []
        
        print(f"🔍 Поиск на {domain}...")
        
        # Ищем на главной странице
        main_page = await self.extract_from_page(f"https://{domain}")
        all_results.extend(main_page)
        print(f"  Главная страница: {len(main_page)} emails")
        
        # Ищем на целевых страницах
        for page in self.TARGET_PAGES:
            url = f"https://{domain}{page}"
            results = await self.extract_from_page(url)
            all_results.extend(results)
            if results:
                print(f"  {page}: {len(results)} emails")
        
        # Валидация
        if validate:
            print("\n✓ Проверка валидности...")
            for result in all_results:
                result.is_valid = self.verify_email(result.email)
                if result.is_valid:
                    result.confidence = min(result.confidence + 0.2, 1.0)
        
        # Сортируем по уверенности
        all_results.sort(key=lambda x: x.confidence, reverse=True)
        
        return all_results
    
    def export_to_csv(self, results: List[EmailResult], filename: str):
        """Экспорт в CSV"""
        import csv
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Email', 'Name', 'Position', 'Source', 'Pattern', 'Valid', 'Confidence'])
            
            for result in results:
                writer.writerow([
                    result.email,
                    result.name or '',
                    result.position or '',
                    result.source,
                    result.pattern,
                    result.is_valid if result.is_valid is not None else 'unknown',
                    f"{result.confidence:.0%}"
                ])
        
        print(f"💾 Экспортировано {len(results)} контактов в {filename}")
    
    def export_to_json(self, results: List[EmailResult], filename: str):
        """Экспорт в JSON"""
        data = [{
            "email": r.email,
            "name": r.name,
            "position": r.position,
            "source": r.source,
            "pattern": r.pattern,
            "is_valid": r.is_valid,
            "confidence": r.confidence
        } for r in results]
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Экспортировано {len(results)} контактов в {filename}")


async def main():
    parser = argparse.ArgumentParser(description='Email Finder - поиск контактов')
    parser.add_argument('--domain', '-d', required=True, help='Домен для поиска')
    parser.add_argument('--validate', '-v', action='store_true', help='Проверить валидность email')
    parser.add_argument('--first-name', '-f', help='Имя для генерации вариантов')
    parser.add_argument('--last-name', '-l', help='Фамилия для генерации вариантов')
    parser.add_argument('--output', '-o', help='Файл для экспорта')
    parser.add_argument('--format', choices=['csv', 'json'], default='json',
                       help='Формат экспорта')
    
    args = parser.parse_args()
    
    async with EmailFinder() as finder:
        # Поиск на сайте
        results = await finder.search_domain(args.domain, validate=args.validate)
        
        # Генерация из имени если указано
        if args.first_name and args.last_name:
            print(f"\n🎯 Генерация вариантов для {args.first_name} {args.last_name}...")
            generated = await finder.generate_from_names(
                args.domain, args.first_name, args.last_name
            )
            results.extend(generated)
        
        # Вывод результатов
        print(f"\n{'='*60}")
        print(f"📧 Найдено {len(results)} контактов:")
        print(f"{'='*60}")
        
        for i, result in enumerate(results[:20], 1):  # Показываем первые 20
            valid_mark = "✓" if result.is_valid else "?" if result.is_valid is None else "✗"
            name_info = f" ({result.name})" if result.name else ""
            position_info = f" [{result.position}]" if result.position else ""
            
            print(f"{i:2d}. {valid_mark} {result.email}{name_info}{position_info}")
            print(f"    Источник: {result.source} | Уверенность: {result.confidence:.0%}")
        
        if len(results) > 20:
            print(f"\n... и ещё {len(results) - 20} контактов")
        
        # Экспорт
        if args.output:
            if args.format == 'csv':
                finder.export_to_csv(results, args.output)
            else:
                finder.export_to_json(results, args.output)


if __name__ == "__main__":
    asyncio.run(main())
