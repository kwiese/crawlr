FROM centos:latest

RUN yum update -y
RUN yum install -y epel-release
RUN yum install -y nodejs
RUN yum install -y npm
RUN npm install -y express

ADD ["www/", "www/"]
ADD ["solver/", "solver/"]
ADD ["data_collection/", "data_collection"]
ADD ["setup/crawlr_config", "crawlr_config"]
ADD ["run.py", "run.py"]
RUN ./crawlr_config
EXPOSE 8002

CMD ["/usr/bin/python3.5", "run.py"]
