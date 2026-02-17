# Variables d'Environnement — [NOM_PROJET]

> Ce document liste TOUTES les variables d'environnement du projet.
> Chaque variable est documentée : rôle, format, où la trouver, valeur par défaut.

---

## Backend (.env)

### Application

| Variable | Requis | Description | Format | Défaut | Exemple |
|----------|--------|-------------|--------|--------|---------|
| `APP_ENV` | Oui | Environnement | `development` / `staging` / `production` | `development` | `production` |
| `APP_DEBUG` | Non | Mode debug | `true` / `false` | `false` | `false` |
| `APP_PORT` | Non | Port serveur | Entier | `8000` | `8000` |
| `APP_HOST` | Non | Host serveur | String | `0.0.0.0` | `0.0.0.0` |
| `API_BASE_URL` | Oui | URL publique de l'API | URL | — | `https://api.nom-projet.com` |
| `FRONTEND_URL` | Oui | URL du frontend (CORS) | URL | — | `https://nom-projet.com` |
| `SECRET_KEY` | Oui | Clé secrète application | String 64+ chars | — | `openssl rand -hex 32` |

### Supabase

| Variable | Requis | Description | Où la trouver |
|----------|--------|-------------|---------------|
| `SUPABASE_URL` | Oui | URL du projet Supabase | Settings → API → Project URL |
| `SUPABASE_ANON_KEY` | Oui | Clé publique (anon) | Settings → API → anon public |
| `SUPABASE_SERVICE_KEY` | Oui | Clé service (admin) | Settings → API → service_role |
| `DATABASE_URL` | Oui | URL PostgreSQL directe | Settings → Database → Connection string |

### Redis

| Variable | Requis | Description | Défaut |
|----------|--------|-------------|--------|
| `REDIS_URL` | Oui | URL de connexion Redis | `redis://localhost:6379/0` |
| `CELERY_BROKER_URL` | Oui | Broker Celery | Identique à `REDIS_URL` |
| `CELERY_RESULT_BACKEND` | Non | Backend résultats Celery | Identique à `REDIS_URL` |

### Stripe

| Variable | Requis | Description | Où la trouver |
|----------|--------|-------------|---------------|
| `STRIPE_SECRET_KEY` | Oui | Clé secrète Stripe | Developers → API Keys |
| `STRIPE_WEBHOOK_SECRET` | Oui | Secret webhook | Developers → Webhooks → Signing secret |
| `STRIPE_PRICE_ID_FREE` | Non | Price ID plan Free | Products → [Produit] → Price ID |
| `STRIPE_PRICE_ID_PRO` | Oui | Price ID plan Pro | Products → [Produit] → Price ID |
| `STRIPE_PRICE_ID_TEAM` | Oui | Price ID plan Team | Products → [Produit] → Price ID |
| `STRIPE_PRICE_ID_BUSINESS` | Non | Price ID plan Business | Products → [Produit] → Price ID |

### IA / LLM

| Variable | Requis | Description | Où la trouver |
|----------|--------|-------------|---------------|
| `ANTHROPIC_API_KEY` | Selon projet | Clé API Claude | console.anthropic.com |
| `OPENAI_API_KEY` | Selon projet | Clé API OpenAI | platform.openai.com |
| `LLM_MODEL` | Non | Modèle par défaut | — | `claude-sonnet-4-20250514` |
| `LLM_MAX_TOKENS` | Non | Tokens max par requête | Entier | `4096` |

### Email

| Variable | Requis | Description | Où la trouver |
|----------|--------|-------------|---------------|
| `BREVO_API_KEY` | Oui | Clé API Brevo | SMTP & API → API Keys |
| `EMAIL_FROM` | Oui | Adresse d'envoi | — | `noreply@nom-projet.com` |
| `EMAIL_FROM_NAME` | Non | Nom d'affichage | — | `[NOM_PROJET]` |

### Monitoring

| Variable | Requis | Description | Où la trouver |
|----------|--------|-------------|---------------|
| `SENTRY_DSN` | Oui (prod) | DSN Sentry | Settings → Projects → Client Keys |
| `SENTRY_ENVIRONMENT` | Non | Environnement Sentry | — | `production` |
| `LANGSMITH_API_KEY` | Non | Clé LangSmith | — |
| `LANGSMITH_PROJECT` | Non | Nom projet LangSmith | — |

---

## Frontend (.env.local)

| Variable | Requis | Description | Exemple |
|----------|--------|-------------|---------|
| `NEXT_PUBLIC_APP_URL` | Oui | URL publique du frontend | `https://nom-projet.com` |
| `NEXT_PUBLIC_API_URL` | Oui | URL publique de l'API | `https://api.nom-projet.com` |
| `NEXT_PUBLIC_SUPABASE_URL` | Oui | URL Supabase | `https://xxx.supabase.co` |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Oui | Clé publique Supabase | `eyJ...` |
| `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY` | Oui | Clé publique Stripe | `pk_live_...` |
| `NEXT_PUBLIC_SENTRY_DSN` | Non | DSN Sentry frontend | `https://...@sentry.io/...` |
| `NEXT_PUBLIC_GA_ID` | Non | Google Analytics ID | `G-XXXXXXXX` |

> ⚠️ Toute variable préfixée `NEXT_PUBLIC_` est exposée côté client. Ne JAMAIS y mettre de secret.

---

## Variables par environnement

### Development

```bash
APP_ENV=development
APP_DEBUG=true
API_BASE_URL=http://localhost:8000
FRONTEND_URL=http://localhost:3000
REDIS_URL=redis://localhost:6379/0
# Stripe en mode test
STRIPE_SECRET_KEY=sk_test_...
```

### Staging

```bash
APP_ENV=staging
APP_DEBUG=false
API_BASE_URL=https://staging-api.nom-projet.com
FRONTEND_URL=https://staging.nom-projet.com
# Stripe en mode test
STRIPE_SECRET_KEY=sk_test_...
```

### Production

```bash
APP_ENV=production
APP_DEBUG=false
API_BASE_URL=https://api.nom-projet.com
FRONTEND_URL=https://nom-projet.com
# Stripe en mode live
STRIPE_SECRET_KEY=sk_live_...
```

---

## Sécurité

### Règles

1. **JAMAIS de secret dans le code source** — tout dans les variables d'environnement
2. **JAMAIS de `.env` committé** — `.env` est dans `.gitignore`
3. **`.env.example` toujours à jour** — sans les valeurs réelles, juste le format
4. **Rotation régulière** — changer les clés tous les 6 mois minimum
5. **Secrets différents par environnement** — dev ≠ staging ≠ prod

### En cas de fuite

1. Révoquer immédiatement la clé compromise
2. Générer une nouvelle clé
3. Déployer avec la nouvelle clé
4. Auditer les accès avec l'ancienne clé
5. Documenter l'incident

---

## Checklist

- [ ] Toutes les variables documentées ci-dessus
- [ ] `.env.example` à jour dans backend/ et frontend/
- [ ] Aucun secret dans le code source
- [ ] Variables de prod configurées dans Railway
- [ ] Variables de prod configurées dans Vercel
- [ ] CORS configuré avec `FRONTEND_URL`
