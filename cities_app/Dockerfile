FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    postgresql-client \
    postgis pkg-config libcairo2-dev \
    libsystemd-dev libgirepository1.0-dev \
    libpython3-dev libdbus-1-dev netcat-traditional
    # && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

RUN pip install "cython<3.0.0" wheel; pip install "pyyaml==5.4.1" --no-build-isolation
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install flask

ENV PYTHONUNBUFFERED=1

EXPOSE 5000

# CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"]
# python -m flask run --host=0.0.0.0 --port=5000
# CMD ["python3", "cities_app/app.py"]