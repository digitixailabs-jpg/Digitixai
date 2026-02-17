# Contributing — [NOM_PROJET]

> Ce document décrit comment contribuer au projet.
> À lire avant toute PR.

---

## Prérequis

- Python 3.12+
- Node.js 20+
- Redis (local ou Docker)
- Compte Supabase (dev)
- Git

---

## Setup local

### 1. Cloner le repo

```bash
git clone https://github.com/[org]/[nom-projet].git
cd [nom-projet]
```

### 2. Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Éditer .env avec les valeurs de dev
```

### 3. Frontend

```bash
cd frontend
npm install
cp .env.example .env.local
# Éditer .env.local avec les valeurs de dev
```

### 4. Lancer en local

```bash
# Terminal 1 — Redis
docker run -d -p 6379:6379 redis:alpine

# Terminal 2 — Backend
cd backend && uvicorn app.main:app --reload --port 8000

# Terminal 3 — Celery
cd backend && celery -A app.workers.celery worker --loglevel=info

# Terminal 4 — Frontend
cd frontend && npm run dev
```

---

## Workflow Git

### Branches

| Branche | Usage | Protection |
|---------|-------|-----------|
| `main` | Production | Protégée — merge via PR uniquement |
| `develop` | Staging / intégration | Protégée — merge via PR |
| `feat/[nom]` | Nouvelle feature | Libre |
| `fix/[nom]` | Bugfix | Libre |
| `refactor/[nom]` | Refactoring | Libre |
| `docs/[nom]` | Documentation | Libre |

### Flow

```
1. Créer une branche depuis develop
   git checkout develop
   git pull origin develop
   git checkout -b feat/ma-feature

2. Développer + committer (voir conventions ci-dessous)

3. Pousser la branche
   git push origin feat/ma-feature

4. Ouvrir une PR vers develop

5. Review + merge

6. develop → main via PR quand release ready
```

---

## Conventions de commit

Format : **Conventional Commits**

```
<type>(<scope>): <description>

[body optionnel]

[footer optionnel]
```

### Types

| Type | Usage | Exemple |
|------|-------|---------|
| `feat` | Nouvelle feature | `feat(auth): add Google OAuth login` |
| `fix` | Bugfix | `fix(api): handle null payload in webhook` |
| `docs` | Documentation | `docs(api): update endpoint examples` |
| `refactor` | Refactoring (pas de changement fonctionnel) | `refactor(services): extract billing logic` |
| `test` | Ajout/modification de tests | `test(diff): add edge case for nested arrays` |
| `chore` | Maintenance, deps, CI | `chore(deps): bump fastapi to 0.110` |
| `style` | Formatting, linting (pas de changement de code) | `style(backend): run ruff format` |
| `perf` | Amélioration performance | `perf(api): add Redis cache on GET /endpoints` |

### Règles

- Description en anglais, impératif, minuscule : "add feature" pas "Added feature"
- Scope optionnel mais recommandé : `(auth)`, `(api)`, `(ui)`, `(db)`
- Première ligne < 72 caractères
- Body : pourquoi le changement (pas comment — le code montre le comment)

---

## Standards de code

### Python (Backend)

| Règle | Outil |
|-------|-------|
| Formatting | `ruff format` |
| Linting | `ruff check` |
| Type hints | Requis sur toutes les fonctions publiques |
| Docstrings | Requises sur les services et endpoints |
| Tests | Requis pour toute nouvelle feature |

```bash
# Vérifier avant de committer
cd backend
ruff format .
ruff check .
pytest
```

### TypeScript (Frontend)

| Règle | Outil |
|-------|-------|
| Formatting | `prettier` |
| Linting | `eslint` |
| Types | Strict mode — pas de `any` sauf justification |
| Composants | Functional components + hooks uniquement |

```bash
# Vérifier avant de committer
cd frontend
npm run lint
npm run type-check
npm run test
```

---

## Tests

### Backend — requis pour chaque PR

```bash
cd backend
pytest                          # Tous les tests
pytest --cov=app                # Avec coverage
pytest -x                       # Stop au premier échec
```

### Frontend — requis pour chaque PR

```bash
cd frontend
npm run test                    # Unit tests
npm run test:e2e                # E2E (si applicable)
```

### Coverage minimum

| Module | Minimum requis |
|--------|---------------|
| Services critiques | 100% |
| Endpoints API | 85% |
| Backend global | 80% |
| Frontend composants | 70% |

---

## Checklist PR

Avant de soumettre une PR, vérifier :

### Code
- [ ] Le code compile sans erreur
- [ ] `ruff format` + `ruff check` passent (backend)
- [ ] `npm run lint` + `npm run type-check` passent (frontend)
- [ ] Pas de `console.log` / `print()` oubliés
- [ ] Pas de secrets ou données sensibles
- [ ] Pas de `TODO` sans issue associée

### Tests
- [ ] Tests ajoutés pour les nouvelles features
- [ ] Tests existants passent toujours
- [ ] Coverage minimum respecté

### Documentation
- [ ] CHANGELOG.md mis à jour
- [ ] docs/ mis à jour si changement d'API, architecture, ou comportement
- [ ] context.md mis à jour si décision architecturale

### PR description
- [ ] Titre clair (format conventional commit)
- [ ] Description du POURQUOI (pas juste le quoi)
- [ ] Screenshots si changement UI
- [ ] Lien vers l'issue/task si applicable

---

## Structure d'une PR

```markdown
## Description

[Pourquoi ce changement ? Quel problème ça résout ?]

## Changements

- [Changement 1]
- [Changement 2]

## Tests

- [Comment tester ce changement]

## Screenshots (si UI)

[Avant / Après]

## Checklist

- [ ] Tests ajoutés
- [ ] Documentation mise à jour
- [ ] Lint/format OK
```
