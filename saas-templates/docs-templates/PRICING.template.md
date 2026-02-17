# Pricing — [NOM_PROJET]

> Ce document définit la stratégie de pricing, les plans, les limites, et le mapping Stripe.
> Toute modification de pricing doit être documentée ici AVANT implémentation.

---

## Stratégie de pricing

### Modèle

- [ ] Freemium (plan gratuit + plans payants)
- [ ] Free trial (essai gratuit X jours → payant)
- [ ] Pay-as-you-go (facturation à l'usage)
- [ ] Flat rate (prix unique)
- [ ] Tiered (plans par paliers)
- [ ] Per-seat (par utilisateur)

### Métrique de valeur

> La métrique de valeur est CE QUE le client paie. Elle doit être alignée avec la valeur perçue.

**Métrique principale :** [À_COMPLÉTER : ex. nombre d'endpoints, nombre d'analyses, nombre d'utilisateurs, volume de requêtes]

**Pourquoi :** [À_COMPLÉTER : pourquoi cette métrique reflète la valeur pour le client]

---

## Plans

### Grille tarifaire

| | **Free** | **Pro** | **Team** | **Business** |
|---|---|---|---|---|
| **Prix mensuel** | 0€ | [X]€/mois | [X]€/mois | [X]€/mois |
| **Prix annuel** | 0€ | [X]€/an (-20%) | [X]€/an (-20%) | [X]€/an (-20%) |
| [Limite 1] | [X] | [X] | [X] | Illimité |
| [Limite 2] | [X] | [X] | [X] | Illimité |
| [Limite 3] | [X] | [X] | [X] | Illimité |
| Rétention données | [X] jours | [X] jours | [X] jours | [X] jours |
| Support | Community | Email | Email prioritaire | Slack dédié |
| [Feature exclusive 1] | ❌ | ✅ | ✅ | ✅ |
| [Feature exclusive 2] | ❌ | ❌ | ✅ | ✅ |
| [Feature exclusive 3] | ❌ | ❌ | ❌ | ✅ |

### Logique du Free tier

**Objectif du plan gratuit :** [Choisir]
- [ ] Acquisition (attirer un max d'utilisateurs → conversion organique)
- [ ] Product-led growth (l'usage gratuit génère de la visibilité)
- [ ] Réduire la friction (pas de CB requise au signup)

**Le plan gratuit doit :**
- Permettre d'atteindre le Aha Moment
- Être suffisant pour un usage personnel/test
- Créer naturellement le besoin de passer au plan supérieur

**Le plan gratuit ne doit PAS :**
- Être suffisant pour un usage professionnel soutenu
- Cannibaliser les plans payants
- Coûter plus en infra qu'il ne rapporte en conversion

### Logique des limites

| Limite | Pourquoi cette valeur |
|--------|---------------------|
| [Limite 1 Free] | [Justification] |
| [Limite 1 Pro] | [Justification] |
| [Limite 1 Team] | [Justification] |

---

## Mapping Stripe

### Produits

| Plan | Stripe Product ID | Statut |
|------|-------------------|--------|
| Pro | `prod_XXXXXXXXXXXX` | [À créer / Créé] |
| Team | `prod_XXXXXXXXXXXX` | [À créer / Créé] |
| Business | `prod_XXXXXXXXXXXX` | [À créer / Créé] |

### Prices (mensuel)

| Plan | Stripe Price ID | Montant | Récurrence |
|------|----------------|---------|------------|
| Pro Monthly | `price_XXXXXXXXXXXX` | [X]€ | Mensuel |
| Team Monthly | `price_XXXXXXXXXXXX` | [X]€ | Mensuel |
| Business Monthly | `price_XXXXXXXXXXXX` | [X]€ | Mensuel |

### Prices (annuel)

| Plan | Stripe Price ID | Montant | Récurrence |
|------|----------------|---------|------------|
| Pro Annual | `price_XXXXXXXXXXXX` | [X]€ | Annuel |
| Team Annual | `price_XXXXXXXXXXXX` | [X]€ | Annuel |
| Business Annual | `price_XXXXXXXXXXXX` | [X]€ | Annuel |

---

## Flows de paiement

### Inscription → Plan payant

```
1. User sur plan Free
2. Clique "Upgrade" sur la page pricing
3. Sélectionne plan + billing (mensuel/annuel)
4. Redirect → Stripe Checkout
5. Paiement réussi
6. Webhook checkout.session.completed
7. → Mise à jour plan en DB
8. → Activation features premium
9. → Email confirmation paiement
10. Redirect → dashboard avec confirmation
```

### Upgrade (Pro → Team)

```
1. User sur plan Pro
2. Clique "Upgrade" dans settings/billing
3. Stripe proration automatique (crédit du temps restant)
4. Différence facturée immédiatement
5. Webhook customer.subscription.updated
6. → Mise à jour plan en DB
7. → Nouvelles limites activées immédiatement
```

### Downgrade (Team → Pro)

```
1. User sur plan Team
2. Clique "Downgrade" dans settings/billing
3. Changement effectif à la FIN de la période en cours
4. Accès Team maintenu jusqu'à la fin
5. Webhook customer.subscription.updated (à la date de fin)
6. → Mise à jour plan en DB
7. → Limites Pro appliquées
8. → Données au-delà des limites : conservées mais non accessibles
```

### Annulation

```
1. User clique "Annuler mon abonnement"
2. Modal de confirmation avec raison (optionnel)
3. Annulation à la fin de la période en cours
4. Accès maintenu jusqu'à la fin
5. Webhook customer.subscription.deleted
6. → Plan → Free
7. → Email confirmation annulation
8. → Données conservées [X jours] puis archivées
```

### Échec de paiement

```
1. Webhook invoice.payment_failed
2. Email pay_failed envoyé
3. Retry automatique Stripe (3 tentatives sur 7 jours)
4. Si 2ème échec : email pay_retry
5. Si tous les retries échouent :
   → Downgrade vers Free
   → Email de notification
   → Données conservées [X jours]
```

---

## Comportement des limites

### Soft limits (avertissement)

```
80% du quota atteint
  → Banner dans le dashboard
  → Email notif_quota_warning

90% du quota atteint
  → Banner + notification in-app
```

### Hard limits (bloquant)

```
100% du quota atteint
  → Action bloquée
  → Message : "Vous avez atteint la limite de votre plan. Passez au plan [supérieur] pour continuer."
  → CTA → Page pricing
  → Email notif_quota_reached
```

### Reset des quotas

- **Quotas journaliers :** Reset à 00:00 UTC
- **Quotas mensuels :** Reset à la date anniversaire de l'abonnement

---

## Table DB — subscriptions

```sql
CREATE TABLE subscriptions (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) NOT NULL,
    stripe_customer_id TEXT,
    stripe_subscription_id TEXT,
    plan TEXT NOT NULL DEFAULT 'free',  -- free, pro, team, business
    billing_period TEXT,                 -- monthly, yearly
    status TEXT NOT NULL DEFAULT 'active', -- active, past_due, cancelled, expired
    current_period_start TIMESTAMPTZ,
    current_period_end TIMESTAMPTZ,
    cancel_at_period_end BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index
CREATE INDEX idx_subscriptions_user ON subscriptions(user_id);
CREATE INDEX idx_subscriptions_stripe ON subscriptions(stripe_customer_id);
```

---

## Analyse pricing

### Unit economics

| Métrique | Valeur | Objectif |
|----------|--------|----------|
| ARPU (Average Revenue Per User) | — | [X]€/mois |
| CAC (Customer Acquisition Cost) | — | < [X]€ |
| LTV (Lifetime Value) | — | > [X]€ |
| LTV/CAC ratio | — | > 3 |
| Churn mensuel | — | < 5% |
| Conversion Free → Payant | — | > 5% |

### Benchmarks marché

| Concurrent | Plan comparable | Prix | Ce qu'il inclut |
|-----------|----------------|------|-----------------|
| [Concurrent 1] | [Plan] | [Prix] | [Features] |
| [Concurrent 2] | [Plan] | [Prix] | [Features] |
| [Concurrent 3] | [Plan] | [Prix] | [Features] |

---

## Checklist

- [ ] Plans définis avec limites claires
- [ ] Stripe Products et Prices créés (test + live)
- [ ] Flow checkout implémenté et testé
- [ ] Webhooks Stripe configurés et testés
- [ ] Upgrade/downgrade fonctionnels
- [ ] Gestion échec de paiement
- [ ] Soft limits (80%, 90%) avec notifications
- [ ] Hard limits (100%) bloquants
- [ ] Page pricing sur le site
- [ ] Page billing dans le dashboard
- [ ] Emails de paiement configurés
- [ ] Portail client Stripe activé (gestion CB)
