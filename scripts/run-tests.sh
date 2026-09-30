#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
for t in check-generated.sh test-generators.sh test-resolve-wiki-root.sh test-agent-handoff-validator.sh test-private-terms.sh; do
  bash "$ROOT_DIR/scripts/$t"
done
