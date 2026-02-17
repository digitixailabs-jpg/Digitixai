# Analytics & Tracking — [NOM_PROJET]

> Ce document définit tous les événements à tracker et les KPIs.

---

## Stack Analytics

| Outil | Usage |
|-------|-------|
| [Plausible/PostHog/Mixpanel] | Product analytics |
| Stripe Dashboard | Revenue metrics |
| Sentry | Error tracking |
| LangSmith | LLM monitoring |

---

## Événements à tracker

### Acquisition

| Event | Trigger | Propriétés |
|-------|---------|------------|
| `page_view` | Chaque page | `path`, `referrer`, `utm_*` |
| `landing_cta_click` | Click CTA landing | `cta_location`, `cta_text` |
| `pricing_view` | Vue page pricing | `source` |

### Activation

| Event | Trigger | Propriétés |
|-------|---------|------------|
| `signup_started` | Début inscription | `method` (email/google) |
| `signup_completed` | Inscription réussie | `user_id`, `method` |
| `email_verified` | Email confirmé | `user_id` |
| `onboarding_step` | Chaque étape onboarding | `step`, `user_id` |
| `onboarding_completed` | Fin onboarding | `user_id`, `duration` |
| `first_[action]` | Première action clé | `user_id` |

### Engagement

| Event | Trigger | Propriétés |
|-------|---------|------------|
| `[feature]_created` | Création ressource | `user_id`, `type` |
| `[feature]_viewed` | Vue détail | `user_id`, `resource_id` |
| `[feature]_completed` | Traitement terminé | `user_id`, `resource_id`, `duration` |
| `settings_updated` | Modif paramètres | `user_id`, `setting` |

### Retention

| Event | Trigger | Propriétés |
|-------|---------|------------|
| `login` | Connexion | `user_id`, `method` |
| `session_start` | Début session | `user_id` |
| `daily_active` | 1x/jour par user | `user_id`, `date` |

### Revenue

| Event | Trigger | Propriétés |
|-------|---------|------------|
| `checkout_started` | Début checkout | `user_id`, `plan`, `price` |
| `checkout_completed` | Paiement réussi | `user_id`, `plan`, `price`, `revenue` |
| `checkout_abandoned` | Abandon checkout | `user_id`, `plan`, `step` |
| `subscription_upgraded` | Upgrade plan | `user_id`, `from_plan`, `to_plan` |
| `subscription_downgraded` | Downgrade | `user_id`, `from_plan`, `to_plan` |
| `subscription_cancelled` | Annulation | `user_id`, `plan`, `reason` |
| `refund_requested` | Demande remboursement | `user_id`, `amount`, `reason` |

### Errors

| Event | Trigger | Propriétés |
|-------|---------|------------|
| `error_api` | Erreur 5xx | `endpoint`, `error_code`, `user_id` |
| `error_client` | Erreur JS | `message`, `stack`, `user_id` |
| `error_payment` | Échec paiement | `user_id`, `error_code` |

---

## Implémentation

### Frontend (exemple avec Plausible)

```typescript
// lib/analytics.ts
export const trackEvent = (
  event: string,
  props?: Record<string, string | number | boolean>
) => {
  if (typeof window !== 'undefined' && window.plausible) {
    window.plausible(event, { props });
  }
};

// Utilisation
trackEvent('signup_completed', { method: 'email' });
trackEvent('checkout_started', { plan: 'pro', price: 29 });
```

### Backend (événements serveur)

```python
# services/analytics.py
from posthog import Posthog

posthog = Posthog(settings.POSTHOG_API_KEY)

def track_event(
    user_id: str,
    event: str,
    properties: dict = None
):
    posthog.capture(
        distinct_id=user_id,
        event=event,
        properties=properties or {}
    )

# Utilisation
track_event(user.id, 'report_completed', {
    'report_id': report.id,
    'duration_seconds': duration
})
```

---

## KPIs et métriques

### North Star Metric

| Métrique | Définition | Cible |
|----------|------------|-------|
| **[À définir]** | [Ex: Rapports générés / semaine] | [X] |

### Acquisition

| Métrique | Calcul | Cible |
|----------|--------|-------|
| Visitors | Unique visitors / mois | |
| Signup rate | Signups / Visitors | >5% |
| CAC | Marketing spend / New customers | <[X]€ |

### Activation

| Métrique | Calcul | Cible |
|----------|--------|-------|
| Activation rate | Users qui font [action clé] / Total signups | >40% |
| Time to value | Temps médian signup → [action clé] | <5 min |
| Onboarding completion | Users qui finissent onboarding / Total | >70% |

### Engagement

| Métrique | Calcul | Cible |
|----------|--------|-------|
| DAU | Daily Active Users | |
| WAU | Weekly Active Users | |
| DAU/MAU | Stickiness | >20% |
| [Actions] / user / mois | Moyenne | |

### Retention

| Métrique | Calcul | Cible |
|----------|--------|-------|
| D1 Retention | Users actifs J+1 / Signups J0 | >40% |
| D7 Retention | Users actifs J+7 / Signups J0 | >25% |
| D30 Retention | Users actifs J+30 / Signups J0 | >15% |
| Churn rate | Cancelled / Total subscribers | <5%/mois |

### Revenue

| Métrique | Calcul | Cible |
|----------|--------|-------|
| MRR | Monthly Recurring Revenue | |
| ARR | MRR × 12 | |
| ARPU | MRR / Paying users | |
| LTV | ARPU × Avg lifetime (mois) | |
| LTV/CAC | | >3 |
| Conversion rate | Paying / Total users | >5% |

---

## Dashboards

### Dashboard opérationnel (quotidien)

- Signups aujourd'hui
- Revenue aujourd'hui
- Erreurs (count, top 5)
- [Feature] usage

### Dashboard stratégique (hebdo/mensuel)

- Funnel acquisition → activation → payment
- Retention cohorts
- MRR growth
- Churn analysis

---

## Propriétés utilisateur

Propriétés à associer à chaque user pour segmentation :

| Propriété | Type | Source |
|-----------|------|--------|
| `plan` | string | Stripe |
| `signup_date` | date | Auth |
| `signup_source` | string | UTM |
| `country` | string | IP/profile |
| `total_[actions]` | number | Computed |
| `last_active` | date | Computed |

---

## UTM Tracking

### Paramètres

| Param | Usage | Exemple |
|-------|-------|---------|
| `utm_source` | Origine trafic | google, twitter, newsletter |
| `utm_medium` | Type canal | cpc, organic, email |
| `utm_campaign` | Nom campagne | launch_jan_2026 |
| `utm_content` | Variante | cta_hero, cta_footer |

### Persistence

Stocker UTMs au signup :
1. Capturer au premier visit (localStorage)
2. Envoyer au signup
3. Stocker dans `profiles.utm_*`

---

## RGPD / Privacy

### Consentement

- [ ] Banner cookie au premier visit
- [ ] Option opt-out analytics
- [ ] Pas de tracking si opt-out

### Anonymisation

- [ ] IP anonymisée (si Plausible : par défaut)
- [ ] Pas de PII dans events (pas d'email, nom)
- [ ] User ID hashé si partagé avec tiers

### Data retention

| Donnée | Rétention |
|--------|-----------|
| Analytics events | 24 mois |
| User properties | Durée du compte |
| Logs | 30 jours |
