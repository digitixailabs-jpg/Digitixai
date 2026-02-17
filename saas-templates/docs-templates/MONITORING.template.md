# Monitoring & Alertes — [NOM_PROJET]

> Ce document définit la stratégie de monitoring et les runbooks d'incidents.

---

## Stack Monitoring

| Outil | Usage | URL |
|-------|-------|-----|
| Sentry | Error tracking | sentry.io |
| Railway Metrics | Infra monitoring | railway.app |
| Vercel Analytics | Frontend perf | vercel.com |
| LangSmith | LLM traces | langsmith.com |
| UptimeRobot/BetterStack | Uptime | [url] |

---

## Métriques clés

### Infrastructure

| Métrique | Seuil warning | Seuil critical | Action |
|----------|---------------|----------------|--------|
| CPU usage | >70% | >90% | Scale up |
| Memory usage | >70% | >85% | Scale up / investigate leak |
| Disk usage | >70% | >85% | Cleanup / expand |
| Response time p95 | >500ms | >2s | Investigate |
| Response time p99 | >1s | >5s | Investigate |
| Error rate | >1% | >5% | Investigate |

### Application

| Métrique | Seuil warning | Seuil critical | Action |
|----------|---------------|----------------|--------|
| API errors 5xx | >10/min | >50/min | Investigate |
| API errors 4xx | >100/min | >500/min | Check abuse |
| Queue length | >100 | >500 | Scale workers |
| Job failure rate | >5% | >20% | Investigate |
| Auth failures | >50/min | >200/min | Check brute force |

### Business

| Métrique | Seuil warning | Seuil critical | Action |
|----------|---------------|----------------|--------|
| Signups/jour | <50% baseline | <20% baseline | Check funnel |
| Payments failed | >10% | >30% | Check Stripe |
| Churn spike | >2x normal | >5x normal | Investigate |

---

## Alertes configurées

### Critical (PagerDuty/SMS)

| Alerte | Condition | Destinataire |
|--------|-----------|--------------|
| Site down | HTTP 5xx > 1min | On-call |
| DB down | Connection failed | On-call |
| Payment system down | Stripe webhook fail > 5min | On-call |
| Security breach | Suspicious auth pattern | On-call + Security |

### Warning (Slack/Email)

| Alerte | Condition | Destinataire |
|--------|-----------|--------------|
| High error rate | 5xx > 1% pendant 5min | #alerts |
| Slow response | p95 > 2s pendant 5min | #alerts |
| Queue backup | Jobs pending > 100 | #alerts |
| Disk space low | >70% | #alerts |
| LLM API errors | >10% fail rate | #alerts |

### Info (Slack daily digest)

| Alerte | Condition | Destinataire |
|--------|-----------|--------------|
| Daily stats | 9h chaque jour | #metrics |
| Weekly report | Lundi 9h | #metrics |

---

## Configuration Sentry

### Backend (Python)

```python
# app/main.py
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.celery import CeleryIntegration

sentry_sdk.init(
    dsn=settings.SENTRY_DSN,
    environment=settings.APP_ENV,
    traces_sample_rate=0.1,  # 10% des transactions
    profiles_sample_rate=0.1,
    integrations=[
        FastApiIntegration(),
        CeleryIntegration(),
    ],
    # Ne pas envoyer PII
    send_default_pii=False,
    # Filtrer les erreurs non pertinentes
    before_send=filter_events,
)

def filter_events(event, hint):
    # Ignorer les 404
    if 'exc_info' in hint:
        exc_type, exc_value, tb = hint['exc_info']
        if isinstance(exc_value, HTTPException) and exc_value.status_code == 404:
            return None
    return event
```

### Frontend (Next.js)

```typescript
// sentry.client.config.ts
import * as Sentry from '@sentry/nextjs';

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  environment: process.env.NODE_ENV,
  tracesSampleRate: 0.1,
  replaysSessionSampleRate: 0.1,
  replaysOnErrorSampleRate: 1.0,
});
```

---

## Configuration LangSmith

```python
# app/services/llm_service.py
import os
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = settings.LANGSMITH_API_KEY
os.environ["LANGCHAIN_PROJECT"] = "[NOM_PROJET]"

# Toutes les calls LangChain sont auto-tracées
```

### Métriques LLM à surveiller

| Métrique | Seuil | Action |
|----------|-------|--------|
| Latency p50 | >2s | Optimize prompt |
| Latency p95 | >10s | Check model/fallback |
| Cost/request | >$0.10 | Review prompt length |
| Error rate | >5% | Check API status |
| Token usage | Budget >80% | Alert finance |

---

## Logging

### Format

```python
# Structured logging avec structlog
import structlog

logger = structlog.get_logger()

# Usage
logger.info(
    "report_created",
    user_id=user.id,
    report_id=report.id,
    duration_ms=duration
)

# Output JSON
{
    "event": "report_created",
    "user_id": "uuid",
    "report_id": "uuid",
    "duration_ms": 1234,
    "timestamp": "2026-01-15T10:30:00Z",
    "level": "info"
}
```

### Niveaux

