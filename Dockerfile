FROM python:3.12-alpine AS base

RUN apk add python3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 80
CMD ["uvicorn", "demo:app", "--host", "0.0.0.0", "--port", "80"]