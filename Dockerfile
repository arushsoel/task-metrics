FROM python:3.12-slim

WORKDIR /opt/app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
ENV PYTHONUNBUFFERED=1

# Allow overriding the listen port via $PORT
EXPOSE 8080
ENTRYPOINT ["python", "app.py"]
