# CONTEXT.md — Source de Vérité

> Dernière mise à jour : 2026-02-17

---

## QUI JE SUIS

Développeur freelance spécialisé dans la construction de SaaS, APIs, Agents IA et systèmes d'automatisation. Basé à Marseille, France. Travail 100% remote.

Je code avec Claude Code. Je ship vite, propre, et en production.

---

## LES DEUX MONDES

### Monde 1 — Société (SASU détenue par SAS)
- Associé : responsable marketing et vente
- Mon rôle : dev technique, construction des SaaS
- Statut actuel : **2 SaaS prêts, en attente de lancement marketing par l'associé**
- Règle : je n'investis plus de temps dev société tant que le marketing n'a pas lancé le premier SaaS
- Produits société : PayloadDiff, Leak Detector

### Monde 2 — Moi solo (ce repo)
- Freelance + personal branding + mes propres produits
- Je n'attends personne. Je contrôle tout.
- Objectif : générer du cashflow rapidement via plusieurs canaux
- Ce repo documente exclusivement le Monde 2
- Statut actuel : Phase 0 terminée, Phase 1 (Lancement) en cours
- Site : altidigitech.com (studio technologique, vitrine + offres + newsletter)
- Email pro : contact@altidigitech.com
- Facturation : via Altidigitech SASU (Henrri)

**Tout ce qui suit concerne le Monde 2.**

---

## POSITIONNEMENT

**Je ne suis pas un dev fullstack généraliste. Je ne vends pas du temps. Je vends des résultats.**

Je suis un **builder de systèmes** — je prends un problème métier et je livre un produit complet en production : backend, frontend, IA, paiement, déploiement, monitoring.

### Ce que je livre
- **SaaS complets** — De l'idée au déploiement production
- **APIs sur mesure** — REST, intégrations tierces, webhooks, architectures async
- **Agents IA** — Intégrations LLM dans des workflows métier concrets
- **Automatisations** — Workers background, pipelines de données, orchestration de tâches

### Ce que je ne fais PAS
- Sites vitrine / WordPress
- Refontes CSS / design pur
- Maintenance de legacy code sans vision produit
- POC jetables sans objectif de production

---

## STACK TECHNIQUE

| Couche | Technologies |
|---|---|
| **Backend** | FastAPI · Python 3.12+ |
| **Queue/Workers** | Celery · Redis |
| **Frontend** | Next.js 14 · TypeScript · Tailwind · shadcn/ui |
| **Database** | Supabase PostgreSQL |
| **Auth** | Supabase Auth |
| **Paiement** | Stripe |
| **IA/LLM** | Claude API · OpenAI · LangChain · LangGraph |
| **Scraping** | Playwright |
| **Deploy Backend** | Railway |
| **Deploy Frontend** | Vercel |
| **CDN/DNS** | Cloudflare |
| **Monitoring** | Sentry · LangSmith |
| **Email** | Brevo |
| **CI/CD** | GitHub Actions |
| **Dev Tool** | Claude Code |

---

## PRÉSENCE EN LIGNE

| Plateforme | URL | Statut |
|---|---|---|
| Site web | altidigitech.com | ✅ Live |
| LinkedIn | linkedin.com/in/fabricegangitano | ✅ Optimisé |
| Malt | malt.fr/profile/fabricegangitano | ✅ Profil complet, TJM 350€/jour |
| Twitter/X | x.com/FabGangi | ✅ Créé |
| Cal.com | cal.com/altidigitech | ✅ Opérationnel |
| Newsletter | Brevo (contact@altidigitech.com) | ✅ Formulaire sur le site |
| Facturation | Henrri | ✅ Compte créé (config SIRET/IBAN en attente) |
| GitHub | github.com/digitixailabs-jpg | ✅ Actif |

---

## OFFRES PACKAGÉES

| Offre | Prix | Délai | Contenu |
|---|---|---|---|
| Audit & Stratégie Technique | À partir de 990€ | 3-5 jours | Audit archi, recommandations, plan d'action PDF, call 1h |
| API / Intégration IA | À partir de 2 500€ | 1-2 semaines | API REST FastAPI, intégration LLM, automatisation, tests, déploiement, 30j support |
| MVP SaaS Complet | À partir de 4 900€ | 2-4 semaines | Backend + frontend + auth + Stripe + déploiement + monitoring, 60j support |

---

## PRODUITS EN PRODUCTION (preuves de compétence)

> Ces SaaS appartiennent à la société (Monde 1) mais servent de portfolio et de preuves concrètes pour le Monde 2.

