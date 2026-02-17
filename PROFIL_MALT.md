# Profil Malt.fr — Guide Complet

---

## TITRE DU PROFIL

```
Développeur Python / Next.js — SaaS, APIs, Agents IA & Automatisations
```

> **Pourquoi ce titre :** Il contient les mots-clés que les clients Malt recherchent (Python, Next.js, SaaS, API, IA, Automatisation) tout en positionnant sur un créneau premium. Pas "fullstack généraliste" — un builder de systèmes.

---

## BIO (section "À propos")

Je conçois et développe des produits digitaux complets — du SaaS clé en main à l'agent IA autonome.

Cofondateur technique d'une startup, j'ai construit 2 SaaS de A à Z, déployés en production avec utilisateurs réels. Je ne fais pas de maquettes ni de POC jetables : je livre des systèmes robustes, testés, documentés et prêts à scaler.

**Ce que je construis :**

→ **SaaS complets** — Architecture backend + frontend + auth + paiement + déploiement. Mes 2 produits en production (PayloadDiff et Leak Detector) en sont la preuve.

→ **APIs performantes** — APIs REST avec FastAPI, intégrations tierces (Stripe, webhooks, APIs partenaires), architectures async avec Celery et Redis pour le traitement en background.

→ **Agents IA & intégrations LLM** — Intégration de Claude API et GPT dans des workflows métier concrets. Pas du chatbot gadget : de l'IA qui produit des résultats mesurables (analyse automatisée, génération de contenu structuré, prise de décision assistée).

→ **Automatisations** — Workflows automatisés, workers background, pipelines de données, orchestration de tâches complexes. Ce qui prenait des heures à vos équipes tourne tout seul 24/7.

**Mon stack :**
Python 3.12 · FastAPI · Celery · Redis · Next.js 14 · TypeScript · Tailwind · Supabase PostgreSQL · Stripe · Railway · Vercel · Claude API · Playwright · Sentry

**Ma méthode :**
Sprints courts, livraisons fréquentes, visibilité à chaque étape. Code documenté, versionné, testé — pas de dette technique cachée.

📍 Basé à Marseille — disponible en remote pour toute la France.

---

## COMPÉTENCES À SÉLECTIONNER (tags Malt)

### Priorité 1 — Ce qui génère le plus de missions
1. Python
2. FastAPI
3. Next.js
4. TypeScript
5. API REST

### Priorité 2 — Différenciation premium
6. Intelligence Artificielle
7. Automatisation
8. SaaS
9. Supabase
10. Stripe

### Priorité 3 — Complément technique
11. PostgreSQL
12. Redis
13. Tailwind CSS
14. Celery
15. Playwright

---

## FICHE PORTFOLIO #1 — PayloadDiff

### Titre
PayloadDiff — Proxy de monitoring pour webhooks avec détection de breaking changes

### Description

**Le problème :** Les développeurs intégrant des APIs tierces (Stripe, Shopify, HubSpot) subissent des changements de schéma webhook sans préavis. Résultat : du code qui casse en production, des heures de debugging, et des données perdues.

**Ce que j'ai construit :** Un proxy transparent qui capture chaque webhook, le forward instantanément vers la destination (< 50ms de latence ajoutée), compare la structure JSON au baseline, et alerte par email si un breaking change est détecté.

**Architecture technique :**
- Backend FastAPI avec forwarding asynchrone (forward-first, fail open)
- Workers Celery + Redis pour le diff en background sans impacter la latence
- Frontend Next.js 14 + TypeScript avec dashboard temps réel
- Supabase PostgreSQL pour le stockage, Supabase Auth pour l'authentification
- Paiement Stripe avec 4 plans (Free → Business à 199€/mois)
- Déployé sur Railway (backend) + Vercel (frontend) + Cloudflare (CDN/DNS)
- Monitoring Sentry, emails transactionnels via Brevo
- Documentation technique complète (specs, architecture, API reference, sécurité, tests)

**Résultat :** Produit complet livré seul, de l'idée au déploiement production.

**Tags :** FastAPI, Python, Next.js, TypeScript, Redis, Celery, Supabase, Stripe, API, Webhooks

---

## FICHE PORTFOLIO #2 — Leak Detector

