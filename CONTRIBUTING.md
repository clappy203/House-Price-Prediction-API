# Contributing

Thanks for your interest in improving this project!

## Getting started

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
make install        # installs the package + dev tools + pre-commit hooks
make train          # creates artifacts/model.joblib
make check          # runs lint, type-checks, and tests
```

## Ground rules

- Every change should keep `make check` green (ruff, black, mypy, pytest).
- Add or update tests for any behavior change.
- Keep public functions typed and documented.
- Commits are checked by `pre-commit`; run `pre-commit run --all-files` before pushing.

## Pull requests

1. Fork and create a feature branch.
2. Make your change with tests.
3. Ensure CI passes.
4. Open a PR describing the motivation and approach.
