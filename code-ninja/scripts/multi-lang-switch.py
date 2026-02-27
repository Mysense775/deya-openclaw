#!/usr/bin/env python3
"""
Multi-Lang Switch
Помогает переключаться между языками программирования.
Показывает эквиваленты конструкций: Python <-> JavaScript <-> TypeScript <-> Go

Пример:
    python multi-lang-switch.py --from python --to javascript "list comprehension"
    python multi-lang-switch.py --show python "dictionary"
"""

import argparse
from typing import Dict, List


# База знаний конструкций
LANGUAGE_PATTERNS = {
    "list_comprehension": {
        "python": "[x for x in items if x > 0]",
        "javascript": "items.filter(x => x > 0).map(x => x)",
        "typescript": "items.filter((x: number) => x > 0).map(x => x)",
        "go": "// Используйте цикл:\nresult := []int{}\nfor _, x := range items {\n    if x > 0 {\n        result = append(result, x)\n    }\n}",
        "description": "Фильтрация и преобразование списка"
    },
    "dictionary": {
        "python": "data = {'key': 'value'}",
        "javascript": "const data = {key: 'value'};",
        "typescript": "const data: Record<string, string> = {key: 'value'};",
        "go": "data := map[string]string{\"key\": \"value\"}",
        "description": "Ассоциативный массив / хеш-таблица"
    },
    "class": {
        "python": """class User:
    def __init__(self, name):
        self.name = name
    
    def greet(self):
        return f"Hello, {self.name}!\"""",
        "javascript": """class User {
    constructor(name) {
        this.name = name;
    }
    
    greet() {
        return `Hello, ${this.name}!`;
    }
}""",
        "typescript": """class User {
    name: string;
    
    constructor(name: string) {
        this.name = name;
    }
    
    greet(): string {
        return `Hello, ${this.name}!`;
    }
}""",
        "go": """type User struct {
    Name string
}

func (u User) Greet() string {
    return fmt.Sprintf("Hello, %s!", u.Name)
}""",
        "description": "Определение класса с методом"
    },
    "async_function": {
        "python": """async def fetch_data():
    result = await api.get('/data')
    return result""",
        "javascript": """async function fetchData() {
    const result = await api.get('/data');
    return result;
}""",
        "typescript": """async function fetchData(): Promise<Data> {
    const result = await api.get('/data');
    return result;
}""",
        "go": """func fetchData() (*Data, error) {
    result, err := api.Get("/data")
    if err != nil {
        return nil, err
    }
    return result, nil
}""",
        "description": "Асинхронная функция с await"
    },
    "error_handling": {
        "python": """try:
    result = risky_operation()
except ValueError as e:
    logger.error(f"Error: {e}")
    raise""",
        "javascript": """try {
    const result = riskyOperation();
} catch (e) {
    logger.error(`Error: ${e}`);
    throw e;
}""",
        "typescript": """try {
    const result = riskyOperation();
} catch (e: any) {
    logger.error(`Error: ${e.message}`);
    throw e;
}""",
        "go": """result, err := riskyOperation()
if err != nil {
    log.Printf("Error: %v", err)
    return err
}""",
        "description": "Обработка ошибок"
    },
    "lambda": {
        "python": "lambda x: x * 2",
        "javascript": "x => x * 2",
        "typescript": "(x: number) => x * 2",
        "go": "func(x int) int { return x * 2 }",
        "description": "Анонимная функция / lambda"
    },
    "destructuring": {
        "python": "a, b = (1, 2)",
        "javascript": "const [a, b] = [1, 2];",
        "typescript": "const [a, b]: [number, number] = [1, 2];",
        "go": "a, b := 1, 2",
        "description": "Деструктуризация / множественное присваивание"
    },
    "string_interpolation": {
        "python": "f'Hello, {name}!'",
        "javascript": "`Hello, ${name}!`",
        "typescript": "`Hello, ${name}!`",
        "go": "fmt.Sprintf(\"Hello, %s!\", name)",
        "description": "Интерполяция строк"
    },
    "type_annotation": {
        "python": "def greet(name: str) -> str:",
        "javascript": "// JSDoc:\n/** @param {string} name @returns {string} */",
        "typescript": "function greet(name: string): string {",
        "go": "func greet(name string) string {",
        "description": "Аннотация типов"
    },
    "default_params": {
        "python": "def greet(name='World'):",
        "javascript": "function greet(name = 'World') {",
        "typescript": "function greet(name: string = 'World') {",
        "go": "func greet(name string) string {\n    if name == \"\" {\n        name = \"World\"\n    }",
        "description": "Параметры по умолчанию"
    },
    "decorator": {
        "python": "@app.route('/api')\ndef handler():",
        "javascript": "@Route('/api')\nhandler() {",
        "typescript": "@Route('/api')\nhandler() {",
        "go": "// Middleware паттерн:\nr.HandleFunc(\"/api\", handler)",
        "description": "Декоратор / middleware"
    },
}


