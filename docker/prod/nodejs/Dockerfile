FROM node:12.2.0 as node
MAINTAINER Dongbox <sfreebobo@163.com>

RUN npm install -g @vue/cli@4.3.1 --registry=https://registry.npm.taobao.org

WORKDIR /code
COPY frontend/package.json /code/
RUN npm install --registry=https://registry.npm.taobao.org
#ENV PATH="/code/node_modules/.bin:$PATH"
COPY frontend/ /code
RUN npm run build
# nginx
FROM nginx:1.13.12-alpine
#ARG NODE_ENV
COPY docker/prod/nodejs/nginx_production.conf /etc/nginx/conf.d/default.conf
COPY --from=node /code/dist /usr/share/nginx/html
# delete moddule
RUN rm -rf node_module

