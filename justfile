setup:
    just setup-python
    just npm-i

setup-python:
    uv sync

npm-i:
    cd ui && npm i

update-deps:
    nix flake update
    uv sync --upgrade
    cd ui && npm update && npm audit fix

build:
    python -m app.build

deploy:
    netlify deploy --prod

lint-python:
    uv run ruff check
    uv run ruff format --check
