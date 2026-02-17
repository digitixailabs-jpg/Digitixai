# API Documentation — [NOM_PROJET]

> Documentation complète de l'API REST.
> Version: 1.0.0 | Base URL: `https://api.[nom].com/api/v1`

---

## Authentification

### Type
Bearer Token (JWT Supabase)

### Obtenir un token

```bash
# Via Supabase Auth (frontend)
const { data: { session } } = await supabase.auth.getSession()
const token = session.access_token
```

### Utiliser le token

```bash
curl -X GET "https://api.[nom].com/api/v1/profile" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Erreurs d'authentification

| Status | Code | Description |
|--------|------|-------------|
| 401 | `AUTH_UNAUTHORIZED` | Token manquant |
| 401 | `AUTH_TOKEN_EXPIRED` | Token expiré |
| 401 | `AUTH_TOKEN_INVALID` | Token invalide |
| 403 | `AUTH_FORBIDDEN` | Permissions insuffisantes |

---

## Format des réponses

### Succès

```json
{
  "success": true,
  "data": { ... },
  "meta": {
    "page": 1,
    "limit": 20,
    "total": 150
  }
}
```

### Erreur

```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable message",
    "details": { ... }
  }
}
```

---

## Rate Limiting

| Endpoint | Limite | Fenêtre |
|----------|--------|---------|
| Authentifié | 100 req | 1 minute |
| Non authentifié | 20 req | 1 minute |

Headers de réponse :
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1642000000
```

Si limite atteinte : `429 Too Many Requests`

---

## Endpoints

### Profile

#### GET /profile

Récupère le profil de l'utilisateur connecté.

**Auth required**: Yes

**Response** `200 OK`
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "email": "user@example.com",
    "full_name": "John Doe",
    "avatar_url": "https://...",
    "subscription_status": "active",
    "subscription_tier": "pro",
    "credits_remaining": 100,
    "created_at": "2026-01-15T10:30:00Z"
  }
}
```

---

#### PATCH /profile

Met à jour le profil de l'utilisateur.

**Auth required**: Yes

**Request body**
```json
{
  "full_name": "Jane Doe",
  "avatar_url": "https://..."
}
```

| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| full_name | string | No | Max 255 chars |
| avatar_url | string | No | Valid URL |

**Response** `200 OK`
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "full_name": "Jane Doe",
    ...
  }
}
```

**Errors**
| Status | Code | Condition |
|--------|------|-----------|
| 422 | `VALIDATION_ERROR` | Invalid data |

---

### [Feature] Resources

#### POST /[resources]

Crée une nouvelle ressource.

**Auth required**: Yes

**Request body**
```json
{
  "field_1": "value",
  "field_2": "value"
}
```

| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| field_1 | string | Yes | Max 255 chars |
| field_2 | string | No | - |

**Response** `201 Created`
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "field_1": "value",
    "field_2": "value",
    "status": "pending",
    "created_at": "2026-01-15T10:30:00Z"
  }
}
```

**Errors**
| Status | Code | Condition |
|--------|------|-----------|
| 400 | `VALIDATION_ERROR` | Invalid input |
| 401 | `AUTH_UNAUTHORIZED` | Not authenticated |
| 429 | `QUOTA_EXCEEDED` | Limit reached |

---

#### GET /[resources]

Liste les ressources de l'utilisateur.

**Auth required**: Yes

**Query parameters**
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| page | integer | 1 | Page number |
| limit | integer | 20 | Items per page (max 100) |
| status | string | - | Filter by status |
| sort | string | -created_at | Sort field (prefix `-` for desc) |

**Example**
```bash
GET /api/v1/resources?page=1&limit=10&status=completed&sort=-created_at
```

**Response** `200 OK`
```json
{
  "success": true,
  "data": [
    {
      "id": "uuid",
      "field_1": "value",
      "status": "completed",
      "created_at": "2026-01-15T10:30:00Z"
    }
  ],
  "meta": {
    "page": 1,
    "limit": 10,
    "total": 45,
    "total_pages": 5
  }
}
```

---

#### GET /[resources]/{id}

Récupère une ressource spécifique.

**Auth required**: Yes

**Path parameters**
| Param | Type | Description |
|-------|------|-------------|
| id | uuid | Resource ID |

**Response** `200 OK`
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "field_1": "value",
    "field_2": "value",
    "status": "completed",
    "result": { ... },
    "created_at": "2026-01-15T10:30:00Z",
    "updated_at": "2026-01-15T11:00:00Z"
  }
}
```

