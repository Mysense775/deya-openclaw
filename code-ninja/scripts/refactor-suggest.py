#!/usr/bin/env python3
"""
Refactor Suggest
Анализирует код и предлагает конкретные улучшения.

Пример:
    python refactor-suggest.py /path/to/file.py
    python refactor-suggest.py /path/to/project --full
"""

import ast
import sys
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class RefactoringSuggestion:
    """Предложение по рефакторингу"""
    line: int
    type: str
    message: str
    current_code: str
    suggested_code: str
    benefits: List[str]
    priority: str = "medium"


class RefactoringAnalyzer:
    """Анализатор кода для рефакторинга"""
    
    def __init__(self, filepath: str):
        self.filepath = Path(filepath)
        self.suggestions = []
        self.content = ""
        self.tree = None
        
    def analyze(self) -> List[RefactoringSuggestion]:
        """Запускает полный анализ файла"""
        print(f"🔍 Анализирую {self.filepath}...")
        
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                self.content = f.read()
        except Exception as e:
            print(f"❌ Ошибка чтения: {e}")
            return []
        
        # Парсим AST
        try:
            self.tree = ast.parse(self.content)
        except SyntaxError as e:
            print(f"❌ Синтаксическая ошибка: {e}")
            return []
        
        # Запускаем проверки
        self._check_long_functions()
        self._check_nested_loops()
        self._check_duplicate_code()
        self._check_magic_numbers()
        self._check_long_lines()
        self._check_complex_conditions()
        self._check_bare_excepts()
        self._check_print_statements()
        self._check_list_concatenation()
        self._check_comprehension_opportunities()
        
        # Сортируем по приоритету
        priority_order = {'high': 0, 'medium': 1, 'low': 2}
        self.suggestions.sort(key=lambda x: priority_order.get(x.priority, 3))
        
        return self.suggestions
    
    def _check_long_functions(self):
        """Проверяет длинные функции"""
        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef):
                lines = node.end_lineno - node.lineno if node.end_lineno else 0
                
                if lines > 50:
                    # Получаем код функции
                    func_code = self._get_node_code(node)
                    
                    self.suggestions.append(RefactoringSuggestion(
                        line=node.lineno,
                        type="long_function",
                        message=f"Функция '{node.name}' слишком длинная ({lines} строк)",
                        current_code=func_code[:200] + "..." if len(func_code) > 200 else func_code,
                        suggested_code=f"# Разбейте на 2-3 функции:\n# 1. {node.name}_setup()\n# 2. {node.name}_process()\n# 3. {node.name}_cleanup()",
                        benefits=[
                            "Улучшит читаемость",
                            "Облегчит тестирование",
                            "Упростит отладку"
                        ],
                        priority="high" if lines > 100 else "medium"
                    ))
    
    def _check_nested_loops(self):
        """Проверяет вложенные циклы"""
        for node in ast.walk(self.tree):
            if isinstance(node, (ast.For, ast.While)):
                # Считаем вложенность
                depth = self._get_loop_depth(node)
                if depth >= 3:
                    self.suggestions.append(RefactoringSuggestion(
                        line=node.lineno,
                        type="deep_nesting",
                        message=f"Глубокая вложенность циклов ({depth} уровня)",
                        current_code=self._get_node_code(node)[:150] + "...",
                        suggested_code="# Используйте:\n# 1. Генераторы/итераторы\n# 2. Функции высшего порядка (map, filter)\n# 3. List/dict comprehensions",
                        benefits=[
                            "Улучшит производительность",
                            "Сделает код чище",
                            "Упростит понимание"
                        ],
                        priority="medium"
                    ))
    
    def _check_magic_numbers(self):
        """Проверяет магические числа"""
        MAGIC_NUMBERS = {'0', '1', '-1'}  # Эти обычно ок
        
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
                num_str = str(node.value)
                if num_str not in MAGIC_NUMBERS and len(num_str) > 1:
                    # Проверяем, есть ли константа рядом
                    parent = self._get_parent(node)
                    if not isinstance(parent, ast.Assign):  # Не присваивание константе
                        self.suggestions.append(RefactoringSuggestion(
                            line=node.lineno,
                            type="magic_number",
                            message=f"Магическое число: {node.value}",
                            current_code=f"x = {node.value}  # что это?",
                            suggested_code=f"# Создайте константу:\n{self._to_constant_name(node.value)} = {node.value}  # описание",
                            benefits=[
                                "Код станет самодокументируемым",
                                "Легче менять значение",
                                "Понятнее для других"
                            ],
                            priority="low"
                        ))
    
    def _check_long_lines(self):
        """Проверяет длинные строки"""
        lines = self.content.split('\n')
        for i, line in enumerate(lines, 1):
            if len(line) > 100:
                self.suggestions.append(RefactoringSuggestion(
                    line=i,
                    type="long_line",
                    message=f"Слишком длинная строка ({len(line)} символов)",
                    current_code=line[:80] + "...",
                    suggested_code="# Разбейте на несколько строк:\n# Используйте скобки для автоматического переноса",
                    benefits=[
                        "Улучшит читаемость",
                        "Не нужно скроллить",
                        "Лучше в code review"
                    ],
                    priority="low"
                ))
    
    def _check_complex_conditions(self):
        """Проверяет сложные условия"""
        for node in ast.walk(self.tree):
            if isinstance(node, ast.If):
                # Считаем сложность условия
                complexity = self._count_condition_complexity(node.test)
                if complexity > 4:
                    self.suggestions.append(RefactoringSuggestion(
                        line=node.lineno,
                        type="complex_condition",
                        message=f"Сложное условие (сложность: {complexity})",
                        current_code=self._get_node_code(node)[:150] + "...",
                        suggested_code="# Вынесите в переменные:\nis_valid = condition1 and condition2\nshould_process = condition3 or condition4\nif is_valid and should_process:",
                        benefits=[
                            "Улучшит читаемость",
                            "Облегчит отладку",
                            "Самодокументируемо"
                        ],
                        priority="medium"
                    ))
    
    def _check_bare_excepts(self):
        """Проверяет голые except:"""
        for node in ast.walk(self.tree):
            if isinstance(node, ast.ExceptHandler):
                if node.type is None:
                    self.suggestions.append(RefactoringSuggestion(
                        line=node.lineno,
                        type="bare_except",
                        message="Голый 'except:' ловит все ошибки включая KeyboardInterrupt",
                        current_code="try:\n    ...\nexcept:\n    ...",
                        suggested_code="try:\n    ...\nexcept SpecificError as e:\n    logger.error(f'Ошибка: {e}')",
                        benefits=[
                            "Не будете прятать баги",
                            "Можно будет прервать программу",
                            "Лучшая диагностика"
                        ],
                        priority="high"
                    ))
    
    def _check_print_statements(self):
        """Проверяет print в production коде"""
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name) and node.func.id == 'print':
                    self.suggestions.append(RefactoringSuggestion(
                        line=node.lineno,
                        type="print_statement",
                        message="Используйте logger вместо print",
                        current_code="print('Debug info')",
                        suggested_code="import logging\nlogger = logging.getLogger(__name__)\nlogger.info('Debug info')",
                        benefits=[
                            "Уровни логирования",
                            "Настраиваемый вывод",
                            "Лучше для production"
                        ],
                        priority="low"
                    ))
    
    def _check_list_concatenation(self):
        """Проверяет конкатенацию списков в цикле"""
        for node in ast.walk(self.tree):
            if isinstance(node, ast.For):
                for child in ast.walk(node):
                    if isinstance(child, ast.AugAssign):
                        if isinstance(child.op, ast.Add) and isinstance(child.target, ast.Name):
                            self.suggestions.append(RefactoringSuggestion(
                                line=child.lineno,
                                type="list_concatenation",
                                message="Медленная конкатенация списка в цикле",
                                current_code="result = []\nfor x in items:\n    result += [process(x)]",
                                suggested_code="# Используйте list comprehension:\nresult = [process(x) for x in items]\n\n# Или append:\nresult = []\nfor x in items:\n    result.append(process(x))",
                                benefits=[
                                    "O(n) вместо O(n²)",
                                    "Быстрее в разы",
                                    "Чище код"
                                ],
                                priority="medium"
                            ))
                            break
    
    def _check_comprehension_opportunities(self):
        """Ищет возможности для comprehensions"""
        for node in ast.walk(self.tree):
            if isinstance(node, ast.For):
                # Проверяем, является ли цикл простым преобразованием
                if len(node.body) == 1:
                    if isinstance(node.body[0], ast.Append):
                        # Это можно превратить в list comprehension
                        pass  # Упрощённая проверка
    
    def _check_duplicate_code(self):
        """Простая проверка дублирования (упрощённая)"""
        # Для полноценной проверки нужен более сложный анализ
        pass
    
    # Вспомогательные методы
    def _get_node_code(self, node: ast.AST) -> str:
        """Получает исходный код узла"""
        lines = self.content.split('\n')
        if hasattr(node, 'lineno') and hasattr(node, 'end_lineno'):
            start = node.lineno - 1
            end = node.end_lineno if node.end_lineno else start + 1
            return '\n'.join(lines[start:end])
        return ""
    
    def _get_loop_depth(self, node: ast.AST, depth: int = 0) -> int:
        """Считает глубину вложенности циклов"""
        max_depth = depth
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.For, ast.While)):
                child_depth = self._get_loop_depth(child, depth + 1)
                max_depth = max(max_depth, child_depth)
        return max_depth
    
    def _get_parent(self, node: ast.AST) -> Optional[ast.AST]:
        """Находит родителя узла"""
        for parent in ast.walk(self.tree):
            for child in ast.iter_child_nodes(parent):
                if child is node:
                    return parent
        return None
    
    def _count_condition_complexity(self, node: ast.AST) -> int:
        """Считает сложность условия"""
        count = 0
        for child in ast.walk(node):
            if isinstance(child, (ast.And, ast.Or)):
                count += 1
            elif isinstance(child, ast.Compare):
                count += len(child.ops)
        return count
    
    def _to_constant_name(self, value) -> str:
        """Преобразует число в имя константы"""
        # Простая эвристика
        if value == 60:
            return "SECONDS_PER_MINUTE"
        elif value == 3600:
            return "SECONDS_PER_HOUR"
        elif value == 86400:
            return "SECONDS_PER_DAY"
        else:
            return f"CONSTANT_{value}"


