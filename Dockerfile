# ---------- Stage 1: "builder" ----------
# Install dependencies here. This stage is thrown away afterwards,
# so build tools never end up in the final image.
FROM python:3.12-slim AS builder

WORKDIR /build
COPY requirements.txt .
# --prefix=/install puts packages in one folder we can copy later
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# ---------- Stage 2: "runtime" ----------
# The small image that actually runs.
FROM python:3.12-slim

# Don't run as root inside the container (basic security practice)
RUN useradd --create-home appuser

WORKDIR /app

# Copy only the installed packages from the builder stage
COPY --from=builder /install /usr/local

# Copy the app code last: code changes often, so Docker can reuse
# the cached layers above and rebuild faster.
COPY app.py .

ENV APP_VERSION=1.0.0
USER appuser
EXPOSE 5000

# gunicorn is a production server (Flask's built-in one is for development only)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]
