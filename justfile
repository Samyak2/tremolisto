comp-sync:
    just compile
    just sync

compile:
    pip-compile requirements.in --strip-extras --generate-hashes

sync:
    pip-sync

serve:
    uvicorn app.main:app --reload --port 3009

build:
    python -m app.build_html

deploy:
    netlify deploy --prod