### Titre
Leak Detector — Outil IA d'audit de landing pages pour optimiser la conversion

### Description

**Le problème :** Les entreprises dépensent des milliers d'euros en acquisition (SEA, SEO, réseaux sociaux) mais leur landing page fait fuir les visiteurs. Identifier les points de friction demande normalement un audit UX coûteux et long.

**Ce que j'ai construit :** Un outil qui analyse automatiquement une landing page en 30 secondes grâce à l'IA. L'utilisateur entre son URL, Playwright capture la page, Claude API analyse chaque élément (copy, CTA, structure, hiérarchie visuelle), et un rapport détaillé identifie les fuites de conversion avec des recommandations actionnables.

**Architecture technique :**
- Backend FastAPI avec scraping headless via Playwright
- Analyse IA via Claude API (Sonnet) avec prompts optimisés
- Workers Celery + Redis pour le traitement async des analyses
- Frontend Next.js 14 + TypeScript
- Supabase PostgreSQL + Auth
- Paiement Stripe
- Déployé sur Railway + Vercel
- CI/CD GitHub Actions

**Résultat :** De l'idée au produit en production, développé intégralement en solo.

**Tags :** Python, FastAPI, Intelligence Artificielle, Claude API, Next.js, Playwright, Supabase, Stripe, SaaS

---

## PARAMÈTRES DU PROFIL

| Paramètre | Valeur recommandée |
|---|---|
| **TJM** | 350€ → monter à 400€ après 2 avis → 450€ après 5 avis |
| **Disponibilité** | Temps partiel (missions courtes 1-2 semaines) |
| **Télétravail** | 100% remote |
| **Localisation** | Marseille |
| **Langues** | Français (natif), Anglais (professionnel) |
| **Expérience** | 1-3 ans (ne ment pas, tes SaaS compensent) |

---

## PHOTO DE PROFIL

Investis 30 minutes là-dessus. Sur Malt, les profils avec une photo pro ont 3x plus de clics :

- Fond neutre (mur blanc ou extérieur lumineux)
- Tenue pro-casual (chemise ou polo, pas de t-shirt gaming)
- Cadrage visage + épaules
- Lumière naturelle de face
- Sourire léger, regard caméra

---

## STRATÉGIE PREMIERS MOIS

### Semaine 1 — Setup
- [ ] Créer le profil avec tout le contenu ci-dessus
- [ ] Ajouter les 2 fiches portfolio avec screenshots des dashboards
- [ ] Photo de profil pro
- [ ] Activer les alertes email sur les mots-clés cibles

### Semaines 2-4 — Chasse
- [ ] Postuler à TOUTE mission pertinente dans les 2h après publication
- [ ] Répondre aux messages clients en moins de 1h
- [ ] Mots-clés à surveiller : MVP, SaaS, API, automatisation, IA, Python, FastAPI, Next.js, bot, scraping, LLM, agent
- [ ] Accepter une première mission même si légèrement en dessous du TJM cible

### Mois 2+ — Montée en puissance
- [ ] Demander un avis 5★ après CHAQUE mission
- [ ] Augmenter le TJM de 50€ par palier
- [ ] Publier 1 article sur le blog communautaire Malt pour la visibilité
- [ ] Objectif : 3 avis avant la fin du mois 3

---

## TEMPLATE DE CANDIDATURE

```
Bonjour [Prénom],

Votre projet m'intéresse — [reformuler leur besoin en 1 phrase].

C'est exactement le type de système que je construis. J'ai développé
2 SaaS complets en production (PayloadDiff et Leak Detector) avec
le même stack : FastAPI, Next.js, Supabase, [techno pertinente].

[1-2 phrases montrant que tu as compris LEUR besoin spécifique]

Je suis disponible pour en discuter cette semaine.

[Ton prénom]
```

### Ce qui fait la différence
- **Reformuler le besoin** du client (prouve que tu as lu l'annonce)
- **Mentionner un projet concret** similaire au leur
- **Proposer un call** rapidement
- **Être court** (5-8 lignes max, les clients lisent 20 candidatures)

---

*Document de référence pour le profil Malt.fr — À adapter selon l'évolution du profil et les retours terrain.*
