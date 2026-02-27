#!/usr/bin/env python3
"""
deya-generate-image.py
Генерация изображений Деи с правильной внешностью и локацией

Использование:
    python deya-generate-image.py --scene morning-work
    python deya-generate-image.py --scene evening-planning --aspect portrait
    python deya-generate-image.py --custom "working with team in office"
"""

import argparse
import json
import sys

# Базовый промт Деи на основе детального анализа
BASE_PROMPT = """Professional woman in her early 30s, elegant minimal style, 
dark brown hair in loose messy bun or flowing naturally with soft waves,
minimal makeup with warm natural tones, intelligent confident expression with slight thoughtful smile,
oval face shape, warm dark eyes, straight nose, medium full lips with natural color,

wearing beige linen suit or camel wool coat depending on season, oversized white shirt underneath,
minimal gold jewelry - thin delicate necklace and small earrings, no large accessories,

location: modern coworking space or cozy cafe in Kazan Russia, large window with city view,
urban background with buildings visible through glass,

warm golden hour lighting creating soft shadows on face, realistic photography style,
cinematic composition, shallow depth of field, 85mm portrait lens look,
color palette: beige, cream, camel, soft gold, olive, warm neutrals only"""

# Запрещенные элементы (негативный промт)
NEGATIVE_ELEMENTS = "frangipani, beach, sand, tropical, Bali, sunset ocean, barefoot, neon lights, party"

# Сцены
SCENES = {
    "morning-work": {
        "desc": "Утренняя работа",
        "prompt": "Morning light, woman working on laptop at minimalist desk, coffee cup nearby, focused expression, Kazan city view through large window, productive atmosphere"
    },
    "evening-planning": {
        "desc": "Вечернее планирование",
        "prompt": "Golden hour evening light, woman planning on tablet with charts and graphs, thoughtful expression, city skyline in background, calm productive mood"
    },
    "coffee-break": {
        "desc": "Кофе-брейк",
        "prompt": "Taking break with coffee cup, looking at city view from office window, relaxed but professional, authentic moment, warm atmosphere"
    },
    "team-meeting": {
        "desc": "Командная работа",
        "prompt": "In modern meeting room, discussing with team, presenting ideas, confident gesture, glass walls, city view, professional environment"
    },
    "creative-work": {
        "desc": "Творческая работа",
        "prompt": "Sketching ideas on tablet, surrounded by holographic interfaces, creative flow, modern office space, technology meets elegance"
    },
    "outdoor-walk": {
        "desc": "Прогулка по городу",
        "prompt": "Walking on Bauman street Kazan, autumn or spring weather, elegant coat, thinking about plans, urban background, purposeful stride"
    }
}

def get_full_prompt(scene_key=None, custom_desc=None, mood="professional"):
    """Собирает полный промт для генерации"""
    
    if custom_desc:
        scene_part = custom_desc
    elif scene_key and scene_key in SCENES:
        scene_part = SCENES[scene_key]["prompt"]
    else:
        scene_part = "Professional portrait, confident pose, modern office environment"
    
    # Добавляем настроение
    mood_prompt = {
        "professional": "confident and focused",
        "creative": "inspired and thoughtful", 
        "relaxed": "calm and approachable",
        "energetic": "dynamic and purposeful"
    }.get(mood, "confident and focused")
    
    full_prompt = f"{BASE_PROMPT}, {scene_part}, {mood_prompt}, {NEGATIVE_ELEMENTS}"
    
    return full_prompt

def generate_image(scene=None, custom=None, aspect="portrait", mood="professional"):
    """Генерирует изображение через API"""
    
    prompt = get_full_prompt(scene, custom, mood)
    
    # Aspect ratio
    aspect_ratios = {
        "portrait": "portrait_4_3",
        "landscape": "landscape_16_9", 
        "square": "square_1_1",
        "story": "portrait_9_16"
    }
    
    size = aspect_ratios.get(aspect, "portrait_4_3")
    
    # Формируем запрос
    request = {
        "model": "fal-ai/flux-2-flex",
        "messages": [{"role": "user", "content": prompt}],
        "image_size": size
    }
    
    print(f"🎨 Генерация: {SCENES.get(scene, {}).get('desc', 'Custom') if not custom else 'Custom'}")
    print(f"📐 Aspect ratio: {size}")
    print(f"📝 Prompt preview: {prompt[:100]}...")
    print()
    print(json.dumps(request, indent=2, ensure_ascii=False))

def main():
    parser = argparse.ArgumentParser(description='Генерация изображений Деи')
    parser.add_argument('--scene', choices=list(SCENES.keys()), 
                       help='Готовая сцена')
    parser.add_argument('--custom', type=str,
                       help='Кастомное описание сцены')
    parser.add_argument('--aspect', choices=['portrait', 'landscape', 'square', 'story'],
                       default='portrait', help='Соотношение сторон')
    parser.add_argument('--mood', choices=['professional', 'creative', 'relaxed', 'energetic'],
                       default='professional', help='Настроение')
    parser.add_argument('--list', action='store_true',
                       help='Показать доступные сцены')
    
    args = parser.parse_args()
    
    if args.list:
        print("📸 Доступные сцены:")
        for key, data in SCENES.items():
            print(f"  {key:20s} — {data['desc']}")
        return
    
    if not args.scene and not args.custom:
        parser.print_help()
        print("\n💡 Используй --list чтобы увидеть доступные сцены")
        return
    
    generate_image(args.scene, args.custom, args.aspect, args.mood)

if __name__ == "__main__":
    main()
