FROM tiangolo/uvicorn-gunicorn:python3.11

RUN mkdir -p /app
WORKDIR /app
COPY . .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

ENV HOST 0.0.0.0
EXPOSE 8080
