FROM centos:latest

RUN yum update -y && \
yum -y install https://centos7.iuscommunity.org/ius-release.rpm && \
yum install -y python35u.x86_64 python35u-devel.x86_64 python35u-pip.noarch && \
/usr/bin/pip3.5 install flask && \
/usr/bin/pip3.5 install googlemaps && \
/usr/bin/pip3.5 install asyncio && \
/usr/bin/pip3.5 install grequests && \
/usr/bin/pip3.5 install python-dateutil && \
mkdir /var/log/crawlr && \
touch /var/log/crawlr/crawlr.log

ADD ["data_collection.py", "data_collection.py"]
ADD ["keys.py", "keys.py"]
ADD ["server.py", "server.py"]
ADD ["log.py", "log.py"]
ADD ["host_url.txt", "logurl.txt"]

EXPOSE 80

CMD ["/usr/bin/python3.5", "server.py"]
