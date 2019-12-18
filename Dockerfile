# 生成 wotpython 镜像 命令`docker build -f ./Dockerfile -t wotpython .`

FROM python

MAINTAINER chaochaokeji<chaochaokeji@aliyun.com>

WORKDIR /app

VOLUME /app

RUN pip install requests

RUN pip install beautifulsoup4

RUN pip install pymongo

CMD python -u main.py