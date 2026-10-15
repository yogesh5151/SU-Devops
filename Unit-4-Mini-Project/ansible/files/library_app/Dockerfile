FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

RUN mkdir -p /data \
    && useradd --create-home appuser \
    && chown -R appuser:appuser /app /data

USER appuser

EXPOSE 5000

CMD ["python", "app.py"]
