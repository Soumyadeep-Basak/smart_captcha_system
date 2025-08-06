# Dockerfile for Python Selenium bot

FROM python:3.9-slim

WORKDIR /bot

COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "form_bot.py"]
