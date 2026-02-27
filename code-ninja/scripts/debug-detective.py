#!/usr/bin/env python3
"""
Debug Detective
Интеллектуальный поиск корня проблем в коде.
Анализирует traceback, логи, находит причину ошибки.

Пример:
    python debug-detective.py --traceback error.log
    python debug-detective.py --analyze-file app.py --line 42
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import subprocess


@dataclass
class ErrorPattern:
    """Паттерн ошибки и её решение"""
    pattern: str
    name: str
    description: str
    solution: str
    severity: str = "medium"


# База знаний ошибок
ERROR_PATTERNS = [
    ErrorPattern(
        pattern=r"ModuleNotFoundError: No module named '(\w+)'",
        name="Отсутствующий модуль",
        description="Python не может найти модуль {match}",
        solution="Установите: pip install {match}",
        severity="high"
    ),
    ErrorPattern(
        pattern=r"ImportError: cannot import name '(\w+)'",
        name="Неверный импорт",
        description="Не удалось импортировать {match} - возможно, циклический импорт или неправильное имя",
        solution="Проверьте правильность имени или разорвите циклический импорт",
        severity="high"
    ),
    ErrorPattern(
        pattern=r"AttributeError: '(\w+)' object has no attribute '(\w+)'",
        name="Отсутствующий атрибут",
        description="Объект {group1} не имеет атрибута {group2}",
        solution="Проверьте название атрибута или тип объекта",
        severity="medium"
    ),
    ErrorPattern(
        pattern=r"KeyError: '(\w+)'",
        name="Отсутствующий ключ",
        description="Ключ {match} не найден в словаре",
        solution="Используйте .get() или проверяйте наличие ключа перед доступом",
        severity="medium"
    ),
    ErrorPattern(
        pattern=r"IndexError: list index out of range",
        name="Индекс вне диапазона",
        description="Обращение к несуществующему индексу списка",
        solution="Проверяйте длину списка перед доступом по индексу",
        severity="medium"
    ),
    ErrorPattern(
        pattern=r"TypeError: '(\w+)' object is not callable",
        name="Невызываемый объект",
        description="Попытка вызвать как функцию то, что не является функцией",
        solution="Проверьте тип переменной - возможно, переопределили функцию",
        severity="medium"
    ),
    ErrorPattern(
        pattern=r"ValueError: (.*)",
        name="Неверное значение",
        description="{match}",
        solution="Проверьте входные данные на соответствие ожидаемому формату",
        severity="medium"
    ),
    ErrorPattern(
        pattern=r" sqlalchemy.*OperationalError.*Connection refused",
        name="Нет подключения к БД",
        description="Не удалось подключиться к базе данных",
        solution="Проверьте: 1) Запущен ли PostgreSQL 2) Правильные ли credentials 3) Доступен ли порт",
        severity="high"
    ),
    ErrorPattern(
        pattern=r" sqlalchemy.*IntegrityError.*duplicate key",
        name="Дубликат ключа",
        description="Попытка вставить дубликат уникального ключа",
        solution="Проверьте уникальность данных перед вставкой или используйте ON CONFLICT",
        severity="medium"
    ),
    ErrorPattern(
        pattern=r"ConnectionResetError",
        name="Соединение сброшено",
        description="Клиент закрыл соединение до завершения запроса",
        solution="Нормально для long-polling, но проверьте timeout'ы",
        severity="low"
    ),
    ErrorPattern(
        pattern=r"asyncpg.*too many connections",
        name="Переполнение пула соединений",
        description="Все соединения с БД заняты",
        solution="Увеличьте pool_size или проверьте, что соединения закрываются",
        severity="high"
    ),
    ErrorPattern(
        pattern=r"Pydantic.*validation error",
        name="Ошибка валидации Pydantic",
        description="Данные не соответствуют схеме",
        solution="Проверьте типы данных в запросе или обновите схему",
        severity="medium"
    ),
    ErrorPattern(
        pattern=r"RecursionError",
        name="Бесконечная рекурсия",
        description="Функция вызывает сама себя бесконечно",
        solution="Проверьте базовый случай рекурсии или используйте итерацию",
        severity="high"
    ),
    ErrorPattern(
        pattern=r"MemoryError",
        name="Недостаточно памяти",
        description="Процесс исчерпал доступную память",
        solution="Оптимизируйте использование памяти, используйте генераторы, проверьте утечки",
        severity="critical"
    ),
    ErrorPattern(
        pattern=r"TimeoutError|asyncio.*TimeoutError",
        name="Таймаут",
        description="Операция превысила лимит времени",
        solution="Увеличьте timeout или оптимизируйте операцию",
        severity="medium"
    ),
]


class DebugDetective:
    """Детектив отладки — ищет корень проблемы"""
    
    def __init__(self):
        self.findings = []
        self.suggestions = []
    
    def analyze_traceback(self, traceback_text: str) -> Dict:
        """Анализирует traceback и находит проблему"""
        print("🔍 Анализирую traceback...")
        
        # Извлекаем последнее исключение
        lines = traceback_text.strip().split('\n')
        
        # Находим тип ошибки и сообщение (обычно в последних строках)
        error_line = None
        for line in reversed(lines):
            if line.strip() and not line.startswith(' '):
                error_line = line.strip()
                break
        
        if not error_line:
            return {'error': 'Не удалось найти строку с ошибкой'}
        
        print(f"   Найдена ошибка: {error_line[:100]}")
        
        # Ищем соответствие в паттернах
        matched_pattern = None
        match_data = None
        
        for pattern in ERROR_PATTERNS:
            regex_match = re.search(pattern.pattern, traceback_text, re.IGNORECASE)
            if regex_match:
                matched_pattern = pattern
                match_data = regex_match
                break
        
        # Извлекаем стек вызовов
        stack_trace = self._extract_stack_trace(lines)
        
        # Находим файл и строку с ошибкой
        error_location = self._find_error_location(lines)
        
        result = {
            'error_line': error_line,
            'matched_pattern': matched_pattern,
            'match_data': match_data,
            'stack_trace': stack_trace,
            'error_location': error_location,
            'analysis': self._analyze_context(traceback_text, matched_pattern)
        }
        
        return result
    
    def _extract_stack_trace(self, lines: List[str]) -> List[Dict]:
        """Извлекает стек вызовов из traceback"""
        stack = []
        
        # Паттерн для строки файла
        file_pattern = r'File "([^"]+)", line (\d+), in (\w+)'
        
        for i, line in enumerate(lines):
            match = re.match(file_pattern, line.strip())
            if match:
                filename, line_num, function = match.groups()
                # Ищем код в следующей строке
                code_line = ""
                if i + 1 < len(lines):
                    code_line = lines[i + 1].strip()
                
                stack.append({
                    'file': filename,
                    'line': int(line_num),
                    'function': function,
                    'code': code_line
                })
        
        return stack
    
    def _find_error_location(self, lines: List[str]) -> Optional[Dict]:
        """Находит место ошибки (последний вызов в стеке)"""
        stack = self._extract_stack_trace(lines)
        if stack:
            return stack[-1]
        return None
    
    def _analyze_context(self, traceback_text: str, pattern: Optional[ErrorPattern]) -> str:
        """Анализирует контекст и даёт рекомендации"""
        analysis = []
        
        if pattern:
            analysis.append(f"Тип ошибки: {pattern.name}")
            analysis.append(f"Описание: {pattern.description}")
            analysis.append(f"Решение: {pattern.solution}")
        else:
            analysis.append("Неизвестный тип ошибки - требуется ручной анализ")
        
        # Дополнительный контекст
        if "async" in traceback_text.lower():
            analysis.append("💡 Обратите внимание: ошибка в асинхронном коде - проверьте await")
        
        if "sqlalchemy" in traceback_text.lower():
            analysis.append("💡 Проблема с БД - проверьте подключение и миграции")
        
        if "pydantic" in traceback_text.lower():
            analysis.append("💡 Проблема валидации - проверьте схемы и входные данные")
        
        return "\n".join(analysis)
    
    def analyze_file_context(self, filepath: str, line_number: int, context_lines: int = 5) -> str:
        """Анализирует контекст вокруг строки с ошибкой"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except Exception as e:
            return f"Не удалось прочитать файл: {e}"
        
        start = max(0, line_number - context_lines - 1)
        end = min(len(lines), line_number + context_lines)
        
        result = []
        for i in range(start, end):
            marker = ">>> " if i == line_number - 1 else "    "
            result.append(f"{marker}{i+1:4d}: {lines[i].rstrip()}")
        
        return "\n".join(result)
    
    def suggest_fix(self, analysis: Dict) -> str:
        """Предлагает конкретное исправление"""
        pattern = analysis.get('matched_pattern')
        location = analysis.get('error_location')
        
        if not pattern:
            return "Требуется ручной анализ ошибки"
        
        fix = f"🛠️  ИСПРАВЛЕНИЕ:\n"
        fix += f"\n{pattern.solution}\n"
        
        if location:
            fix += f"\n📍 Место: {location['file']}:{location['line']}"
            fix += f"\n   Функция: {location['function']}"
            if location['code']:
                fix += f"\n   Код: {location['code'][:60]}"
        
        return fix


