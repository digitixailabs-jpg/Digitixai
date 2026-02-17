# Sécurité — [NOM_PROJET]

> Ce document définit toutes les mesures de sécurité du projet.
> À implémenter AVANT le déploiement en production.

---

## Vue d'ensemble

### Niveau de sensibilité des données

| Type de donnée | Sensibilité | Protection requise |
|----------------|-------------|-------------------|
| Credentials (passwords) | Critique | Hash + Salt (Supabase Auth) |
| Tokens (JWT) | Haute | Expiration courte, refresh |
| PII (email, nom) | Haute | Chiffrement en transit, RLS |
| Données métier | Moyenne | RLS, validation |
| Logs | Basse | Pas de PII dans logs |

---

## Authentification

### Provider

- **Supabase Auth** : Gère entièrement l'auth
- Pas de stockage de passwords côté backend
- JWT signé par Supabase

### Configuration sessions

| Paramètre | Valeur | Raison |
|-----------|--------|--------|
| JWT expiration | 1 heure | Limite l'impact si token compromis |
| Refresh token | 7 jours | UX vs sécurité |
| Refresh rotation | Enabled | Invalide ancien token au refresh |

### Password policy

| Règle | Valeur |
|-------|--------|
| Longueur minimum | 8 caractères |
| Complexité | Au moins 1 lettre et 1 chiffre |
| Historique | Non réutilisable (3 derniers) |
| Expiration | Non (pas de rotation forcée) |

### Brute force protection

| Mesure | Configuration |
|--------|---------------|
| Rate limit login | 5 tentatives / 15 minutes |
| Lockout | 15 minutes après 5 échecs |
| Notification | Email si login depuis nouveau device |

---

## Autorisation

### Modèle

- **RBAC** (Role-Based Access Control) simplifié
- Rôles stockés dans `profiles.role`
- Vérification à chaque requête API

### Rôles

| Rôle | Niveau | Permissions |
|------|--------|-------------|
| `anonymous` | 0 | Pages publiques uniquement |
| `user` | 1 | CRUD sur ses propres ressources |
| `premium` | 2 | Accès features premium |
| `admin` | 99 | Accès total + admin panel |

### Row Level Security (RLS)

**Toutes les tables doivent avoir RLS activé.**

Pattern standard :

```sql
-- Activer RLS
ALTER TABLE my_table ENABLE ROW LEVEL SECURITY;

-- Policy SELECT : user voit ses données
CREATE POLICY "Users can view own data"
ON my_table FOR SELECT
USING (auth.uid() = user_id);

-- Policy INSERT : user crée ses données
CREATE POLICY "Users can insert own data"
ON my_table FOR INSERT
WITH CHECK (auth.uid() = user_id);

-- Policy UPDATE : user modifie ses données
CREATE POLICY "Users can update own data"
ON my_table FOR UPDATE
USING (auth.uid() = user_id);

-- Policy DELETE : user supprime ses données
CREATE POLICY "Users can delete own data"
ON my_table FOR DELETE
USING (auth.uid() = user_id);

-- Policy admin : accès total
CREATE POLICY "Admins have full access"
ON my_table FOR ALL
USING (
  EXISTS (
    SELECT 1 FROM profiles
    WHERE id = auth.uid() AND role = 'admin'
  )
);
```

### Vérification backend

```python
# Toujours vérifier que l'utilisateur a accès à la ressource
async def get_report(report_id: str, current_user: User):
    report = await fetch_report(report_id)
    
    # Vérifier ownership
    if report.user_id != current_user.id:
        raise AppException(
            code=ErrorCode.AUTH_FORBIDDEN,
            message="Accès non autorisé",
            status_code=403
        )
    
    return report
```

---

## Validation des entrées

### Principes

1. **Ne jamais faire confiance aux inputs** : Tout valider côté serveur
2. **Validation stricte** : Rejeter ce qui n'est pas explicitement autorisé
3. **Defense in depth** : Frontend + Backend validation

