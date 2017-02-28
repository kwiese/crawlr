FROM centos:latest

RUN yum update -y && \
yum install -y epel-release && \
yum install -y wget bzip2 gcc gcc-c++ nginx && \
yum -y install https://centos7.iuscommunity.org/ius-release.rpm && \
yum install -y python35u.x86_64 python35u-devel.x86_64 python35u-pip.noarch && \
/usr/bin/pip3.5 install Django && \
/usr/bin/pip3.5 install uwsgi && \
/usr/bin/pip3.5 install requests && \
/usr/bin/pip3.5 install grequests && \
/usr/bin/pip3.5 install googlemaps && \
/usr/bin/pip3.5 install asyncio && \
/usr/bin/pip3.5 install python-dateutil && \
/usr/bin/pip3.5 install redis && \
/usr/bin/pip3.5 install Cython && \
/usr/bin/pip3.5 install gunicorn && \
/usr/bin/pip3.5 install PyMySQL

ADD ["setup/nginx.conf", "nginx.conf"]
ADD ["nginx.conf", "nginx/nginx.conf"]

RUN mkdir /etc/nginx/sites-enabled && \
ln -s /nginx/nginx.conf /etc/nginx/sites-enabled/ && \
mv nginx.conf /etc/nginx/ && \
mkdir /var/log/crawlr && \
touch /var/log/crawlr/crawlr.log && \
mkdir /var/log/nginx_logs && \
touch /var/log/nginx_logs/error.log

ADD ["setup/setup.py", "setup.py"]

RUN /usr/bin/wget http://packages.gurobi.com/7.0/gurobi7.0.1_linux64.tar.gz && \
mv gurobi7.0.1_linux64.tar.gz /opt/ && \
/bin/tar xzvf /opt/gurobi7.0.1_linux64.tar.gz -C /opt/ && \
rm /opt/gurobi7.0.1_linux64.tar.gz && \
rm /opt/gurobi701/linux64/setup.py && \
cp setup.py /opt/gurobi701/linux64/ && \
/usr/bin/python3.5 /opt/gurobi701/linux64/setup.py install && \
/usr/bin/wget http://files.gurobi.com/cloud/libaes70.so.bz2 && \
/usr/bin/bzip2 -d libaes70.so.bz2 && \
chmod 755 libaes70.so && \
rm /opt/gurobi701/linux64/lib/libaes70.so && \
mv libaes70.so /opt/gurobi701/linux64/lib/

ADD ["crawlrProject/", "crawlrProject/"]
ADD ["solver/", "crawlrProject/solver/"]
ADD ["fastcode/", "crawlrProject/solver/fastcode/"]
RUN cd crawlrProject/solver/fastcode && /usr/bin/python3.5 setup.py build_ext --inplace && cd -

ADD ["www/bounds.py", "crawlrProject/bounds.py"]
ADD ["data_collection/host_url.txt", "crawlrProject/logurl.txt"]
ADD ["data_collection/host_url.txt", "crawlrProject/crawlr/logurl.txt"]
ADD ["www_crawlr_tech.crt", "www_crawlr_tech.crt"]
ADD ["www_crawlr_tech.key", "www_crawlr_tech.key"]
ADD ["uwsgi_params", "uwsgi_params"]

EXPOSE 443
EXPOSE 80
CMD ["gunicorn", "crawlrProject.wsgi"]

#CMD ["uwsgi", "--socket", "/tmp/uwsgi.sock", "--chdir", "/crawlrProject", "--module", "crawlrProject.wsgi", "--chmod-socket=664"]
