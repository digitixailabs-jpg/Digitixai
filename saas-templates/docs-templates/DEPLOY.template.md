# Déploiement — [NOM_PROJET]

> Ce document décrit la configuration de déploiement et les procédures.

---

## Architecture de déploiement

```
┌─────────────────────────────────────────────────────────────────┐
│                           PRODUCTION                             │
│                                                                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐       │
│  │   Vercel     │    │   Railway    │    │   Railway    │       │
│  │  (Frontend)  │    │  (Backend)   │    │   (Redis)    │       │
│  │              │    │              │    │              │       │
│  │  Next.js     │───▶│  FastAPI     │◀──▶│  Celery      │       │
│  │  SSR/Static  │    │  + Workers   │    │  Broker      │       │
│  └──────────────┘    └──────────────┘    └──────────────┘       │
│         │                   │                                    │
│         │                   │                                    │
│         ▼                   ▼                                    │
│  ┌──────────────────────────────────────────────────────┐       │
│  │                    Supabase                           │       │
│  │            PostgreSQL + Auth + Storage                │       │
│  └──────────────────────────────────────────────────────┘       │
└─────────────────────────────────────────────────────────────────┘
```

---

## Environnements

| Environnement | URL | Branch | Auto-deploy |
|---------------|-----|--------|-------------|
| Production | [nom].com | `main` | Oui |
| Staging | staging.[nom].com | `develop` | Oui |
| Preview | [hash].vercel.app | PR | Oui |

---

## Frontend (Vercel)

### Configuration

```json
// vercel.json
{
  "framework": "nextjs",
  "buildCommand": "npm run build",
  "outputDirectory": ".next",
  "regions": ["cdg1"],
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        { "key": "X-Frame-Options", "value": "SAMEORIGIN" },
        { "key": "X-Content-Type-Options", "value": "nosniff" },
        { "key": "Referrer-Policy", "value": "strict-origin-when-cross-origin" }
      ]
    }
  ],
  "rewrites": [
    {
      "source": "/api/backend/:path*",
      "destination": "https://api.[nom].com/:path*"
    }
  ]
}
```

### Variables d'environnement (Vercel Dashboard)

| Variable | Production | Staging | Preview |
|----------|------------|---------|---------|
| `NEXT_PUBLIC_APP_URL` | https://[nom].com | https://staging.[nom].com | Auto |
| `NEXT_PUBLIC_API_URL` | https://api.[nom].com | https://api-staging.[nom].com | Staging |
| `NEXT_PUBLIC_SUPABASE_URL` | [prod URL] | [staging URL] | Staging |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | [prod key] | [staging key] | Staging |
| `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY` | pk_live_xxx | pk_test_xxx | Test |

### Domaine custom

1. Vercel Dashboard → Project → Settings → Domains
2. Ajouter `[nom].com` et `www.[nom].com`
3. Configurer DNS :
   ```
   A     @     76.76.21.21
   CNAME www   cname.vercel-dns.com
   ```

---

## Backend (Railway)

### Configuration

```toml
# railway.toml
[build]
builder = "DOCKERFILE"
dockerfilePath = "Dockerfile"

[deploy]
healthcheckPath = "/health"
healthcheckTimeout = 10
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 3

[[services]]
name = "api"
internalPort = 8000

[[services]]
name = "worker"
command = "celery -A app.workers.celery worker --loglevel=info"
```

### Dockerfile

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy code
COPY . .

# Expose port
EXPOSE 8000

# Run
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Variables d'environnement (Railway Dashboard)

| Variable | Production | Staging |
|----------|------------|---------|
| `APP_ENV` | production | staging |
| `APP_DEBUG` | false | true |
| `APP_SECRET_KEY` | [secret] | [secret] |
| `SUPABASE_URL` | [prod URL] | [staging URL] |
| `SUPABASE_SERVICE_KEY` | [prod key] | [staging key] |
| `REDIS_URL` | [Railway Redis URL] | [Railway Redis URL] |
| `STRIPE_SECRET_KEY` | sk_live_xxx | sk_test_xxx |
| `STRIPE_WEBHOOK_SECRET` | whsec_xxx | whsec_xxx |
| `ANTHROPIC_API_KEY` | [key] | [key] |
| `SENTRY_DSN` | [dsn] | [dsn] |

### Domaine custom

1. Railway Dashboard → Service → Settings → Domains
2. Ajouter `api.[nom].com`
3. Configurer DNS :
   ```
   CNAME api [railway-domain].up.railway.app
   ```

---

## Redis (Railway)

