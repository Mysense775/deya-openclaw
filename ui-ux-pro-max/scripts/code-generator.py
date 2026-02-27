#!/usr/bin/env python3
"""
UI-UX Code Generator
Превращает описание в готовый React/Tailwind код

Пример:
    python code-generator.py "кнопка с градиентом, закругленная, с иконкой" --type button
"""

import argparse
import json
import sys
from typing import Dict, List

# База знаний UI компонентов
COMPONENTS_DB = {
    "button": {
        "variants": {
            "primary": "bg-blue-600 hover:bg-blue-700 text-white",
            "secondary": "bg-gray-200 hover:bg-gray-300 text-gray-800",
            "outline": "border-2 border-blue-600 text-blue-600 hover:bg-blue-50",
            "ghost": "text-blue-600 hover:bg-blue-50",
            "danger": "bg-red-600 hover:bg-red-700 text-white",
            "gradient": "bg-gradient-to-r from-blue-500 to-purple-600 text-white"
        },
        "sizes": {
            "sm": "px-3 py-1.5 text-sm",
            "md": "px-4 py-2 text-base",
            "lg": "px-6 py-3 text-lg",
            "xl": "px-8 py-4 text-xl"
        },
        "shapes": {
            "rounded": "rounded-lg",
            "pill": "rounded-full",
            "square": "rounded-none",
            "soft": "rounded-[20px]"
        }
    },
    "card": {
        "variants": {
            "default": "bg-white shadow-md",
            "outline": "border border-gray-200",
            "elevated": "bg-white shadow-xl",
            "glass": "bg-white/80 backdrop-blur-sm",
            "gradient": "bg-gradient-to-br from-blue-50 to-purple-50"
        },
        "padding": {
            "sm": "p-4",
            "md": "p-6",
            "lg": "p-8"
        }
    },
    "input": {
        "variants": {
            "default": "border-gray-300 focus:border-blue-500 focus:ring-blue-500",
            "outline": "border-2 border-gray-300 focus:border-blue-600",
            "filled": "bg-gray-100 border-transparent focus:bg-white focus:border-blue-500",
            "underline": "border-0 border-b-2 border-gray-300 rounded-none focus:border-blue-500"
        },
        "sizes": {
            "sm": "px-3 py-1.5 text-sm",
            "md": "px-4 py-2 text-base",
            "lg": "px-4 py-3 text-lg"
        }
    },
    "badge": {
        "variants": {
            "default": "bg-gray-100 text-gray-800",
            "primary": "bg-blue-100 text-blue-800",
            "success": "bg-green-100 text-green-800",
            "warning": "bg-yellow-100 text-yellow-800",
            "danger": "bg-red-100 text-red-800",
            "gradient": "bg-gradient-to-r from-blue-500 to-purple-600 text-white"
        }
    }
}

# Дизайн-токены (из твоего бренда)
TOKENS = {
    "colors": {
        "primary": "#3b82f6",
        "primary-dark": "#2563eb",
        "secondary": "#8b5cf6",
        "accent": "#7c3aed",
        "success": "#10b981",
        "warning": "#f59e0b",
        "danger": "#ef4444",
        "dark": "#0d0d12",
        "gray": {
            "50": "#f9fafb",
            "100": "#f3f4f6",
            "200": "#e5e7eb",
            "300": "#d1d5db",
            "400": "#9ca3af",
            "500": "#6b7280",
            "600": "#4b5563",
            "700": "#374151",
            "800": "#1f2937",
            "900": "#111827"
        }
    },
    "radius": {
        "sm": "4px",
        "md": "8px",
        "lg": "12px",
        "xl": "16px",
        "2xl": "20px",
        "full": "9999px"
    },
    "shadows": {
        "sm": "0 1px 2px 0 rgb(0 0 0 / 0.05)",
        "md": "0 4px 6px -1px rgb(0 0 0 / 0.1)",
        "lg": "0 10px 15px -3px rgb(0 0 0 / 0.1)",
        "xl": "0 20px 25px -5px rgb(0 0 0 / 0.1)"
    }
}


