FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /proyecto

RUN apt-get update \
    && apt-get install -y --no-install-recommends libfreetype6 fontconfig \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY outputs ./outputs
COPY README.md .

EXPOSE 8000

CMD ["python", "app/web.py"]
