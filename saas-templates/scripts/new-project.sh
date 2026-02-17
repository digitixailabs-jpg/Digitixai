#!/bin/bash

# =============================================================================
# new-project.sh - Create a new SaaS project from templates
# =============================================================================

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATES_DIR="$(dirname "$SCRIPT_DIR")"

print_success() { echo -e "${GREEN}✓${NC} $1"; }
print_warning() { echo -e "${YELLOW}⚠${NC} $1"; }
print_error() { echo -e "${RED}✗${NC} $1"; }
print_header() { echo -e "\n${GREEN}=== $1 ===${NC}\n"; }

if [ -z "$1" ]; then
    echo "Usage: $0 <project-name>"
    exit 1
fi

PROJECT_NAME="$1"
PROJECT_DIR="$(pwd)/$PROJECT_NAME"

if [ -d "$PROJECT_DIR" ]; then
    print_error "Directory $PROJECT_DIR already exists"
    exit 1
fi

print_header "Creating new project: $PROJECT_NAME"

mkdir -p "$PROJECT_DIR"/{backend,frontend,docs}
cd "$PROJECT_DIR"

# Copy backend
cp -r "$TEMPLATES_DIR/backend-starter/"* backend/
print_success "Backend setup complete"

# Copy frontend
cp -r "$TEMPLATES_DIR/frontend-starter/"* frontend/
print_success "Frontend setup complete"

# Copy docs (rename .template.md to .md)
for file in "$TEMPLATES_DIR/docs-templates/"*.template.md; do
    filename=$(basename "$file" .template.md)
    cp "$file" "docs/${filename}.md"
done
print_success "Documentation templates copied"

# Copy root files
cp "$TEMPLATES_DIR/docs-templates/CLAUDE.template.md" "CLAUDE.md"
cp "$TEMPLATES_DIR/docs-templates/context.template.md" "context.md"

# Copy legal
mkdir -p docs/legal
cp -r "$TEMPLATES_DIR/legal-templates/"* docs/legal/

# Copy CI/CD
mkdir -p .github/workflows
cp "$TEMPLATES_DIR/deploy-configs/.github/workflows/"* .github/workflows/

# Create README
cat > README.md << EOF
# $PROJECT_NAME

## Quick Start

### Backend
\`\`\`bash
cd backend && python -m venv venv && source venv/bin/activate
pip install -r requirements.txt && cp .env.example .env
uvicorn app.main:app --reload
\`\`\`

### Frontend
\`\`\`bash
cd frontend && npm install && cp .env.example .env.local
npm run dev
\`\`\`

## Documentation
See \`/docs\` for SPEC.md, ARCH.md, UI.md, etc.
EOF

# Create .gitignore
cat > .gitignore << 'EOF'
node_modules/
venv/
__pycache__/
.env
.env.local
.next/
dist/
.DS_Store
*.log
coverage/
.pytest_cache/
EOF

# Init git
git init && git add . && git commit -m "feat: initial setup from saas-templates"

print_header "Done! 🎉"
echo "Next: cd $PROJECT_NAME && fill context.md, CLAUDE.md, docs/SPEC.md"
