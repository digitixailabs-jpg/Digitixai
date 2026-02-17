# Migrations Database — [NOM_PROJET]

> Ce document définit la stratégie de migrations et l'historique des changements DB.

---

## Stratégie

### Principes

1. **Migrations forward-only** : Pas de rollback auto, préparer migration inverse si nécessaire
2. **Backward compatible** : Chaque migration doit être compatible avec le code en prod pendant le deploy
3. **Atomique** : Une migration = un changement logique
4. **Testée** : Tester en staging avant prod
5. **Documentée** : Chaque migration décrite ici

### Workflow

```
1. Créer migration en local
   └── supabase migration new [name]

2. Tester en local
   └── supabase db reset (applique toutes migrations)

3. Appliquer en staging
   └── supabase db push --linked

4. Valider en staging
   └── Tests manuels + automatisés

5. Appliquer en production
   └── supabase db push --linked (sur projet prod)

6. Documenter ici
```

---

## Commandes Supabase CLI

```bash
# Login
supabase login

# Lier projet
supabase link --project-ref [project-id]

# Créer nouvelle migration
supabase migration new [nom_descriptif]
# Crée: supabase/migrations/[timestamp]_[nom_descriptif].sql

# Appliquer migrations (remote)
supabase db push

# Reset local (recrée DB + applique toutes migrations)
supabase db reset

# Voir différences
supabase db diff

# Générer migration depuis diff
supabase db diff -f [nom_migration]

# Voir status migrations
supabase migration list
```

---

## Conventions de nommage

```
[timestamp]_[action]_[table]_[detail].sql

Exemples:
20260115100000_create_users_table.sql
20260115100100_add_profiles_stripe_fields.sql
20260115100200_create_reports_table.sql
20260115100300_add_reports_status_index.sql
20260116090000_alter_profiles_add_credits.sql
```

### Actions

| Action | Usage |
|--------|-------|
| `create` | Nouvelle table |
| `alter` | Modifier table existante |
| `add` | Ajouter colonne/index/constraint |
| `drop` | Supprimer élément |
| `rename` | Renommer |
| `seed` | Données initiales |

---

## Structure des fichiers

```
supabase/
├── config.toml
├── migrations/
│   ├── 20260115100000_create_profiles_table.sql
│   ├── 20260115100100_create_reports_table.sql
│   └── ...
├── seed.sql              # Données de test (local only)
└── functions/            # Edge functions (si utilisées)
```

---

## Templates de migration

### Créer une table

```sql
-- migrations/[timestamp]_create_[table]_table.sql

-- Create table
CREATE TABLE [table_name] (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    
    -- Business fields
    name VARCHAR(255) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    
    -- Timestamps
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_[table]_user_id ON [table_name](user_id);
CREATE INDEX idx_[table]_status ON [table_name](status);
CREATE INDEX idx_[table]_created_at ON [table_name](created_at DESC);

-- Enable RLS
ALTER TABLE [table_name] ENABLE ROW LEVEL SECURITY;

-- RLS Policies
CREATE POLICY "[table]_select_own"
    ON [table_name] FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "[table]_insert_own"
    ON [table_name] FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "[table]_update_own"
    ON [table_name] FOR UPDATE
    USING (auth.uid() = user_id);

CREATE POLICY "[table]_delete_own"
    ON [table_name] FOR DELETE
    USING (auth.uid() = user_id);

-- Updated_at trigger
CREATE TRIGGER set_[table]_updated_at
    BEFORE UPDATE ON [table_name]
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

### Ajouter une colonne

```sql
-- migrations/[timestamp]_add_[table]_[column].sql

-- Add column (avec default pour backward compatibility)
ALTER TABLE [table_name]
ADD COLUMN [column_name] [TYPE] DEFAULT [default_value];

-- Si colonne NOT NULL sans default, faire en 2 étapes:
-- 1. Ajouter nullable
ALTER TABLE [table_name] ADD COLUMN [column_name] [TYPE];

-- 2. Backfill
UPDATE [table_name] SET [column_name] = [value] WHERE [column_name] IS NULL;

-- 3. Ajouter NOT NULL (migration suivante, après deploy code)
ALTER TABLE [table_name] ALTER COLUMN [column_name] SET NOT NULL;
```

### Ajouter un index

```sql
-- migrations/[timestamp]_add_[table]_[column]_index.sql

-- Create index concurrently (ne bloque pas les writes)
CREATE INDEX CONCURRENTLY idx_[table]_[column] ON [table_name]([column]);
```

### Supprimer une colonne

```sql
-- migrations/[timestamp]_drop_[table]_[column].sql

-- ⚠️ S'assurer que le code n'utilise plus cette colonne AVANT d'appliquer

ALTER TABLE [table_name] DROP COLUMN [column_name];
```

### Renommer

```sql
-- migrations/[timestamp]_rename_[table]_[old]_to_[new].sql

-- Renommer colonne
ALTER TABLE [table_name] RENAME COLUMN [old_name] TO [new_name];

-- Renommer table
ALTER TABLE [old_table] RENAME TO [new_table];
```

---

## Fonction utilitaire updated_at

```sql
-- À créer en première migration

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';
```

---

## Historique des migrations

### V1.0.0 - Initial Schema

| # | Migration | Description | Date | Auteur |
|---|-----------|-------------|------|--------|
| 1 | `20260115100000_create_profiles_table` | Table profiles avec champs Stripe | 2026-01-15 | [Nom] |
| 2 | `20260115100100_create_[feature]_table` | Table principale feature | 2026-01-15 | [Nom] |

### V1.1.0 - [Feature name]

| # | Migration | Description | Date | Auteur |
|---|-----------|-------------|------|--------|
| 3 | `20260120100000_add_profiles_credits` | Ajout système de crédits | 2026-01-20 | [Nom] |

---

## Seed data (développement)

```sql
-- supabase/seed.sql
-- Données de test pour environnement local

-- User de test (créé via Supabase Auth d'abord)
-- INSERT INTO profiles (id, email, full_name) VALUES
-- ('test-user-uuid', 'test@example.com', 'Test User');

-- Données de test feature
-- INSERT INTO [table] (user_id, name, status) VALUES
-- ('test-user-uuid', 'Test Item 1', 'completed'),
-- ('test-user-uuid', 'Test Item 2', 'pending');
```

---

## Checklist pré-migration (Production)

- [ ] Migration testée en local (`supabase db reset`)
- [ ] Migration appliquée en staging
- [ ] Tests passent en staging
- [ ] Code compatible avec ancien ET nouveau schema
- [ ] Backup récent vérifié
- [ ] Migration documentée ici
- [ ] Plan de rollback préparé (si applicable)
- [ ] Fenêtre de maintenance communiquée (si downtime)

---

## Rollback

### Si migration a échoué

```sql
-- Créer migration de rollback
supabase migration new rollback_[original_migration]

-- Contenu: opération inverse
-- Ex: si ADD COLUMN, faire DROP COLUMN
```

### Si données corrompues

1. Stopper l'application
2. Restaurer backup (voir BACKUP.md)
3. Réappliquer migrations jusqu'à version stable
4. Redéployer code compatible
5. Post-mortem

---

## Bonnes pratiques

### DO ✅

- Migrations petites et atomiques
- Tester en staging d'abord
- Backward compatible pendant deploy
- Indexes CONCURRENTLY
- Documenter chaque migration

### DON'T ❌

- Modifier une migration déjà appliquée en prod
- Supprimer colonne utilisée par le code
- ALTER TABLE sur grosse table sans CONCURRENTLY
- Migration avec downtime sans prévenir
- Oublier les RLS policies
