FROM node:16-alpine

WORKDIR /app

COPY ./public /app/public
COPY ./package.json /app/package.json

RUN npm install

EXPOSE 3000

CMD ["npx", "serve", "-s", "public", "-l", "3000"]