### PayloadDiff
- **URL :** payloaddiff.io
- **Problème :** Les webhooks d'APIs tierces changent de structure sans préavis → code qui casse en prod
- **Solution :** Proxy transparent qui forward les webhooks (< 50ms), compare la structure JSON au baseline, alerte si breaking change détecté
- **Architecture :** FastAPI (forward async, fail open) · Celery + Redis (diff background) · Next.js 14 + TypeScript · Supabase · Stripe (4 plans Free → 199€/mois) · Railway + Vercel + Cloudflare · Sentry · Brevo
- **Développé :** Intégralement en solo

### Leak Detector
- **URL :** [à compléter]
- **Problème :** Les entreprises dépensent en acquisition mais leur landing page fait fuir les visiteurs
- **Solution :** Analyse IA automatique d'une landing page en 30 secondes via Playwright + Claude API, rapport avec recommandations actionnables
- **Architecture :** FastAPI + Playwright · Claude API Sonnet · Celery + Redis · Next.js 14 + TypeScript · Supabase · Stripe · Railway + Vercel · CI/CD GitHub Actions
- **Développé :** Intégralement en solo

---

## STRATÉGIE DE REVENUS — 3 CANAUX

### Canal 1 — Freelance Malt (cashflow immédiat)
- **Quoi :** Missions courtes (1-2 semaines) sur Malt.fr
- **TJM :** 350€ au lancement → 400€ après 2 avis → 450-500€ après 5 avis
- **Cible :** Startups et PME qui cherchent du dev SaaS, API, IA, automatisation
- **Pourquoi :** Revenu le plus rapide, pas de dépendance algo/audience
- **Objectif :** Première mission < 4 semaines, 3 avis 5★ avant mois 3

### Canal 2 — Personal branding / Build in public (leads + autorité)
- **Plateformes :** LinkedIn (principal) + Twitter/X (secondaire)
- **Rythme :** 3 posts/semaine, même contenu adapté aux 2 plateformes
- **Angle :** Build in public tech — je montre ce que je construis, comment et pourquoi
- **Pourquoi LinkedIn :** Les acheteurs B2B sont là. Algo encore généreux en reach organique
- **Pourquoi Twitter/X :** Communauté indie hackers / #buildinpublic. Viralité tech
- **Objectif :** Premiers DM entrants avant mois 3

### Canal 3 — Micro-SaaS solo (revenu récurrent)
- **Quand :** Dès que le freelance génère du cashflow de base (mois 2+)
- **Quoi :** Un micro-SaaS shippé en 1 semaine max, pricing 19-49€/mois
- **Règle :** Petit, utile, payant, rapide à builder
- **Objectif :** Premier MRR avant mois 4

### Canaux écartés (pour l'instant)
- **TikTok :** ROI temps/résultat trop faible pour du B2B/SaaS. À reconsidérer quand les 3 canaux tournent
- **YouTube :** Temps de production trop élevé
- **Instagram :** Pas pertinent pour le positionnement tech/B2B

---

## FUNNEL DE VENTE — ARCHITECTURE COMPLÈTE

### Principe fondamental
Chaque étape du funnel POUSSE mécaniquement vers la suivante. Pas d'espoir, pas de chance. Un système.

### Vue d'ensemble

```
                    ┌─────────────────────────────┐
                    │   LAYER 1 — VISIBILITÉ      │
                    │   (Attirer des inconnus)     │
                    │                             │
                    │  LinkedIn    Twitter/X       │
                    │  3x/sem     3x/sem          │
                    │  Build in public            │
                    │         +                    │
                    │  Outil gratuit sur site      │
                    │  (lead magnet technique)     │
                    └──────────┬──────────────────┘
                               │
                               ▼
                    ┌─────────────────────────────┐
                    │   LAYER 2 — CONFIANCE       │
                    │   (Transformer en audience)  │
                    │                             │
                    │  Site perso one-page         │
                    │  (QG de conversion)          │
                    │         +                    │
                    │  Newsletter hebdo            │
                    │  "Ce que j'ai buildé"        │
                    │         +                    │
                    │  GitHub (ce repo + projets)  │
                    │         +                    │
                    │  Études de cas / témoignages │
                    └──────────┬──────────────────┘
                               │
                               ▼
                    ┌─────────────────────────────┐
                    │   LAYER 3 — CONVERSION      │
                    │   (Transformer en client)    │
                    │                             │
                    │  4 portes de sortie :        │
                    │                             │
                    │  🔵 Offres packagées fixes   │
                    │     → Call de 15 min         │
                    │     → Devis → Mission        │
                    │                             │
                    │  🟢 Malt.fr                  │
                    │     → Mission freelance      │
                    │                             │
                    │  🟡 Micro-SaaS solo          │
                    │     → Abonnement Stripe      │
                    │                             │
                    │  🔴 DM LinkedIn/Twitter      │
                    │     → Projet custom          │
                    └─────────────────────────────┘
```

