set shell := ["bash", "-O", "globstar", "-c"]

# `just --list --unsorted`
default:
    @just --list --unsorted

# Run shellcheck, markdownlint, and yamllint
lint:
    git ls-files '*.sh' | xargs shellcheck
    git ls-files '*.md' | xargs markdownlint-cli2 --no-globs
    git ls-files '*.yaml' '*.yml' '.yamllint' | xargs yamllint --strict

# Check shell script and oxfmt formatting
format:
    git ls-files '*.sh' | xargs shfmt -d --indent 4 --binary-next-line --case-indent
    oxfmt --check

# Run all pre-commit checks
precommit: format lint
    pre-commit run --all-files
