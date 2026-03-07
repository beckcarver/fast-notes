# fast notes
Super basic fast-api app mostly built to learn the basics of fast-api and python api project conventions

## Running the backend locally
uv run uvicorn src.fast_notes.main:app --reload

## Running frontend and backend via docker
docker compose up -d --build --remove-orphans
