# UI & Design System — [NOM_PROJET]

> Ce document définit tous les éléments visuels, composants et leurs états.
> Référence pour le développement frontend et pour assurer la cohérence.

---

## Design tokens

### Couleurs

```css
/* Brand */
--color-primary: #[HEX];        /* Actions principales */
--color-primary-hover: #[HEX];
--color-primary-active: #[HEX];

--color-secondary: #[HEX];      /* Actions secondaires */
--color-secondary-hover: #[HEX];

/* Feedback */
--color-success: #22C55E;       /* Succès, validé */
--color-warning: #F59E0B;       /* Attention */
--color-error: #EF4444;         /* Erreur */
--color-info: #3B82F6;          /* Information */

/* Neutrals */
--color-background: #FFFFFF;
--color-surface: #F9FAFB;
--color-border: #E5E7EB;
--color-text-primary: #111827;
--color-text-secondary: #6B7280;
--color-text-muted: #9CA3AF;
--color-text-inverse: #FFFFFF;

/* Dark mode (si applicable) */
--color-background-dark: #111827;
--color-surface-dark: #1F2937;
--color-border-dark: #374151;
--color-text-primary-dark: #F9FAFB;
```

### Typography

```css
/* Font family */
--font-sans: 'Inter', system-ui, sans-serif;
--font-mono: 'JetBrains Mono', monospace;

/* Font sizes */
--text-xs: 0.75rem;     /* 12px */
--text-sm: 0.875rem;    /* 14px */
--text-base: 1rem;      /* 16px */
--text-lg: 1.125rem;    /* 18px */
--text-xl: 1.25rem;     /* 20px */
--text-2xl: 1.5rem;     /* 24px */
--text-3xl: 1.875rem;   /* 30px */
--text-4xl: 2.25rem;    /* 36px */

/* Font weights */
--font-normal: 400;
--font-medium: 500;
--font-semibold: 600;
--font-bold: 700;

/* Line heights */
--leading-tight: 1.25;
--leading-normal: 1.5;
--leading-relaxed: 1.75;
```

### Spacing

```css
/* Base unit: 4px */
--space-1: 0.25rem;     /* 4px */
--space-2: 0.5rem;      /* 8px */
--space-3: 0.75rem;     /* 12px */
--space-4: 1rem;        /* 16px */
--space-5: 1.25rem;     /* 20px */
--space-6: 1.5rem;      /* 24px */
--space-8: 2rem;        /* 32px */
--space-10: 2.5rem;     /* 40px */
--space-12: 3rem;       /* 48px */
--space-16: 4rem;       /* 64px */
--space-20: 5rem;       /* 80px */
```

### Border radius

```css
--radius-none: 0;
--radius-sm: 0.25rem;   /* 4px */
--radius-md: 0.375rem;  /* 6px */
--radius-lg: 0.5rem;    /* 8px */
--radius-xl: 0.75rem;   /* 12px */
--radius-2xl: 1rem;     /* 16px */
--radius-full: 9999px;
```

### Shadows

```css
--shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
--shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);
--shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1);
--shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.1);
```

---

## Breakpoints

| Nom | Min-width | Usage |
|-----|-----------|-------|
| `sm` | 640px | Mobile landscape |
| `md` | 768px | Tablet |
| `lg` | 1024px | Desktop |
| `xl` | 1280px | Large desktop |
| `2xl` | 1536px | Ultra wide |

### Approche

- **Mobile-first** : Styles par défaut pour mobile
- Media queries pour élargir, pas rétrécir

---

## Composants UI

### Button

#### Variants

| Variant | Usage |
|---------|-------|
| `primary` | Action principale (1 par écran max) |
| `secondary` | Actions secondaires |
| `outline` | Actions tertiaires |
| `ghost` | Actions subtiles (nav, icônes) |
| `destructive` | Actions dangereuses (suppression) |
| `link` | Navigation inline |

#### Sizes

| Size | Height | Padding | Font |
|------|--------|---------|------|
| `sm` | 32px | 12px 16px | 14px |
| `md` | 40px | 16px 20px | 14px |
| `lg` | 48px | 20px 24px | 16px |

