FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim

WORKDIR /app

# Copy workspace root files for dependency resolution
COPY pyproject.toml uv.lock ./

# Copy API package
COPY apps/apis ./apps/apis

# Enable bytecode compilation during installation
ENV UV_COMPILE_BYTECODE=1

# Install dependencies for the api package
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --package apis

# Python optimizations
ENV PYTHONOPTIMIZE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Use the virtual environment
ENV PATH="/app/.venv/bin:$PATH"

# Make the 'apis' package importable
ENV PYTHONPATH="/app/apps/apis/src:$PYTHONPATH"

# Create a non-root user
RUN addgroup --system app && \
    adduser --system --ingroup app app && \
    chown -R app:app /app

# Switch to non-root user
USER app

# Expose FastAPI port
EXPOSE 8000

# Move into the source directory
WORKDIR /app/apps/apis/src

# Run FastAPI
CMD ["uvicorn", "apis.app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]