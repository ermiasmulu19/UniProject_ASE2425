FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE 1  
ENV PYTHONUNBUFFERED 1        

WORKDIR /playerservice

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /playerservice/
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /playerservice/

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8003"]