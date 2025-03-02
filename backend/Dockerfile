FROM python:3.9

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./app /app/app

COPY ./entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
FROM node:16-alpine

WORKDIR /app

COPY ./public /app/public
COPY ./package.json /app/package.json

RUN npm install

EXPOSE 3000

CMD ["npx", "serve", "-s", "public", "-l", "3000"]