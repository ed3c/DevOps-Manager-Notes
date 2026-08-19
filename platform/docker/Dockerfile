FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN groupadd --system app && useradd --system --gid app --create-home app

WORKDIR /app
COPY platform/app /app/platform/app
RUN python -m pip install --no-cache-dir /app/platform/app

USER app
EXPOSE 8000

CMD ["uvicorn", "manager_demo.main:app", "--host", "0.0.0.0", "--port", "8000"]
