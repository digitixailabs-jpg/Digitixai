# Spécifications Fonctionnelles — [NOM_PROJET]

> Ce document décrit TOUT ce que le produit fait, du point de vue utilisateur.
> Chaque feature doit être spécifiée avant d'être développée.

---

## Vue d'ensemble

### Résumé produit
[À_COMPLÉTER : 2-3 phrases décrivant ce que fait le produit]

### Parcours utilisateur principal
```
[Étape 1] → [Étape 2] → [Étape 3] → [Résultat]
```

---

## Features

### F1 — [Nom de la feature]

#### Description
[Ce que fait cette feature, pourquoi elle existe]

#### User stories
- En tant que [persona], je veux [action] afin de [bénéfice]
- En tant que [persona], je veux [action] afin de [bénéfice]

#### Flow détaillé

```
1. User [action]
   → System [réaction]
   → UI [affichage]

2. User [action]
   → System [réaction]
   → UI [affichage]

3. ...
```

#### Inputs

| Champ | Type | Requis | Validation | Exemple |
|-------|------|--------|------------|---------|
| [champ] | [string/number/etc] | [Oui/Non] | [Règles] | [Valeur exemple] |

#### Outputs

| Élément | Type | Description |
|---------|------|-------------|
| [élément] | [type] | [description] |

#### États UI

| État | Condition | Affichage |
|------|-----------|-----------|
| Loading | Pendant traitement | [Description] |
| Success | Traitement OK | [Description] |
| Empty | Pas de résultat | [Description] |
| Error | Erreur survenue | [Description] |

#### Edge cases

| Cas | Comportement attendu |
|-----|---------------------|
| [Cas limite 1] | [Comment on gère] |
| [Cas limite 2] | [Comment on gère] |
| [Cas limite 3] | [Comment on gère] |

#### Erreurs possibles

| Code erreur | Condition | Message user |
|-------------|-----------|--------------|
| [CODE] | [Quand] | [Message affiché] |

---

### F2 — [Nom de la feature]

[Répéter la structure ci-dessus pour chaque feature]

---

## Authentification

### Méthodes supportées

- [ ] Email + Password
- [ ] Magic Link
- [ ] OAuth Google
- [ ] OAuth GitHub
- [ ] Autre : [Préciser]

### Flow inscription

```
1. User entre email
   → Validation format email
   → Check si email existe déjà
   
2. User entre password
   → Validation force password (min 8 chars, 1 majuscule, 1 chiffre)
   
3. User clique "S'inscrire"
   → Création compte Supabase
   → Email de confirmation envoyé
   → Redirect vers [page]
   
4. User clique lien confirmation
   → Compte activé
   → Auto-login
   → Redirect vers [dashboard]
```

### Flow connexion

```
1. User entre email + password
   → Validation credentials
   
2. Si OK
   → Session créée
   → Redirect vers [dashboard]
   
3. Si KO
   → Message "Email ou mot de passe incorrect"
   → Pas d'indication sur lequel est faux (sécurité)
```

### Flow mot de passe oublié

```
1. User clique "Mot de passe oublié"
   → Affiche formulaire email
   
2. User entre email
   → Email reset envoyé (même si compte n'existe pas - sécurité)
   → Message "Si ce compte existe, un email a été envoyé"
   
3. User clique lien reset
   → Formulaire nouveau password
   → Validation force password
   → Password mis à jour
   → Auto-login
```

### Gestion de session

| Paramètre | Valeur |
|-----------|--------|
| Durée session | [X heures/jours] |
| Refresh token | [Oui/Non] |
| Remember me | [Oui/Non] |
| Multi-device | [Oui/Non] |

---

## Paiement

### Produits Stripe

| Produit | Type | Prix | Billing |
|---------|------|------|---------|
| [Nom] | [one-time/subscription] | [X€] | [monthly/yearly/once] |

### Flow achat one-time

```
1. User clique "Acheter"
   → Création Checkout Session Stripe
   → Redirect vers Stripe Checkout
   
2. User paie
   → Webhook payment_intent.succeeded
   → Crédit ajouté au compte / Accès débloqué
   → Redirect vers success_url
   
3. Si abandon
   → Redirect vers cancel_url
   → Rien ne change côté compte
```

### Flow abonnement

