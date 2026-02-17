# Instructions Claude Code — [NOM_PROJET]

> Ce fichier est lu automatiquement par Claude Code à chaque session.
> Adapter les sections marquées [À_COMPLÉTER] avant de commencer le dev.

---

## Contexte projet

Lire `context.md` pour comprendre la vision et les décisions.
Lire `docs/SPEC.md` pour les spécifications fonctionnelles.
Lire `docs/ARCH.md` pour l'architecture technique.

---

## Stack technique

| Couche | Technologie | Version exacte |
|--------|-------------|----------------|
| Backend | FastAPI | 0.109.x |
| Python | Python | 3.12.x |
| Queue | Celery | 5.3.x |
| Cache/Broker | Redis | 7.x |
| Frontend | Next.js | 14.2.x |
| TypeScript | TypeScript | 5.4.x |
| CSS | Tailwind CSS | 3.4.x |
| Database | Supabase PostgreSQL | 15.x |
| Auth | Supabase Auth | - |
| Paiement | Stripe | API 2024-x |

---

## Commandes utiles

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# Worker Celery
celery -A app.workers.celery worker --loglevel=info

# Frontend
cd frontend
npm install
npm run dev

# Tests
cd backend && pytest
cd frontend && npm run test

# Lint
cd backend && ruff check .
cd frontend && npm run lint

# Build prod
cd frontend && npm run build
```

---

## Structure projet

```
[NOM_PROJET]/
├── CLAUDE.md                 ← Ce fichier
├── context.md                ← Vision & contexte
├── backend/
│   ├── app/
│   │   ├── main.py           ← Point d'entrée FastAPI
│   │   ├── config.py         ← Settings Pydantic
│   │   ├── api/
│   │   │   ├── deps.py       ← Dépendances injection
│   │   │   └── v1/
│   │   │       ├── router.py ← Router principal v1
│   │   │       └── endpoints/
│   │   ├── core/
│   │   │   ├── security.py   ← Auth, JWT
│   │   │   ├── errors.py     ← Exceptions custom
│   │   │   └── logging.py    ← Logger structuré
│   │   ├── models/           ← Pydantic models DB
│   │   ├── schemas/          ← Pydantic schemas API
│   │   ├── services/         ← Logique métier
│   │   └── workers/          ← Tasks Celery
│   ├── tests/
│   ├── .env.example
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── app/              ← App Router Next.js
│   │   ├── components/
│   │   ├── lib/
│   │   ├── hooks/
│   │   └── types/
│   ├── public/
│   ├── .env.example
│   └── package.json
└── docs/
    ├── SPEC.md
    ├── ARCH.md
    └── ...
```

---

## Conventions de code

### Python

```python
# ✅ Correct
def get_user_by_email(email: str) -> User | None:
    """Récupère un utilisateur par email.
    
    Args:
        email: Email de l'utilisateur.
        
    Returns:
        User si trouvé, None sinon.
    """
    pass

# ❌ Incorrect
def getUser(email):
    pass
```

- **Naming** : snake_case (variables, fonctions), PascalCase (classes)
- **Type hints** : Obligatoires sur toutes les fonctions
- **Docstrings** : Google style, obligatoires sur fonctions publiques
- **Imports** : Groupés (stdlib, third-party, local), triés alphabétiquement
- **Logging** : Utiliser `logger` du module `core.logging`, jamais `print()`

### TypeScript

```typescript
// ✅ Correct
interface UserProps {
  email: string;
  name: string;
  isActive?: boolean;
}

const UserCard: React.FC<UserProps> = ({ email, name, isActive = true }) => {
  return <div>{name}</div>;
};

// ❌ Incorrect
const UserCard = (props: any) => {
  return <div>{props.name}</div>;
};
```

- **Naming** : camelCase (variables, fonctions), PascalCase (composants, types, interfaces)
- **Types** : Jamais de `any`, utiliser `unknown` si vraiment nécessaire
- **Interfaces vs Types** : Préférer `interface` pour les objets
- **Exports** : Named exports préférés, default export pour les pages/layouts

### SQL / Supabase

```sql
-- ✅ Correct
CREATE TABLE user_reports (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    report_type VARCHAR(50) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index sur les colonnes de recherche fréquente
CREATE INDEX idx_user_reports_user_id ON user_reports(user_id);
```

- **Tables** : snake_case, pluriel
- **Colonnes** : snake_case
- **Timestamps** : Toujours `created_at` et `updated_at` avec TIMESTAMPTZ
- **IDs** : UUID par défaut
- **Foreign keys** : Toujours avec ON DELETE approprié

---

## Structure des réponses API

### Succès

```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "attribute": "value"
  },
  "meta": {
    "page": 1,
    "total": 100
  }
}
```

### Erreur

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Message user-friendly",
    "details": {
      "field": "email",
      "reason": "Format invalide"
    }
  }
}
```

