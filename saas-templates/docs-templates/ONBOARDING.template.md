# Onboarding — [NOM_PROJET]

> Ce document décrit le parcours d'activation des nouveaux utilisateurs.
> L'objectif : amener l'utilisateur au "Aha moment" le plus vite possible.

---

## Aha Moment

> Le moment où l'utilisateur comprend la valeur du produit.

**Définition :** [À_COMPLÉTER : l'action qui prouve que l'utilisateur a compris la valeur]

**Exemples :**
- PayloadDiff : l'utilisateur reçoit son premier diff de webhook
- Leak Detector : l'utilisateur voit son premier rapport d'analyse
- Slack : l'utilisateur envoie son premier message dans une équipe

**Métrique :** [À_COMPLÉTER : comment on mesure si l'utilisateur a atteint le Aha moment]

**Objectif :** [X]% des inscrits atteignent le Aha moment en [X heures/jours]

---

## Funnel d'activation

```
Inscription
    ↓ Objectif : 100%
Confirmation email
    ↓ Objectif : 80%
Premier login
    ↓ Objectif : 70%
Setup initial ([action clé])
    ↓ Objectif : 50%
Aha Moment ([résultat])
    ↓ Objectif : 40%
Usage récurrent (retour J+7)
    ↓ Objectif : 25%
Conversion payant
    Objectif : 10%
```

### Métriques par étape

| Étape | Métrique | Objectif | Actuel |
|-------|----------|----------|--------|
| Inscription → Confirmation | Taux de confirmation email | 80% | — |
| Confirmation → Premier login | Taux de premier login | 70% | — |
| Premier login → Setup | Taux de complétion setup | 50% | — |
| Setup → Aha Moment | Taux d'activation | 40% | — |
| Aha Moment → J+7 | Rétention semaine 1 | 25% | — |
| J+7 → Payant | Taux de conversion | 10% | — |

---

## Parcours step-by-step

### Étape 1 — Inscription

**Page :** `/register`

**Flow :**
```
1. User arrive (depuis landing, ad, referral)
2. Formulaire : email + password (minimum de friction)
3. Clic "Créer mon compte"
4. Email de confirmation envoyé
5. Redirect → page "Vérifiez votre email"
```

**Optimisations :**
- Champs minimum (email + password uniquement)
- Pas de captcha sauf si spam détecté
- Social login si pertinent (Google OAuth)
- Message clair sur la proposition de valeur au-dessus du formulaire

---

### Étape 2 — Premier login / Welcome

**Page :** `/dashboard` (première visite)

**Flow :**
```
1. User confirme email et arrive sur le dashboard
2. Modal/Banner de bienvenue avec guide en 3 étapes
3. Chaque étape a un CTA clair
4. Progression visible (1/3, 2/3, 3/3)
```

**Contenu du welcome :**

| Étape | Titre | Action | CTA |
|-------|-------|--------|-----|
| 1/3 | [Titre étape 1] | [Ce que l'utilisateur doit faire] | [Texte du bouton] |
| 2/3 | [Titre étape 2] | [Ce que l'utilisateur doit faire] | [Texte du bouton] |
| 3/3 | [Titre étape 3] | [Ce que l'utilisateur doit faire] | [Texte du bouton] |

**Règles :**
- Maximum 3 étapes. Pas 5, pas 7. Trois.
- Chaque étape prend < 2 minutes
- L'utilisateur peut skip (mais on track le skip)
- Progression sauvegardée (s'il revient, il reprend où il en était)

---

### Étape 3 — Setup initial

**Ce que l'utilisateur configure :**

| Élément | Obligatoire | Pourquoi |
|---------|-------------|----------|
| [Config 1] | Oui | [Nécessaire pour le Aha moment] |
| [Config 2] | Non | [Améliore l'expérience] |
| [Config 3] | Non | [Personnalisation] |

**Règle :** ne demander QUE ce qui est nécessaire pour atteindre le Aha moment. Tout le reste peut venir après.

---

### Étape 4 — Aha Moment

**Trigger :** [À_COMPLÉTER : quelle action déclenche le résultat]

**Feedback immédiat :**
- UI : [Ce que l'utilisateur voit — succès, résultat, données]
- Notification : [Toast / Email / Rien]
- CTA suivant : [Prochaine action recommandée]

---

## Emails d'onboarding

| Email | Trigger | Délai | Objet | Objectif |
|-------|---------|-------|-------|----------|
| Bienvenue | Inscription | Immédiat | [Objet] | Confirmer + guider vers premier login |
| Rappel setup | Setup non complété | J+1 | [Objet] | Ramener l'utilisateur pour finir le setup |
| Tips & tricks | Setup complété | J+3 | [Objet] | Montrer des features avancées |
| Feedback | J+7 | J+7 | [Objet] | Demander un retour, identifier les blocages |
| Upgrade hint | Usage régulier + plan free | J+14 | [Objet] | Présenter les avantages du plan payant |

### Règles emails onboarding
- Maximum 5 emails sur les 14 premiers jours
- Arrêter la séquence dès que l'utilisateur convertit en payant
- Chaque email a UN seul CTA
- Unsubscribe facile et respecté

---

## Réduction de friction

### Points de friction identifiés

| Friction | Impact | Solution |
|----------|--------|----------|
| Confirmation email lente | Abandon avant premier login | Email prioritaire + page d'attente claire |
| Setup trop long | Drop-off à l'onboarding | Réduire aux champs essentiels uniquement |
| Pas de données au premier login | Dashboard vide = confusion | Données de démo ou guided tour |
| Pas de feedback après action | Utilisateur ne sait pas si ça a marché | Toast de succès + résultat visible |
| Paywall trop tôt | Utilisateur part avant de voir la valeur | Free tier ou trial suffisant pour le Aha moment |

### Empty states

Chaque page du dashboard doit avoir un empty state qui guide vers l'action :

| Page | Empty state message | CTA |
|------|-------------------|-----|
| [Page principale] | [Message encourageant] | [Action à faire] |
| [Page secondaire] | [Message explicatif] | [Action à faire] |

---

## A/B Tests prévus

| Test | Variante A | Variante B | Métrique | Statut |
|------|-----------|-----------|----------|--------|
| Formulaire inscription | Email + password | Google OAuth uniquement | Taux d'inscription | [À faire] |
| Welcome modal | 3 étapes | Vidéo 60s | Taux de complétion | [À faire] |
| Premier email | Tips produit | Question ouverte | Taux d'ouverture | [À faire] |

---

## Checklist

- [ ] Aha moment défini et mesurable
- [ ] Funnel d'activation tracké (chaque étape)
- [ ] Parcours onboarding en 3 étapes max
- [ ] Empty states sur toutes les pages dashboard
- [ ] Séquence emails onboarding configurée
- [ ] Données de démo ou guided tour pour le premier login
- [ ] Temps inscription → Aha moment < [X minutes]
