comp-sync:
    just compile
    just sync

compile:
    pip-compile requirements.in --strip-extras --generate-hashes

sync:
    pip-sync

build:
    python -m app.build

deploy:
    netlify deploy --prod
