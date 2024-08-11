FROM node:lts-alpine

WORKDIR /frontend

# install simple http server for serving static content
RUN npm install -g http-server && npm i vue-loader

# copy both 'package.json' and 'package-lock.json' (if available)
COPY frontend/package*.json ./

# install project dependencies
RUN npm install

# copy project files and folders to the current working directory (i.e. 'app' folder)
COPY frontend .

# build app for production with minification
RUN npm run build

EXPOSE 8001
# CMD [ "http-server", "dist", "-a", "0.0.0.0", "-p", "8001" ]
CMD [ "npm", "run", "start" ]