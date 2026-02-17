# Changelog — [NOM_PROJET]

Toutes les modifications notables de ce projet sont documentées ici.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added
- 

### Changed
-

### Fixed
-

### Removed
-

---

## [1.0.0] - 2026-XX-XX

### Added
- 🎉 Initial release
- Authentification (email + Google OAuth)
- Dashboard utilisateur
- [Feature principale] avec [détails]
- Paiement Stripe (subscription/one-time)
- Panel admin basique

### Technical
- Backend FastAPI déployé sur Railway
- Frontend Next.js 14 déployé sur Vercel
- Database Supabase PostgreSQL
- Queue Celery + Redis

---

## Convention de versioning

### Semantic Versioning

```
MAJOR.MINOR.PATCH

MAJOR : Changements incompatibles (breaking changes)
MINOR : Nouvelles fonctionnalités (backward compatible)
PATCH : Bug fixes (backward compatible)
```

### Exemples

| Version | Type | Exemple |
|---------|------|---------|
| 1.0.0 → 2.0.0 | MAJOR | Refonte API, changement de structure DB |
| 1.0.0 → 1.1.0 | MINOR | Nouvelle feature, nouvel endpoint |
| 1.0.0 → 1.0.1 | PATCH | Bug fix, correction typo |

### Pre-release

```
1.0.0-alpha.1  → Très instable, en développement
1.0.0-beta.1   → Feature complete, en test
1.0.0-rc.1     → Release candidate, prêt pour prod
1.0.0          → Release stable
```

---

## Types de changements

- **Added** : Nouvelles fonctionnalités
- **Changed** : Modifications de fonctionnalités existantes
- **Deprecated** : Fonctionnalités qui seront supprimées
- **Removed** : Fonctionnalités supprimées
- **Fixed** : Corrections de bugs
- **Security** : Corrections de vulnérabilités

---

## Template d'entrée

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added
- Nouvelle feature X (#PR_NUMBER)
- Support de Y pour Z

### Changed
- Amélioration performance de A
- Refactoring de B pour meilleure maintenabilité

### Fixed
- Correction bug où X causait Y (#ISSUE_NUMBER)
- Fix typo dans message d'erreur

### Security
- Mise à jour dépendance X (CVE-XXXX-XXXX)

### Breaking Changes
- ⚠️ L'endpoint `/api/v1/old` est remplacé par `/api/v1/new`
- ⚠️ Le champ `old_field` est renommé `new_field`
```

---

## Liens

[Unreleased]: https://github.com/[org]/[repo]/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/[org]/[repo]/releases/tag/v1.0.0
