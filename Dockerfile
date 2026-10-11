FROM ghcr.io/astral-sh/uv:0.11.15 AS uv
FROM python:3.12-slim
COPY --from=uv /uv /uvx /bin/
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev
COPY aviation_audit.py flight_research.py ./
COPY scripts ./scripts
CMD ["uv", "run", "--no-dev", "python", "scripts/demo.py"]