---

### LAYER 1 — VISIBILITÉ (Attirer des inconnus)

**Objectif :** Être vu par les bonnes personnes, régulièrement, sans payer.

#### Contenu LinkedIn + Twitter (3x/semaine)

| Type | Fréquence | Format | Objectif |
|---|---|---|---|
| "Je viens de builder ça" | 1x/sem | Screenshot/vidéo 30s + histoire du problème résolu | Prouver la compétence |
| "Ce que j'ai appris" | 1x/sem | Texte, leçon d'un projet/échec | Créer de la connexion humaine |
| "Hot take / opinion" | 1x/sem | Texte, point de vue tranché sur IA/SaaS/dev | Générer du reach via le débat |
| "Résultat client" | Dès dispo | Étude de cas anonymisée | Preuve sociale |

#### Règles de contenu
- Première ligne = hook (la seule chose que les gens voient avant de cliquer "voir plus")
- Compréhensible par un fondateur non-technique
- Montrer des RÉSULTATS, pas du process
- Chaque post a un CTA implicite : profil → site → offres
- Jamais de contenu qui attire des juniors au lieu de clients
- Recycler : un post LinkedIn → un thread Twitter → un bout de newsletter

#### L'outil gratuit (lead magnet technique)
- **Concept :** Un micro-outil en ligne qui résout un vrai problème en 30 secondes
- **Exemple :** Version gratuite limitée de Leak Detector (1 analyse/jour, rapport simplifié) OU un testeur de webhooks OU un mini audit de performance API
- **Pourquoi c'est l'arme ultime :** 
  - Il démontre tes compétences EN LIVE (pas de blabla, du concret)
  - Il tourne 24/7 sans toi
  - Il capture des emails ("entre ton email pour recevoir le rapport")
  - Il se partage naturellement (les gens partagent des outils utiles)
  - Il alimente ton contenu ("j'ai analysé 500 landing pages avec mon outil, voici les 3 erreurs les plus fréquentes")
- **Effort :** 1-2 jours de dev max (tu as déjà la base avec Leak Detector)
- **Hébergement :** [ton-domaine-perso].com/tools/[nom-outil]

---

### LAYER 2 — CONFIANCE (Transformer en audience fidèle)

**Objectif :** Quelqu'un a vu un post ou testé l'outil gratuit. Il doit maintenant se dire "ce mec est sérieux, je le garde en tête".

