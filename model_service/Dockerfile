FROM python:3.11-slim AS builder

WORKDIR /app/
COPY ./requirements.txt /app/

RUN python -m venv venv/ &&  \
    venv/bin/pip install --root-user-action=ignore --no-cache-dir --disable-pip-version-check -r requirements.txt

FROM python:3.11-slim AS runner

ENV PATH="/app/venv/bin:$PATH"

WORKDIR /app/
COPY --from=builder /app/venv/ venv/
COPY / /app/

CMD ["python", "main.py"]