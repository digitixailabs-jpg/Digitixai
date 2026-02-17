# Catalogue des Erreurs — [NOM_PROJET]

> Ce document liste TOUTES les erreurs possibles, leurs codes, messages et comportements.
> Chaque erreur doit être documentée avant d'être implémentée.

---

## Conventions

### Format code erreur

```
[DOMAIN]_[CATEGORY]_[SPECIFIC]
```

Exemples :
- `AUTH_INVALID_CREDENTIALS`
- `PAYMENT_CARD_DECLINED`
- `RESOURCE_NOT_FOUND`

### Format réponse erreur

```json
{
  "success": false,
  "error": {
    "code": "AUTH_INVALID_CREDENTIALS",
    "message": "Email ou mot de passe incorrect.",
    "details": {
      "field": "password"
    }
  }
}
```

---

## Erreurs Authentification (AUTH_*)

### AUTH_INVALID_CREDENTIALS

| Attribut | Valeur |
|----------|--------|
| HTTP Status | 401 |
| Code | `AUTH_INVALID_CREDENTIALS` |
| Message FR | Email ou mot de passe incorrect. |
| Message EN | Invalid email or password. |
| Cause | Login avec mauvais email/password |
| Action user | Vérifier email et mot de passe |
| Log level | INFO |

### AUTH_EMAIL_EXISTS

| Attribut | Valeur |
|----------|--------|
| HTTP Status | 409 |
| Code | `AUTH_EMAIL_EXISTS` |
| Message FR | Un compte existe déjà avec cet email. |
| Message EN | An account already exists with this email. |
| Cause | Inscription avec email existant |
| Action user | Se connecter ou utiliser un autre email |
| Log level | INFO |

### AUTH_TOKEN_EXPIRED

| Attribut | Valeur |
|----------|--------|
| HTTP Status | 401 |
| Code | `AUTH_TOKEN_EXPIRED` |
| Message FR | Votre session a expiré. Veuillez vous reconnecter. |
| Message EN | Your session has expired. Please log in again. |
| Cause | JWT expiré |
| Action user | Auto-redirect vers login |
| Log level | DEBUG |

### AUTH_TOKEN_INVALID

| Attribut | Valeur |
|----------|--------|
| HTTP Status | 401 |
| Code | `AUTH_TOKEN_INVALID` |
| Message FR | Session invalide. Veuillez vous reconnecter. |
| Message EN | Invalid session. Please log in again. |
| Cause | JWT malformé ou signature invalide |
| Action user | Auto-redirect vers login |
| Log level | WARN |

### AUTH_UNAUTHORIZED

| Attribut | Valeur |
|----------|--------|
| HTTP Status | 401 |
| Code | `AUTH_UNAUTHORIZED` |
| Message FR | Vous devez être connecté pour accéder à cette page. |
| Message EN | You must be logged in to access this page. |
| Cause | Accès ressource protégée sans auth |
| Action user | Redirect vers login avec return URL |
| Log level | DEBUG |

### AUTH_FORBIDDEN

| Attribut | Valeur |
|----------|--------|
| HTTP Status | 403 |
| Code | `AUTH_FORBIDDEN` |
| Message FR | Vous n'avez pas accès à cette ressource. |
| Message EN | You don't have access to this resource. |
| Cause | User n'a pas les permissions requises |
| Action user | Contacter support si erreur |
| Log level | WARN |

### AUTH_EMAIL_NOT_VERIFIED

| Attribut | Valeur |
|----------|--------|
| HTTP Status | 403 |
| Code | `AUTH_EMAIL_NOT_VERIFIED` |
| Message FR | Veuillez vérifier votre email avant de continuer. |
| Message EN | Please verify your email to continue. |
| Cause | Email non confirmé |
| Action user | Cliquer sur lien dans email ou renvoyer |
| Log level | INFO |

### AUTH_RESET_TOKEN_EXPIRED

| Attribut | Valeur |
|----------|--------|
| HTTP Status | 400 |
| Code | `AUTH_RESET_TOKEN_EXPIRED` |
| Message FR | Ce lien a expiré. Demandez un nouveau lien de réinitialisation. |
| Message EN | This link has expired. Request a new reset link. |
| Cause | Reset password link expiré (>1h) |
| Action user | Redemander un reset |
| Log level | INFO |

### AUTH_PASSWORD_TOO_WEAK

