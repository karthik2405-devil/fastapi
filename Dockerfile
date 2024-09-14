FROM python:3.10.0

WORKDIR /usr/src/app

COPY requirements.txt .
# .  # Copy requirements.txt to the current directory in the container

RUN pip install --no-cache-dir -r requirements.txt  # Install dependencies without caching

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]  

