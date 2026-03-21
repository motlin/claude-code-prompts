set shell := ["bash", "-O", "globstar", "-c"]

default:
    @just --list --unsorted

# Run shellcheck on shell scripts
shellcheck:
    git ls-files '*.sh' | xargs shellcheck

# Format shell scripts with shfmt
shfmt:
    git ls-files '*.sh' | xargs shfmt --write --indent 4 --binary-next-line --case-indent

# Run all pre-commit checks
precommit: shellcheck shfmt
    @echo "All pre-commit checks passed!"