def print_suggestions(suggestions: List[RefactoringSuggestion]):
    """Красивый вывод предложений"""
    print("\n" + "="*70)
    print("🛠️  ПРЕДЛОЖЕНИЯ ПО РЕФАКТОРИНГУ")
    print("="*70)
    
    if not suggestions:
        print("\n✅ Код выглядит хорошо! Нет критических проблем.")
        return
    
    # Группируем по приоритету
    high = [s for s in suggestions if s.priority == 'high']
    medium = [s for s in suggestions if s.priority == 'medium']
    low = [s for s in suggestions if s.priority == 'low']
    
    if high:
        print(f"\n🔴 ВЫСОКИЙ ПРИОРИТЕТ ({len(high)}):")
        for i, s in enumerate(high, 1):
            print(f"\n   {i}. {s.message}")
            print(f"      Строка: {s.line}")
            print(f"\n      Текущий код:")
            for line in s.current_code.split('\n')[:3]:
                print(f"      {line}")
            print(f"\n      💡 Рекомендация:")
            for line in s.suggested_code.split('\n'):
                print(f"      {line}")
            print(f"\n      Преимущества:")
            for benefit in s.benefits:
                print(f"      • {benefit}")
    
    if medium:
        print(f"\n🟡 СРЕДНИЙ ПРИОРИТЕТ ({len(medium)}):")
        for i, s in enumerate(medium, 1):
            print(f"   {i}. Строка {s.line}: {s.message}")
    
    if low:
        print(f"\n🟢 НИЗКИЙ ПРИОРИТЕТ ({len(low)}):")
        for i, s in enumerate(low, 1):
            print(f"   {i}. Строка {s.line}: {s.message}")
    
    print("\n" + "="*70)
    print(f"Всего предложений: {len(suggestions)}")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Refactor Suggest - предлагает улучшения кода'
    )
    parser.add_argument(
        'path',
        help='Путь к файлу или директории'
    )
    parser.add_argument(
        '--full', '-f', action='store_true',
        help='Полный анализ всех файлов в директории'
    )
    
    args = parser.parse_args()
    
    path = Path(args.path)
    
    if path.is_file():
        analyzer = RefactoringAnalyzer(str(path))
        suggestions = analyzer.analyze()
        print_suggestions(suggestions)
    elif path.is_dir() and args.full:
        all_suggestions = []
        for py_file in path.rglob('*.py'):
            if '__pycache__' in str(py_file):
                continue
            analyzer = RefactoringAnalyzer(str(py_file))
            suggestions = analyzer.analyze()
            all_suggestions.extend(suggestions)
        
        print(f"\n📊 Анализ завершён: {len(list(path.rglob('*.py')))} файлов")
        print_suggestions(all_suggestions)
    else:
        print("Укажите файл или используйте --full для директории")
        sys.exit(1)


if __name__ == "__main__":
    main()
