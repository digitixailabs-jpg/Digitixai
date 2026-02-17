# Performance — [NOM_PROJET]

> Ce document définit les objectifs de performance, les benchmarks, et les stratégies d'optimisation.

---

## Objectifs de performance

### Temps de réponse API

| Endpoint type | Objectif P50 | Objectif P95 | Objectif P99 | Max absolu |
|---------------|-------------|-------------|-------------|------------|
| Lecture simple (GET) | < 50ms | < 100ms | < 200ms | 500ms |
| Écriture simple (POST/PUT) | < 100ms | < 200ms | < 500ms | 1s |
| Avec traitement IA/LLM | < 2s | < 5s | < 10s | 30s |
| Tâche async (Celery) | Immédiat (< 100ms) | — | — | — |
| Webhook forward | < 50ms | < 100ms | < 200ms | 500ms |

### Frontend

| Métrique | Objectif | Outil de mesure |
|----------|----------|-----------------|
| LCP (Largest Contentful Paint) | < 2.5s | Lighthouse |
| FID (First Input Delay) | < 100ms | Lighthouse |
| CLS (Cumulative Layout Shift) | < 0.1 | Lighthouse |
| TTI (Time to Interactive) | < 3s | Lighthouse |
| Lighthouse Score | > 90 | Lighthouse |
| Bundle size (gzip) | < 200KB | `next build` |

### Base de données

| Requête type | Objectif | Max absolu |
|-------------|----------|------------|
| SELECT simple (index) | < 5ms | 20ms |
| SELECT avec JOIN | < 20ms | 100ms |
| INSERT/UPDATE | < 10ms | 50ms |
| Requête complexe (agrégation) | < 100ms | 500ms |

---

## Benchmarks actuels

> À remplir après chaque test de performance.

| Date | Endpoint | P50 | P95 | P99 | RPS | Notes |
|------|----------|-----|-----|-----|-----|-------|
| [Date] | [Endpoint] | [ms] | [ms] | [ms] | [req/s] | [Notes] |

---

## Tests de charge

### Outils

- **locust** (Python) — Tests de charge HTTP
- **k6** — Alternative JS/Go, scripts versionnés

### Scénarios de test

#### Scénario 1 — Usage normal
```
Utilisateurs simultanés : 50
Durée : 5 minutes
Mix :
  - 60% GET endpoints principaux
  - 25% POST/PUT (création/modification)
  - 10% Auth (login/refresh)
  - 5% Webhook reception
```

#### Scénario 2 — Pic de charge
```
Utilisateurs simultanés : 200
Ramp-up : 0 → 200 en 2 minutes
Durée plateau : 5 minutes
Même mix que scénario 1
```

#### Scénario 3 — Stress test
```
Utilisateurs simultanés : 500+
Ramp-up : progressif jusqu'à failure
Objectif : identifier le point de rupture
```

### Template Locust

```python
# tests/load/locustfile.py
from locust import HttpUser, task, between

class SaaSUser(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        # Login
        response = self.client.post("/api/v1/auth/login", json={
            "email": "loadtest@example.com",
            "password": "testpassword"
        })
        self.token = response.json()["access_token"]
        self.headers = {"Authorization": f"Bearer {self.token}"}
    
    @task(6)
    def get_main_resource(self):
        self.client.get("/api/v1/[ressource]", headers=self.headers)
    
    @task(2)
    def create_resource(self):
        self.client.post("/api/v1/[ressource]", 
            headers=self.headers,
            json={"field": "value"})
    
    @task(1)
    def get_dashboard(self):
        self.client.get("/api/v1/dashboard", headers=self.headers)
```

### Exécution

```bash
# Test local
locust -f tests/load/locustfile.py --host=http://localhost:8000

# Test headless (CI)
locust -f tests/load/locustfile.py --host=https://api.nom-projet.com \
  --users 50 --spawn-rate 5 --run-time 5m --headless
```

---

## Stratégies d'optimisation

### Backend

| Stratégie | Impact | Complexité | Statut |
|-----------|--------|------------|--------|
| Index DB sur colonnes filtrées | 🔴 Élevé | 🟢 Simple | [À faire / Fait] |
| Cache Redis (résultats fréquents) | 🔴 Élevé | 🟡 Moyen | [À faire / Fait] |
| Connection pooling PostgreSQL | 🟡 Moyen | 🟢 Simple | [À faire / Fait] |
| Requêtes async (httpx) | 🟡 Moyen | 🟢 Simple | [À faire / Fait] |
| Pagination systématique | 🟡 Moyen | 🟢 Simple | [À faire / Fait] |
| Background tasks (Celery) | 🔴 Élevé | 🟡 Moyen | [À faire / Fait] |
| Compression gzip réponses | 🟢 Faible | 🟢 Simple | [À faire / Fait] |
| Rate limiting par tier | 🟡 Moyen | 🟡 Moyen | [À faire / Fait] |

### Frontend

| Stratégie | Impact | Complexité | Statut |
|-----------|--------|------------|--------|
| Images optimisées (next/image) | 🔴 Élevé | 🟢 Simple | [À faire / Fait] |
| Code splitting (dynamic imports) | 🟡 Moyen | 🟢 Simple | [À faire / Fait] |
| SSR/SSG pages statiques | 🔴 Élevé | 🟡 Moyen | [À faire / Fait] |
| Prefetch liens navigation | 🟢 Faible | 🟢 Simple | [À faire / Fait] |
| Cache API (SWR/React Query) | 🟡 Moyen | 🟡 Moyen | [À faire / Fait] |
| Lazy loading composants lourds | 🟡 Moyen | 🟢 Simple | [À faire / Fait] |
| Bundle analyzer | 🟡 Moyen | 🟢 Simple | [À faire / Fait] |

### Infrastructure

| Stratégie | Impact | Complexité | Statut |
|-----------|--------|------------|--------|
| CDN (Cloudflare) | 🔴 Élevé | 🟢 Simple | [À faire / Fait] |
| Edge caching headers | 🟡 Moyen | 🟢 Simple | [À faire / Fait] |
| Auto-scaling Railway | 🟡 Moyen | 🟡 Moyen | [À faire / Fait] |
| Redis pour sessions | 🟢 Faible | 🟢 Simple | [À faire / Fait] |

---

## Monitoring performance

### Alertes

| Métrique | Seuil warning | Seuil critique | Action |
|----------|--------------|----------------|--------|
| P95 latence API | > 500ms | > 2s | Investiguer queries lentes |
| Error rate | > 1% | > 5% | Rollback si nécessaire |
| CPU usage | > 70% | > 90% | Scale up |
| Memory usage | > 70% | > 90% | Investiguer memory leaks |
| DB connections | > 80% pool | > 95% pool | Augmenter pool size |

### Dashboard Sentry

Configurer les transactions Sentry pour tracer :
- Temps par endpoint
- Temps DB par requête
- Temps appels externes (LLM, Stripe, etc.)

---

## Checklist pré-launch

- [ ] Lighthouse score > 90 sur toutes les pages publiques
- [ ] Tests de charge exécutés (scénario 1 + 2)
- [ ] Index DB créés sur toutes les colonnes filtrées/triées
- [ ] Cache Redis configuré pour les requêtes fréquentes
- [ ] CDN activé (Cloudflare)
- [ ] Compression gzip activée
- [ ] Images optimisées
- [ ] Monitoring performance configuré (Sentry)
- [ ] Alertes latence configurées
