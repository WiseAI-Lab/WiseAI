FROM python:3.7.5

ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code
ADD wise_agent_web/requirements.txt /code/

RUN pip install -r requirements.txt -i http://pypi.douban.com/simple --trusted-host pypi.douban.com

ADD . /code

CMD ["sh", "/code/docker/prod/django/container-start.sh"]