```
1. User sélectionne plan
   → Création Checkout Session (mode: subscription)
   → Redirect vers Stripe Checkout
   
2. User paie
   → Webhook checkout.session.completed
   → Subscription créée en DB
   → Accès features premium activé
   
3. Chaque renouvellement
   → Webhook invoice.paid
   → Subscription prolongée
   
4. Si échec paiement
   → Webhook invoice.payment_failed
   → Email user
   → Grace period [X jours]
   → Downgrade si non résolu
```

### Gestion abonnement

- Upgrade : [Comment ça marche]
- Downgrade : [Comment ça marche]
- Annulation : [Immédiate ou fin de période]
- Remboursement : [Politique]

---

## Notifications

### Emails transactionnels

| Trigger | Sujet | Contenu |
|---------|-------|---------|
| Inscription | [Sujet] | [Résumé contenu] |
| Reset password | [Sujet] | [Résumé contenu] |
| Paiement réussi | [Sujet] | [Résumé contenu] |
| [Autre] | [Sujet] | [Résumé contenu] |

### Notifications in-app

| Trigger | Type | Message |
|---------|------|---------|
| [Action] | [toast/banner/modal] | [Message] |

---

## Permissions et rôles

### Rôles

| Rôle | Description |
|------|-------------|
| anonymous | Non connecté |
| user | Utilisateur standard |
| premium | Utilisateur payant |
| admin | Administrateur |

### Matrice de permissions

| Action | anonymous | user | premium | admin |
|--------|-----------|------|---------|-------|
| Voir landing | ✅ | ✅ | ✅ | ✅ |
| Créer compte | ✅ | - | - | - |
| [Action] | | | | |
| [Action] | | | | |
| Accès admin | ❌ | ❌ | ❌ | ✅ |

---

## Limites et quotas

| Ressource | Free | Tier 1 | Tier 2 | Tier 3 |
|-----------|------|--------|--------|--------|
| [Ressource] | [X/jour] | [X/jour] | [X/jour] | Illimité |
| [Ressource] | [X] | [X] | [X] | [X] |

### Comportement dépassement

- Soft limit : [Avertissement, continue]
- Hard limit : [Bloqué, message affiché]
- Reset : [Quotidien à 00:00 UTC / Mensuel à date anniversaire]

---

## Pages et navigation

### Sitemap

```
/                       → Landing page (public)
/login                  → Connexion (public)
/register               → Inscription (public)
/forgot-password        → Reset password (public)
/dashboard              → Dashboard principal (auth)
/dashboard/[feature]    → Page feature (auth)
/settings               → Paramètres compte (auth)
/settings/billing       → Gestion abonnement (auth)
/admin                  → Admin panel (admin only)
/api/...                → API routes
```

### Navigation principale

| Élément | Visible si | Lien vers |
|---------|------------|-----------|
| Logo | Toujours | / ou /dashboard |
| [Nav item] | [Condition] | [URL] |
| [Nav item] | [Condition] | [URL] |
| Compte | Connecté | /settings |
| Login | Non connecté | /login |

---

## Internationalisation

### Langues supportées V1

- [ ] Français (fr)
- [ ] Anglais (en)
- [ ] Autre : [Préciser]

### Stratégie

- Détection : [Browser locale / User setting / URL param]
- Fallback : [Langue par défaut]
- Stockage préférence : [Local storage / DB]

---

## Accessibilité

### Cibles

- [ ] WCAG 2.1 AA
- [ ] Navigation clavier complète
- [ ] Screen reader compatible
- [ ] Contraste suffisant

### Checklist

- [ ] Alt text sur images
- [ ] Labels sur tous les inputs
- [ ] Focus visible
- [ ] Skip to content link
- [ ] Aria labels où nécessaire

---

## SEO

### Pages indexées

| Page | Title | Meta description | Canonical |
|------|-------|------------------|-----------|
| / | [Title] | [Description] | [URL] |
| [Page] | [Title] | [Description] | [URL] |

### Données structurées

- [ ] Organization
- [ ] Product
- [ ] FAQ
- [ ] Autre : [Préciser]

---

## Out of scope V1

Liste explicite de ce qui n'est PAS inclus dans la V1 :

1. [Feature exclue] — Raison : [Pourquoi]
2. [Feature exclue] — Raison : [Pourquoi]
3. [Feature exclue] — Raison : [Pourquoi]

---

## Questions ouvertes

| Question | Contexte | Décision | Date |
|----------|----------|----------|------|
| [Question] | [Contexte] | [En attente / Décidé : X] | [Date] |
