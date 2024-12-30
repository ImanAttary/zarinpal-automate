## For running test (on windows):
    - cd zarinpal
    - python -m venv venv
    - cd .\venv\Scripts
    - .\activate 
    - cd ../.. 
    - pip install -r requirements.txt 
    - pytest


## For running test (on macOS):
    - cd zarinpal
    - python -m venv venv
    - source venv/bin/activate
    - cd ../.. 
    - pip install -r requirements.txt 
    - pytest



## For running test (linux):
    - docker compose up -d --build
    - docker logs -f pytest
    - docker compose down

## For Local TEST on Linux:

    - docker compose -f docker-compose-local.yml up -d --build