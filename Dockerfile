FROM centos:latest

RUN yum update -y
RUN yum install -y epel-release
RUN yum install -y wget bzip2

ADD ["crawlrProject/", "crawlrProject/"]
ADD ["solver/", "crawlrProject/solver/"]
ADD ["www/bounds.py", "crawlrProject/bounds.py"]
ADD ["setup/crawlr_config", "crawlr_config"]
ADD ["setup/config_env", "config_env"]
ADD ["setup/setup.py", "setup.py"]
ADD ["data_collection/urls.txt", "urls.txt"]

RUN ./crawlr_config
RUN source ./config_env
RUN cd crawlrProject && /usr/bin/python3.5 manage.py collectstatic && cd -
EXPOSE 8002

CMD ["/usr/bin/python3.5", "crawlrProject/manage.py", "runserver", "0.0.0.0:8000"]
