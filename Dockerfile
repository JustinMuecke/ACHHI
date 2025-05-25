FROM python:3.9

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

COPY . /app
ENV PYTHONUNBUFFERED=1
CMD ["python3", "/app/src/bot.py"]