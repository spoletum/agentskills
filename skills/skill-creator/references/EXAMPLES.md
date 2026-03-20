# Skill Creation Examples

Loaded when: You need concrete examples of well-structured skills.

## Example 1: Simple Utility Skill (Dice Rolling)

**File**: `roll-dice/SKILL.md`
**Lines**: ~15
**Use case**: Single, well-defined task

```markdown
---
name: roll-dice
description: Roll dice with true randomness. Use when asked to roll a die (d6, d20, etc.), roll dice, or generate a random dice roll.
---

To roll a die, use the following command:

```bash
shuf -i 1-<sides> -n 1        # Linux/Mac
Get-Random -Minimum 1 -Maximum (<sides> + 1)  # PowerShell
```

Replace `<sides>` with the number of sides (e.g., 6 for d6, 20 for d20).
```

**Why it works**:
- Minimal frontmatter, clear description
- No unnecessary explanation of what dice are
- Concrete commands for different platforms
- Single focus (just rolling dice)

---

## Example 2: Complex Workflow Skill (Database Migration)

**File**: `db-migrate/SKILL.md`
**Lines**: ~80
**Use case**: Multi-step workflow with validation

```markdown
---
name: db-migrate
description: Run database migrations safely with backup, verification, and rollback. Use when modifying database schema, adding tables/columns, or updating production databases.
metadata:
  author: team-backend
  version: "1.0.0"
---

# Database Migration

Run database schema changes safely with proper safeguards.

## When to Use

- Adding/modifying tables or columns
- Creating indexes
- Any ALTER TABLE operations
- Schema updates in production

## Pre-flight Checklist

Before running migrations:
- [ ] Backup created: `scripts/backup.sh`
- [ ] Migration tested locally
- [ ] Migration file reviewed by 1+ team member
- [ ] Maintenance window scheduled (for production)
- [ ] Rollback plan documented

## Migration Workflow

### Step 1: Create Backup

**ALWAYS** create a backup first:

```bash
./scripts/backup.sh --env <environment>
```

Verify backup exists:
```bash
ls -la backups/ | head -5
```

### Step 2: Run Migration

Execute exactly this command (no additional flags):

```bash
python scripts/migrate.py --verify --backup
```

The `--verify` flag validates schema changes before applying.
The `--backup` flag ensures backup exists (redundant but safe).

### Step 3: Verify Results

Check migration output:
- Exit code 0: Success
- Exit code 1: Validation failed, no changes made
- Exit code 2: Error during migration (CHECK BACKUP)

Verify schema:
```bash
psql $DATABASE_URL -c "\dt" | grep <new_table>
```

### Step 4: Validation Tests

Run post-migration validation:

```bash
pytest tests/migration/ -v
```

## Gotchas

- Our migration system requires explicit transaction boundaries in `.sql` files
- Foreign key checks are disabled during migrations by default
- The `migrate.py` script has a 5-minute timeout - large table alterations may fail
- Indexes on tables >1M rows should use `CONCURRENTLY` flag

## Rollback Procedure

If migration fails after step 3:

```bash
# 1. Stop application
kubectl scale deployment app --replicas=0

# 2. Restore from backup
./scripts/restore.sh backups/<backup-file>

# 3. Verify restoration
./scripts/verify.sh

# 4. Restart application
kubectl scale deployment app --replicas=3
```

## Examples

### Example 1: Adding a Column

**Input**: "Add a 'status' column to the orders table"

**Process**:
1. Create migration file: `migrations/20240115_add_order_status.sql`
2. Content:
   ```sql
   BEGIN;
   ALTER TABLE orders ADD COLUMN status VARCHAR(20) DEFAULT 'pending';
   CREATE INDEX idx_orders_status ON orders(status);
   COMMIT;
   ```
3. Run migration workflow above
4. Verify: `SELECT column_name FROM information_schema.columns WHERE table_name = 'orders'`

### Example 2: Failed Migration Recovery

**Input**: "Migration failed with timeout error"

**Process**:
1. Check if backup exists: `ls backups/`
2. Stop traffic to affected service
3. Run rollback procedure above
4. Split migration into smaller batches
5. Retry with smaller scope
```

**Why it works**:
- Clear trigger conditions in description
- Checklist for manual verification steps
- Exact commands (prescriptive for safety)
- Gotchas capture non-obvious constraints
- Validation loop in workflow (run, verify, test)
- Rollback procedure for failure cases
- Real examples with concrete commands

