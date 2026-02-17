# Architecture Technique — [NOM_PROJET]

> Ce document décrit la structure technique complète du projet.
> Toute modification d'architecture doit être reflétée ici.

---

## Vue d'ensemble

### Diagramme d'architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         FRONTEND                                 │
│                      (Vercel Edge)                               │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                    Next.js 14                            │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐              │    │
│  │  │  Pages   │  │Components│  │  Hooks   │              │    │
│  │  └────┬─────┘  └──────────┘  └──────────┘              │    │
│  │       │                                                  │    │
│  │       ▼                                                  │    │
│  │  ┌──────────────────────────────────────┐              │    │
│  │  │         Supabase Client (Auth)        │              │    │
│  │  └──────────────────────────────────────┘              │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ HTTPS
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                         BACKEND                                  │
│                       (Railway)                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                    FastAPI                               │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐              │    │
│  │  │   API    │  │ Services │  │  Models  │              │    │
│  │  └────┬─────┘  └────┬─────┘  └──────────┘              │    │
│  │       │             │                                    │    │
│  │       ▼             ▼                                    │    │
│  │  ┌──────────────────────────────────────┐              │    │
│  │  │              Celery Tasks             │◄─── Redis    │    │
│  │  └──────────────────────────────────────┘              │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │
          ┌───────────────────┼───────────────────┐
          │                   │                   │
          ▼                   ▼                   ▼
    ┌──────────┐       ┌──────────┐       ┌──────────┐
    │ Supabase │       │  Claude  │       │  Stripe  │
    │    DB    │       │   API    │       │   API    │
    └──────────┘       └──────────┘       └──────────┘
