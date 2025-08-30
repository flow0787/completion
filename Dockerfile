# build
FROM python:3.9-slim as builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# package
FROM python:3.9-slim as prod

RUN useradd appuser

WORKDIR /app

COPY --from=builder /root/.local /root/.local
COPY --chown=appuser:appuser app.py .
COPY --chown=appuser:appuser requirements.txt .

USER appuser

EXPOSE 5500

ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:5500", "app:app"]