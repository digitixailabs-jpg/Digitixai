# Tâches — [NOM_PROJET]

> Ce document liste toutes les tâches à réaliser, organisées par phase.
> Cocher les tâches au fur et à mesure de l'avancement.

---

## Légende

- 🔴 Bloquant / Critique
- 🟡 Important
- 🟢 Nice to have
- ⏳ En cours
- ✅ Terminé
- ❌ Abandonné

---

## Phase 1 — Setup & Infrastructure

### Backend

- [ ] 🔴 Créer repo GitHub
- [ ] 🔴 Setup FastAPI avec structure de base
- [ ] 🔴 Configurer variables d'environnement
- [ ] 🔴 Setup Supabase projet
- [ ] 🔴 Créer tables initiales (migrations)
- [ ] 🔴 Configurer RLS policies
- [ ] 🟡 Setup Celery + Redis
- [ ] 🟡 Configurer Sentry
- [ ] 🟢 Setup LangSmith

### Frontend

- [ ] 🔴 Setup Next.js avec structure de base
- [ ] 🔴 Configurer Tailwind
- [ ] 🔴 Setup Supabase Auth client
- [ ] 🔴 Créer composants UI de base
- [ ] 🟡 Configurer Sentry

### DevOps

- [ ] 🔴 Configurer Railway (backend)
- [ ] 🔴 Configurer Vercel (frontend)
- [ ] 🔴 Setup CI/CD GitHub Actions
- [ ] 🟡 Configurer domaine custom
- [ ] 🟡 Setup SSL

---

## Phase 2 — Authentification

### Backend

- [ ] 🔴 Endpoint GET /profile
- [ ] 🔴 Endpoint PATCH /profile
- [ ] 🔴 Middleware auth (JWT validation)
- [ ] 🟡 Rate limiting sur auth endpoints

### Frontend

- [ ] 🔴 Page /login
- [ ] 🔴 Page /register
- [ ] 🔴 Page /forgot-password
- [ ] 🔴 Hook useAuth
- [ ] 🔴 Protected routes middleware
- [ ] 🟡 OAuth Google
- [ ] 🟡 Page /reset-password
- [ ] 🟢 Remember me

### Tests

- [ ] 🔴 Test login success/failure
- [ ] 🔴 Test register
- [ ] 🔴 Test protected route access

---

## Phase 3 — Feature principale : [NOM_FEATURE]

### Backend

- [ ] 🔴 Endpoint POST /[resource] - Création
- [ ] 🔴 Endpoint GET /[resource] - Liste
- [ ] 🔴 Endpoint GET /[resource]/{id} - Détail
- [ ] 🔴 Endpoint PATCH /[resource]/{id} - Update
- [ ] 🔴 Endpoint DELETE /[resource]/{id} - Suppression
- [ ] 🔴 Service [feature] - Logique métier
- [ ] 🔴 Task Celery - Traitement async
- [ ] 🟡 Validation inputs
- [ ] 🟡 Gestion erreurs complète

### Frontend

- [ ] 🔴 Page dashboard
- [ ] 🔴 Page liste [resource]
- [ ] 🔴 Page détail [resource]
- [ ] 🔴 Formulaire création
- [ ] 🔴 Composant card [resource]
- [ ] 🟡 États loading/error/empty
- [ ] 🟡 Pagination
- [ ] 🟢 Filtres/recherche

### Tests

- [ ] 🔴 Test CRUD [resource]
- [ ] 🔴 Test edge cases
- [ ] 🟡 Test UI composants

---

## Phase 4 — Paiement

### Backend

- [ ] 🔴 Endpoint POST /billing/checkout
- [ ] 🔴 Endpoint POST /billing/portal
- [ ] 🔴 Webhook Stripe handler
- [ ] 🔴 Gestion subscription status
- [ ] 🟡 Gestion crédits (si applicable)

### Frontend

- [ ] 🔴 Page /pricing
- [ ] 🔴 Composant CheckoutButton
- [ ] 🔴 Page success après paiement
- [ ] 🔴 Page /settings/billing
- [ ] 🟡 Affichage subscription status

### Stripe

- [ ] 🔴 Créer produits dans Stripe
- [ ] 🔴 Configurer webhook endpoint
- [ ] 🔴 Configurer Customer Portal
- [ ] 🟡 Tester flow complet en mode test

### Tests

- [ ] 🔴 Test webhook signature
- [ ] 🔴 Test création checkout
- [ ] 🟡 Test flow complet E2E

---

## Phase 5 — Polish & UX

### UI/UX

- [ ] 🔴 Responsive mobile
- [ ] 🔴 Loading states partout
- [ ] 🔴 Error states partout
- [ ] 🔴 Empty states partout
- [ ] 🟡 Animations/transitions
- [ ] 🟡 Toasts notifications
- [ ] 🟢 Dark mode

### SEO & Marketing

- [ ] 🔴 Meta tags toutes pages
- [ ] 🔴 OG images
- [ ] 🔴 Favicon
- [ ] 🔴 Landing page finale
- [ ] 🟡 robots.txt
- [ ] 🟡 sitemap.xml
- [ ] 🟢 Structured data

### Legal

- [ ] 🔴 Page CGU
- [ ] 🔴 Page Privacy Policy
- [ ] 🔴 Banner cookies (si analytics)
- [ ] 🟡 Mentions légales

---

## Phase 6 — Tests & QA

### Tests automatisés

- [ ] 🔴 Tests unitaires backend (>70% coverage)
- [ ] 🔴 Tests API endpoints critiques
- [ ] 🟡 Tests composants frontend
- [ ] 🟡 Tests E2E flow principal

### QA manuel

- [ ] 🔴 Test flow inscription → paiement
- [ ] 🔴 Test feature principale tous cas
- [ ] 🔴 Test responsive (mobile, tablet, desktop)
- [ ] 🔴 Test sur différents navigateurs
- [ ] 🟡 Test accessibilité basique
- [ ] 🟡 Test performance (Lighthouse)

---

## Phase 7 — Déploiement & Launch

### Pre-launch

- [ ] 🔴 Variables d'env production configurées
- [ ] 🔴 Stripe en mode live
- [ ] 🔴 Domaine configuré
- [ ] 🔴 SSL actif
- [ ] 🔴 Monitoring configuré
- [ ] 🔴 Backup DB vérifié
- [ ] 🟡 Analytics configuré

### Launch

- [ ] 🔴 Deploy production
- [ ] 🔴 Smoke test en prod
- [ ] 🔴 Vérifier paiement fonctionne
- [ ] 🟡 Annoncer sur réseaux

### Post-launch

- [ ] 🔴 Monitorer erreurs 24h
- [ ] 🔴 Monitorer performance
- [ ] 🟡 Recueillir feedback users
- [ ] 🟡 Prioriser bugs/améliorations

---

## Backlog (Non planifié)

| Tâche | Priorité | Effort estimé | Notes |
|-------|----------|---------------|-------|
| [Tâche future 1] | 🟡 | M | |
| [Tâche future 2] | 🟢 | S | |

---

## Notes de session

### [DATE]

- [Note sur l'avancement]
- [Blocage rencontré]
- [Décision prise]

---

## Métriques

| Métrique | Cible | Actuel |
|----------|-------|--------|
| Tâches Phase 1 | 100% | 0% |
| Tâches Phase 2 | 100% | 0% |
| Tâches Phase 3 | 100% | 0% |
| Coverage tests | >70% | 0% |
| Lighthouse score | >90 | - |