#### États

| État | Apparence |
|------|-----------|
| Default | Couleur normale |
| Hover | Couleur -10% luminosité |
| Active/Pressed | Couleur -20% luminosité |
| Focus | Ring 2px offset 2px |
| Disabled | Opacity 50%, cursor not-allowed |
| Loading | Spinner + texte "Chargement..." |

```tsx
// Exemples d'utilisation
<Button variant="primary" size="md">Créer</Button>
<Button variant="secondary" size="sm">Annuler</Button>
<Button variant="destructive" size="md">Supprimer</Button>
<Button variant="ghost" size="sm"><Icon /></Button>
<Button disabled>Désactivé</Button>
<Button loading>Chargement...</Button>
```

---

### Input

#### Types

- Text, Email, Password, Number, Tel, URL
- Textarea
- Select
- Checkbox, Radio
- Switch/Toggle
- Date picker

#### États

| État | Apparence |
|------|-----------|
| Default | Border gray-300 |
| Hover | Border gray-400 |
| Focus | Border primary, ring |
| Error | Border red-500, message erreur |
| Disabled | Background gray-100, cursor not-allowed |
| Read-only | Background gray-50 |

#### Anatomie

```
┌─────────────────────────────────────┐
│ Label *                             │  ← Label (requis si required)
├─────────────────────────────────────┤
│ ┌─────────────────────────────────┐ │
│ │ Placeholder / Value             │ │  ← Input
│ └─────────────────────────────────┘ │
│ Helper text ou message d'erreur     │  ← Description
└─────────────────────────────────────┘
```

```tsx
<Input
  label="Email"
  type="email"
  placeholder="vous@exemple.com"
  error="Format email invalide"
  required
/>
```

---

### Card

```
┌─────────────────────────────────────┐
│ Header (optionnel)                  │
├─────────────────────────────────────┤
│                                     │
│ Content                             │
│                                     │
├─────────────────────────────────────┤
│ Footer (optionnel)                  │
└─────────────────────────────────────┘
```

- Border radius: lg
- Shadow: sm (hover: md)
- Padding: 24px

---

### Toast / Notification

#### Types

| Type | Icône | Couleur |
|------|-------|---------|
| Success | ✓ Check | Green |
| Error | ✕ X | Red |
| Warning | ⚠ Alert | Yellow |
| Info | ℹ Info | Blue |

#### Comportement

- Position: Top-right
- Duration: 5s (success/info), 8s (warning), persistent (error with action)
- Stacking: Max 3 visibles, FIFO
- Dismissable: Click X ou swipe

---

### Modal / Dialog

#### Sizes

| Size | Width |
|------|-------|
| `sm` | 400px |
| `md` | 500px |
| `lg` | 600px |
| `xl` | 800px |
| `full` | 100% - 40px margin |

#### Anatomie

```
┌─────────────────────────────────────┐
│ [X]                    Title        │  ← Header avec close
├─────────────────────────────────────┤
│                                     │
│ Content                             │
│                                     │
├─────────────────────────────────────┤
│              [Cancel] [Confirm]     │  ← Footer actions
└─────────────────────────────────────┘
```

#### Comportement

- Backdrop: Click ferme (sauf si `persistent`)
- Escape: Ferme
- Focus trap: Oui
- Scroll: Body scroll lock

---

### Table

#### Fonctionnalités

- [ ] Sorting (click header)
- [ ] Pagination
- [ ] Selection (checkbox)
- [ ] Row actions
- [ ] Empty state
- [ ] Loading state

#### États lignes

| État | Apparence |
|------|-----------|
| Default | Background transparent |
| Hover | Background gray-50 |
| Selected | Background primary-50 |
| Disabled | Opacity 50% |

---

### Empty states

Chaque liste/table doit avoir un empty state défini :

```
┌─────────────────────────────────────┐
│                                     │
│            [Illustration]           │
│                                     │
│         Aucun [élément] trouvé      │
│                                     │
│     Description contextuelle        │
│                                     │
│          [Action primaire]          │
│                                     │
└─────────────────────────────────────┘
```

