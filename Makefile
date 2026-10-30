.PHONY: install lint format test run image ci act-ci

install:
	pip install -e ".[dev]"

lint:
	ruff check .
	ruff format --check .
	mypy app

format:
	ruff format .
	ruff check --fix .

test:
	pytest --cov=app --cov-report=term-missing --cov-fail-under=80

run:
	uvicorn app.main:app --reload

image:
	docker build -t taskapi:local .

ci: lint test image

act-ci:
	act push -W .github/workflows/ci.yml
