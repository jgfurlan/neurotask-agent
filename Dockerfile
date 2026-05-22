FROM python:3.12-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml .
COPY ocean_cortex_agent/ ./ocean_cortex_agent/
RUN pip install --no-cache-dir --user .

FROM python:3.12-slim AS runner

WORKDIR /app

COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

COPY ocean_cortex_agent/ /app/ocean_cortex_agent/

EXPOSE 8000

CMD ["uvicorn", "ocean_cortex_agent.main:app", "--host", "0.0.0.0", "--port", "8000"]
