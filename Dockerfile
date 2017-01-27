FROM centos:latest

RUN yum update -y
RUN yum install -y epel-release
RUN yum install -y wget bzip2

ADD ["www/", "www/"]
ADD ["solver/", "solver/"]
ADD ["setup/crawlr_config", "crawlr_config"]
ADD ["setup/config_env", "config_env"]
ADD ["setup/start_env", "start_env"]
ADD ["run.py", "run.py"]
ADD ["setup/setup.py", "setup.py"]
ADD ["data_collection/urls.txt", "urls.txt"]

RUN ./crawlr_config
RUN source ./config_env
EXPOSE 8002

CMD ["/usr/bin/python3.5", "run.py"]