### Backend (Pydantic)

```python
from pydantic import BaseModel, EmailStr, Field, validator
import re

class CreateReportRequest(BaseModel):
    url: str = Field(..., min_length=1, max_length=2048)
    title: str = Field(..., min_length=1, max_length=255)
    
    @validator('url')
    def validate_url(cls, v):
        # Accepter uniquement http/https
        if not v.startswith(('http://', 'https://')):
            raise ValueError('URL must start with http:// or https://')
        return v
    
    @validator('title')
    def sanitize_title(cls, v):
        # Supprimer caractères dangereux
        return re.sub(r'[<>"\']', '', v)
```

### Frontend (Zod)

```typescript
import { z } from 'zod';

const createReportSchema = z.object({
  url: z.string()
    .url('URL invalide')
    .max(2048, 'URL trop longue'),
  title: z.string()
    .min(1, 'Titre requis')
    .max(255, 'Titre trop long')
    .transform(val => val.replace(/[<>"']/g, '')),
});
```

### Inputs à risque

| Input | Risque | Mitigation |
|-------|--------|------------|
| URLs | SSRF, XSS | Whitelist protocoles, sanitize |
| HTML/Markdown | XSS | Sanitize avec DOMPurify |
| SQL identifiers | Injection | Parameterized queries uniquement |
| File uploads | RCE, DoS | Validation MIME, taille max, sandbox |
| JSON | DoS (nested) | Limiter profondeur |

---

## Protection XSS

### Frontend

```typescript
// Utiliser React qui échappe par défaut
// ❌ Dangereux
<div dangerouslySetInnerHTML={{ __html: userContent }} />

// ✅ Safe
<div>{userContent}</div>

// Si HTML nécessaire, sanitizer avec DOMPurify
import DOMPurify from 'dompurify';
<div dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(userContent) }} />
```

### Headers CSP

```typescript
// next.config.js
const securityHeaders = [
  {
    key: 'Content-Security-Policy',
    value: `
      default-src 'self';
      script-src 'self' 'unsafe-inline' 'unsafe-eval' https://js.stripe.com;
      style-src 'self' 'unsafe-inline';
      img-src 'self' data: https:;
      font-src 'self';
      connect-src 'self' https://*.supabase.co https://api.stripe.com;
      frame-src https://js.stripe.com;
    `.replace(/\s{2,}/g, ' ').trim()
  }
];
```

---

## Protection CSRF

### Supabase

- Supabase utilise des JWT dans headers, pas de cookies de session
- CSRF non applicable pour les appels API

### Formulaires

- Pour les actions sensibles, implémenter double-submit cookie si nécessaire
- Vérifier `Origin` header sur mutations

---

## Rate limiting

### Configuration

| Endpoint | Limite | Fenêtre | Action si dépassé |
|----------|--------|---------|-------------------|
| `/api/*` (auth) | 100 req | 1 minute | 429 + Retry-After |
| `/api/*` (anon) | 20 req | 1 minute | 429 |
| `/api/auth/login` | 5 req | 15 minutes | 429 + temp lockout |
| `/api/webhooks/*` | 1000 req | 1 minute | 429 |
| `/api/[heavy_operation]` | 10 req | 1 minute | 429 |

### Implémentation (FastAPI)

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.get("/api/v1/reports")
@limiter.limit("100/minute")
async def list_reports(request: Request):
    pass
