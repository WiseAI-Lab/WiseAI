FROM python:3.7.7

ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code
ADD requirements/django.txt /code/

RUN pip install -r django.txt -i https://mirrors.bfsu.edu.cn/pypi/web/simple

ADD . /code

CMD ["./docker/wait-for-it.sh", "db:5432", "--", "sh", "/code/docker/dev/django/container-start.sh"]