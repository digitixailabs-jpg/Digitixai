# Context — [NOM_PROJET]

> Ce document définit la vision, le contexte business et les décisions fondamentales du projet.
> À remplir AVANT tout développement.

---

## Vision

### En une phrase
[À_COMPLÉTER : Quel problème résout-on, pour qui, en quoi c'est mieux que l'existant ?]

### Pourquoi maintenant ?
[À_COMPLÉTER : Quel changement de marché/techno rend ce projet viable aujourd'hui ?]

---

## Proposition de valeur

| Élément | Description |
|---------|-------------|
| **Input utilisateur** | [Ce que l'user fournit] |
| **Output livré** | [Ce qu'il obtient] |
| **Temps de livraison** | [En combien de temps] |
| **Prix** | [Combien ça coûte] |
| **Avant/Après** | [Ce qu'il faisait avant vs maintenant] |

---

## Personas

### Persona principal (80% des users)

| Attribut | Description |
|----------|-------------|
| **Qui** | [Rôle, taille entreprise, contexte] |
| **Douleur principale** | [Le problème urgent qu'il veut résoudre] |
| **Douleurs secondaires** | [Autres frustrations] |
| **Alternative actuelle** | [Comment il gère ça aujourd'hui] |
| **Coût de l'alternative** | [En temps, argent, frustration] |
| **Déclencheur d'achat** | [Moment où il cherche une solution] |
| **Budget disponible** | [Fourchette acceptable] |
| **Objections prévisibles** | [Pourquoi il hésiterait] |

### Persona secondaire (si applicable)

[À_COMPLÉTER si pertinent]

---

## Business model

### Pricing

| Tier | Prix | Inclus | Cible |
|------|------|--------|-------|
| [Tier 1] | [X€/mois ou X€/unité] | [Features] | [Qui] |
| [Tier 2] | [X€/mois ou X€/unité] | [Features] | [Qui] |
| [Tier 3] | [X€/mois ou X€/unité] | [Features] | [Qui] |

### Unit economics

| Métrique | Valeur cible | Notes |
|----------|--------------|-------|
| **Coût d'acquisition (CAC)** | [X€] | |
| **Coût marginal par user/action** | [X€] | [Détail LLM, infra] |
| **Prix moyen** | [X€] | |
| **Marge brute** | [X%] | |
| **LTV cible** | [X€] | |
| **LTV/CAC cible** | [>3x] | |

### Revenus projetés

| Mois | Users payants | MRR | Notes |
|------|---------------|-----|-------|
| M1 | | | Launch |
| M3 | | | |
| M6 | | | |
| M12 | | | |

---

## Marché

### Taille

| Segment | TAM | SAM | SOM |
|---------|-----|-----|-----|
| [Segment] | [X€] | [X€] | [X€] |

### Concurrence

| Concurrent | Forces | Faiblesses | Notre différenciation |
|------------|--------|------------|----------------------|
| [Nom] | | | |
| [Nom] | | | |
| Alternative DIY | | | |

### Tendances favorables

1. [Tendance 1 et pourquoi elle nous aide]
2. [Tendance 2]
3. [Tendance 3]

### Risques marché

| Risque | Probabilité | Impact | Mitigation |
|--------|-------------|--------|------------|
| [Risque] | [H/M/L] | [H/M/L] | [Action] |

---

## Décisions techniques

### Choix structurants

| Décision | Choix retenu | Pourquoi | Alternative rejetée | Pourquoi rejetée |
|----------|--------------|----------|---------------------|------------------|
| Database | Supabase | Auth intégré, RLS, realtime | Firebase | Vendor lock-in, pricing opaque |
| Backend | FastAPI | Perf, typing, async natif | Django | Overhead, moins flexible |
| Frontend | Next.js 14 | App Router, RSC, SEO | Remix | Écosystème plus petit |
| LLM | Claude API | Qualité, contexte long | GPT-4 | Coût, moins fiable |
| Queue | Celery + Redis | Mature, fiable | Dramatiq | Moins de docs |
| Hosting backend | Railway | DX, pricing simple | AWS | Complexité |
| Hosting frontend | Vercel | Intégration Next.js | Netlify | Moins optimisé Next |

### Principes d'architecture

1. **Séparation stricte** : Backend API pure, Frontend consomme l'API
2. **Stateless backend** : Aucun état en mémoire, tout en DB/Redis
3. **Jobs async** : Tout traitement >500ms passe par Celery
4. **Fail gracefully** : Toujours un fallback si service externe down

---

## Dépendances externes

| Service | Usage | Criticité | SLA | Fallback | Coût estimé |
|---------|-------|-----------|-----|----------|-------------|
| Supabase | DB + Auth | Critique | 99.9% | - | [X€/mois] |
| Claude API | [Usage] | Critique | 99% | OpenAI | [X€/mois] |
| Stripe | Paiement | Critique | 99.99% | - | 2.9% + 0.30€ |
| Redis (Railway) | Queue broker | Haute | 99.9% | - | [X€/mois] |
| [Autre] | | | | | |

---

## État actuel du projet

### Phase actuelle

- [ ] **Phase 1 — Cadrage** : context.md, CLAUDE.md, SPEC.md
- [ ] **Phase 2 — Architecture** : ARCH.md, SECURITY.md, ERRORS.md
- [ ] **Phase 3 — UI/Contenu** : UI.md, COPY.md
- [ ] **Phase 4 — Planification** : TASKS.md, TESTS.md, DEPLOY.md
- [ ] **Phase 5 — Backend dev**
- [ ] **Phase 6 — Frontend dev**
- [ ] **Phase 7 — Tests & QA**
- [ ] **Phase 8 — Deploy & Launch**

### Historique des décisions importantes

| Date | Décision | Contexte | Impact |
|------|----------|----------|--------|
| [Date] | [Décision] | [Pourquoi] | [Conséquence] |

---

## Liens et ressources

| Ressource | URL |
|-----------|-----|
| Repository | [À_COMPLÉTER] |
| Production | [À_COMPLÉTER] |
| Staging | [À_COMPLÉTER] |
| Supabase Dashboard | [À_COMPLÉTER] |
| Stripe Dashboard | [À_COMPLÉTER] |
| Railway Dashboard | [À_COMPLÉTER] |
| Vercel Dashboard | [À_COMPLÉTER] |
| Sentry | [À_COMPLÉTER] |
| Analytics | [À_COMPLÉTER] |

---

## Objectifs de lancement

### Critères de succès V1

| Critère | Cible | Mesure |
|---------|-------|--------|
| Time to market | [X jours] | Date de launch |
| Coût de dev | [<X€] | Budget consommé |
| Premier € | [Semaine X] | Date première transaction |
| Users M1 | [X] | Comptes créés |
| Paying users M1 | [X] | Conversions |

### Ce qui est OUT of scope V1

1. [Feature explicitement exclue]
2. [Feature explicitement exclue]
3. [Feature explicitement exclue]

---

## Notes et réflexions

[Espace libre pour notes, idées, questions ouvertes]
