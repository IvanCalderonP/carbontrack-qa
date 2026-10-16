.PHONY: install backend-install frontend-install backend-test frontend-test test lint coverage up down clean

install: backend-install frontend-install

backend-install:
	cd backend && python -m pip install -r requirements-dev.txt

frontend-install:
	cd frontend && npm ci

backend-test:
	cd backend && pytest

frontend-test:
	cd frontend && npm test

test: backend-test frontend-test

lint:
	cd backend && ruff check app tests migrations ../sample-data/generate_samples.py && ruff format --check app tests migrations ../sample-data/generate_samples.py
	cd frontend && npm run lint && npm run typecheck

coverage:
	cd backend && pytest --cov=app --cov-report=term-missing --cov-report=html --cov-fail-under=85
	cd frontend && npm run coverage

up:
	docker compose up --build

down:
	docker compose down

clean:
	cd frontend && node -e "require('fs').rmSync('dist',{recursive:true,force:true});require('fs').rmSync('coverage',{recursive:true,force:true})"
	cd backend && python -c "import shutil;shutil.rmtree('htmlcov',ignore_errors=True)"
