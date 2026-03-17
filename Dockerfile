FROM python:3.11

WORKDIR /app

COPY . .

RUN pip install groq python-dotenv

CMD ["python","main.py"]