FROM python:3.12
ADD . /
WORKDIR /
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple \
  && pip install -r requirements.txt

# should edit /etc/apt/sources.list.d/debian.sources on debian:12 in python:3.12 docker image
RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list.d/debian.sources \
  && sed -i 's/security.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list.d/debian.sources \
  && apt-get update \
  && apt-get install -y \
  && apt-get install poppler-utils -y
EXPOSE 5000
CMD ["python", "app.py"]
