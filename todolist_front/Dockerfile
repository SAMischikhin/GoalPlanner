FROM node:12.20.0-alpine as build
WORKDIR /app
COPY package*.json ./
RUN npm install -g npm@7.24.0
RUN npm i
COPY . ./
RUN npm run build
CMD npm run start