| Attribut | Valeur |
|----------|--------|
| HTTP Status | 422 |
| Code | `AUTH_PASSWORD_TOO_WEAK` |
| Message FR | Le mot de passe doit contenir au moins 8 caractères. |
| Message EN | Password must be at least 8 characters. |
| Cause | Password ne respecte pas les règles |
| Action user | Choisir un mot de passe plus fort |
| Log level | DEBUG |

---

## Erreurs Validation (VALIDATION_*)

### VALIDATION_REQUIRED

| Attribut | Valeur |
|----------|--------|
| HTTP Status | 422 |
| Code | `VALIDATION_REQUIRED` |
| Message FR | Ce champ est requis. |
| Message EN | This field is required. |
| Details | `{ "field": "field_name" }` |
| Cause | Champ obligatoire manquant |
| Action user | Remplir le champ |
| Log level | DEBUG |

### VALIDATION_EMAIL_FORMAT

| Attribut | Valeur |
|----------|--------|
| HTTP Status | 422 |
| Code | `VALIDATION_EMAIL_FORMAT` |
| Message FR | Veuillez entrer une adresse email valide. |
| Message EN | Please enter a valid email address. |
| Details | `{ "field": "email", "value": "invalid@" }` |
| Cause | Format email invalide |
| Action user | Corriger l'email |
| Log level | DEBUG |

### VALIDATION_MIN_LENGTH

| Attribut | Valeur |
|----------|--------|
| HTTP Status | 422 |
| Code | `VALIDATION_MIN_LENGTH` |
| Message FR | Ce champ doit contenir au moins {min} caractères. |
| Message EN | This field must be at least {min} characters. |
| Details | `{ "field": "field_name", "min": 8 }` |
| Cause | Texte trop court |
| Action user | Ajouter plus de caractères |
| Log level | DEBUG |

### VALIDATION_MAX_LENGTH

| Attribut | Valeur |
|----------|--------|
| HTTP Status | 422 |
| Code | `VALIDATION_MAX_LENGTH` |
| Message FR | Ce champ ne peut pas dépasser {max} caractères. |
| Message EN | This field cannot exceed {max} characters. |
| Details | `{ "field": "field_name", "max": 255 }` |
| Cause | Texte trop long |
| Action user | Raccourcir le texte |
| Log level | DEBUG |

### VALIDATION_INVALID_FORMAT

| Attribut | Valeur |
|----------|--------|
| HTTP Status | 422 |
| Code | `VALIDATION_INVALID_FORMAT` |
| Message FR | Format invalide. |
| Message EN | Invalid format. |
| Details | `{ "field": "field_name", "expected": "UUID" }` |
| Cause | Format de donnée incorrect |
| Action user | Corriger le format |
| Log level | DEBUG |

### VALIDATION_INVALID_URL

