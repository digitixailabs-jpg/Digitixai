# Backup & Recovery — [NOM_PROJET]

> Ce document définit la stratégie de backup et les procédures de restauration.

---

## Vue d'ensemble

| Donnée | Criticité | Backup | Rétention | RTO | RPO |
|--------|-----------|--------|-----------|-----|-----|
| Database (Supabase) | Critique | Auto daily | 7 jours (free) / 30 jours (pro) | <1h | <24h |
| User uploads | Haute | Supabase Storage | Permanent | <1h | <1h |
| Code | Haute | Git | Permanent | <5min | 0 |
| Config/Secrets | Haute | Manual export | N/A | <30min | N/A |
| Logs | Basse | Railway retention | 7-30 jours | N/A | N/A |

**RTO** = Recovery Time Objective (temps max pour restaurer)
**RPO** = Recovery Point Objective (perte de données max acceptable)

---

## Database (Supabase)

### Backups automatiques

Supabase effectue des backups automatiques :
- **Free tier** : Daily, 7 jours de rétention
- **Pro tier** : Daily, 30 jours de rétention + Point-in-Time Recovery

### Accéder aux backups

1. Supabase Dashboard → Project → Settings → Database
2. Section "Backups"
3. Liste des backups disponibles

### Restaurer un backup (Supabase Pro)

1. Dashboard → Settings → Database → Backups
2. Sélectionner le backup souhaité
3. Click "Restore"
4. ⚠️ Cela écrase la DB actuelle

### Export manuel (recommandé avant migrations risquées)

```bash
# Via Supabase CLI
supabase db dump -f backup_$(date +%Y%m%d_%H%M%S).sql

# Via pg_dump direct
pg_dump "postgresql://postgres:[password]@db.[project].supabase.co:5432/postgres" \
  --no-owner \
  --no-privileges \
  -f backup_$(date +%Y%m%d_%H%M%S).sql
```

### Restore depuis dump

```bash
# Reset et restore
psql "postgresql://postgres:[password]@db.[project].supabase.co:5432/postgres" \
  -f backup_20260115_120000.sql
```

---

## Point-in-Time Recovery (PITR)

Disponible sur Supabase Pro. Permet de restaurer à n'importe quel moment des 7 derniers jours.

### Quand utiliser PITR

- Suppression accidentelle de données
- Corruption de données
- Besoin de restaurer à un moment précis (avant un incident)

### Procédure

1. Dashboard → Settings → Database
2. Click "Point in Time Recovery"
3. Sélectionner date/heure
4. Confirmer restauration
5. ⚠️ Downtime pendant restauration

---

## User uploads (Supabase Storage)

### Backup

Supabase Storage n'a pas de backup automatique intégré. Options :

**Option 1 : Script de sync périodique**

```python
# scripts/backup_storage.py
import os
from supabase import create_client

supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_KEY"])

def backup_bucket(bucket_name: str, local_path: str):
    """Download tous les fichiers d'un bucket"""
    files = supabase.storage.from_(bucket_name).list()
    
    for file in files:
        data = supabase.storage.from_(bucket_name).download(file["name"])
        
        local_file = os.path.join(local_path, file["name"])
        os.makedirs(os.path.dirname(local_file), exist_ok=True)
        
        with open(local_file, "wb") as f:
            f.write(data)

# Usage
backup_bucket("uploads", "./backups/storage/uploads/")
```

**Option 2 : Sync vers S3/R2**

Configurer un job périodique qui copie vers un autre bucket.

---

## Code (Git)

Le code est versionné sur GitHub. En cas de perte :

```bash
# Clone fresh
git clone https://github.com/[org]/[repo].git

# Restaurer une version spécifique
git checkout [commit-hash]
git checkout tags/v1.0.0
```

---

## Secrets et configuration

### Export des secrets

**Ne jamais** stocker les secrets en clair. Procédure pour documentation :

1. Lister toutes les variables d'environnement
2. Documenter dans un password manager (1Password, Bitwarden)
3. Stocker les clés de récupération hors-ligne

