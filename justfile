setup:
    just setup-python
    just npm-i

setup-python:
    python -m pip install pip-tools~=7.4.1
    just sync

comp-sync:
    just compile
    just sync

compile:
    pip-compile requirements.in --strip-extras --generate-hashes

sync:
    pip-sync

npm-i:
    cd ui && npm i

update-deps:
    pip-compile requirements.in --strip-extras --generate-hashes --upgrade
    cd ui && npm update

build:
    python -m app.build

deploy:
    netlify deploy --prod

lint-python:
    ruff check
    black --check .
    isort . --check