**Errors**
| Status | Code | Condition |
|--------|------|-----------|
| 404 | `RESOURCE_NOT_FOUND` | Resource doesn't exist |
| 403 | `AUTH_FORBIDDEN` | Not owner |

---

#### PATCH /[resources]/{id}

Met à jour une ressource.

**Auth required**: Yes

**Path parameters**
| Param | Type | Description |
|-------|------|-------------|
| id | uuid | Resource ID |

**Request body**
```json
{
  "field_1": "new value"
}
```

**Response** `200 OK`
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "field_1": "new value",
    ...
  }
}
```

---

#### DELETE /[resources]/{id}

Supprime une ressource.

**Auth required**: Yes

**Path parameters**
| Param | Type | Description |
|-------|------|-------------|
| id | uuid | Resource ID |

**Response** `204 No Content`

**Errors**
| Status | Code | Condition |
|--------|------|-----------|
| 404 | `RESOURCE_NOT_FOUND` | Resource doesn't exist |
| 403 | `AUTH_FORBIDDEN` | Not owner |

---

### Billing

#### POST /billing/checkout

Crée une session Stripe Checkout.

**Auth required**: Yes

**Request body**
```json
{
  "price_id": "price_xxx",
  "success_url": "https://app.example.com/success",
  "cancel_url": "https://app.example.com/pricing"
}
```

**Response** `200 OK`
```json
{
  "success": true,
  "data": {
    "checkout_url": "https://checkout.stripe.com/..."
  }
}
```

---

#### POST /billing/portal

Crée une session Stripe Customer Portal.

**Auth required**: Yes

**Request body**
```json
{
  "return_url": "https://app.example.com/settings"
}
```

**Response** `200 OK`
```json
{
  "success": true,
  "data": {
    "portal_url": "https://billing.stripe.com/..."
  }
}
```

---

### Webhooks

#### POST /webhooks/stripe

Reçoit les événements Stripe.

**Auth**: Stripe signature (header `stripe-signature`)

**Events handled**
| Event | Action |
|-------|--------|
| `checkout.session.completed` | Create/update subscription |
| `invoice.paid` | Extend subscription |
| `invoice.payment_failed` | Mark payment failed |
| `customer.subscription.deleted` | Cancel subscription |

**Response** `200 OK`
```json
{
  "received": true
}
```

---

## Health Check

#### GET /health

Vérifie l'état de l'API.

**Auth required**: No

**Response** `200 OK`
```json
{
  "status": "healthy",
  "checks": {
    "api": "ok",
    "database": "ok",
    "redis": "ok"
  }
}
```

**Response** `503 Service Unavailable` (si un check fail)
```json
{
  "status": "degraded",
  "checks": {
    "api": "ok",
    "database": "error",
    "redis": "ok"
  }
}
```

---

## Codes d'erreur

Voir `docs/ERRORS.md` pour la liste complète.

| Code | HTTP | Description |
|------|------|-------------|
| `AUTH_UNAUTHORIZED` | 401 | Authentication required |
| `AUTH_FORBIDDEN` | 403 | Insufficient permissions |
| `VALIDATION_ERROR` | 422 | Invalid input data |
| `RESOURCE_NOT_FOUND` | 404 | Resource doesn't exist |
| `QUOTA_EXCEEDED` | 429 | Usage limit reached |
| `INTERNAL_ERROR` | 500 | Server error |

---

## SDKs & Examples

### cURL

```bash
# Get profile
curl -X GET "https://api.[nom].com/api/v1/profile" \
  -H "Authorization: Bearer $TOKEN"

# Create resource
curl -X POST "https://api.[nom].com/api/v1/resources" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"field_1": "value"}'
```

### JavaScript/TypeScript

```typescript
const API_URL = 'https://api.[nom].com/api/v1';

async function createResource(token: string, data: CreateResourceInput) {
  const response = await fetch(`${API_URL}/resources`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });
  
  return response.json();
}
```

### Python

```python
import requests

API_URL = 'https://api.[nom].com/api/v1'

def create_resource(token: str, data: dict):
    response = requests.post(
        f'{API_URL}/resources',
        headers={'Authorization': f'Bearer {token}'},
        json=data
    )
    return response.json()
```

---

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-15 | Initial release |