| Attribut | Valeur |
|----------|--------|
| HTTP Status | 422 |
| Code | `VALIDATION_INVALID_URL` |
| Message FR | Veuillez entrer une URL valide (ex: https://exemple.com). |
| Message EN | Please enter a valid URL (e.g., https://example.com). |
| Details | `{ "field": "url" }` |
| Cause | URL malformée |
| Action user | Corriger l'URL |
| Log level | DEBUG |

---

## Erreurs Ressources (RESOURCE_*)

### RESOURCE_NOT_FOUND

| Attribut | Valeur |
|----------|--------|
| HTTP Status | 404 |
| Code | `RESOURCE_NOT_FOUND` |
| Message FR | Cette ressource n'existe pas ou a été supprimée. |
| Message EN | This resource doesn't exist or has been deleted. |
| Details | `{ "resource": "report", "id": "uuid" }` |
| Cause | ID invalide ou ressource supprimée |
| Action user | Retourner à la liste |
| Log level | INFO |

### RESOURCE_ALREADY_EXISTS

| Attribut | Valeur |
|----------|--------|
| HTTP Status | 409 |
| Code | `RESOURCE_ALREADY_EXISTS` |
| Message FR | Cet élément existe déjà. |
| Message EN | This item already exists. |
| Cause | Tentative de création de doublon |
| Action user | Utiliser l'existant ou modifier |
| Log level | INFO |

### RESOURCE_LOCKED

| Attribut | Valeur |
|----------|--------|
| HTTP Status | 423 |
| Code | `RESOURCE_LOCKED` |
| Message FR | Cette ressource est en cours de traitement. Réessayez dans quelques instants. |
| Message EN | This resource is being processed. Please try again shortly. |
| Cause | Ressource en cours de modification |
| Action user | Attendre et réessayer |
| Log level | INFO |

---

## Erreurs Paiement (PAYMENT_*)

### PAYMENT_CARD_DECLINED

| Attribut | Valeur |
|----------|--------|
| HTTP Status | 402 |
| Code | `PAYMENT_CARD_DECLINED` |
| Message FR | Votre carte a été refusée. Veuillez utiliser un autre moyen de paiement. |
| Message EN | Your card was declined. Please try another payment method. |
| Cause | Carte refusée par la banque |
| Action user | Utiliser autre carte ou contacter banque |
| Log level | INFO |

### PAYMENT_INSUFFICIENT_FUNDS

| Attribut | Valeur |
|----------|--------|
| HTTP Status | 402 |
| Code | `PAYMENT_INSUFFICIENT_FUNDS` |
| Message FR | Fonds insuffisants. Veuillez utiliser un autre moyen de paiement. |
| Message EN | Insufficient funds. Please try another payment method. |
| Cause | Solde insuffisant |
| Action user | Utiliser autre carte |
| Log level | INFO |

### PAYMENT_EXPIRED_CARD

| Attribut | Valeur |
|----------|--------|
| HTTP Status | 402 |
| Code | `PAYMENT_EXPIRED_CARD` |
| Message FR | Votre carte a expiré. Veuillez mettre à jour vos informations de paiement. |
| Message EN | Your card has expired. Please update your payment information. |
| Cause | Date expiration dépassée |
| Action user | Mettre à jour la carte |
| Log level | INFO |

### PAYMENT_INVALID_CVC

| Attribut | Valeur |
|----------|--------|
| HTTP Status | 402 |
| Code | `PAYMENT_INVALID_CVC` |
| Message FR | Le code de sécurité est incorrect. |
| Message EN | The security code is incorrect. |
| Cause | CVC erroné |
| Action user | Vérifier le code au dos de la carte |
| Log level | INFO |

### PAYMENT_PROCESSING_ERROR

| Attribut | Valeur |
|----------|--------|
| HTTP Status | 500 |
| Code | `PAYMENT_PROCESSING_ERROR` |
| Message FR | Une erreur est survenue lors du paiement. Réessayez ou contactez le support. |
| Message EN | An error occurred during payment. Please try again or contact support. |
| Cause | Erreur Stripe ou réseau |
| Action user | Réessayer |
| Log level | ERROR |

---

## Erreurs Quota/Limite (QUOTA_*)

### QUOTA_EXCEEDED

| Attribut | Valeur |
|----------|--------|
| HTTP Status | 429 |
| Code | `QUOTA_EXCEEDED` |
| Message FR | Vous avez atteint votre limite. Passez à un plan supérieur pour continuer. |
| Message EN | You've reached your limit. Upgrade your plan to continue. |
| Details | `{ "limit": 10, "used": 10, "reset_at": "ISO_DATE" }` |
| Cause | Quota mensuel/quotidien atteint |
| Action user | Upgrade ou attendre reset |
| Log level | INFO |

### QUOTA_RATE_LIMITED

| Attribut | Valeur |
|----------|--------|
| HTTP Status | 429 |
| Code | `QUOTA_RATE_LIMITED` |
| Message FR | Trop de requêtes. Veuillez patienter quelques instants. |
| Message EN | Too many requests. Please wait a moment. |
| Details | `{ "retry_after": 60 }` |
| Cause | Rate limit API atteint |
| Action user | Attendre et réessayer |
| Log level | WARN |

---

## Erreurs Externes (EXTERNAL_*)

### EXTERNAL_SERVICE_UNAVAILABLE

| Attribut | Valeur |
|----------|--------|
| HTTP Status | 503 |
| Code | `EXTERNAL_SERVICE_UNAVAILABLE` |
| Message FR | Service temporairement indisponible. Réessayez dans quelques instants. |
| Message EN | Service temporarily unavailable. Please try again shortly. |
| Details | `{ "service": "openai" }` |
| Cause | API tierce down ou timeout |
| Action user | Réessayer |
| Log level | ERROR |
| Fallback | [Décrire le fallback si existe] |

### EXTERNAL_API_ERROR

| Attribut | Valeur |
|----------|--------|
| HTTP Status | 502 |
| Code | `EXTERNAL_API_ERROR` |
| Message FR | Une erreur est survenue. Notre équipe a été notifiée. |
| Message EN | An error occurred. Our team has been notified. |
| Cause | Réponse inattendue d'API externe |
| Action user | Réessayer |
| Log level | ERROR |

---

## Erreurs Système (SYSTEM_*)

### SYSTEM_INTERNAL_ERROR

| Attribut | Valeur |
|----------|--------|
| HTTP Status | 500 |
| Code | `SYSTEM_INTERNAL_ERROR` |
| Message FR | Une erreur inattendue est survenue. Notre équipe a été notifiée. |
| Message EN | An unexpected error occurred. Our team has been notified. |
| Cause | Erreur non gérée |
| Action user | Réessayer ou contacter support |
| Log level | ERROR |

### SYSTEM_MAINTENANCE

| Attribut | Valeur |
|----------|--------|
| HTTP Status | 503 |
| Code | `SYSTEM_MAINTENANCE` |
| Message FR | Service en maintenance. Nous serons de retour très bientôt. |
| Message EN | Service under maintenance. We'll be back very soon. |
| Cause | Maintenance planifiée |
| Action user | Attendre |
| Log level | INFO |

### SYSTEM_DATABASE_ERROR

| Attribut | Valeur |
|----------|--------|
| HTTP Status | 500 |
| Code | `SYSTEM_DATABASE_ERROR` |
| Message FR | Erreur de base de données. Réessayez dans quelques instants. |
| Message EN | Database error. Please try again shortly. |
| Cause | Erreur Supabase/PostgreSQL |
| Action user | Réessayer |
| Log level | ERROR |

---

## Erreurs Métier ([DOMAIN]_*)

### [À compléter selon le domaine métier]

| Attribut | Valeur |
|----------|--------|
| HTTP Status | |
| Code | |
| Message FR | |
| Message EN | |
| Cause | |
| Action user | |
| Log level | |

---

## Mapping HTTP → Erreur générique

Si une erreur n'a pas de code spécifique, utiliser :

| HTTP | Code | Message FR |
|------|------|------------|
| 400 | `BAD_REQUEST` | Requête invalide. |
| 401 | `UNAUTHORIZED` | Non authentifié. |
| 403 | `FORBIDDEN` | Accès refusé. |
| 404 | `NOT_FOUND` | Ressource non trouvée. |
| 422 | `VALIDATION_ERROR` | Données invalides. |
| 429 | `RATE_LIMITED` | Trop de requêtes. |
| 500 | `INTERNAL_ERROR` | Erreur serveur. |
| 502 | `BAD_GATEWAY` | Erreur de passerelle. |
| 503 | `SERVICE_UNAVAILABLE` | Service indisponible. |

---

## Implémentation

### Backend (Python)

```python
# app/core/errors.py
from enum import Enum
from fastapi import HTTPException

class ErrorCode(str, Enum):
    AUTH_INVALID_CREDENTIALS = "AUTH_INVALID_CREDENTIALS"
    AUTH_EMAIL_EXISTS = "AUTH_EMAIL_EXISTS"
    # ... tous les codes
    
class AppException(HTTPException):
    def __init__(
        self,
        code: ErrorCode,
        message: str,
        status_code: int = 400,
        details: dict = None
    ):
        super().__init__(
            status_code=status_code,
            detail={
                "success": False,
                "error": {
                    "code": code.value,
                    "message": message,
                    "details": details
                }
            }
        )

# Utilisation
raise AppException(
    code=ErrorCode.AUTH_INVALID_CREDENTIALS,
    message="Email ou mot de passe incorrect.",
    status_code=401
)
```

### Frontend (TypeScript)

```typescript
// lib/errors.ts
export const ERROR_MESSAGES: Record<string, { fr: string; en: string }> = {
  AUTH_INVALID_CREDENTIALS: {
    fr: "Email ou mot de passe incorrect.",
    en: "Invalid email or password."
  },
  // ... tous les codes
};

export function getErrorMessage(code: string, locale: 'fr' | 'en'): string {
  return ERROR_MESSAGES[code]?.[locale] ?? ERROR_MESSAGES.INTERNAL_ERROR[locale];
}
```
