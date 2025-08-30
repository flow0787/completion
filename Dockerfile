# build
FROM python:3.9-slim as builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --user --no-cache-dir -r requirements.txt

# package
FROM python:3.9-slim as prod

RUN useradd appuser

WORKDIR /app

COPY --from=builder /root/.local /home/appuser/.local
COPY --chown=appuser:appuser app.py .
COPY --chown=appuser:appuser requirements.txt .

ENV PATH=/home/appuser/.local/bin:$PATH \
    PYTHONPATH=/home/appuser/.local/lib/python3.9/site-packages:$PYTHONPATH

USER appuser

EXPOSE 5500

ENTRYPOINT ["python", "-m", "gunicorn", "-b", "0.0.0.0:5500", "app:app"]