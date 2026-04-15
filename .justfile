run:
    uv run python -m ddnet_change_color

test:
    uv run pytest --cov=ddnet_change_color

lint:
    uv run ruff check . && uv run pyright

format:
    uv run ruff format . && uv run ruff check --fix .

check: lint test

dev:
    uv sync --dev

install:
    uv sync

clean:
    rm -rf .pytest_cache .ruff_cache .coverage htmlcov __pycache__ */__pycache__ */*/__pycache__