def parse_description(description: str) -> Dict:
    """Анализирует описание и извлекает параметры"""
    desc = description.lower()
    
    params = {
        "variant": "primary",
        "size": "md",
        "shape": "rounded",
        "icon": False,
        "gradient": False,
        "glass": False,
        "animation": False
    }
    
    # Определяем тип компонента
    if any(word in desc for word in ["кнопка", "button", "btn"]):
        params["type"] = "button"
    elif any(word in desc for word in ["карточка", "card", "карта"]):
        params["type"] = "card"
    elif any(word in desc for word in ["поле", "input", "ввод"]):
        params["type"] = "input"
    elif any(word in desc for word in ["бейдж", "badge", "метка"]):
        params["type"] = "badge"
    else:
        params["type"] = "button"  # default
    
    # Определяем вариант (для разных компонентов разные дефолты)
    if params["type"] == "card":
        params["variant"] = "default"  # default для карточки
    elif any(word in desc for word in ["главная", "primary", "основная"]):
        params["variant"] = "primary"
    elif any(word in desc for word in ["вторичная", "secondary", "серая"]):
        params["variant"] = "secondary"
    elif any(word in desc for word in ["контур", "outline", "обводка"]):
        params["variant"] = "outline"
    elif any(word in desc for word in ["опасность", "danger", "красная", "удалить"]):
        params["variant"] = "danger"
    elif any(word in desc for word in ["градиент", "gradient", "перелив"]):
        params["variant"] = "gradient"
        params["gradient"] = True
    elif any(word in desc for word in ["стекло", "glass", "прозрачная", "glassmorphism"]):
        params["variant"] = "glass"
        params["glass"] = True
    
    # Определяем размер
    if any(word in desc for word in ["маленькая", "small", "sm", "мини"]):
        params["size"] = "sm"
    elif any(word in desc for word in ["большая", "large", "lg", "большой"]):
        params["size"] = "lg"
    elif any(word in desc for word in ["огромная", "xl", "extra"]):
        params["size"] = "xl"
    
    # Определяем форму
    if any(word in desc for word in ["пилюля", "pill", "круглая", "полностью"]):
        params["shape"] = "pill"
    elif any(word in desc for word in ["квадратная", "square", "острая"]):
        params["shape"] = "square"
    elif any(word in desc for word in ["мягкая", "soft", "20px", "балийская"]):
        params["shape"] = "soft"
    
    # Проверяем иконку
    if any(word in desc for word in ["иконка", "icon", "стрелка", "значок"]):
        params["icon"] = True
    
    # Проверяем анимацию
    if any(word in desc for word in ["анимация", "animation", "пульсация", "hover"]):
        params["animation"] = True
    
    return params


def generate_button(params: Dict) -> str:
    """Генерирует React-код для кнопки"""
    component_db = COMPONENTS_DB["button"]
    
    classes = [
        "inline-flex items-center justify-center font-medium transition-all duration-200",
        component_db["variants"][params["variant"]],
        component_db["sizes"][params["size"]],
        component_db["shapes"][params["shape"]]
    ]
    
    if params["animation"]:
        classes.append("hover:scale-105 active:scale-95 hover:shadow-lg")
    
    class_string = " ".join(classes)
    
    if params["icon"]:
        code = f'''import {{ ArrowRight }} from 'lucide-react';

export function Button({{ children, onClick, disabled }}) {{
  return (
    <button
      onClick={{onClick}}
      disabled={{disabled}}
      className="{class_string} disabled:opacity-50 disabled:cursor-not-allowed gap-2"
    >
      {{children}}
      <ArrowRight className="w-4 h-4" />
    </button>
  );
}}'''
    else:
        code = f'''export function Button({{ children, onClick, disabled }}) {{
  return (
    <button
      onClick={{onClick}}
      disabled={{disabled}}
      className="{class_string} disabled:opacity-50 disabled:cursor-not-allowed"
    >
      {{children}}
    </button>
  );
}}'''
    
    return code


