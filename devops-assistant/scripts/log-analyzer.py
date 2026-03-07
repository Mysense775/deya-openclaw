#!/usr/bin/env python3
"""
Log Analyzer - анализатор логов
Ищет ошибки, предупреждения и аномалии в логах
"""

import argparse
import re
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import json

class LogAnalyzer:
    """Анализатор логов"""
    
    # Паттерны для поиска
    ERROR_PATTERNS = [
        r'error',
        r'exception',
        r'failed',
        r'failure',
        r'critical',
        r'fatal',
        r'panic',
        r'crash',
        r'timeout',
        r'refused',
        r'connection.*reset',
        r'permission.*denied',
        r'out of memory',
        r'disk full',
        r'502 bad gateway',
        r'503 service unavailable',
        r'504 gateway timeout'
    ]
    
    WARNING_PATTERNS = [
        r'warning',
        r'deprecated',
        r'obsolete',
        r'slow',
        r'timeout',
        r'retry',
        r'reconnect',
        r'high.*memory',
        r'high.*cpu',
        r'disk.*space'
    ]
    
    # Форматы логов
    LOG_FORMATS = {
        'nginx': r'(?P<ip>\S+) - - \[(?P<time>[^\]]+)\] "(?P<method>\S+) (?P<path>\S+) (?P<protocol>\S+)" (?P<status>\d+)',
        'apache': r'(?P<ip>\S+) \S+ \S+ \[(?P<time>[^\]]+)\] "(?P<method>\S+) (?P<path>\S+) (?P<protocol>\S+)" (?P<status>\d+)',
        'syslog': r'(?P<time>\w+ \d+ \d+:\d+:\d+) (?P<host>\S+) (?P<service>\S+): (?P<message>.*)',
        'docker': r'(?P<time>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+Z) (?P<level>\w+) (?P<message>.*)',
        'python': r'(?P<time>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d+) - (?P<level>\w+) - (?P<message>.*)'
    }
    
    def __init__(self, log_file: str):
        self.log_file = Path(log_file)
        self.errors = []
        self.warnings = []
        self.stats = defaultdict(int)
    
    def analyze(self, pattern: str = None, since: str = None, 
                errors_only: bool = False, warnings_only: bool = False) -> dict:
        """Анализирует лог файл"""
        
        if not self.log_file.exists():
            return {'error': f'Log file not found: {self.log_file}'}
        
        print(f"📄 Analyzing: {self.log_file}")
        
        # Определяем формат
        log_format = self._detect_format()
        
        results = {
            'file': str(self.log_file),
            'total_lines': 0,
            'errors': [],
            'warnings': [],
            'status_codes': Counter(),
            'ip_addresses': Counter(),
            'services': Counter(),
            'time_distribution': defaultdict(int)
        }
        
        try:
            with open(self.log_file, 'r', encoding='utf-8', errors='ignore') as f:
                for line_num, line in enumerate(f, 1):
                    results['total_lines'] += 1
                    line = line.strip()
                    
                    if not line:
                        continue
                    
                    # Проверяем пользовательский паттерн
                    if pattern and re.search(pattern, line, re.IGNORECASE):
                        results['errors'].append({
                            'line': line_num,
                            'content': line[:200],
                            'type': 'pattern_match'
                        })
                        continue
                    
                    # Парсим строку лога
                    parsed = self._parse_line(line, log_format)
                    
                    # Проверяем на ошибки
                    if self._is_error(line, parsed):
                        if not warnings_only:
                            results['errors'].append({
                                'line': line_num,
                                'content': line[:200],
                                'type': 'error',
                                'parsed': parsed
                            })
                    
                    # Проверяем на предупреждения
                    elif self._is_warning(line, parsed):
                        if not errors_only:
                            results['warnings'].append({
                                'line': line_num,
                                'content': line[:200],
                                'type': 'warning',
                                'parsed': parsed
                            })
                    
                    # Собираем статистику
                    if parsed:
                        if 'status' in parsed:
                            results['status_codes'][parsed['status']] += 1
                        if 'ip' in parsed:
                            results['ip_addresses'][parsed['ip']] += 1
                        if 'service' in parsed:
                            results['services'][parsed['service']] += 1
                        
                        # Временное распределение
                        if 'time' in parsed:
                            hour = self._extract_hour(parsed['time'])
                            if hour:
                                results['time_distribution'][hour] += 1
            
            return results
            
        except Exception as e:
            return {'error': str(e)}
    
    def _detect_format(self) -> str:
        """Определяет формат лога по первым строкам"""
        try:
            with open(self.log_file, 'r') as f:
                sample = f.read(1000)
                
                for format_name, pattern in self.LOG_FORMATS.items():
                    if re.search(pattern, sample):
                        return format_name
        except:
            pass
        
        return 'generic'
    
    def _parse_line(self, line: str, log_format: str) -> dict:
        """Парсит строку лога"""
        pattern = self.LOG_FORMATS.get(log_format)
        
        if pattern:
            match = re.search(pattern, line)
            if match:
                return match.groupdict()
        
        return {}
    
    def _is_error(self, line: str, parsed: dict) -> bool:
        """Проверяет, является ли строка ошибкой"""
        line_lower = line.lower()
        
        # Проверяем паттерны
        for pattern in self.ERROR_PATTERNS:
            if re.search(pattern, line_lower):
                return True
        
        # Проверяем уровень логирования
        if parsed.get('level', '').upper() in ['ERROR', 'CRITICAL', 'FATAL']:
            return True
        
        # Проверяем HTTP статус
        status = parsed.get('status', '')
        if status and status[0] in ['4', '5']:
            return True
        
        return False
    
    def _is_warning(self, line: str, parsed: dict) -> bool:
        """Проверяет, является ли строка предупреждением"""
        line_lower = line.lower()
        
        # Проверяем паттерны
        for pattern in self.WARNING_PATTERNS:
            if re.search(pattern, line_lower):
                return True
        
        # Проверяем уровень логирования
        if parsed.get('level', '').upper() == 'WARNING':
            return True
        
        return False
    
    def _extract_hour(self, time_str: str) -> str:
        """Извлекает час из строки времени"""
        # Пробуем разные форматы
        patterns = [
            r'(\d{2}):\d{2}:\d{2}',  # HH:MM:SS
            r'T(\d{2}):\d{2}',       # ISO format
        ]
        
        for pattern in patterns:
            match = re.search(pattern, time_str)
            if match:
                return match.group(1) + ':00'
        
        return None
    
    def print_report(self, results: dict):
        """Выводит отчёт об анализе"""
        print(f"\n{'='*70}")
        print(f"📊 LOG ANALYSIS REPORT")
        print(f"{'='*70}")
        print(f"File: {results['file']}")
        print(f"Total lines: {results['total_lines']:,}")
        print(f"Errors found: {len(results['errors'])}")
        print(f"Warnings found: {len(results['warnings'])}")
        
        # Ошибки
        if results['errors']:
            print(f"\n❌ ERRORS ({len(results['errors'])}):")
            print("-" * 70)
            for i, error in enumerate(results['errors'][:10], 1):
                print(f"{i}. Line {error['line']}: {error['content'][:100]}")
            
            if len(results['errors']) > 10:
                print(f"   ... and {len(results['errors']) - 10} more")
        
        # Предупреждения
        if results['warnings']:
            print(f"\n⚠️  WARNINGS ({len(results['warnings'])}):")
            print("-" * 70)
            for i, warning in enumerate(results['warnings'][:5], 1):
                print(f"{i}. Line {warning['line']}: {warning['content'][:100]}")
            
            if len(results['warnings']) > 5:
                print(f"   ... and {len(results['warnings']) - 5} more")
        
        # HTTP статусы
        if results['status_codes']:
            print(f"\n📈 HTTP STATUS CODES:")
            print("-" * 70)
            for code, count in results['status_codes'].most_common(10):
                emoji = '✅' if code[0] == '2' else '🟡' if code[0] == '3' else '❌'
                print(f"   {emoji} {code}: {count}")
        
        # Топ IP адресов
        if results['ip_addresses']:
            print(f"\n🌐 TOP IP ADDRESSES:")
            print("-" * 70)
            for ip, count in results['ip_addresses'].most_common(5):
                print(f"   {ip}: {count} requests")
        
        # Временное распределение
        if results['time_distribution']:
            print(f"\n⏰ REQUESTS BY HOUR:")
            print("-" * 70)
            for hour in sorted(results['time_distribution'].keys()):
                count = results['time_distribution'][hour]
                bar = '█' * min(count // 10, 50)
                print(f"   {hour}: {bar} ({count})")
        
        print(f"\n{'='*70}")
    
    def tail(self, lines: int = 100, follow: bool = False):
        """Показывает последние строки лога"""
        try:
            with open(self.log_file, 'r') as f:
                if follow:
                    # Режим follow (как tail -f)
                    import time
                    f.seek(0, 2)  # Переходим в конец
                    print(f"👁️  Following {self.log_file} (Ctrl+C to stop)\n")
                    
                    try:
                        while True:
                            line = f.readline()
                            if line:
                                print(line, end='')
                            else:
                                time.sleep(0.1)
                    except KeyboardInterrupt:
                        print("\n\n👋 Stopped")
                else:
                    # Просто последние N строк
                    all_lines = f.readlines()
                    for line in all_lines[-lines:]:
                        print(line, end='')
                        
        except Exception as e:
            print(f"❌ Error: {e}")

def main():
    parser = argparse.ArgumentParser(description='Анализатор логов')
    parser.add_argument('logfile', help='Путь к файлу логов')
    parser.add_argument('--pattern', '-p', help='Поиск по регулярному выражению')
    parser.add_argument('--errors-only', '-e', action='store_true', help='Только ошибки')
    parser.add_argument('--warnings-only', '-w', action='store_true', help='Только предупреждения')
    parser.add_argument('--tail', '-t', type=int, help='Показать последние N строк')
    parser.add_argument('--follow', '-f', action='store_true', help='Следить за файлом (tail -f)')
    parser.add_argument('--json', '-j', help='Экспортировать в JSON файл')
    parser.add_argument('--since', '-s', help='Анализировать с даты (YYYY-MM-DD)')
    
    args = parser.parse_args()
    
    analyzer = LogAnalyzer(args.logfile)
    
    if args.tail or args.follow:
        analyzer.tail(lines=args.tail or 100, follow=args.follow)
    else:
        results = analyzer.analyze(
            pattern=args.pattern,
            since=args.since,
            errors_only=args.errors_only,
            warnings_only=args.warnings_only
        )
        
        if 'error' in results:
            print(f"❌ {results['error']}")
        else:
            analyzer.print_report(results)
            
            if args.json:
                with open(args.json, 'w') as f:
                    json.dump(results, f, indent=2)
                print(f"\n✅ Report exported to {args.json}")

if __name__ == '__main__':
    main()