#### Site perso one-page (QG de conversion)
- **URL :** [ton-prenom-nom].dev ou [ton-brand].com
- **Hébergement :** Vercel (gratuit)
- **Stack :** Next.js (évidemment — c'est ta vitrine technique)

**Structure de la page :**

```
1. HERO — Accroche (1 phrase) + sous-titre + CTA principal
   "Je construis des SaaS, APIs et agents IA qui tournent en production."
   [Voir mes offres] [Tester mon outil gratuit]

2. PREUVES — Tes 2 SaaS en production
   PayloadDiff : screenshot + 1 ligne + lien
   Leak Detector : screenshot + 1 ligne + lien
   + Logos des technos (FastAPI, Next.js, Supabase, Stripe...)

3. OFFRES PACKAGÉES — 3 offres claires avec prix
   (détail ci-dessous)

4. TÉMOIGNAGES — Avis Malt + retours clients
   (vide au début, à remplir dès la première mission)

5. OUTIL GRATUIT — Embedded ou lien vers le lead magnet
   "Testez votre landing page gratuitement"
   → Capture email

6. NEWSLETTER — Inscription
   "Chaque semaine, ce que j'ai buildé et ce que j'ai appris"

7. CONTACT — Calendly/Cal.com pour booker un call de 15 min
   + Lien Malt + Lien LinkedIn + Lien Twitter
```

**Règles du site :**
- Zéro page "à propos" séparée. Tout est sur une seule page.
- Temps de chargement < 2 secondes (c'est ta vitrine technique)
- Mobile-first (les gens cliquent depuis LinkedIn sur leur phone)
- Pas de stock photos. Screenshots réels, code réel, résultats réels.

#### Newsletter hebdo
- **Outil :** Brevo (gratuit jusqu'à 300 emails/jour, tu connais déjà)
- **Rythme :** 1x/semaine, le mardi ou jeudi matin
- **Format :** Court (< 500 mots). Ce que j'ai buildé cette semaine + 1 leçon + 1 lien utile
- **Objectif :** Rester dans la tête des gens qui ne sont pas encore prêts à acheter
- **Capture :** Via l'outil gratuit + footer du site + CTA dans les posts LinkedIn/Twitter

#### GitHub (ce repo)
- Ce repo freelance-hub = ta source de vérité
- Tes repos SaaS (publics ou partiels) = preuve technique
- Un profil GitHub propre avec README de profil optimisé

---

### LAYER 3 — CONVERSION (Transformer en client qui paie)

**Objectif :** Quelqu'un te fait confiance. Il faut que passer à l'achat soit FRICTIONLESS.

#### Les 3 offres packagées (CRITICAL)

> Tu ne vends pas du temps. Tu vends un RÉSULTAT avec un prix fixe.
> Le client ne veut pas "un dev à 350€/jour". Il veut "mon problème résolu pour X€".

| Offre | Ce que le client obtient | Prix | Durée | Marge visée |
|---|---|---|---|---|
| **🔵 STARTER — Audit & Plan** | Audit technique de son projet/idée + architecture recommandée + roadmap chiffrée. Livrable : document PDF détaillé + call de restitution 30 min | 500€ fixe | 1-2 jours | Élevée |
| **🟢 BUILD — MVP / Feature** | Un MVP SaaS fonctionnel OU une feature complète livrée en production. Backend + frontend + auth + deploy | 2 500 - 5 000€ fixe | 1-2 semaines | Moyenne |
| **🟡 SCALE — Système complet** | Système complet : SaaS + paiement + monitoring + documentation + handover. Ou agent IA + automatisation + intégrations | 5 000 - 10 000€+ fixe | 2-4 semaines | Élevée |

**Pourquoi 3 offres :**
- Le STARTER est une porte d'entrée low-risk. Le client teste sans gros engagement → s'il est content, il prend le BUILD
- Le BUILD est le sweet spot. C'est ce qui remplace le freelance au TJM classique, mais packagé = plus attractif
- Le SCALE est le premium. Peu de clients mais gros ticket

**Règle d'or :** Le client choisit l'offre, pas le nombre de jours. Tu gères ton temps comme tu veux. Si tu livres le BUILD en 4 jours au lieu de 10, tu gagnes 2500€ en 4 jours = 625€/jour effectif. C'est ça l'avantage du packagé.

#### Processus de vente

```
Le client voit une offre sur le site
        ↓
CTA → Book un call de 15 min (Cal.com / Calendly)
        ↓
Call découverte (15 min) :
  - Comprendre le besoin
  - Qualifier (budget, timeline, sérieux)
  - Proposer l'offre adaptée
        ↓
Devis envoyé dans les 24h (template prêt)
        ↓
Acompte 50% via Stripe ou virement
        ↓
Livraison
        ↓
Solde 50%
        ↓
Demande d'avis (Malt si mission Malt, témoignage si hors Malt)
        ↓
Post LinkedIn "étude de cas" → alimente le Layer 1
```

#### Malt.fr (en parallèle)
- Profil optimisé (voir profil-malt-alti.md)
- Même offres packagées mais adaptées au format Malt
- Les avis Malt alimentent la section témoignages du site perso
- Malt = canal complémentaire, pas canal principal à terme

#### Micro-SaaS solo (revenu récurrent)
- Lancé à partir du mois 2+ quand le freelance tourne
- Shippé en 1 semaine max
- Pricing 19-49€/mois
- Promu via la newsletter + LinkedIn/Twitter
- Le MRR s'accumule pendant que tu fais des missions

---

## MÉTRIQUES À TRACKER

### Visibilité (Layer 1)
| Métrique | Objectif mois 1 | Objectif mois 3 | Objectif mois 6 |
|---|---|---|---|
| Vues LinkedIn / semaine | 1 000 | 5 000 | 15 000 |
| Followers LinkedIn | 100 | 500 | 1 500 |
| Followers Twitter | 50 | 300 | 1 000 |
| Utilisateurs outil gratuit / semaine | 10 | 50 | 200 |

### Confiance (Layer 2)
| Métrique | Objectif mois 1 | Objectif mois 3 | Objectif mois 6 |
|---|---|---|---|
| Visiteurs site perso / semaine | 50 | 200 | 500 |
| Inscrits newsletter | 10 | 100 | 500 |
| Avis Malt 5★ | 0 | 3 | 8 |

### Conversion (Layer 3)
| Métrique | Objectif mois 1 | Objectif mois 3 | Objectif mois 6 |
|---|---|---|---|
| Calls de découverte / mois | 1 | 4 | 8 |
| Missions signées / mois | 0 | 2 | 3 |
| CA freelance / mois | 0€ | 3 000€ | 5 000€ |
| MRR micro-SaaS | 0€ | 0€ | 500€ |
| CA total / mois | 0€ | 3 000€ | 5 500€ |

---

## OUTILS DU FUNNEL

| Besoin | Outil | Coût |
|---|---|---|
| Site perso | Next.js sur Vercel | Gratuit |
| Prise de RDV | Cal.com (open source) | Gratuit |
| Newsletter | Brevo | Gratuit (< 300 emails/jour) |
| Paiement | Stripe | Commission uniquement |
| Outil gratuit | Hébergé sur ton site (Railway backend) | ~5€/mois |
| CRM / suivi leads | Notion ou Google Sheet | Gratuit |
| Analytics site | Plausible ou Umami (self-hosted) | Gratuit |
| Devis / factures | Henrri ou Tiime | Gratuit |

**Coût total du funnel : < 10€/mois.** Tout le reste c'est du temps.

---

## TYPES DE CONTENU (LinkedIn + Twitter)

### Post type 1 — "Je viens de builder ça" (1x/semaine)
Screenshot ou vidéo 30s d'un feature, SaaS, automatisation. Problème résolu + techno utilisée + résultat concret.

### Post type 2 — "Ce que j'ai appris" (1x/semaine)
Leçon tirée d'un projet, échec, décision technique. Les gens apprennent des erreurs des autres.

### Post type 3 — "Hot take / opinion tranchée" (1x/semaine)
Point de vue cash sur l'IA, les SaaS, le dev, l'automatisation. Débat = reach.

### Post type 4 — "Résultat client / étude de cas" (dès qu'il y en a)
Mission livrée ou SaaS vendu → post anonymisé. Preuve sociale ultime.

### Recyclage de contenu
```
1 post LinkedIn
   → Adapté en thread Twitter
   → Le meilleur du mois → Newsletter
   → Les stats de l'outil gratuit → Post dédié
   → Étude de cas → Témoignage sur le site
```

### Règles de contenu
- Compréhensible par un fondateur non-technique
- Montrer, pas raconter
- Toujours un hook dans la première ligne
- Chaque post a un CTA implicite vers le profil/site
- Jamais de contenu qui attire des juniors au lieu de clients

---

## OBJECTIFS

### Court terme (0-3 mois)
1. Profil Malt live → première mission
2. Site perso live avec offres packagées
3. Outil gratuit live sur le site
4. LinkedIn + Twitter actifs (3 posts/semaine)
5. Newsletter lancée
6. 2-3 missions complétées avec avis 5★
7. Premiers DM entrants
8. Objectif CA : 3 000€/mois

### Moyen terme (3-6 mois)
1. Pipeline de leads entrants régulier
2. Premier micro-SaaS solo lancé
3. Offres packagées rodées, conversion en hausse
4. 100+ inscrits newsletter
5. Marque personnelle reconnue dans la niche IA/automatisation
6. Objectif CA : 5 000€/mois (freelance + MRR)

### Long terme (6-12 mois)
1. MRR micro-SaaS > 1 000€/mois
2. Capacité à choisir ses missions
3. Réduction progressive du freelance si MRR suffisant
4. Personal brand établi = les clients viennent à moi
5. Objectif CA : 8 000€+/mois

---

## PRINCIPES

- **Ship > Perfect** — Un produit livré bat un produit parfait jamais sorti
- **Résultats > Temps** — Je vends des outcomes, pas des jours
- **Preuves > Promesses** — Mes SaaS en production parlent mieux qu'un CV
- **Cashflow > Vanity metrics** — 1 client qui paie > 10 000 followers
- **Build in public** — Montrer ce que je construis, pas raconter ce que je pourrais faire
- **Focus > Dispersion** — 3 canaux maîtrisés > 7 canaux médiocres
- **Système > Effort** — Chaque action alimente les autres (contenu → leads → clients → contenu)
- **Code production-ready** — Documentation, tests, error handling, monitoring. Toujours
- **Je n'attends personne** — Si je peux le faire, je le fais maintenant
