FROM centos:latest

RUN yum update -y

ADD ["data_collection.py", "data_collection.py"]
ADD ["keys.py", "keys.py"]
ADD ["server.py", "server.py"]
ADD ["data_config", "data_config"]
RUN ./data_config

CMD ["/usr/bin/python3.5", "server.py"]
