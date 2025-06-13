# Stage 1: Build dependencies
FROM python:3-alpine AS builder

WORKDIR /app

# Install build dependencies
RUN apk add --no-cache gcc musl-dev libffi-dev

# Create virtual environment manually
RUN python3 -m venv /app/venv
ENV VIRTUAL_ENV=/app/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Stage 2: Final container
FROM python:3-alpine AS runner

WORKDIR /app

# Copy virtual environment and app code
COPY --from=builder /app/venv /app/venv
COPY . .

# Copy the .env file into container
COPY .env .env

# Set environment
ENV VIRTUAL_ENV=/app/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV PORT=8000

# Expose port and run server
EXPOSE ${PORT}
CMD ["gunicorn", "--bind", ":8000", "--workers", "2", "django_project.wsgi"]
