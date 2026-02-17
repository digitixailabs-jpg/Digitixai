# Emails Transactionnels — [NOM_PROJET]

> Ce document catalogue TOUS les emails envoyés par l'application.
> Chaque email : trigger, contenu, design, provider config.

---

## Provider

| Paramètre | Valeur |
|-----------|--------|
| **Service** | Brevo (ex-Sendinblue) |
| **API** | v3 REST |
| **Sender** | noreply@[nom-projet].com |
| **Sender Name** | [NOM_PROJET] |
| **Reply-to** | support@[nom-projet].com |
| **Rate limit** | 300 emails/jour (gratuit) |

---

## Catalogue des emails

### Authentification

| ID | Trigger | Objet | Priorité |
|----|---------|-------|----------|
| `auth_confirm` | Inscription | Confirmez votre email | 🔴 Critique |
| `auth_reset` | Demande reset password | Réinitialisez votre mot de passe | 🔴 Critique |
| `auth_password_changed` | Password modifié | Votre mot de passe a été modifié | 🟡 Important |
| `auth_login_new_device` | Login depuis nouveau device | Nouvelle connexion détectée | 🟢 Optionnel |

### Onboarding

| ID | Trigger | Objet | Délai | Priorité |
|----|---------|-------|-------|----------|
| `onboard_welcome` | Inscription confirmée | Bienvenue sur [NOM_PROJET] ! | Immédiat | 🔴 Critique |
| `onboard_reminder` | Setup non complété | Il ne vous reste qu'une étape | J+1 | 🟡 Important |
| `onboard_tips` | Setup complété | 3 astuces pour bien démarrer | J+3 | 🟢 Optionnel |
| `onboard_feedback` | Compte actif 7 jours | Comment se passe votre expérience ? | J+7 | 🟢 Optionnel |

### Paiement

| ID | Trigger | Objet | Priorité |
|----|---------|-------|----------|
| `pay_success` | Paiement réussi | Merci pour votre abonnement | 🔴 Critique |
| `pay_failed` | Échec paiement | Problème avec votre paiement | 🔴 Critique |
| `pay_retry` | 2ème échec paiement | Action requise : mettez à jour votre moyen de paiement | 🔴 Critique |
| `pay_cancelled` | Annulation abonnement | Votre abonnement a été annulé | 🟡 Important |
| `pay_downgrade` | Downgrade plan | Votre plan a été modifié | 🟡 Important |
| `pay_invoice` | Facture générée | Votre facture [NOM_PROJET] | 🟡 Important |

### Notifications produit

| ID | Trigger | Objet | Priorité |
|----|---------|-------|----------|
| `notif_[event]` | [Événement métier] | [Objet] | [Priorité] |
| `notif_[alert]` | [Alerte métier] | [Objet] | [Priorité] |
| `notif_quota_warning` | 80% du quota atteint | Vous approchez de votre limite | 🟡 Important |
| `notif_quota_reached` | 100% du quota | Limite atteinte — passez au plan supérieur | 🔴 Critique |

---

## Templates

### Structure commune

```
┌─────────────────────────────────────────┐
│  [Logo NOM_PROJET]                      │
├─────────────────────────────────────────┤
│                                         │
│  [Titre]                                │
│                                         │
│  [Corps du message - 2-3 lignes max]    │
│                                         │
│  ┌─────────────────────┐                │
│  │    [CTA Button]     │                │
│  └─────────────────────┘                │
│                                         │
│  [Texte secondaire si nécessaire]       │
│                                         │
├─────────────────────────────────────────┤
│  [Footer : liens légaux, unsubscribe]   │
└─────────────────────────────────────────┘
```

### Règles de rédaction

- **Objet** : < 50 caractères, action claire, pas de majuscules partout
- **Corps** : 2-3 phrases max. Un seul message par email.
- **CTA** : Un seul bouton principal. Texte = verbe d'action ("Confirmer mon email", pas "Cliquer ici")
- **Ton** : Professionnel mais humain. Pas de jargon. Pas d'emoji dans l'objet.
- **Footer** : Lien de désinscription + adresse légale + liens CGU/Privacy

---

## Détail par email

### auth_confirm — Confirmation email

```
Objet : Confirmez votre email
Expéditeur : NOM_PROJET <noreply@nom-projet.com>

---

Bonjour,

Confirmez votre adresse email pour activer votre compte [NOM_PROJET].

[Confirmer mon email →]

Ce lien expire dans 24 heures.
Si vous n'avez pas créé de compte, ignorez cet email.
```

### auth_reset — Reset password

```
Objet : Réinitialisez votre mot de passe
Expéditeur : NOM_PROJET <noreply@nom-projet.com>

---

Bonjour,

Vous avez demandé à réinitialiser votre mot de passe.

[Réinitialiser mon mot de passe →]

Ce lien expire dans 1 heure.
Si vous n'êtes pas à l'origine de cette demande, ignorez cet email
et votre mot de passe restera inchangé.
```

### pay_failed — Échec paiement

```
Objet : Problème avec votre paiement
Expéditeur : NOM_PROJET <noreply@nom-projet.com>

---

Bonjour,

Le renouvellement de votre abonnement [Plan] a échoué.

Pour éviter toute interruption de service, mettez à jour
votre moyen de paiement.

[Mettre à jour mon paiement →]

Votre accès reste actif pendant [X jours].
```

### [Répéter pour chaque email critique]

---

## Configuration Brevo

### Listes

| Liste | Usage | Trigger inscription |
|-------|-------|-------------------|
| `all_users` | Tous les utilisateurs | Inscription |
| `paying_users` | Utilisateurs payants | Paiement réussi |
| `churned` | Ex-utilisateurs | Annulation + 30 jours |

### Automations Brevo

| Automation | Trigger | Séquence |
|-----------|---------|----------|
| Onboarding | Ajout à `all_users` | welcome → reminder (J+1) → tips (J+3) → feedback (J+7) |
| Winback | Ajout à `churned` | [À définir] |

---

## Implémentation backend

### Service email

```python
# app/services/email.py

async def send_email(
    to: str,
    template_id: str,
    params: dict,
    tags: list[str] = None
) -> bool:
    """
    Envoi email via Brevo API.
    - template_id : ID du template Brevo
    - params : variables dynamiques (nom, lien, etc.)
    - tags : pour le tracking (ex: ["auth", "onboarding"])
    """
    pass
```

### Envoi async (Celery)

Les emails non-critiques (onboarding, notifications) passent par Celery :

```python
# app/workers/tasks/emails.py

@celery_app.task
def send_email_task(to: str, template_id: str, params: dict):
    """Task Celery pour envoi email en background."""
    pass
```

Les emails critiques (auth_confirm, auth_reset, pay_failed) sont envoyés **de manière synchrone** pour garantir la délivrabilité.

---

## Délivrabilité

### Checklist

- [ ] SPF configuré sur le domaine
- [ ] DKIM configuré sur le domaine
- [ ] DMARC configuré sur le domaine
- [ ] Domaine d'envoi vérifié dans Brevo
- [ ] Reply-to configuré (support@)
- [ ] Unsubscribe header présent
- [ ] Tests envoi reçus dans inbox (pas spam)

### Monitoring

| Métrique | Objectif | Alerte si |
|----------|----------|-----------|
| Taux de délivrabilité | > 98% | < 95% |
| Taux d'ouverture | > 40% (transactionnel) | < 20% |
| Taux de bounce | < 2% | > 5% |
| Taux de spam report | < 0.1% | > 0.3% |