```

---

## Stack technique détaillé

### Backend

| Composant | Technologie | Version | Rôle |
|-----------|-------------|---------|------|
| Framework | FastAPI | 0.109.x | API REST |
| Runtime | Python | 3.12.x | Langage |
| Task Queue | Celery | 5.3.x | Jobs async |
| Broker | Redis | 7.x | Message broker |
| ORM/Client | Supabase-py | 2.x | Accès DB |
| Validation | Pydantic | 2.x | Schemas |
| HTTP Client | httpx | 0.27.x | Appels externes |
| Logging | structlog | 24.x | Logs structurés |

### Frontend

| Composant | Technologie | Version | Rôle |
|-----------|-------------|---------|------|
| Framework | Next.js | 14.2.x | React framework |
| Runtime | Node.js | 20.x | Runtime |
| Language | TypeScript | 5.4.x | Typage |
| CSS | Tailwind CSS | 3.4.x | Styling |
| UI Components | shadcn/ui | latest | Primitives UI |
| Forms | React Hook Form | 7.x | Gestion forms |
| Validation | Zod | 3.x | Validation schemas |
| State | Zustand | 4.x | State management |
| HTTP | fetch / SWR | native/2.x | Data fetching |

### Infrastructure

| Service | Provider | Usage |
|---------|----------|-------|
| Database | Supabase | PostgreSQL + Auth + Storage |
| Backend hosting | Railway | FastAPI + Celery workers |
| Frontend hosting | Vercel | Next.js SSR/SSG |
| Redis | Railway | Celery broker + cache |
| CDN | Vercel Edge | Assets statiques |
| DNS | [Porkbun/Cloudflare] | Domaine |
| Monitoring | Sentry | Error tracking |
| LLM Monitoring | LangSmith | Traces LLM |

---

## Schéma de base de données

### Tables

#### users (géré par Supabase Auth)

```sql
-- Table gérée automatiquement par Supabase Auth
-- On y accède via auth.users()
-- Données custom dans public.profiles
```

#### profiles

```sql
CREATE TABLE profiles (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    email VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    avatar_url TEXT,
    
    -- Subscription
    stripe_customer_id VARCHAR(255) UNIQUE,
    subscription_status VARCHAR(50) DEFAULT 'free',
    subscription_tier VARCHAR(50),
    subscription_current_period_end TIMESTAMPTZ,
    
    -- Usage
    credits_remaining INTEGER DEFAULT 0,
    
    -- Metadata
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_profiles_stripe_customer ON profiles(stripe_customer_id);
CREATE INDEX idx_profiles_subscription_status ON profiles(subscription_status);

-- RLS
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own profile"
    ON profiles FOR SELECT
    USING (auth.uid() = id);

CREATE POLICY "Users can update own profile"
    ON profiles FOR UPDATE
    USING (auth.uid() = id);
```

#### [TABLE_MÉTIER_1]

```sql
CREATE TABLE [nom_table] (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    
    -- Champs métier
    [champ_1] [TYPE] [CONSTRAINTS],
    [champ_2] [TYPE] [CONSTRAINTS],
    
    -- Status
    status VARCHAR(50) DEFAULT 'pending',
    
    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_[table]_user_id ON [nom_table](user_id);
CREATE INDEX idx_[table]_status ON [nom_table](status);
CREATE INDEX idx_[table]_created_at ON [nom_table](created_at DESC);

-- RLS
ALTER TABLE [nom_table] ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own [table]"
    ON [nom_table] FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own [table]"
    ON [nom_table] FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own [table]"
    ON [nom_table] FOR UPDATE
    USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own [table]"
    ON [nom_table] FOR DELETE
    USING (auth.uid() = user_id);
```

### Diagramme relations

```
profiles
    │
    ├──< [table_1] (1:N)
    │       │
    │       └──< [table_1_details] (1:N)
    │
    └──< [table_2] (1:N)
```

### Migrations

Voir `docs/MIGRATIONS.md` pour la stratégie et l'historique.

---

## API Endpoints

### Convention

- Base URL: `https://api.[domain].com/api/v1`
- Auth: Bearer token (Supabase JWT)
- Format: JSON
- Errors: Format standardisé (voir ERRORS.md)

### Endpoints

#### Auth (via Supabase - pas de backend custom)

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| - | - | Géré par Supabase Client | - |

#### Profiles

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/profiles/me` | Profil utilisateur courant | Required |
| PATCH | `/profiles/me` | Update profil | Required |

**GET /profiles/me**

Response:
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "email": "user@example.com",
    "full_name": "John Doe",
    "subscription_status": "active",
    "subscription_tier": "pro",
    "credits_remaining": 100
  }
}
```

#### [Feature 1]

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/[resource]` | Créer [resource] | Required |
| GET | `/[resource]` | Liste [resources] | Required |
| GET | `/[resource]/{id}` | Détail [resource] | Required |
| PATCH | `/[resource]/{id}` | Update [resource] | Required |
| DELETE | `/[resource]/{id}` | Supprimer [resource] | Required |

**POST /[resource]**

Request:
```json
{
  "field_1": "value",
  "field_2": "value"
}
```

Response (201):
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "field_1": "value",
    "field_2": "value",
    "status": "pending",
    "created_at": "2024-01-15T10:30:00Z"
  }
}
```

**GET /[resource]**

Query params:
- `page` (int, default: 1)
- `limit` (int, default: 20, max: 100)
- `status` (string, optional)
- `sort` (string, default: "-created_at")

Response:
```json
{
  "success": true,
  "data": [...],
  "meta": {
    "page": 1,
    "limit": 20,
    "total": 150,
    "total_pages": 8
  }
}
```

#### Webhooks

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/webhooks/stripe` | Stripe events | Stripe signature |

---

## Structure des dossiers

### Backend

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Point d'entrée FastAPI
│   ├── config.py               # Settings (Pydantic BaseSettings)
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py             # Dépendances (get_current_user, etc.)
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── router.py       # Router principal v1
│   │       └── endpoints/
│   │           ├── __init__.py
│   │           ├── profiles.py
│   │           ├── [feature].py
│   │           └── webhooks.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── security.py         # JWT validation, auth helpers
│   │   ├── errors.py           # Exceptions custom + handlers
│   │   └── logging.py          # Config structlog
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   └── [domain].py         # Modèles DB (si ORM, sinon skip)
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── common.py           # Schemas partagés (Response, Error)
│   │   ├── profile.py
│   │   └── [feature].py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── supabase.py         # Client Supabase singleton
│   │   ├── stripe_service.py   # Logique Stripe
│   │   ├── llm_service.py      # Appels Claude/OpenAI
│   │   └── [feature]_service.py
│   │
│   └── workers/
│       ├── __init__.py
│       ├── celery.py           # Config Celery
│       └── tasks/
│           ├── __init__.py
│           └── [feature]_tasks.py
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── test_[feature].py
│
├── .env.example
├── requirements.txt
├── pyproject.toml
└── Dockerfile
```

### Frontend

```
frontend/
├── src/
│   ├── app/
│   │   ├── layout.tsx          # Root layout
│   │   ├── page.tsx            # Landing page
│   │   ├── globals.css
│   │   │
│   │   ├── (auth)/             # Auth group (layout partagé)
│   │   │   ├── layout.tsx
│   │   │   ├── login/
│   │   │   │   └── page.tsx
│   │   │   ├── register/
│   │   │   │   └── page.tsx
│   │   │   └── forgot-password/
│   │   │       └── page.tsx
│   │   │
│   │   ├── (dashboard)/        # Dashboard group (auth required)
│   │   │   ├── layout.tsx
│   │   │   ├── dashboard/
│   │   │   │   └── page.tsx
│   │   │   ├── [feature]/
│   │   │   │   └── page.tsx
│   │   │   └── settings/
│   │   │       ├── page.tsx
│   │   │       └── billing/
│   │   │           └── page.tsx
│   │   │
│   │   ├── (marketing)/        # Marketing pages (public)
│   │   │   ├── layout.tsx
│   │   │   ├── pricing/
│   │   │   │   └── page.tsx
│   │   │   └── about/
│   │   │       └── page.tsx
│   │   │
│   │   └── api/                # Route handlers
│   │       └── webhooks/
│   │           └── stripe/
│   │               └── route.ts
│   │
│   ├── components/
│   │   ├── ui/                 # Primitives (shadcn)
│   │   │   ├── button.tsx
│   │   │   ├── input.tsx
│   │   │   └── ...
│   │   ├── forms/
│   │   │   ├── login-form.tsx
│   │   │   └── [feature]-form.tsx
│   │   ├── layouts/
│   │   │   ├── header.tsx
│   │   │   ├── sidebar.tsx
│   │   │   └── footer.tsx
│   │   └── shared/
│   │       ├── loading.tsx
│   │       ├── error-boundary.tsx
│   │       └── empty-state.tsx
│   │
│   ├── lib/
│   │   ├── supabase/
│   │   │   ├── client.ts       # Browser client
│   │   │   ├── server.ts       # Server client
│   │   │   └── middleware.ts   # Auth middleware
│   │   ├── api.ts              # Fetch wrapper vers backend
│   │   ├── utils.ts            # Helpers (cn, formatDate, etc.)
│   │   └── constants.ts
│   │
│   ├── hooks/
│   │   ├── use-auth.ts
│   │   ├── use-profile.ts
│   │   └── use-[feature].ts
│   │
│   ├── types/
│   │   ├── index.ts
│   │   ├── api.ts              # Types réponses API
│   │   └── [feature].ts
│   │
│   └── stores/                 # Zustand stores (si besoin)
│       └── [feature]-store.ts
│
├── public/
│   ├── favicon.ico
│   ├── og-image.png
│   └── robots.txt
│
├── .env.example
├── tailwind.config.ts
├── tsconfig.json
├── next.config.js
└── package.json
```

---

## Authentification

### Flow

```
1. Frontend: Supabase Auth (signUp, signIn, signOut)
2. Frontend: Obtient JWT via supabase.auth.getSession()
3. Frontend: Envoie JWT dans header Authorization: Bearer <token>
4. Backend: Valide JWT via Supabase (verify)
5. Backend: Extrait user_id du JWT
6. Backend: Utilise user_id pour RLS et requêtes
```

### Validation JWT (Backend)

```python
# app/api/deps.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.services.supabase import supabase_client

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    token = credentials.credentials
    
    try:
        user = supabase_client.auth.get_user(token)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        return user.user
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
```

---

## Jobs asynchrones (Celery)

### Configuration

```python
# app/workers/celery.py
from celery import Celery
from app.config import settings

celery_app = Celery(
    "worker",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["app.workers.tasks"]
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=300,  # 5 minutes max
    worker_prefetch_multiplier=1,
)
```

### Pattern de task

```python
# app/workers/tasks/[feature]_tasks.py
from app.workers.celery import celery_app
from app.services.supabase import supabase_client

@celery_app.task(bind=True, max_retries=3)
def process_[feature](self, item_id: str):
    try:
        # 1. Récupérer données
        # 2. Traitement
        # 3. Update DB
        # 4. Return result
        pass
    except Exception as exc:
        # Retry avec backoff exponentiel
        self.retry(exc=exc, countdown=2 ** self.request.retries)
```

---

## Intégrations externes

### Claude API

```python
# app/services/llm_service.py
import anthropic
from app.config import settings

client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)

async def generate_analysis(prompt: str, context: str) -> str:
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=[
            {"role": "user", "content": f"{context}\n\n{prompt}"}
        ]
    )
    return message.content[0].text
```

### Stripe

Voir `stripe-templates/STRIPE-SETUP.md` pour le détail.

---

## Performance

### Caching

| Donnée | TTL | Stratégie |
|--------|-----|-----------|
| Profile user | 5 min | Cache Redis, invalidate on update |
| [Donnée] | [TTL] | [Stratégie] |

### Rate limiting

| Endpoint | Limite | Fenêtre |
|----------|--------|---------|
| `/api/*` (auth) | 100 req | 1 minute |
| `/api/*` (anon) | 20 req | 1 minute |
| `/webhooks/*` | 1000 req | 1 minute |

---

## Sécurité

Voir `docs/SECURITY.md` pour le détail complet.

---

## Monitoring

Voir `docs/MONITORING.md` pour le détail complet.
