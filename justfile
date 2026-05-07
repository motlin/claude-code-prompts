set shell := ["bash", "-O", "globstar", "-c"]

# `just --list --unsorted`
default:
    @just --list --unsorted

# Run shellcheck, markdownlint, and yamllint
lint:
    git ls-files '*.sh' | xargs shellcheck
    git ls-files '*.md' | xargs markdownlint-cli2 --no-globs
    git ls-files '*.yaml' '*.yml' '.yamllint' | xargs yamllint --strict

# Format shell scripts and JSON; fail if anything changed
format:
    git ls-files '*.sh' | xargs shfmt -w --indent 4 --binary-next-line --case-indent
    oxfmt
    git diff --exit-code

# Run all pre-commit checks
precommit: format lint
    pre-commit run --all-files