def generate_card(params: Dict) -> str:
    """Генерирует React-код для карточки"""
    component_db = COMPONENTS_DB["card"]
    
    classes = [
        "rounded-[20px]",
        component_db["variants"][params["variant"]],
        component_db["padding"][params["size"]]
    ]
    
    if params["animation"]:
        classes.append("hover:shadow-xl transition-shadow duration-300")
    
    class_string = " ".join(classes)
    
    code = f'''export function Card({{ children, title, subtitle }}) {{
  return (
    <div className="{class_string}">
      {{(title || subtitle) && (
        <div className="mb-4">
          {{title && <h3 className="text-lg font-semibold text-gray-900">{{title}}</h3>}}
          {{subtitle && <p className="text-sm text-gray-600">{{subtitle}}</p>}}
        </div>
      )}}
      {{children}}
    </div>
  );
}}'''
    
    return code


def generate_input(params: Dict) -> str:
    """Генерирует React-код для поля ввода"""
    component_db = COMPONENTS_DB["input"]
    
    classes = [
        "w-full rounded-lg border outline-none transition-colors",
        component_db["variants"][params["variant"]],
        component_db["sizes"][params["size"]]
    ]
    
    class_string = " ".join(classes)
    
    code = f'''export function Input({{ 
  placeholder, 
  value, 
  onChange, 
  type = "text",
  label,
  error
}}) {{
  return (
    <div className="w-full">
      {{label && (
        <label className="block text-sm font-medium text-gray-700 mb-1">
          {{label}}
        </label>
      )}}
      <input
        type={{type}}
        value={{value}}
        onChange={{onChange}}
        placeholder={{placeholder}}
        className="{class_string} {{error ? 'border-red-500 focus:border-red-500 focus:ring-red-500' : ''}}"
      />
      {{error && <p className="mt-1 text-sm text-red-600">{{error}}</p>}}
    </div>
  );
}}'''
    
    return code


def generate_badge(params: Dict) -> str:
    """Генерирует React-код для бейджа"""
    component_db = COMPONENTS_DB["badge"]
    
    classes = [
        "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium",
        component_db["variants"][params["variant"]]
    ]
    
    class_string = " ".join(classes)
    
    code = f'''export function Badge({{ children }}) {{
  return (
    <span className="{class_string}">
      {{children}}
    </span>
  );
}}'''
    
    return code


def main():
    parser = argparse.ArgumentParser(
        description="Генератор React-компонентов из описания"
    )
    parser.add_argument(
        "description",
        help="Описание компонента (например: 'кнопка с градиентом, закругленная')"
    )
    parser.add_argument(
        "--type",
        choices=["button", "card", "input", "badge", "auto"],
        default="auto",
        help="Тип компонента (auto = определить автоматически)"
    )
    parser.add_argument(
        "--output",
        "-o",
        help="Файл для сохранения (если не указан — вывод в консоль)"
    )
    
    args = parser.parse_args()
    
    # Парсим описание
    params = parse_description(args.description)
    
    # Если тип указан явно — используем его
    if args.type != "auto":
        params["type"] = args.type
    
    # Генерируем код
    generators = {
        "button": generate_button,
        "card": generate_card,
        "input": generate_input,
        "badge": generate_badge
    }
    
    generator = generators.get(params["type"], generate_button)
    code = generator(params)
    
    # Выводим результат
    output = f'''// Сгенерировано UI-UX-Pro-Max
// Описание: {args.description}
// Тип: {params["type"]}
// Вариант: {params["variant"]}
// Размер: {params["size"]}

{code}
'''
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"✅ Компонент сохранён в {args.output}")
    else:
        print(output)
    
    # Выводим информацию о параметрах
    print(f"\n🎨 Параметры:")
    print(f"   Тип: {params['type']}")
    print(f"   Вариант: {params['variant']}")
    print(f"   Размер: {params['size']}")
    print(f"   Форма: {params['shape']}")
    print(f"   Иконка: {'да' if params['icon'] else 'нет'}")
    print(f"   Анимация: {'да' if params['animation'] else 'нет'}")


if __name__ == "__main__":
    main()