### Codes HTTP

| Code | Usage |
|------|-------|
| 200 | Succès GET/PUT/PATCH |
| 201 | Succès POST (création) |
| 204 | Succès DELETE |
| 400 | Bad Request (input invalide) |
| 401 | Unauthorized (non authentifié) |
| 403 | Forbidden (pas les droits) |
| 404 | Not Found |
| 422 | Validation Error (Pydantic) |
| 429 | Too Many Requests (rate limit) |
| 500 | Internal Server Error |

---

## Gestion des erreurs

### Backend

```python
# Dans core/errors.py — exceptions custom
class AppException(Exception):
    def __init__(self, code: str, message: str, status_code: int = 400):
        self.code = code
        self.message = message
        self.status_code = status_code

# Utilisation
from app.core.errors import AppException

async def get_report(report_id: str):
    report = await fetch_report(report_id)
    if not report:
        raise AppException(
            code="REPORT_NOT_FOUND",
            message="Ce rapport n'existe pas",
            status_code=404
        )
    return report
```

### Frontend

```typescript
// Wrapper fetch avec gestion erreur
const response = await api.get<ReportResponse>('/reports/123');

if (!response.success) {
  // Afficher toast avec response.error.message
  toast.error(response.error.message);
  return;
}

// Utiliser response.data
```

---

## INTERDICTIONS ABSOLUES

⛔ **Ne JAMAIS faire :**

1. **Modifier les fichiers core sans demande explicite**
   - `core/security.py`
   - `core/errors.py`
   - `core/logging.py`

2. **Commit des secrets**
   - Clés API, tokens, mots de passe
   - Utiliser `.env` + `.env.example`

3. **Skip la validation des inputs**
   - Toujours valider avec Pydantic (backend)
   - Toujours valider avec Zod (frontend)

4. **Créer des fichiers hors structure**
   - Respecter l'arborescence définie
   - Demander si besoin d'un nouveau dossier

5. **Utiliser `any` en TypeScript**
   - Typer correctement ou utiliser `unknown`

6. **Console.log en production**
   - Utiliser le logger structuré

7. **Requêtes SQL directes**
   - Passer par le client Supabase
   - Utiliser les RLS policies

8. **Ignorer les edge cases**
   - Consulter ERRORS.md pour tous les cas
   - Implémenter le handling approprié

9. **Modifier le schéma DB sans migration**
   - Toujours créer une migration Supabase
   - Documenter dans MIGRATIONS.md

10. **Déployer sans tests**
    - Tests unitaires sur la logique métier
    - Tests E2E sur les flows critiques

---

## Workflow de développement

### Avant de coder

1. Vérifier que la tâche est dans TASKS.md
2. Lire la spec correspondante dans SPEC.md
3. Vérifier ARCH.md pour la structure
4. Consulter ERRORS.md pour les erreurs à gérer

### Pendant le code

1. Une tâche atomique à la fois
2. Respecter les conventions ci-dessus
3. Logger les opérations importantes
4. Gérer tous les cas d'erreur

### Après le code

1. Vérifier que ça lint sans erreur
2. Tester manuellement le flow
3. Marquer la tâche done dans TASKS.md

---

## Variables d'environnement requises

### Backend (.env)

```bash
# App
APP_ENV=development
APP_DEBUG=true
APP_SECRET_KEY=

# Supabase
SUPABASE_URL=
SUPABASE_ANON_KEY=
SUPABASE_SERVICE_KEY=

# Redis
REDIS_URL=redis://localhost:6379/0

# Stripe
STRIPE_SECRET_KEY=
STRIPE_WEBHOOK_SECRET=

# LLM
ANTHROPIC_API_KEY=
OPENAI_API_KEY=

# Monitoring
SENTRY_DSN=
LANGSMITH_API_KEY=
```

### Frontend (.env.local)

```bash
# Public (exposées au client)
NEXT_PUBLIC_APP_URL=http://localhost:3000
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=

# Server only
STRIPE_SECRET_KEY=
STRIPE_WEBHOOK_SECRET=
```

---

## Notes spécifiques au projet

[À_COMPLÉTER : Ajouter ici les règles/exceptions spécifiques à ce projet]