---

## Example 3: Agent Configuration (Specialized Agent)

**File**: `code-reviewer/agent.json`
**Use case**: Defining a specialized AI agent

```json
{
  "name": "code-reviewer",
  "description": "Expert code reviewer focused on security, performance, and maintainability. Use when reviewing pull requests, auditing code, or checking for security issues.",
  "version": "1.0.0",
  "skills": ["security-check", "performance-audit", "style-check"],
  "config": {
    "model": "claude-3-opus-20240229",
    "temperature": 0.3,
    "max_tokens": 4000
  },
  "system_prompt": "You are an expert code reviewer with deep knowledge of security vulnerabilities, performance patterns, and clean code principles. Focus on catching critical issues, not style nits. Explain the 'why' behind your suggestions. Ask clarifying questions when code intent is unclear.",
  "tools": ["Read", "Grep", "Bash(git:*)"],
  "metadata": {
    "author": "security-team",
    "review_focus": ["security", "performance", "maintainability"],
    "tags": ["review", "security", "code-quality"]
  }
}
```

**Why it works**:
- Clear purpose in description
- Specific model for complex reasoning (opus)
- Lower temperature for consistency
- Curated list of relevant skills
- System prompt defines persona and priorities
- Limited tools (focused scope)

---

## Example 4: Command Definition (CLI Tool)

**File**: `deploy/command.json`
**Use case**: Packaging a CLI command with arguments

```json
{
  "name": "deploy",
  "description": "Deploy application to specified environment. Use when releasing code to staging or production.",
  "version": "1.0.0",
  "command": "./scripts/deploy.sh",
  "arguments": [
    {
      "name": "environment",
      "description": "Target environment (staging, production)",
      "required": true,
      "type": "string",
      "enum": ["staging", "production"]
    },
    {
      "name": "version",
      "description": "Version to deploy (tag or commit)",
      "required": true,
      "type": "string"
    }
  ],
  "options": {
    "--dry-run": {
      "description": "Show what would be deployed without executing",
      "type": "boolean",
      "default": false
    },
    "--force": {
      "description": "Skip confirmation prompts",
      "type": "boolean",
      "default": false
    },
    "--rollback": {
      "description": "Deploy previous version (rollback mode)",
      "type": "boolean",
      "default": false
    }
  },
  "help_text": "Deploy application to target environment.\n\nRequires:\n- Valid AWS credentials\n- kubectl configured for target cluster\n- Docker logged in to registry\n\nExamples:\n  deploy staging v1.2.3\n  deploy production v1.2.3 --dry-run\n  deploy production --rollback",
  "examples": [
    "deploy staging v1.2.3",
    "deploy production v1.2.3 --dry-run",
    "deploy production --rollback"
  ],
  "metadata": {
    "author": "devops-team",
    "dangerous": true,
    "tags": ["deploy", "release", "production"]
  }
}
```

**Why it works**:
- Clear description with trigger words
- Required vs optional arguments explicit
- Validation via enum for environment
- Dry-run option for safety
- Help text lists prerequisites
- Metadata flags dangerous operations

---

## Common Patterns Summary

| Pattern | Use When | Example |
|---------|----------|---------|
| **Prescriptive steps** | Safety-critical operations | Database migrations |
| **Checklists** | Multi-step workflows | Pre-flight checks |
| **Gotchas** | Non-obvious constraints | API quirks, naming conventions |
| **Validation loops** | Quality assurance | Run → Validate → Fix → Repeat |
| **Templates** | Consistent output format | Report generation |
| **Progressive disclosure** | Large reference material | Load details on-demand |

## Anti-Patterns to Avoid

❌ **Too generic**: "Handle errors appropriately" 
✅ **Specific**: "Catch TimeoutError and retry with exponential backoff"

❌ **No trigger**: "This skill helps with databases"
✅ **Clear trigger**: "Use when running schema migrations or ALTER TABLE operations"

❌ **Menu of options**: "You can use A, B, or C..."
✅ **Default + escape hatch**: "Use A. For edge case X, use B instead."

❌ **Explaining basics**: "PDFs are a file format that..."
✅ **Jump to specifics**: "Use pdfplumber for text extraction..."

❌ **One giant file**: 2000 lines covering everything
✅ **Progressive disclosure**: Core in SKILL.md, details in references/
