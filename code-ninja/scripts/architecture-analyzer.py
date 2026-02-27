#!/usr/bin/env python3
"""
Architecture Analyzer
Анализирует структуру Python-проекта, находит проблемы архитектуры,
циклические импорты, слишком большие файлы и функции.

Пример:
    python architecture-analyzer.py /path/to/project
"""

import ast
import os
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict
import json


class CodeMetrics:
    """Метрики кода"""
    def __init__(self):
        self.lines_of_code = 0
        self.functions = 0
        self.classes = 0
        self.imports = 0
        self.complexity = 0  # Простая цикломатическая сложность


class ArchitectureAnalyzer:
    """Анализатор архитектуры проекта"""
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.files_analyzed = 0
        self.issues = []
        self.metrics = defaultdict(CodeMetrics)
        self.import_graph = defaultdict(set)  # файл -> импорты
        self.all_files = []
        
    def analyze(self) -> Dict:
        """Запускает полный анализ"""
        print(f"🔍 Анализирую {self.project_path}...")
        
        # Находим все Python файлы
        self.all_files = list(self.project_path.rglob("*.py"))
        self.files_analyzed = len(self.all_files)
        
        print(f"   Найдено {self.files_analyzed} Python файлов")
        
        # Анализируем каждый файл
        for file_path in self.all_files:
            self._analyze_file(file_path)
        
        # Проверяем проблемы
        self._check_circular_imports()
        self._check_large_files()
        self._check_long_functions()
        self._check_architecture_smells()
        
        return self._generate_report()
    
    def _analyze_file(self, file_path: Path):
        """Анализирует один файл"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
        except Exception as e:
            self.issues.append({
                'type': 'read_error',
                'file': str(file_path),
                'message': f'Не могу прочитать файл: {e}'
            })
            return
        
        # Базовые метрики
        rel_path = str(file_path.relative_to(self.project_path))
        self.metrics[rel_path].lines_of_code = len(lines)
        
        # Парсим AST
        try:
            tree = ast.parse(content)
        except SyntaxError as e:
            self.issues.append({
                'type': 'syntax_error',
                'file': rel_path,
                'message': f'Синтаксическая ошибка: {e}'
            })
            return
        
        # Анализируем AST
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                self.metrics[rel_path].functions += 1
                # Считаем сложность (количество ветвлений)
                self.metrics[rel_path].complexity += self._count_branches(node)
            elif isinstance(node, ast.ClassDef):
                self.metrics[rel_path].classes += 1
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                self.metrics[rel_path].imports += 1
                self._record_imports(rel_path, node)
    
    def _count_branches(self, node: ast.FunctionDef) -> int:
        """Считает количество ветвлений в функции"""
        branches = 1  # Базовый путь
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For)):
                branches += 1
            elif isinstance(child, ast.ExceptHandler):
                branches += 1
        return branches
    
    def _record_imports(self, file_path: str, node):
        """Записывает импорты для построения графа"""
        if isinstance(node, ast.Import):
            for alias in node.names:
                self.import_graph[file_path].add(alias.name.split('.')[0])
        elif isinstance(node, ast.ImportFrom) and node.module:
            module = node.module.split('.')[0]
            self.import_graph[file_path].add(module)
    
    def _check_circular_imports(self):
        """Проверяет циклические импорты"""
        # Строим граф и ищем циклы
        visited = set()
        recursion_stack = set()
        
        def has_cycle(node, path=[]):
            visited.add(node)
            recursion_stack.add(node)
            path.append(node)
            
            for neighbor in self.import_graph.get(node, set()):
                if neighbor not in visited:
                    if has_cycle(neighbor, path.copy()):
                        return True
                elif neighbor in recursion_stack:
                    # Нашли цикл
                    cycle_start = path.index(neighbor)
                    cycle = path[cycle_start:] + [neighbor]
                    self.issues.append({
                        'type': 'circular_import',
                        'severity': 'high',
                        'message': f'Циклический импорт: {" -> ".join(cycle)}'
                    })
                    return True
            
            recursion_stack.remove(node)
            return False
        
        for file in self.import_graph:
            if file not in visited:
                has_cycle(file)
    
    def _check_large_files(self):
        """Проверяет слишком большие файлы"""
        LARGE_FILE_THRESHOLD = 500  # строк
        VERY_LARGE_THRESHOLD = 1000
        
        for file_path, metrics in self.metrics.items():
            if metrics.lines_of_code > VERY_LARGE_THRESHOLD:
                self.issues.append({
                    'type': 'very_large_file',
                    'severity': 'high',
                    'file': file_path,
                    'message': f'Файл слишком большой: {metrics.lines_of_code} строк (>{VERY_LARGE_THRESHOLD})',
                    'suggestion': 'Разбейте файл на модули'
                })
            elif metrics.lines_of_code > LARGE_FILE_THRESHOLD:
                self.issues.append({
                    'type': 'large_file',
                    'severity': 'medium',
                    'file': file_path,
                    'message': f'Большой файл: {metrics.lines_of_code} строк (>{LARGE_FILE_THRESHOLD})',
                    'suggestion': 'Рассмотрите разделение на части'
                })
    
    def _check_long_functions(self):
        """Проверяет длинные функции (по сложности)"""
        HIGH_COMPLEXITY = 10
        VERY_HIGH_COMPLEXITY = 20
        
        # Это упрощённая проверка - для реального проекта нужен более точный анализ
        for file_path, metrics in self.metrics.items():
            if metrics.complexity > VERY_HIGH_COMPLEXITY:
                self.issues.append({
                    'type': 'very_complex_file',
                    'severity': 'high',
                    'file': file_path,
                    'message': f'Высокая цикломатическая сложность: {metrics.complexity}',
                    'suggestion': 'Рефакторите: выделите функции, упростите условия'
                })
    
    def _check_architecture_smells(self):
        """Проверяет архитектурные проблемы"""
        # Ищем God Classes (много методов в одном классе)
        # Ищем utils.py (слишком общие имена)
        
        for file_path in self.metrics.keys():
            # Проверяем слишком общие имена
            filename = Path(file_path).name
            if filename in ['utils.py', 'helpers.py', 'common.py', 'misc.py']:
                self.issues.append({
                    'type': 'vague_name',
                    'severity': 'low',
                    'file': file_path,
                    'message': f'Слишком общее имя файла: {filename}',
                    'suggestion': 'Переименуйте в something_specific.py'
                })
    
    def _generate_report(self) -> Dict:
        """Генерирует отчёт"""
        total_lines = sum(m.lines_of_code for m in self.metrics.values())
        total_functions = sum(m.functions for m in self.metrics.values())
        total_classes = sum(m.classes for m in self.metrics.values())
        
        # Сортируем проблемы по severity
        severity_order = {'high': 0, 'medium': 1, 'low': 2}
        sorted_issues = sorted(
            self.issues,
            key=lambda x: severity_order.get(x.get('severity', 'low'), 3)
        )
        
        report = {
            'summary': {
                'files_analyzed': self.files_analyzed,
                'total_lines': total_lines,
                'total_functions': total_functions,
                'total_classes': total_classes,
                'issues_found': len(self.issues),
                'high_severity': len([i for i in self.issues if i.get('severity') == 'high']),
                'medium_severity': len([i for i in self.issues if i.get('severity') == 'medium']),
                'low_severity': len([i for i in self.issues if i.get('severity') == 'low']),
            },
            'top_files_by_size': sorted(
                [(f, m.lines_of_code) for f, m in self.metrics.items()],
                key=lambda x: x[1],
                reverse=True
            )[:10],
            'issues': sorted_issues[:20],  # Топ 20 проблем
            'recommendations': self._generate_recommendations()
        }
        
        return report
    
    def _generate_recommendations(self) -> List[str]:
        """Генерирует рекомендации"""
        recs = []
        
        high_issues = [i for i in self.issues if i.get('severity') == 'high']
        if high_issues:
            recs.append(f"🚨 Исправьте {len(high_issues)} критических проблем перед релизом")
        
        circular = [i for i in self.issues if i['type'] == 'circular_import']
        if circular:
            recs.append("🔄 Устраните циклические импорты - они вызывают проблемы при загрузке")
        
        large_files = [i for i in self.issues if i['type'] in ['large_file', 'very_large_file']]
        if large_files:
            recs.append(f"📦 Разбейте {len(large_files)} больших файлов на модули")
        
        if not recs:
            recs.append("✅ Архитектура выглядит хорошо! Продолжайте в том же духе")
        
        return recs


def print_report(report: Dict):
    """Красивый вывод отчёта"""
    print("\n" + "="*60)
    print("📊 ОТЧЁТ АНАЛИЗА АРХИТЕКТУРЫ")
    print("="*60)
    
    summary = report['summary']
    print(f"\n📁 Файлов проанализировано: {summary['files_analyzed']}")
    print(f"📝 Всего строк кода: {summary['total_lines']:,}")
    print(f"⚡ Функций: {summary['total_functions']}")
    print(f"🔷 Классов: {summary['total_classes']}")
    
    print(f"\n🎯 Проблем найдено: {summary['issues_found']}")
    if summary['high_severity']:
        print(f"   🔴 Критических: {summary['high_severity']}")
    if summary['medium_severity']:
        print(f"   🟡 Средних: {summary['medium_severity']}")
    if summary['low_severity']:
        print(f"   🟢 Низких: {summary['low_severity']}")
    
    if report['top_files_by_size']:
        print("\n📏 Самые большие файлы:")
        for file, lines in report['top_files_by_size'][:5]:
            print(f"   {lines:>4} строк  {file}")
    
    if report['issues']:
        print("\n⚠️  ТОП ПРОБЛЕМ:")
        for i, issue in enumerate(report['issues'][:10], 1):
            severity = issue.get('severity', 'low')
            icon = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}.get(severity, '⚪')
            print(f"\n   {icon} [{severity.upper()}] {issue.get('type', 'issue')}")
            if 'file' in issue:
                print(f"      Файл: {issue['file']}")
            print(f"      {issue['message']}")
            if 'suggestion' in issue:
                print(f"      💡 {issue['suggestion']}")
    
    print("\n💡 РЕКОМЕНДАЦИИ:")
    for rec in report['recommendations']:
        print(f"   {rec}")
    
    print("\n" + "="*60)


def main():
    if len(sys.argv) < 2:
        print("Использование: python architecture-analyzer.py <путь_к_проекту>")
        print("Пример: python architecture-analyzer.py /path/to/ai-router")
        sys.exit(1)
    
    project_path = sys.argv[1]
    
    if not os.path.exists(project_path):
        print(f"❌ Путь не существует: {project_path}")
        sys.exit(1)
    
    analyzer = ArchitectureAnalyzer(project_path)
    report = analyzer.analyze()
    
    print_report(report)
    
    # Сохраняем JSON отчёт
    output_file = "architecture_report.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Полный отчёт сохранён: {output_file}")
    
    # Exit code для CI/CD
    high_issues = report['summary']['high_severity']
    if high_issues > 0:
        print(f"\n⚠️  Найдено {high_issues} критических проблем!")
        sys.exit(1)


if __name__ == "__main__":
    main()