### Création

1. Railway Dashboard → New → Database → Redis
2. Copier `REDIS_URL` dans les variables backend

### Configuration

- Max memory: 25MB (free tier) / 256MB+ (paid)
- Eviction policy: allkeys-lru

---

## Supabase

### Projets

| Environnement | Projet Supabase |
|---------------|-----------------|
| Production | [nom]-prod |
| Staging | [nom]-staging |

### Configuration

1. **Auth** :
   - Enable Email provider
   - Configure Site URL : `https://[nom].com`
   - Configure Redirect URLs : 
     - `https://[nom].com/**`
     - `https://staging.[nom].com/**`
     - `http://localhost:3000/**`

2. **Database** :
   - Exécuter migrations depuis `MIGRATIONS.md`
   - Activer RLS sur toutes les tables

3. **Edge Functions** (si utilisées) :
   - Deploy via CLI

### Migrations

```bash
# Login Supabase CLI
supabase login

# Link projet
supabase link --project-ref [project-id]

# Push migrations
supabase db push

# Générer nouvelle migration
supabase migration new [name]
```

---

## DNS (Porkbun/Cloudflare)

### Records

| Type | Name | Value | TTL |
|------|------|-------|-----|
| A | @ | 76.76.21.21 | 300 |
| CNAME | www | cname.vercel-dns.com | 300 |
| CNAME | api | [railway].up.railway.app | 300 |
| TXT | @ | [verification Vercel] | 300 |
| MX | @ | [si email custom] | 300 |

---

## CI/CD (GitHub Actions)

### Backend

```yaml
# .github/workflows/deploy-backend.yml
name: Deploy Backend

on:
  push:
    branches: [main]
    paths:
      - 'backend/**'

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: pip install -r backend/requirements.txt
      - run: cd backend && pytest

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: railwayapp/railway-action@v1
        with:
          service: api
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
```

### Frontend

```yaml
# .github/workflows/deploy-frontend.yml
name: Deploy Frontend

on:
  push:
    branches: [main]
    paths:
      - 'frontend/**'

jobs:
  # Vercel auto-deploy via GitHub integration
  # Ce workflow est optionnel pour tests
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: cd frontend && npm ci
      - run: cd frontend && npm run lint
      - run: cd frontend && npm run test
```

---

## Procédure de déploiement

### Release standard

```bash
# 1. Merge develop → main (via PR)

# 2. Le deploy est automatique via:
#    - Vercel (frontend)
#    - Railway (backend)

# 3. Vérifier les déploiements
#    - Vercel: https://vercel.com/[team]/[project]
#    - Railway: https://railway.app/project/[id]

# 4. Smoke test en prod
#    - [ ] Landing page charge
#    - [ ] Login fonctionne
#    - [ ] Feature principale OK
#    - [ ] Paiement test (si applicable)
```

### Rollback

```bash
# Frontend (Vercel)
# Dashboard → Deployments → Sélectionner version précédente → "..."  → Promote to Production

# Backend (Railway)  
# Dashboard → Deployments → Sélectionner version → Redeploy

# Database
# Voir BACKUP.md pour procédure restore
```

### Hotfix

```bash
# 1. Créer branche depuis main
git checkout main
git pull
git checkout -b hotfix/[description]

# 2. Fix + commit
git add .
git commit -m "fix: [description]"

# 3. Push et PR directe vers main
git push origin hotfix/[description]

# 4. Merge après review rapide

# 5. Cherry-pick vers develop
git checkout develop
git cherry-pick [commit-hash]
git push
```

---

## Monitoring post-deploy

### Checklist

- [ ] Pas d'erreurs Sentry
- [ ] Latence API normale (<500ms p95)
- [ ] Pas de 5xx dans les logs
- [ ] Workers Celery actifs
- [ ] Redis connecté

### Alertes

Configurer dans Sentry/Railway :
- Alerte si error rate > 1%
- Alerte si latence p95 > 2s
- Alerte si service down > 1min

---

## Secrets rotation

### Procédure

1. Générer nouveau secret
2. Ajouter nouveau secret aux variables (ne pas supprimer ancien)
3. Redéployer
4. Vérifier que tout fonctionne
5. Supprimer ancien secret
6. Documenter la rotation

### Schedule

| Secret | Fréquence |
|--------|-----------|
| APP_SECRET_KEY | 90 jours |
| API keys (Anthropic, etc.) | 90 jours |
| Stripe keys | Pas de rotation (sauf compromis) |
| Supabase keys | Pas de rotation (sauf compromis) |
