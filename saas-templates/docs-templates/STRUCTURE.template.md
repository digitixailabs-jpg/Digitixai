# Structure du Projet — [NOM_PROJET]

> Ce document décrit l'organisation des fichiers et dossiers du projet.
> À mettre à jour quand la structure change significativement.

---

## Vue d'ensemble

```
[NOM_PROJET]/
├── backend/                    # API FastAPI + Workers
├── frontend/                   # App Next.js
├── database/                   # Schéma SQL + seeds
├── docs/                       # Documentation complète
├── .github/                    # CI/CD
├── context.md                  # 📌 Source de vérité
├── CLAUDE.md                   # Instructions Claude Code
├── README.md                   # Présentation projet
├── STRUCTURE.md                # Ce fichier
└── CHANGELOG.md                # Historique versions
```

---

## Backend

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Point d'entrée FastAPI
│   │
│   ├── api/
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── router.py       # Router principal v1
│   │       └── endpoints/      # Un fichier par ressource
│   │           ├── __init__.py
│   │           ├── auth.py     # /api/v1/auth/*
│   │           ├── users.py    # /api/v1/users/*
│   │           └── [ressource].py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py           # Settings (pydantic BaseSettings)
│   │   ├── logging.py          # Configuration logs structurés
│   │   ├── security.py         # Auth middleware, JWT, API keys
│   │   └── exceptions.py       # Exceptions custom
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── requests.py         # Pydantic models (input)
│   │   └── responses.py        # Pydantic models (output)
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── [service].py        # Un fichier par domaine métier
│   │   └── [service].py
│   │
│   ├── workers/
│   │   ├── __init__.py
│   │   ├── celery.py           # Configuration Celery
│   │   └── tasks/
│   │       ├── __init__.py
│   │       └── [task].py       # Un fichier par type de task
│   │
│   └── utils/
│       ├── __init__.py
│       └── [util].py
│
├── tests/
│   ├── conftest.py             # Fixtures pytest
│   ├── test_[module].py        # Tests unitaires
│   └── test_api/
│       └── test_[endpoint].py  # Tests d'intégration API
│
├── .env.example                # Variables d'environnement template
├── requirements.txt            # Dépendances Python
├── Dockerfile                  # Image Docker
└── railway.toml                # Config Railway
```

### Conventions Backend

| Règle | Convention |
|-------|-----------|
| 1 endpoint = 1 fichier | `endpoints/users.py` gère `/api/v1/users/*` |
| 1 service = 1 domaine | `services/billing.py` gère toute la logique paiement |
| 1 task = 1 fichier | `tasks/send_email.py` gère l'envoi d'emails |
| Models séparés | `requests.py` (input) et `responses.py` (output) |
| Config centralisée | Tout dans `core/config.py` via pydantic BaseSettings |

---

## Frontend

```
frontend/
├── src/
│   ├── app/                    # Next.js App Router
│   │   ├── layout.tsx          # Layout racine
│   │   ├── page.tsx            # Landing page (/)
│   │   ├── (auth)/             # Group routes auth
│   │   │   ├── login/page.tsx
│   │   │   ├── register/page.tsx
│   │   │   └── forgot-password/page.tsx
│   │   ├── (dashboard)/        # Group routes dashboard
│   │   │   ├── layout.tsx      # Layout dashboard (sidebar, nav)
│   │   │   ├── dashboard/page.tsx
│   │   │   └── settings/
│   │   │       ├── page.tsx
│   │   │       └── billing/page.tsx
│   │   └── api/                # API routes Next.js (si nécessaire)
│   │
│   ├── components/
│   │   ├── ui/                 # Composants shadcn/ui
│   │   ├── layout/             # Header, Footer, Sidebar, Nav
│   │   ├── forms/              # Composants de formulaire
│   │   └── [feature]/          # Composants par feature
│   │
│   ├── lib/
│   │   ├── api-client.ts       # Client API (fetch wrapper)
│   │   ├── supabase.ts         # Client Supabase
│   │   ├── stripe.ts           # Utils Stripe
│   │   ├── utils.ts            # Helpers génériques
│   │   └── types.ts            # Types TypeScript partagés
│   │
│   ├── hooks/
│   │   ├── use-auth.ts         # Hook authentification
│   │   └── use-[feature].ts    # Hooks custom par feature
│   │
│   └── styles/
│       └── globals.css         # Styles globaux + Tailwind
│
├── public/
│   ├── favicon.ico
│   ├── og-image.png            # Image Open Graph
│   └── [assets statiques]
│
├── .env.example                # Variables d'environnement template
├── next.config.js              # Config Next.js
├── tailwind.config.ts          # Config Tailwind
├── tsconfig.json               # Config TypeScript
├── package.json
└── vercel.json                 # Config Vercel
```

### Conventions Frontend

| Règle | Convention |
|-------|-----------|
| Fichiers composants | kebab-case : `user-card.tsx` |
| Composants | PascalCase : `UserCard` |
| Hooks | camelCase avec préfixe `use` : `useAuth` |
| Types | PascalCase : `UserProfile` |
| Route groups | Parenthèses : `(auth)`, `(dashboard)` |
| Composants UI | Dans `components/ui/` (shadcn) |
| Composants métier | Dans `components/[feature]/` |

---

## Database

```
database/
├── schema.sql                  # Schéma complet (tables, RLS, functions)
├── seed.sql                    # Données de test/dev
└── migrations/                 # Migrations ordonnées (si hors Supabase)
    ├── 001_initial.sql
    ├── 002_[description].sql
    └── ...
```

---

## Documentation

```
docs/
├── SPEC.md                     # Spécifications fonctionnelles
├── ARCH.md                     # Architecture technique + schéma DB
├── API.md                      # Documentation API REST
├── SECURITY.md                 # Sécurité, auth, validation
├── ERRORS.md                   # Catalogue codes d'erreur
├── UI.md                       # Design system, composants
├── COPY.md                     # Textes UI (microcopy)
├── TESTS.md                    # Stratégie de tests
├── DEPLOY.md                   # Guide de déploiement
├── MONITORING.md               # Monitoring & alertes
├── ANALYTICS.md                # Events tracking
├── MIGRATIONS.md               # Stratégie migrations DB
├── BACKUP.md                   # Backup & restore
├── EMAILS.md                   # Emails transactionnels
├── PRICING.md                  # Pricing & plans Stripe
├── ONBOARDING.md               # Parcours utilisateur
├── PERFORMANCE.md              # Performance & optimisation
├── ENV.md                      # Variables d'environnement
├── ROADMAP.md                  # Évolutions futures
├── TASKS.md                    # Tâches & avancement
└── CHANGELOG.md                # Historique des versions
```

### Ordre de lecture recommandé

1. `context.md` → Pourquoi ce projet existe
2. `CLAUDE.md` → Comment travailler dessus
3. `SPEC.md` → Ce que le produit fait
4. `ARCH.md` → Comment c'est construit
5. Le reste selon le besoin

---

## CI/CD

```
.github/
└── workflows/
    ├── ci.yml                  # Tests + lint sur chaque PR
    ├── deploy-staging.yml      # Deploy staging sur push develop
    └── deploy-prod.yml         # Deploy prod sur push main
```

---

## Fichiers racine

| Fichier | Rôle |
|---------|------|
| `context.md` | 📌 Source de vérité — vision, décisions, schéma DB, API |
| `CLAUDE.md` | Instructions pour Claude Code |
| `README.md` | Présentation projet, quick start, liens |
| `STRUCTURE.md` | Ce fichier — organisation du code |
| `CHANGELOG.md` | Historique des versions |
| `.gitignore` | Fichiers exclus de Git |