class LanguageSwitcher:
    """Помощник переключения между языками"""
    
    def __init__(self):
        self.patterns = LANGUAGE_PATTERNS
    
    def show_all(self, pattern_name: str):
        """Показывает паттерн на всех языках"""
        if pattern_name not in self.patterns:
            # Ищем похожие
            similar = [k for k in self.patterns.keys() if pattern_name.lower() in k.lower()]
            if similar:
                print(f"Не найдено '{pattern_name}'. Возможно, вы имели в виду:")
                for s in similar:
                    print(f"  - {s}")
            else:
                print(f"Не найдено '{pattern_name}'")
                print(f"\nДоступные паттерны:")
                for k in self.patterns.keys():
                    print(f"  - {k}")
            return
        
        pattern = self.patterns[pattern_name]
        
        print(f"\n{'='*70}")
        print(f"🔄 {pattern_name.replace('_', ' ').title()}")
        print(f"   {pattern['description']}")
        print(f"{'='*70}")
        
        for lang in ['python', 'javascript', 'typescript', 'go']:
            print(f"\n{self._lang_icon(lang)} {lang.upper()}:")
            print("-" * 40)
            print(pattern[lang])
    
    def translate(self, from_lang: str, to_lang: str, pattern_name: str):
        """Переводит паттерн с одного языка на другой"""
        if pattern_name not in self.patterns:
            print(f"Паттерн '{pattern_name}' не найден")
            return
        
        pattern = self.patterns[pattern_name]
        
        if from_lang not in pattern or to_lang not in pattern:
            print(f"Неподдерживаемый язык. Доступны: python, javascript, typescript, go")
            return
        
        print(f"\n{'='*70}")
        print(f"🔄 {pattern_name.replace('_', ' ').title()}")
        print(f"   {pattern['description']}")
        print(f"{'='*70}")
        
        print(f"\n{self._lang_icon(from_lang)} ИСХОДНЫЙ ({from_lang.upper()}):")
        print("-" * 40)
        print(pattern[from_lang])
        
        print(f"\n{self._lang_icon(to_lang)} РЕЗУЛЬТАТ ({to_lang.upper()}):")
        print("-" * 40)
        print(pattern[to_lang])
        
        # Добавляем советы
        self._print_tips(from_lang, to_lang)
    
    def _lang_icon(self, lang: str) -> str:
        """Возвращает иконку для языка"""
        icons = {
            'python': '🐍',
            'javascript': '💛',
            'typescript': '💙',
            'go': '🐹'
        }
        return icons.get(lang, '•')
    
    def _print_tips(self, from_lang: str, to_lang: str):
        """Печатает советы по переходу"""
        tips = {
            ('python', 'javascript'): [
                "В JS нет встроенных list/dict comprehensions - используйте map/filter",
                "Отступы не важны, но используйте ; для явного завершения",
                "None в Python -> null в JS"
            ],
            ('python', 'typescript'): [
                "Добавьте типы ко всем параметрам и возвращаемым значениям",
                "Используйте interfaces для сложных объектов",
                "Включите strict mode в tsconfig.json"
            ],
            ('python', 'go'): [
                "В Go нет исключений - используйте возврат ошибок",
                "Все переменные должны быть использованы",
                "Экспортируйте через заглавную букву (Name, не name)"
            ],
            ('javascript', 'python'): [
                "Уберите ; и фигурные скобки",
                "const/let -> просто имя переменной",
                "=== -> == (или is для объектов)"
            ],
            ('javascript', 'typescript'): [
                "Добавьте :type к параметрам",
                "Укажите возвращаемый тип функции",
                "Используйте интерфейсы вместо объектов"
            ],
        }
        
        key = (from_lang, to_lang)
        if key in tips:
            print(f"\n💡 Советы по переходу {from_lang} -> {to_lang}:")
            for tip in tips[key]:
                print(f"   • {tip}")
    
    def list_patterns(self):
        """Выводит список всех паттернов"""
        print("\n📚 Доступные паттерны:")
        print("="*70)
        
        # Группируем по категориям
        categories = {
            "Структуры данных": ["dictionary", "list_comprehension", "destructuring"],
            "Функции": ["lambda", "async_function", "default_params", "decorator"],
            "Классы": ["class"],
            "Типы": ["type_annotation", "string_interpolation"],
            "Обработка ошибок": ["error_handling"]
        }
        
        for category, patterns in categories.items():
            print(f"\n{category}:")
            for pattern in patterns:
                if pattern in self.patterns:
                    desc = self.patterns[pattern]['description']
                    print(f"  • {pattern:20s} - {desc}")


def main():
    parser = argparse.ArgumentParser(
        description='Multi-Lang Switch - переключение между языками программирования'
    )
    parser.add_argument(
        'pattern',
        nargs='?',
        help='Название паттерна (например: list_comprehension, class)'
    )
    parser.add_argument(
        '--from', '-f',
        dest='from_lang',
        choices=['python', 'javascript', 'typescript', 'go'],
        help='Исходный язык'
    )
    parser.add_argument(
        '--to', '-t',
        dest='to_lang',
        choices=['python', 'javascript', 'typescript', 'go'],
        help='Целевой язык'
    )
    parser.add_argument(
        '--show', '-s',
        action='store_true',
        help='Показать на всех языках'
    )
    parser.add_argument(
        '--list', '-l',
        action='store_true',
        help='Список всех паттернов'
    )
    
    args = parser.parse_args()
    
    switcher = LanguageSwitcher()
    
    if args.list:
        switcher.list_patterns()
    elif args.show and args.pattern:
        switcher.show_all(args.pattern)
    elif args.from_lang and args.to_lang and args.pattern:
        switcher.translate(args.from_lang, args.to_lang, args.pattern)
    elif args.pattern:
        # По умолчанию показываем на всех языках
        switcher.show_all(args.pattern)
    else:
        print("Использование:")
        print(f"  python multi-lang-switch.py list_comprehension")
        print(f"  python multi-lang-switch.py class --show")
        print(f"  python multi-lang-switch.py lambda --from python --to go")
        print(f"  python multi-lang-switch.py --list")


if __name__ == "__main__":
    main()
