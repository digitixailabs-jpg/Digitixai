# Stripe Setup Guide

> Guide complet pour configurer Stripe dans votre projet.

---

## 1. Créer un compte Stripe

1. Aller sur [stripe.com](https://stripe.com)
2. Créer un compte
3. Compléter la vérification (pour les paiements live)

---

## 2. Récupérer les clés API

### Dashboard → Developers → API Keys

| Clé | Usage | Variable d'env |
|-----|-------|----------------|
| Publishable key (pk_test_...) | Frontend | `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY` |
| Secret key (sk_test_...) | Backend | `STRIPE_SECRET_KEY` |

**⚠️ Ne JAMAIS exposer la Secret Key côté frontend**

---

## 3. Créer les produits et prix

### Dashboard → Products → Add Product

#### Exemple : Plan Pro

1. **Name**: Pro Plan
2. **Description**: Accès complet à toutes les fonctionnalités
3. **Pricing**:
   - Prix mensuel : 29€/mois (récurrent)
   - Prix annuel : 290€/an (récurrent) — optionnel

4. Copier les **Price IDs** (price_xxx) dans vos variables d'environnement :
   - `STRIPE_PRICE_ID_MONTHLY=price_xxx`
   - `STRIPE_PRICE_ID_YEARLY=price_xxx`

---

## 4. Configurer les webhooks

### Dashboard → Developers → Webhooks → Add endpoint

**URL Endpoint** : `https://api.[votre-domaine].com/api/v1/webhooks/stripe`

**Events à écouter** :
- `checkout.session.completed`
- `customer.subscription.created`
- `customer.subscription.updated`
- `customer.subscription.deleted`
- `invoice.paid`
- `invoice.payment_failed`

**Copier le Webhook Secret** (whsec_xxx) → `STRIPE_WEBHOOK_SECRET`

### Test en local avec Stripe CLI

```bash
# Installer Stripe CLI
brew install stripe/stripe-cli/stripe

# Login
stripe login

# Forward webhooks vers localhost
stripe listen --forward-to localhost:8000/api/v1/webhooks/stripe

# Copier le webhook secret affiché
# Ready! Your webhook signing secret is whsec_xxx
```

---

## 5. Configuration Customer Portal

Le Customer Portal permet aux utilisateurs de gérer leur abonnement.

### Dashboard → Settings → Billing → Customer portal

Configurer :
- [x] Update payment methods
- [x] View invoice history
- [x] Cancel subscriptions
- [ ] Update subscriptions (si vous voulez permettre les changements de plan)

---

## 6. Implémentation Backend

### Créer une Checkout Session

```python
# app/api/v1/endpoints/billing.py
import stripe
from fastapi import APIRouter, Depends, HTTPException
from app.config import settings
from app.core.security import get_current_user

router = APIRouter()
stripe.api_key = settings.STRIPE_SECRET_KEY

@router.post("/checkout")
async def create_checkout_session(
    price_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Create a Stripe Checkout session."""
    try:
        session = stripe.checkout.Session.create(
            customer_email=current_user["email"],
            client_reference_id=current_user["id"],
            payment_method_types=["card"],
            line_items=[{
                "price": price_id,
                "quantity": 1,
            }],
            mode="subscription",  # ou "payment" pour one-time
            success_url=f"{settings.FRONTEND_URL}/dashboard?checkout=success",
            cancel_url=f"{settings.FRONTEND_URL}/pricing?checkout=canceled",
            metadata={
                "user_id": current_user["id"],
            },
        )
        
        return {"success": True, "data": {"checkout_url": session.url}}
    
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/portal")
async def create_portal_session(
    current_user: dict = Depends(get_current_user)
):
    """Create a Stripe Customer Portal session."""
    # Get the user's Stripe customer ID from your database
    profile = await get_profile(current_user["id"])
    
    if not profile.get("stripe_customer_id"):
        raise HTTPException(status_code=400, detail="No subscription found")
    
    try:
        session = stripe.billing_portal.Session.create(
            customer=profile["stripe_customer_id"],
            return_url=f"{settings.FRONTEND_URL}/settings/billing",
        )
        
        return {"success": True, "data": {"portal_url": session.url}}
    
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=str(e))
```

---

## 7. Implémentation Frontend

### Bouton Checkout

```typescript
// components/checkout-button.tsx
'use client';

import { useState } from 'react';
import { api } from '@/lib/api';

interface CheckoutButtonProps {
  priceId: string;
  children: React.ReactNode;
}

export function CheckoutButton({ priceId, children }: CheckoutButtonProps) {
  const [loading, setLoading] = useState(false);

  const handleCheckout = async () => {
    setLoading(true);
    
    try {
      const response = await api.post<{ checkout_url: string }>('/billing/checkout', {
        price_id: priceId,
      });
      
      if (response.success && response.data?.checkout_url) {
        window.location.href = response.data.checkout_url;
      } else {
        // Handle error
        console.error(response.error);
      }
    } catch (error) {
      console.error('Checkout error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <button
      onClick={handleCheckout}
      disabled={loading}
      className="btn btn-primary"
    >
      {loading ? 'Loading...' : children}
    </button>
  );
}
```

### Bouton Manage Subscription

```typescript
// components/manage-subscription-button.tsx
'use client';

import { useState } from 'react';
import { api } from '@/lib/api';

export function ManageSubscriptionButton() {
  const [loading, setLoading] = useState(false);

  const handleManage = async () => {
    setLoading(true);
    
    try {
      const response = await api.post<{ portal_url: string }>('/billing/portal');
      
      if (response.success && response.data?.portal_url) {
        window.location.href = response.data.portal_url;
      }
    } catch (error) {
      console.error('Portal error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <button
      onClick={handleManage}
      disabled={loading}
      className="btn btn-secondary"
    >
      {loading ? 'Loading...' : 'Manage Subscription'}
    </button>
  );
}
```

---

## 8. Test du flow

### Mode Test

1. Utiliser les clés `pk_test_` et `sk_test_`
2. Utiliser la carte de test : `4242 4242 4242 4242`
3. Date : n'importe quelle date future
4. CVC : n'importe quel 3 chiffres

### Cartes de test spéciales

| Numéro | Scénario |
|--------|----------|
| 4242 4242 4242 4242 | Succès |
| 4000 0000 0000 0002 | Carte refusée |
| 4000 0000 0000 9995 | Fonds insuffisants |
| 4000 0025 0000 3155 | Requiert 3D Secure |

### Tester les webhooks

```bash
# Trigger un event de test
stripe trigger checkout.session.completed

# Voir les events récents
stripe events list --limit 5
```

---

## 9. Passage en production

### Checklist

- [ ] Remplacer les clés test par les clés live
- [ ] Créer les produits en mode live
- [ ] Configurer le webhook avec l'URL de production
- [ ] Tester un vrai paiement (petit montant, puis rembourser)
- [ ] Vérifier que les emails Stripe sont configurés
- [ ] Configurer les receipts et invoices

### Variables de production

```bash
# Production
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_live_xxx
STRIPE_SECRET_KEY=sk_live_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx
STRIPE_PRICE_ID_MONTHLY=price_xxx  # Price ID live
STRIPE_PRICE_ID_YEARLY=price_xxx   # Price ID live
```

---

## 10. Troubleshooting

### Webhook ne reçoit pas les events

1. Vérifier l'URL du webhook dans Stripe Dashboard
2. Vérifier que le endpoint retourne 200
3. Vérifier les logs dans Stripe → Developers → Webhooks → Recent deliveries

### Signature invalide

1. Vérifier que `STRIPE_WEBHOOK_SECRET` est correct
2. Vérifier que vous utilisez le raw body (pas JSON parsé)
3. Vérifier que le secret correspond à l'endpoint (test vs live)

### Customer non trouvé

1. S'assurer de stocker `stripe_customer_id` après le premier checkout
2. Utiliser `client_reference_id` pour passer le user_id
