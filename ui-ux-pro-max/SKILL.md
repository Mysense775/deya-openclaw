---
name: ui-ux-pro-max
description: UI/UX design intelligence and implementation guidance for building polished interfaces. Use when the user asks for UI design, UX flows, information architecture, visual style direction, design systems/tokens, component specs, copy/microcopy, accessibility, or to generate/critique/refine frontend UI (HTML/CSS/JS, React, Next.js, Vue, Svelte, Tailwind). Includes workflows for (1) generating new UI layouts and styling, (2) improving existing UI/UX, (3) producing design-system tokens and component guidelines, and (4) turning UX recommendations into concrete code changes.
triggers:
  - "сделай дизайн"
  - "ui ux"
  - "компонент"
  - "кнопка"
  - "карточка"
  - "поле ввода"
  - "бейдж"
  - "верстка"
  - "react компонент"
  - "tailwind"
---

# UI-UX-Pro-Max 🎨

Интеллект дизайна с тёплым балийским вайбом.

## Быстрый старт

### Генератор компонентов (из описания в код)

```bash
# Сгенерировать кнопку
python3 scripts/code-generator.py "кнопка с градиентом, большая, с иконкой"

# Сохранить в файл
python3 scripts/code-generator.py "карточка со стеклом" --type card -o Card.tsx
```

### Готовые компоненты (стандартные)

- `assets/components/Button.tsx` — Кнопки (все варианты, иконки, loading)
- `assets/components/Card.tsx` — Карточки (default, gradient, glass, dark)
- `assets/components/Input.tsx` — Поля ввода (с иконками, error/success states)
- `assets/components/Badge.tsx` — Бейджи (статусы, gradient, glow)

### Компоненты с GSAP анимациями ⭐

- `assets/components/ButtonGSAP.tsx` — Кнопки с hover-анимациями и morphing
- `assets/components/CardGSAP.tsx` — Карточки с parallax и glow эффектами
- `assets/components/DeyaGSAP.tsx` — Хуки для кастомных анимаций

### Визуальный превью

Открой `assets/canvas-preview.html` в браузере — там живые примеры всех компонентов.

## Рабочий процесс

### 1. Определи задачу
- Платформа: web / mobile / desktop
- Стек: React/Vue/Svelte, Tailwind/стили
- Контекст: новый проект или улучшение
- Особенности: доступность, анимации, темы

### 2. Выбери подход

**Вариант A: Генератор кода (быстро)**
```bash
python3 scripts/code-generator.py "описание компонента"
```

**Вариант B: Готовые компоненты (гибко)**
- Скопируй из `assets/components/`
- Настрой под проект
- Добавь свою логику

**Вариант C: С нуля (уникально)**
- Используй дизайн-токены из `data/`
- Следуй гайду `deya-touch.md`
- Проверь в `canvas-preview.html`

### 3. Дизайн-токены

```css
/* Цвета */
--color-primary: #3b82f6;
--color-secondary: #8b5cf6;
--color-accent: #7c3aed;
--color-dark: #0d0d12;

/* Градиенты */
--gradient-sunset: linear-gradient(135deg, #f59e0b, #ec4899, #8b5cf6);
--gradient-ocean: linear-gradient(135deg, #0ea5e9, #3b82f6);

/* Скругление (Deya Style) */
--radius-soft: 20px;

/* Тени */
--shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
--shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);
--shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1);
```

### 4. Deya Touch

Ключевые принципы вайба Деи в дизайне:
- **20px скругление** — мягкие формы без острых углов
- **Тёплые градиенты** — закат (оранжевый → розовый → фиолетовый)
- **Воздух** — generous whitespace, не перегружать
- **Живые детали** — плавные transitions (300ms), hover-эффекты
- **Тёплый свет** — не неоновые цвета

Подробнее в `deya-touch.md`

## Структура skill

```
ui-ux-pro-max/
├── SKILL.md                    # Этот файл
├── README.md                   # Документация для пользователя
├── CHANGELOG.md               # История изменений
├── scripts/
│   ├── code-generator.py      # Генератор компонентов ⭐
│   ├── design_system.py       # Генератор токенов
│   └── figma-export.py        # Выгрузка в Figma (TODO)
├── assets/
│   ├── components/            # Готовые React компоненты
│   │   ├── Button.tsx
│   │   ├── Card.tsx
│   │   ├── Input.tsx
│   │   └── Badge.tsx
│   ├── canvas-preview.html    # Визуальный превью 🎨
│   └── data/                  # Дизайн-данные (CSV)
├── references/
│   └── deya-touch.md          # Принципы вайба Деи 🌺
└── tests/                     # Тесты компонентов
```

## Примеры использования

### Кнопка
```tsx
<Button variant="gradient" size="lg" icon>
  Начать путешествие
</Button>
```

### Карточка
```tsx
<Card variant="gradient" padding="lg" title="Заголовок">
  Содержимое карточки
</Card>
```

### Поле ввода
```tsx
<Input 
  label="Email" 
  type="email"
  placeholder="your@email.com"
  error="Неверный формат"
/>
```

### Бейдж
```tsx
<Badge variant="success" dot>Активен</Badge>
<Badge variant="gradient">Pro</Badge>
```

## GSAP Анимации ⭐

### Готовые хуки из DeyaGSAP.tsx

```tsx
import { useFadeIn, useSlideIn, useStagger, useSoftHover } from './DeyaGSAP';

// Плавное появление
const fadeRef = useFadeIn({ duration: 0.8, delay: 0.2 });
<div ref={fadeRef}>Content</div>

// Выезд сбоку
const slideRef = useSlideIn('left', { duration: 0.6 });

// Каскад для списка
const staggerRef = useStagger({ stagger: 0.1, delay: 0.3 });
<ul ref={staggerRef}>
  {items.map(i => <li key={i}>{i}</li>)}
</ul>

// Мягкий hover
const hoverRef = useSoftHover();
<button ref={hoverRef}>Hover me</button>
```

### Компоненты с GSAP

**ButtonGSAP** — hover с morphing скругления:
```tsx
<ButtonGSAP 
  variant="gradient" 
  animate 
  animateOnMount
>
  Кликни меня
</ButtonGSAP>
```

**CardGSAP** — с glow и parallax:
```tsx
<CardGSAP 
  variant="glass" 
  hover 
  glow 
  animate
>
  Содержимое
</CardGSAP>
```

### Принципы анимации Деи

| Свойство | Значение | Описание |
|----------|----------|----------|
| Duration | 0.3-0.7s | Неспешно, но не медленно |
| Easing | `power2.out` | Плавное замедление |
| Hover | `y: -2`, `scale: 1.02` | Мягкий подъём |
| Morphing | `20px → 24px` | Скругление растёт |
| Stagger | 0.1s | Каскад между элементами |

**Никогда:**
- ❌ Резкие движения (`linear` easing)
- ❌ Большие scale (1.1+) — выглядит дёшево
- ❌ Мгновенные переходы (0.1s)

## Roadmap

- [x] code-generator.py
- [x] Button, Card, Input, Badge компоненты
- [x] canvas-preview.html
- [x] deya-touch.md
- [x] GSAP анимации (ButtonGSAP, CardGSAP, DeyaGSAP)
- [ ] figma-export.py
- [ ] a11y-check.py
- [ ] Тёмная тема полностью

## Связь

- Канал: @dayanrouter
- Бот: @ai_router_support_bot
- Сайт: go.airouter.host

---

*Тёплый свет, не неоновое сияние* ✨🌺
