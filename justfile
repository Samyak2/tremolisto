setup:
    just setup-python
    just npm-i

setup-python:
    uv sync

npm-i:
    cd ui && npm i

update-deps:
    uv sync --upgrade
    cd ui && npm update

build:
    python -m app.build

deploy:
    netlify deploy --prod

lint-python:
    ruff check
    ruff format --check
