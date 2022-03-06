FROM alpine

RUN apk add nodejs npm

WORKDIR /app
COPY . .
RUN npm install
RUN npm run build
RUN npm install -g serve

CMD serve -l 10002 -s build