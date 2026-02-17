# SaaS Templates

Templates de production pour lancer des SaaS IA rapidement avec Claude Code.

## Philosophie

- **Produit fini, pas MVP** — Chaque template inclut error handling, sécurité, edge cases
- **Claude Code ready** — Documentation structurée pour exécution parfaite
- **Copier, pas dépendre** — Chaque projet reste autonome, zéro couplage

## Structure

```
saas-templates/
├── docs-templates/      → 26 templates de documentation
├── backend-starter/     → FastAPI + Celery + Supabase
├── frontend-starter/    → Next.js 14 + TypeScript + Tailwind
├── legal-templates/     → CGU, Privacy, GDPR
├── deploy-configs/      → Railway, Vercel, GitHub Actions
├── stripe-templates/    → Webhooks, Checkout, Setup
└── scripts/             → Automatisation création projet
```

## Utilisation

### Créer un nouveau projet

```bash
./scripts/new-project.sh nom-du-projet
```

Ou manuellement :

1. Copier `backend-starter/` → `nouveau-projet/backend/`
2. Copier `frontend-starter/` → `nouveau-projet/frontend/`
3. Copier `docs-templates/` → `nouveau-projet/docs/`
4. Renommer les `.template.md` en `.md`
5. Adapter chaque fichier au projet

### Ordre de remplissage des docs

```
── FONDATIONS ──
1. context.md        → Vision, personas, décisions
2. CLAUDE.md         → Règles Claude Code (adapter si besoin)
3. SPEC.md           → Features, flows, edge cases
4. ARCH.md           → DB, API, structure

── TECHNIQUE ──
5. SECURITY.md       → Auth, validation, rate limiting
6. ERRORS.md         → Catalogue erreurs
7. ENV.md            → Variables d'environnement
8. STRUCTURE.md      → Organisation fichiers/dossiers
9. API.md            → Documentation API

── PRODUIT ──
10. UI.md            → Composants, états, responsive
11. COPY.md          → Tous les textes
12. ONBOARDING.md    → Parcours activation utilisateur
13. EMAILS.md        → Emails transactionnels
14. PRICING.md       → Plans, limites, Stripe mapping

── QUALITÉ ──
15. TESTS.md         → Stratégie tests
16. PERFORMANCE.md   → Benchmarks, optimisation, load testing

── OPÉRATIONS ──
17. DEPLOY.md        → Config prod
18. ANALYTICS.md     → Events tracking
19. MONITORING.md    → Alertes, runbooks
20. MIGRATIONS.md    → Stratégie DB
21. BACKUP.md        → Backup/restore

── PROJET ──
22. CONTRIBUTING.md  → Guide contribution
23. CHANGELOG.md     → Versioning
24. ROADMAP.md       → Évolutions prévues
25. TASKS.md         → Tâches en cours
26. README.md        → Présentation projet
```

## Stack technique

| Couche | Technologie | Version |
|--------|-------------|---------|
| Backend | FastAPI | 0.109+ |
| Python | Python | 3.12+ |
| Queue | Celery + Redis | 5.3+ |
| Frontend | Next.js | 14.x |
| TypeScript | TypeScript | 5.x |
| CSS | Tailwind | 3.x |
| Database | Supabase PostgreSQL | - |
| Auth | Supabase Auth | - |
| Paiement | Stripe | - |
| Backend hosting | Railway | - |
| Frontend hosting | Vercel | - |
| Monitoring | Sentry + LangSmith | - |

## Conventions

### Naming

| Contexte | Convention | Exemple |
|----------|------------|---------|
| Python variables/fonctions | snake_case | `user_email` |
| Python classes | PascalCase | `UserService` |
| TypeScript variables/fonctions | camelCase | `userEmail` |
| TypeScript composants/types | PascalCase | `UserCard` |
| Fichiers Python | snake_case | `user_service.py` |
| Fichiers TypeScript | kebab-case | `user-card.tsx` |
| Tables DB | snake_case pluriel | `users`, `audit_reports` |
| Colonnes DB | snake_case | `created_at` |
| Endpoints API | kebab-case | `/api/v1/user-reports` |

### Git

- Commits conventionnels : `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`
- Une feature = une branche = une PR
- Jamais de push direct sur `main`

## Checklist pré-launch

- [ ] Tous les `.env` configurés (prod)
- [ ] HTTPS forcé
- [ ] Rate limiting actif
- [ ] Logs structurés
- [ ] Monitoring configuré
- [ ] Backups automatiques
- [ ] CGU/Privacy en place
- [ ] Stripe webhooks testés
- [ ] Tests E2E passent
- [ ] SEO meta tags
- [ ] OG images
- [ ] Favicon
- [ ] 404/500 pages custom
- [ ] Mobile responsive vérifié
