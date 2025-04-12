# Use a lightweight Python image
FROM python:3.12-slim-bookworm

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy the project into the image
ADD ./app /app

# COPY uv.lock /uv.lock
COPY uv.lock /app/uv.lock
COPY .python-version /app/python-version

# Sync the project into a new environment, using the frozen lockfile
WORKDIR /app
COPY uv.lock /app/uv.lock
RUN uv sync --frozen

# Expose the port FastAPI will use
EXPOSE 8000

# Run the application using Uvicorn
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]