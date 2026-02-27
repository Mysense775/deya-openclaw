# UI-UX-Pro-Max 🎨

Генератор UI-компонентов с тёплым балийским вайбом. Превращает описание в готовый React + Tailwind код.

## 🚀 Быстрый старт

### Генератор из описания

```bash
# Кнопка
python3 scripts/code-generator.py "кнопка с градиентом, большая, с иконкой"

# Карточка
python3 scripts/code-generator.py "карточка со стеклом, мягкая" --type card

# Сохранить в файл
python3 scripts/code-generator.py "поле ввода с ошибкой" --type input -o Input.tsx
```

### Готовые компоненты

Все компоненты в `assets/components/` — TypeScript + Tailwind + стиль Деи:

- **Button** — 6 вариантов, иконки, loading, анимации
- **Card** — default, gradient, glass, dark, elevated
- **Input** — с иконками, error/success states, password toggle
- **Badge** — статусы, gradient, glow, removable

### Визуальный превью

```bash
open assets/canvas-preview.html
```

Или посмотри живую версию со всеми примерами.

## 📦 Установка компонентов

```bash
# Скопируй нужный компонент
cp skills/ui-ux-pro-max/assets/components/Button.tsx src/components/

# Установи зависимости (если нужны)
npm install lucide-react class-variance-authority clsx tailwind-merge
```

## 🎨 Использование

### Button

```tsx
import { Button } from './components/Button';

// Варианты
<Button variant="primary">Основная</Button>
<Button variant="gradient">Закат 🌅</Button>
<Button variant="danger">Удалить</Button>
<Button variant="outline">Отмена</Button>

// Размеры
<Button size="sm">Маленькая</Button>
<Button size="lg">Большая</Button>

// С иконкой и loading
<Button icon loading>Загрузка...</Button>
```

### Card

```tsx
import { Card } from './components/Card';

<Card variant="gradient" padding="lg" title="Заголовок">
  Содержимое с тёплым градиентом
</Card>

<Card variant="glass" headerAction={<Button>Действие</Button>}>
  Стеклянная карточка
</Card>
```

### Input

```tsx
import { Input } from './components/Input';

<Input 
  label="Email"
  type="email"
  placeholder="your@email.com"
  helperText="Мы никому не скажем"
/>

<Input 
  label="Пароль"
  type="password"
  isPassword
  error="Минимум 8 символов"
/>
```

### Badge

```tsx
import { Badge, StatusBadge } from './components/Badge';

<Badge variant="success" dot>Активен</Badge>
<Badge variant="gradient">Pro</Badge>
<Badge variant="glow">New</Badge>

// Удобные алиасы
<StatusBadge.Active>Работает</StatusBadge.Active>
<StatusBadge.Pending>Ожидание</StatusBadge.Pending>
```

## 🌺 Deya Touch

Принципы дизайна от Деи:

- **20px скругление** — мягкие формы
- **Тёплые градиенты** — закат, океан
- **Воздух** — generous whitespace
- **Плавность** — transitions 300ms
- **Тёплый свет** — не неон

Подробнее в `deya-touch.md`

## 🎯 Что понимает генератор

### Типы компонентов
- `button` — кнопки
- `card` — карточки
- `input` — поля ввода
- `badge` — бейджи

### Варианты
- **primary, secondary, outline, danger, ghost**
- **gradient** — тёплый градиент
- **glass** — glassmorphism

### Размеры
- **sm, md, lg, xl**

### Формы
- **rounded** — стандартное
- **pill** — пилюля
- **soft** — 20px (Deya style)

## 📊 Примеры генерации

```bash
# Кнопка с градиентом и анимацией
$ python3 code-generator.py "кнопка градиентная, большая, с анимацией"
→ Button с gradient, lg, hover:scale-105

# Карточка с тенью
$ python3 code-generator.py "карточка с тенью, мягкая"
→ Card с shadow-md, rounded-[20px]

# Поле для email с ошибкой
$ python3 code-generator.py "поле ввода email, с ошибкой"
→ Input с type="email", error state
```

## 🔧 Дизайн-токены

```css
/* Цвета */
--primary: #3b82f6
--secondary: #8b5cf6
--accent: #7c3aed
--dark: #0d0d12

/* Градиенты */
--gradient-sunset: linear-gradient(135deg, #f59e0b, #ec4899, #8b5cf6)
--gradient-ocean: linear-gradient(135deg, #0ea5e9, #3b82f6)

/* Радиусы */
--radius-soft: 20px
```

## 📁 Структура

```
ui-ux-pro-max/
├── scripts/
│   └── code-generator.py      # ⭐ Генератор
├── assets/
│   ├── components/            # Готовые компоненты
│   │   ├── Button.tsx
│   │   ├── Card.tsx
│   │   ├── Input.tsx
│   │   └── Badge.tsx
│   └── canvas-preview.html    # Визуальный превью
├── references/
│   └── deya-touch.md          # Принципы вайба
└── README.md                  # Этот файл
```

## 🚧 Roadmap

- [x] code-generator.py
- [x] Button, Card, Input, Badge
- [x] canvas-preview.html
- [x] deya-touch.md
- [ ] figma-export.py
- [ ] a11y-check.py
- [ ] Framer Motion анимации

## 💬 Связь

- Канал: @dayanrouter
- Бот: @ai_router_support_bot
- Сайт: go.airouter.host

---

Сгенерировано с теплом и кокосовым рафом ☕🌺