def print_analysis(analysis: Dict, show_context: bool = False):
    """Красивый вывод анализа"""
    print("\n" + "="*70)
    print("🕵️  РЕЗУЛЬТАТ РАССЛЕДОВАНИЯ")
    print("="*70)
    
    # Ошибка
    print(f"\n❌ ОШИБКА:")
    print(f"   {analysis['error_line']}")
    
    # Анализ
    print(f"\n📋 АНАЛИЗ:")
    print(f"   {analysis['analysis']}")
    
    # Стек вызовов
    if analysis['stack_trace']:
        print(f"\n📚 СТЕК ВЫЗОВОВ:")
        for i, frame in enumerate(reversed(analysis['stack_trace'][-5:]), 1):
            print(f"   {i}. {frame['file']}:{frame['line']} в {frame['function']}()")
    
    # Контекст кода
    if show_context and analysis['error_location']:
        location = analysis['error_location']
        print(f"\n💻 КОНТЕКСТ ({location['file']}:{location['line']}):")
        
        detective = DebugDetective()
        context = detective.analyze_file_context(
            location['file'], 
            location['line'],
            context_lines=3
        )
        print(context)
    
    # Исправление
    detective = DebugDetective()
    fix = detective.suggest_fix(analysis)
    print(f"\n{fix}")
    
    print("\n" + "="*70)


