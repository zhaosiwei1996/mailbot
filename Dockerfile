# 使用轻量级 Python 基础镜像
FROM python:3.13-alpine3.20
WORKDIR /export/servers/mailbot
ADD main.py main.py
ADD config.py config.py
ADD libs libs
ADD api api
ADD requirements.txt requirements.txt
RUN mkdir -p tmp
RUN ls -al
RUN pip3 install --no-cache-dir -r requirements.txt
ENTRYPOINT ["python", "main.py"]
