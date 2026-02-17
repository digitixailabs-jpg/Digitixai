# Stratégie de Tests — [NOM_PROJET]

> Ce document définit la stratégie de tests et les cas critiques à couvrir.

---

## Philosophie

### Pyramide de tests

```
        ▲
       /E2E\         ← Peu, lents, critiques
      /─────\
     / Integ \       ← Modéré, API + DB
    /─────────\
   /   Unit    \     ← Beaucoup, rapides
  /─────────────\
```

### Règles

1. **Test ce qui peut casser** : Logique métier, pas les getters
2. **Test les edge cases** : Null, vide, limites
3. **Test les erreurs** : Vérifier que les erreurs sont gérées
4. **Pas de tests fragiles** : Pas de dépendance à l'ordre ou au timing

---

## Backend (Python/pytest)

### Configuration

```python
# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def auth_headers(client):
    # Login et retourner headers avec token
    response = client.post("/api/v1/auth/login", json={
        "email": "test@example.com",
        "password": "testpassword123"
    })
    token = response.json()["data"]["access_token"]
    return {"Authorization": f"Bearer {token}"}
```

### Structure

```
tests/
├── conftest.py           # Fixtures partagées
├── unit/
│   ├── test_services.py  # Tests logique métier
│   └── test_utils.py     # Tests utilitaires
├── integration/
│   ├── test_api.py       # Tests endpoints
│   └── test_db.py        # Tests requêtes DB
└── e2e/
    └── test_flows.py     # Tests parcours complets
```

### Commandes

```bash
# Tous les tests
pytest

# Avec coverage
pytest --cov=app --cov-report=html

# Tests spécifiques
pytest tests/unit/
pytest tests/integration/ -k "test_create"

# Verbose
pytest -v

# Stop au premier échec
pytest -x
```

---

## Frontend (Vitest + Testing Library)

### Configuration

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: './tests/setup.ts',
  },
});
```

```typescript
// tests/setup.ts
import '@testing-library/jest-dom';
import { vi } from 'vitest';

// Mock next/navigation
vi.mock('next/navigation', () => ({
  useRouter: () => ({ push: vi.fn() }),
  usePathname: () => '/',
}));
```

### Structure

```
tests/
├── setup.ts
├── components/
│   ├── Button.test.tsx
│   └── Form.test.tsx
├── hooks/
│   └── useAuth.test.ts
└── pages/
    └── dashboard.test.tsx
```

### Commandes

```bash
# Tous les tests
npm run test

# Watch mode
npm run test:watch

# Coverage
npm run test:coverage

# UI
npm run test:ui
```

---

## Cas critiques à tester

### Authentification

| Cas | Type | Priorité |
|-----|------|----------|
| Login avec credentials valides | Integration | P0 |
| Login avec mauvais password | Integration | P0 |
| Login avec email inexistant | Integration | P0 |
| Accès route protégée sans token | Integration | P0 |
| Accès route protégée avec token expiré | Integration | P0 |
| Refresh token | Integration | P1 |
| Logout | Integration | P1 |
| Register avec email existant | Integration | P0 |
| Password reset flow | E2E | P1 |

### [Feature principale]

| Cas | Type | Priorité |
|-----|------|----------|
| Création [ressource] valide | Integration | P0 |
| Création avec données invalides | Integration | P0 |
| Lecture [ressource] existante | Integration | P0 |
| Lecture [ressource] inexistante | Integration | P0 |
| Lecture [ressource] d'un autre user | Integration | P0 |
| Update [ressource] | Integration | P1 |
| Delete [ressource] | Integration | P1 |
| Liste avec pagination | Integration | P1 |
| Liste vide | Integration | P1 |
| [Edge case métier 1] | Unit | P0 |
| [Edge case métier 2] | Unit | P0 |

### Paiement

| Cas | Type | Priorité |
|-----|------|----------|
| Checkout session création | Integration | P0 |
| Webhook payment_intent.succeeded | Integration | P0 |
| Webhook payment_intent.failed | Integration | P0 |
| Vérification signature webhook | Unit | P0 |
| Subscription créée après paiement | Integration | P0 |
| Accès features premium après paiement | E2E | P1 |

### UI (Frontend)

| Cas | Type | Priorité |
|-----|------|----------|
| Form validation affiche erreurs | Component | P0 |
| Loading state pendant submit | Component | P1 |
| Error state après échec | Component | P0 |
| Empty state quand liste vide | Component | P1 |
| Navigation mobile | E2E | P1 |
| Responsive sur mobile | E2E | P2 |

---

## Exemples de tests

### Unit test (Backend)

```python
# tests/unit/test_services.py
import pytest
from app.services.report_service import calculate_score

def test_calculate_score_perfect():
    """Score parfait quand tous les critères OK"""
    criteria = {"clarity": 10, "trust": 10, "cta": 10}
    assert calculate_score(criteria) == 100

