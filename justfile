compile:
    pip-compile requirements.in --strip-extras --generate-hashes

sync:
    pip-sync
