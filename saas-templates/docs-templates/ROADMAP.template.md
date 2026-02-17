# Roadmap — [NOM_PROJET]

> Ce document liste les évolutions planifiées.
> Objectif : Éviter le feature creep en ayant une vision claire de ce qui vient après V1.

---

## Vision produit

### Court terme (0-3 mois)
[Objectif principal : stabiliser V1, premiers users payants]

### Moyen terme (3-6 mois)
[Objectif : croissance, features différenciantes]

### Long terme (6-12 mois)
[Objectif : scale, expansion marché]

---

## V1.0 — MVP (Current)

**Status** : 🚧 En développement / ✅ Lancé

### Inclus
- [ ] [Feature 1]
- [ ] [Feature 2]
- [ ] [Feature 3]
- [ ] Authentification email + OAuth
- [ ] Paiement Stripe
- [ ] Dashboard basique

### Explicitement exclu (pour V1)
- ❌ [Feature complexe 1] → V1.1
- ❌ [Feature complexe 2] → V1.2
- ❌ API publique → V2.0

---

## V1.1 — [Nom release]

**Target** : [Date cible]
**Theme** : [Ex: Amélioration UX / Nouvelles features / Performance]

### Features planifiées

| Feature | Priorité | Effort | Impact |
|---------|----------|--------|--------|
| [Feature A] | P0 | S | High |
| [Feature B] | P1 | M | Medium |
| [Feature C] | P2 | L | High |

### Détails

#### [Feature A]
- **Description** : [Ce que ça fait]
- **User story** : En tant que [persona], je veux [action] afin de [bénéfice]
- **Dépendances** : [Aucune / Feature X]
- **Effort estimé** : [X jours]

#### [Feature B]
- **Description** : 
- **User story** : 
- **Dépendances** : 
- **Effort estimé** : 

---

## V1.2 — [Nom release]

**Target** : [Date cible]
**Theme** : [Theme]

### Features planifiées

| Feature | Priorité | Effort | Impact |
|---------|----------|--------|--------|
| | | | |

---

## V2.0 — [Nom release]

**Target** : [Date cible]
**Theme** : [Ex: Refonte majeure / API publique / Enterprise]

### Breaking changes envisagés
- [Changement 1]
- [Changement 2]

### Nouvelles features majeures
- [Feature majeure 1]
- [Feature majeure 2]

---

## Backlog (Non planifié)

Features demandées ou envisagées mais pas encore planifiées.

| Feature | Source | Votes/Demandes | Notes |
|---------|--------|----------------|-------|
| [Feature X] | User feedback | 5 | Complexe, attendre validation marché |
| [Feature Y] | Interne | - | Nice to have |
| [Feature Z] | Competitor | - | À évaluer |

---

## Features explicitement rejetées

| Feature | Raison du rejet | Date |
|---------|-----------------|------|
| [Feature] | [Raison : hors scope, trop complexe, pas de demande] | [Date] |

---

## Processus de priorisation

### Critères

| Critère | Poids |
|---------|-------|
| Impact revenue | 30% |
| Demande users | 25% |
| Effort technique | 20% |
| Alignement vision | 15% |
| Urgence/Timing | 10% |

### Scoring

```
Score = (Impact × 0.30) + (Demande × 0.25) + ((10 - Effort) × 0.20) + (Alignement × 0.15) + (Urgence × 0.10)
```

### Labels de priorité

| Label | Signification |
|-------|---------------|
| P0 | Must have cette release |
| P1 | Should have si temps |
| P2 | Nice to have |
| P3 | Backlog |

---

## Comment proposer une feature

1. **Issue GitHub** avec template `feature-request`
2. Décrire :
   - Problème résolu
   - User story
   - Solution proposée (optionnel)
3. L'équipe évalue et ajoute au backlog
4. Review mensuelle pour priorisation

---

## Changelog des décisions roadmap

| Date | Décision | Raison |
|------|----------|--------|
| [Date] | [Feature X] repoussée à V1.2 | Complexité sous-estimée |
| [Date] | [Feature Y] ajoutée V1.1 | Forte demande users |
