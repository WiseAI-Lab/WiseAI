FROM node:12.2.0
LABEL AUHOTR="Dongbox <sfreebobo@163.com>"  

RUN npm install -g @vue/cli@4.3.1 --registry=https://registry.npm.taobao.org

WORKDIR /code
COPY frontend/package.json /code/

RUN npm install --registry=https://registry.npm.taobao.org

COPY frontend/ /code/

CMD ["npm","run", "dev"]