def test_calculate_score_empty():
    """Score 0 quand aucun critère"""
    assert calculate_score({}) == 0

def test_calculate_score_partial():
    """Score proportionnel"""
    criteria = {"clarity": 5, "trust": 10}
    expected = (5 + 10) / 20 * 100  # 75%
    assert calculate_score(criteria) == expected
```

### Integration test (Backend)

```python
# tests/integration/test_reports_api.py
import pytest

def test_create_report_success(client, auth_headers):
    """Création rapport avec données valides"""
    response = client.post(
        "/api/v1/reports",
        json={"url": "https://example.com", "type": "full"},
        headers=auth_headers
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True
    assert "id" in data["data"]
    assert data["data"]["status"] == "pending"

def test_create_report_invalid_url(client, auth_headers):
    """Erreur validation si URL invalide"""
    response = client.post(
        "/api/v1/reports",
        json={"url": "not-a-url", "type": "full"},
        headers=auth_headers
    )
    
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "VALIDATION_INVALID_URL"

def test_create_report_unauthorized(client):
    """Erreur 401 sans authentification"""
    response = client.post(
        "/api/v1/reports",
        json={"url": "https://example.com", "type": "full"}
    )
    
    assert response.status_code == 401
```

### Component test (Frontend)

```typescript
// tests/components/LoginForm.test.tsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { LoginForm } from '@/components/forms/login-form';
import { vi } from 'vitest';

describe('LoginForm', () => {
  it('shows validation error for invalid email', async () => {
    render(<LoginForm onSubmit={vi.fn()} />);
    
    const emailInput = screen.getByLabelText(/email/i);
    fireEvent.change(emailInput, { target: { value: 'invalid' } });
    fireEvent.blur(emailInput);
    
    await waitFor(() => {
      expect(screen.getByText(/email invalide/i)).toBeInTheDocument();
    });
  });

  it('calls onSubmit with valid data', async () => {
    const mockSubmit = vi.fn();
    render(<LoginForm onSubmit={mockSubmit} />);
    
    fireEvent.change(screen.getByLabelText(/email/i), {
      target: { value: 'test@example.com' }
    });
    fireEvent.change(screen.getByLabelText(/mot de passe/i), {
      target: { value: 'password123' }
    });
    fireEvent.click(screen.getByRole('button', { name: /connexion/i }));
    
    await waitFor(() => {
      expect(mockSubmit).toHaveBeenCalledWith({
        email: 'test@example.com',
        password: 'password123'
      });
    });
  });

  it('shows loading state during submission', async () => {
    const mockSubmit = vi.fn(() => new Promise(() => {})); // Never resolves
    render(<LoginForm onSubmit={mockSubmit} />);
    
    // Fill and submit
    fireEvent.change(screen.getByLabelText(/email/i), {
      target: { value: 'test@example.com' }
    });
    fireEvent.change(screen.getByLabelText(/mot de passe/i), {
      target: { value: 'password123' }
    });
    fireEvent.click(screen.getByRole('button', { name: /connexion/i }));
    
    await waitFor(() => {
      expect(screen.getByRole('button')).toBeDisabled();
      expect(screen.getByText(/chargement/i)).toBeInTheDocument();
    });
  });
});
```

---

## Coverage cibles

| Couche | Minimum | Idéal |
|--------|---------|-------|
| Services (logique métier) | 80% | 95% |
| API endpoints | 70% | 85% |
| Components UI | 60% | 80% |
| Utils/Helpers | 90% | 100% |

---

## CI/CD Integration

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: pip install -r backend/requirements.txt
      - run: cd backend && pytest --cov=app --cov-fail-under=70

  frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: cd frontend && npm ci
      - run: cd frontend && npm run test:coverage
```

---

## Mocking

### Backend - Services externes

```python
# tests/conftest.py
from unittest.mock import AsyncMock, patch

@pytest.fixture
def mock_anthropic():
    with patch('app.services.llm_service.client') as mock:
        mock.messages.create = AsyncMock(return_value={
            "content": [{"text": "Mocked response"}]
        })
        yield mock

def test_analysis_with_mocked_llm(client, auth_headers, mock_anthropic):
    response = client.post("/api/v1/analyze", ...)
    # LLM non appelé réellement
```

### Frontend - API

```typescript
// tests/mocks/handlers.ts
import { http, HttpResponse } from 'msw';

export const handlers = [
  http.get('/api/v1/profile', () => {
    return HttpResponse.json({
      success: true,
      data: { id: '1', email: 'test@example.com' }
    });
  }),
  
  http.post('/api/v1/reports', () => {
    return HttpResponse.json({
      success: true,
      data: { id: 'new-report-id', status: 'pending' }
    }, { status: 201 });
  }),
];
```