| Level | Usage | Exemple |
|-------|-------|---------|
| DEBUG | Dev only, verbose | Query SQL |
| INFO | Événements normaux | User created, Payment success |
| WARNING | Situation anormale mais gérée | Rate limit hit, Retry |
| ERROR | Erreur nécessitant attention | API externe down, DB error |
| CRITICAL | Système compromis | Data corruption, Security breach |

### Rétention

| Environnement | Rétention |
|---------------|-----------|
| Production | 30 jours |
| Staging | 7 jours |
| Development | Session |

---

## Health checks

### Endpoint /health

```python
@app.get("/health")
async def health_check():
    checks = {
        "api": "ok",
        "database": await check_db(),
        "redis": await check_redis(),
        "external_apis": await check_external_apis(),
    }
    
    all_ok = all(v == "ok" for v in checks.values())
    
    return JSONResponse(
        status_code=200 if all_ok else 503,
        content={"status": "healthy" if all_ok else "degraded", "checks": checks}
    )

async def check_db():
    try:
        await supabase.from_("profiles").select("id").limit(1).execute()
        return "ok"
    except Exception:
        return "error"
```

### Uptime monitoring

Configurer UptimeRobot/BetterStack :

| Check | URL | Interval | Alert after |
|-------|-----|----------|-------------|
| API Health | https://api.[nom].com/health | 1 min | 2 failures |
| Frontend | https://[nom].com | 1 min | 2 failures |
| Login page | https://[nom].com/login | 5 min | 2 failures |

---

## Runbooks

### RB-001: Site down (5xx errors)

**Symptômes** : Alerte "Site down", users reportent erreurs

**Diagnostic** :
```bash
# 1. Vérifier status services
# Railway Dashboard → Services → Check status

# 2. Vérifier logs récents
# Railway → Service → Logs

# 3. Vérifier Sentry pour erreurs
# Sentry → Issues → Last hour

# 4. Vérifier dépendances
curl https://api.[nom].com/health
```

**Actions** :
1. Si Railway service crashed → Restart service
2. Si DB down → Vérifier Supabase status, contacter support
3. Si code bug → Rollback dernier deploy
4. Si overload → Scale up instances

**Communication** :
- Update status page
- Tweet si >5min downtime

---

### RB-002: Database connection issues

**Symptômes** : Erreurs "connection refused", timeouts DB

**Diagnostic** :
```bash
# 1. Vérifier Supabase Dashboard
# Project → Database → Connection pooler status

# 2. Vérifier nombre de connexions
# SQL: SELECT count(*) FROM pg_stat_activity;
```

**Actions** :
1. Si pool exhausted → Restart backend (libère connexions)
2. Si Supabase incident → Attendre, status.supabase.com
3. Si leak → Identifier code problématique, hotfix

---

### RB-003: High latency

**Symptômes** : Response time >2s, users se plaignent de lenteur

**Diagnostic** :
```bash
# 1. Identifier endpoints lents
# Sentry → Performance → Slowest transactions

# 2. Vérifier charge
# Railway → Metrics → CPU/Memory

# 3. Vérifier external APIs
# LangSmith → Traces → Recent slow
```

**Actions** :
1. Si CPU saturé → Scale up
2. Si query lente → Optimiser (index, query)
3. Si LLM lent → Vérifier Anthropic status, fallback

---

### RB-004: Payment failures spike

**Symptômes** : Taux d'échec paiement >10%

**Diagnostic** :
```bash
# 1. Vérifier Stripe Dashboard
# Payments → Failed → Analyze reasons

# 2. Vérifier logs webhooks
# Stripe → Developers → Webhooks → Recent deliveries
```

**Actions** :
1. Si Stripe incident → status.stripe.com, attendre
2. Si webhook failing → Fix endpoint, replay events
3. Si fraud → Review Radar rules

---

### RB-005: Celery workers stuck

**Symptômes** : Jobs ne progressent pas, queue grandit

**Diagnostic** :
```bash
# 1. Vérifier workers actifs
# Railway → Worker service → Check running

# 2. Vérifier Redis
# Railway → Redis → Memory usage
```

**Actions** :
1. Si worker crashed → Restart
2. Si Redis full → Purge old jobs, scale Redis
3. Si job infini → Kill job, fix code, retry

---

## Dashboards

### Dashboard Ops (Grafana/Railway)

```
┌─────────────────────────────────────────────────────────────┐
│ Request Rate        Error Rate         Response Time        │
│ [████████░░] 150/s  [██░░░░░░░░] 0.5%  [███░░░░░░░] 234ms  │
├─────────────────────────────────────────────────────────────┤
│ CPU Usage           Memory Usage       Active Connections   │
│ [████░░░░░░] 40%    [██████░░░░] 60%   [███░░░░░░░] 45     │
├─────────────────────────────────────────────────────────────┤
│ Queue Length        Worker Count       Job Success Rate     │
│ [██░░░░░░░░] 23     [████░░░░░░] 4     [█████████░] 98%    │
└─────────────────────────────────────────────────────────────┘
```

---

## Contacts escalation

| Level | Délai | Contact |
|-------|-------|---------|
| L1 | 0-15min | On-call engineer |
| L2 | 15-30min | Tech lead |
| L3 | 30min+ | CTO |

| Service | Support |
|---------|---------|
| Supabase | support@supabase.io |
| Railway | Discord / support |
| Stripe | Dashboard chat |
| Anthropic | support@anthropic.com |