### Variables à sauvegarder

| Variable | Location | Recovery |
|----------|----------|----------|
| `SUPABASE_SERVICE_KEY` | Railway/Vercel | Regenerate in Supabase Dashboard |
| `STRIPE_SECRET_KEY` | Railway/Vercel | Stripe Dashboard → API Keys |
| `STRIPE_WEBHOOK_SECRET` | Railway | Stripe Dashboard → Webhooks |
| `ANTHROPIC_API_KEY` | Railway | Anthropic Console |
| `APP_SECRET_KEY` | Railway | Regenerate (rotate sessions) |

---

## Procédures de restauration

### Scenario 1 : Suppression accidentelle de données

**Symptômes** : User ou admin a supprimé des données par erreur

**Procédure** :
1. Identifier l'heure exacte de la suppression
2. Si <24h et PITR disponible :
   - Utiliser PITR pour restaurer à T-1h
3. Si pas de PITR :
   - Restaurer depuis dernier backup daily
   - Accepter perte de données depuis backup
4. Communiquer avec users affectés

**Temps estimé** : 30min - 2h

---

### Scenario 2 : Corruption de base de données

**Symptômes** : Erreurs DB, données incohérentes, contraintes violées

**Procédure** :
1. **Stopper l'application** (éviter plus de corruption)
   ```bash
   # Railway → Service → Stop
   ```
2. Exporter l'état actuel (pour analyse post-mortem)
   ```bash
   supabase db dump -f corrupted_$(date +%Y%m%d).sql
   ```
3. Restaurer depuis dernier backup sain
4. Vérifier intégrité
   ```sql
   -- Check constraints
   SELECT conname, conrelid::regclass FROM pg_constraint WHERE NOT convalidated;
   ```
5. Redémarrer l'application
6. Post-mortem

**Temps estimé** : 1-4h

---

### Scenario 3 : Perte totale infrastructure

**Symptômes** : Provider down, compte compromis, disaster

**Procédure** :
1. Créer nouveau projet Supabase
2. Restaurer DB depuis backup (téléchargé localement ou autre region)
3. Créer nouveaux services Railway/Vercel
4. Configurer nouveaux secrets
5. Mettre à jour DNS
6. Restaurer Storage depuis backup

**Temps estimé** : 4-8h

---

### Scenario 4 : Ransomware / Compte compromis

**Symptômes** : Accès bloqué, données chiffrées, demande de rançon

**Procédure** :
1. **Ne pas payer**
2. Contacter support providers (Supabase, Railway, Vercel)
3. Révoquer tous les tokens/clés
4. Restaurer depuis backup hors-ligne (si disponible)
5. Audit de sécurité complet
6. Déclaration CNIL si données personnelles (GDPR)

**Temps estimé** : 24-72h

---

## Tests de restauration

### Fréquence

| Test | Fréquence | Responsable |
|------|-----------|-------------|
| Restore DB en staging | Mensuel | Tech Lead |
| Vérification backup existe | Hebdo (automatisé) | Monitoring |
| Full disaster recovery drill | Trimestriel | CTO |

### Checklist test restore

```markdown
- [ ] Télécharger dernier backup
- [ ] Créer DB de test
- [ ] Restaurer backup dans DB test
- [ ] Vérifier intégrité données
- [ ] Vérifier nombre de rows cohérent
- [ ] Tester une requête métier
- [ ] Documenter résultat et durée
```

---

## Contacts d'urgence

| Service | Contact | SLA |
|---------|---------|-----|
| Supabase Support | support@supabase.io | 24h (free) / 4h (pro) |
| Railway Support | Discord / support | Best effort |
| Vercel Support | support@vercel.com | 24h |

---

## Checklist mensuelle backup

- [ ] Vérifier que backups Supabase sont actifs
- [ ] Test restore en staging
- [ ] Vérifier secrets documentés et à jour
- [ ] Vérifier accès aux backups (permissions)
- [ ] Review rétention (suffisante ?)