def main():
    parser = argparse.ArgumentParser(
        description='Debug Detective - ищет корень проблем в коде'
    )
    parser.add_argument(
        '--traceback', '-t',
        help='Путь к файлу с traceback'
    )
    parser.add_argument(
        '--text',
        help='Текст traceback напрямую'
    )
    parser.add_argument(
        '--analyze-file',
        help='Путь к файлу для анализа контекста'
    )
    parser.add_argument(
        '--line', '-l', type=int,
        help='Номер строки с ошибкой'
    )
    parser.add_argument(
        '--show-context', '-c', action='store_true',
        help='Показать контекст кода'
    )
    
    args = parser.parse_args()
    
    detective = DebugDetective()
    
    # Получаем traceback
    traceback_text = None
    
    if args.text:
        traceback_text = args.text
    elif args.traceback:
        try:
            with open(args.traceback, 'r', encoding='utf-8') as f:
                traceback_text = f.read()
        except Exception as e:
            print(f"❌ Ошибка чтения файла: {e}")
            sys.exit(1)
    else:
        # Читаем из stdin
        print("Вставьте traceback (Ctrl+D для завершения):")
        traceback_text = sys.stdin.read()
    
    if not traceback_text:
        print("❌ Нет данных для анализа")
        sys.exit(1)
    
    # Анализируем
    analysis = detective.analyze_traceback(traceback_text)
    
    # Дополнительный контекст файла
    if args.analyze_file and args.line:
        analysis['manual_context'] = detective.analyze_file_context(
            args.analyze_file, args.line
        )
    
    # Выводим результат
    print_analysis(analysis, args.show_context)
    
    # Exit code
    pattern = analysis.get('matched_pattern')
    if pattern and pattern.severity in ['critical', 'high']:
        sys.exit(1)


if __name__ == "__main__":
    main()