```

---

## Secrets management

### Règles

1. **Jamais de secrets dans le code** : Utiliser variables d'environnement
2. **Jamais de secrets dans les logs** : Masquer automatiquement
3. **Rotation régulière** : API keys tous les 90 jours
4. **Principe du moindre privilège** : Clés avec permissions minimales

### Variables d'environnement

| Secret | Environnement | Rotation |
|--------|---------------|----------|
| `SUPABASE_SERVICE_KEY` | Railway secrets | 90 jours |
| `STRIPE_SECRET_KEY` | Railway secrets | 90 jours |
| `ANTHROPIC_API_KEY` | Railway secrets | 90 jours |
| `APP_SECRET_KEY` | Railway secrets | 90 jours |

### .env.example

```bash
# ⚠️ Ne JAMAIS commit de vraies valeurs
SUPABASE_SERVICE_KEY=your-service-key-here
STRIPE_SECRET_KEY=sk_test_xxx
```

### .gitignore

```
.env
.env.local
.env.production
*.pem
*.key
```

---

## Protection des données

### En transit

| Protocole | Usage |
|-----------|-------|
| HTTPS | Obligatoire partout |
| TLS 1.2+ | Minimum supporté |
| HSTS | Enabled (1 an) |

### Au repos

| Donnée | Protection |
|--------|------------|
| Database | Supabase encryption at rest |
| Backups | Encrypted |
| Logs | Pas de PII |

### Headers de sécurité

```typescript
// next.config.js
const securityHeaders = [
  { key: 'X-DNS-Prefetch-Control', value: 'on' },
  { key: 'Strict-Transport-Security', value: 'max-age=31536000; includeSubDomains' },
  { key: 'X-Frame-Options', value: 'SAMEORIGIN' },
  { key: 'X-Content-Type-Options', value: 'nosniff' },
  { key: 'Referrer-Policy', value: 'strict-origin-when-cross-origin' },
  { key: 'Permissions-Policy', value: 'camera=(), microphone=(), geolocation=()' },
];
```

---

## Logging sécurité

### Ce qu'on log

| Event | Level | Données |
|-------|-------|---------|
| Login success | INFO | user_id, IP, timestamp |
| Login failure | WARN | email (masqué), IP, reason |
| Permission denied | WARN | user_id, resource, action |
| Rate limit hit | WARN | IP, endpoint |
| Error 500 | ERROR | request_id, stack (sans PII) |

### Ce qu'on ne log JAMAIS

- Passwords (même hashés)
- Tokens / API keys
- Données de carte bancaire
- Contenu des messages utilisateurs

### Format

```python
# Structured logging
logger.info(
    "login_success",
    extra={
        "user_id": user.id,
        "ip": request.client.host,
        "user_agent": request.headers.get("user-agent")
    }
)
```

---

## Webhooks (Stripe)

### Vérification signature

```python
import stripe

@app.post("/api/webhooks/stripe")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    
    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")
    
    # Process event
    return {"received": True}
```

### IP Whitelisting (optionnel)

Stripe IPs : https://stripe.com/docs/ips

---

## Checklist pré-production

### Backend

- [ ] RLS activé sur toutes les tables
- [ ] Rate limiting configuré
- [ ] Validation Pydantic sur tous les endpoints
- [ ] Pas de secrets dans le code
- [ ] Logs ne contiennent pas de PII
- [ ] CORS configuré strictement
- [ ] Webhook signatures vérifiées

### Frontend

- [ ] CSP headers configurés
- [ ] Pas de `dangerouslySetInnerHTML` non sanitisé
- [ ] Validation Zod sur tous les formulaires
- [ ] Variables `NEXT_PUBLIC_` vérifiées (pas de secrets)
- [ ] HTTPS forcé

### Infrastructure

- [ ] HTTPS obligatoire
- [ ] Secrets dans Railway/Vercel secrets
- [ ] Backups configurés
- [ ] Monitoring des erreurs (Sentry)
- [ ] Alertes sur événements suspects

---

## Incident response

### En cas de breach

1. **Contenir** : Révoquer accès compromis
2. **Évaluer** : Identifier données touchées
3. **Notifier** : Users si PII concernée (GDPR: 72h max)
4. **Remédier** : Corriger la faille
5. **Documenter** : Post-mortem

### Contacts

| Rôle | Contact |
|------|---------|
| Security lead | [À_COMPLÉTER] |
| Legal | [À_COMPLÉTER] |
| Supabase support | support@supabase.io |
| Stripe support | Dashboard |