---

### Loading states

#### Skeleton

- Utiliser pour le chargement initial de contenu
- Même dimensions que le contenu final
- Animation: pulse

#### Spinner

- Utiliser pour actions (boutons, refresh)
- Sizes: sm (16px), md (24px), lg (32px)

#### Progress

- Utiliser pour uploads, processus longs
- Determinate (pourcentage connu) ou indeterminate

---

## Pages

### Page structure commune

```
┌─────────────────────────────────────────────────────────────┐
│ Header / Navbar                                             │
├─────────────────────────────────────────────────────────────┤
│ ┌─────────┐ ┌─────────────────────────────────────────────┐ │
│ │         │ │                                             │ │
│ │ Sidebar │ │ Main content                                │ │
│ │         │ │                                             │ │
│ │         │ │ ┌─────────────────────────────────────────┐ │ │
│ │         │ │ │ Page header (title + actions)           │ │ │
│ │         │ │ ├─────────────────────────────────────────┤ │ │
│ │         │ │ │                                         │ │ │
│ │         │ │ │ Page content                            │ │ │
│ │         │ │ │                                         │ │ │
│ │         │ │ └─────────────────────────────────────────┘ │ │
│ └─────────┘ └─────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### Pages à designer

| Page | Layout | États à prévoir |
|------|--------|-----------------|
| Landing | Marketing | - |
| Login | Auth (centered) | Default, Loading, Error |
| Register | Auth (centered) | Default, Loading, Error, Success |
| Dashboard | App (sidebar) | Loading, Empty, Populated |
| [Feature] | App (sidebar) | Loading, Empty, Error, Success |
| Settings | App (sidebar) | Default, Saving |
| Pricing | Marketing | - |
| 404 | Minimal | - |
| 500 | Minimal | - |

---

## Responsive behavior

### Navigation

| Breakpoint | Comportement |
|------------|--------------|
| Mobile (<768px) | Hamburger menu, sidebar hidden |
| Tablet (768-1024px) | Sidebar collapsed (icons only) |
| Desktop (>1024px) | Sidebar expanded |

### Grids

| Breakpoint | Colonnes |
|------------|----------|
| Mobile | 1 |
| Tablet | 2 |
| Desktop | 3-4 |

### Tables

| Breakpoint | Comportement |
|------------|--------------|
| Mobile | Cards ou scroll horizontal |
| Desktop | Table standard |

---

## Animations

### Durées

| Type | Durée | Easing |
|------|-------|--------|
| Micro (hover, focus) | 150ms | ease-out |
| Small (dropdown, tooltip) | 200ms | ease-out |
| Medium (modal, drawer) | 300ms | ease-in-out |
| Large (page transition) | 400ms | ease-in-out |

### Principes

- **Réduire le motion** : Respecter `prefers-reduced-motion`
- **Purpose** : Animation doit avoir un but (feedback, guide attention)
- **Subtile** : Pas de animations flashy ou distrayantes

---

## Accessibilité

### Checklist par composant

| Composant | Focus visible | Keyboard nav | ARIA | Contrast |
|-----------|---------------|--------------|------|----------|
| Button | ✅ | ✅ Enter/Space | role="button" | 4.5:1 |
| Input | ✅ | ✅ Tab | aria-label | 4.5:1 |
| Modal | ✅ | ✅ Esc, Tab trap | role="dialog" | - |
| Dropdown | ✅ | ✅ Arrow keys | role="menu" | 4.5:1 |
| Toast | - | ✅ Dismiss | role="alert" | 4.5:1 |

### Focus order

1. Skip to content link
2. Navigation
3. Main content (top to bottom, left to right)
4. Footer

---

## Assets

### Favicon

- favicon.ico (32x32)
- apple-touch-icon.png (180x180)
- favicon-32x32.png
- favicon-16x16.png

### OG Images

- og-image.png (1200x630)
- twitter-image.png (1200x600)

### Logo

- logo.svg (vecteur)
- logo-dark.svg (pour dark mode)
- logo-icon.svg (icône seule)

---

## Notes

[Espace pour notes spécifiques au projet]
