# [NOM_PROJET]

> [À_COMPLÉTER : Une phrase d'accroche qui décrit ce que fait le produit]

---

## Le Problème

[À_COMPLÉTER : 2-3 phrases décrivant le problème que le produit résout. Concret, douloureux, relatable.]

## La Solution

[À_COMPLÉTER : 2-3 phrases décrivant comment le produit résout ce problème. Clair, concis, orienté résultat.]

```
[Schéma simplifié du flow principal]
Utilisateur → [Action] → [NOM_PROJET] → [Résultat]
```

---

## Quick Start

### Prérequis

- Python 3.12+
- Node.js 20+
- Redis
- Compte Supabase
- [Autres prérequis spécifiques]

### 1. Database

1. Créer un projet Supabase sur [supabase.com](https://supabase.com)
2. Exécuter le schéma dans SQL Editor :
   ```bash
   # Copier le contenu de database/schema.sql
   ```

### 2. Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Éditer .env avec vos valeurs
uvicorn app.main:app --reload --port 8000
```

### 3. Frontend

```bash
cd frontend
npm install
cp .env.example .env.local
# Éditer .env.local
npm run dev
```

### 4. Celery Worker

```bash
cd backend
celery -A app.workers.celery worker --loglevel=info
```

---

## Stack technique

| Couche | Technologie |
|--------|-------------|
| Backend | FastAPI + Python 3.12 |
| Frontend | Next.js 14 + TypeScript + Tailwind |
| Database | Supabase PostgreSQL |
| Auth | Supabase Auth |
| Queue | Celery + Redis |
| Paiement | Stripe |
| IA/LLM | [Claude API / OpenAI / Aucun] |
| Hosting Backend | Railway |
| Hosting Frontend | Vercel |
| Monitoring | Sentry |
| Email | Brevo |

---

## Structure du projet

```
[NOM_PROJET]/
├── CLAUDE.md              # Instructions Claude Code
├── context.md             # Contexte projet & business
├── README.md              # Ce fichier
│
├── docs/
│   ├── SPEC.md            # Spécifications fonctionnelles
│   ├── ARCH.md            # Architecture technique & schéma DB
│   ├── API.md             # Documentation API REST
│   ├── SECURITY.md        # Sécurité
│   ├── ERRORS.md          # Catalogue erreurs
│   ├── UI.md              # Design system
│   ├── COPY.md            # Textes UI
│   ├── TESTS.md           # Stratégie tests
│   ├── DEPLOY.md          # Guide déploiement
│   ├── MONITORING.md      # Monitoring & alertes
│   ├── ANALYTICS.md       # Analytics & métriques
│   ├── MIGRATIONS.md      # Migrations DB
│   ├── BACKUP.md          # Stratégie backup
│   ├── EMAILS.md          # Emails transactionnels
│   ├── PRICING.md         # Pricing & plans
│   ├── ONBOARDING.md      # Parcours utilisateur
│   ├── PERFORMANCE.md     # Performance & optimisation
│   ├── ENV.md             # Variables d'environnement
│   ├── ROADMAP.md         # Évolutions prévues
│   ├── TASKS.md           # Tâches & avancement
│   └── CHANGELOG.md       # Historique versions
│
├── database/
│   ├── schema.sql         # Schéma Supabase
│   └── seed.sql           # Données de dev
│
├── backend/
│   ├── app/
│   │   ├── api/v1/endpoints/   # Routes API
│   │   ├── core/               # Config, logging, security
│   │   ├── services/           # Business logic
│   │   ├── workers/tasks/      # Celery tasks
│   │   └── models/             # Pydantic models
│   ├── tests/
│   ├── requirements.txt
│   ├── Dockerfile
│   └── railway.toml
│
├── frontend/
│   ├── src/
│   │   ├── app/           # Next.js App Router
│   │   ├── components/    # React components
│   │   └── lib/           # Utils, API client, types
│   ├── package.json
│   └── vercel.json
│
└── .github/
    └── workflows/
        └── ci.yml         # CI/CD pipeline
```

---

## Déploiement

### Backend (Railway)
1. Connecter le repo à Railway
2. Configurer les variables d'environnement depuis `.env.example`
3. Deploy

### Frontend (Vercel)
1. Connecter le repo à Vercel
2. Root directory : `frontend`
3. Configurer les variables d'environnement
4. Deploy

Voir [docs/DEPLOY.md](docs/DEPLOY.md) pour le guide complet.

---

## Documentation

| Document | Description |
|----------|-------------|
| [context.md](./context.md) | Vision, business model, décisions |
| [CLAUDE.md](./CLAUDE.md) | Instructions Claude Code |
| [docs/SPEC.md](./docs/SPEC.md) | Spécifications fonctionnelles |
| [docs/ARCH.md](./docs/ARCH.md) | Architecture technique |
| [docs/API.md](./docs/API.md) | Documentation API REST |
| [docs/PRICING.md](./docs/PRICING.md) | Pricing & plans Stripe |
| [docs/DEPLOY.md](./docs/DEPLOY.md) | Guide de déploiement |
| [docs/ENV.md](./docs/ENV.md) | Variables d'environnement |

---

## License

[MIT / Proprietary — À définir]

---

## Liens

| | |
|---|---|
| **Website** | [nom-projet.com](https://nom-projet.com) |
| **API** | [api.nom-projet.com](https://api.nom-projet.com) |
| **Status** | [status.nom-projet.com](https://status.nom-projet.com) |
