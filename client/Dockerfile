FROM node:16-alpine

WORKDIR /app

COPY client/package.json client/package-lock.json ./

RUN npm install

COPY client ./

EXPOSE 8080

CMD ["npm", "run", "dev"]
