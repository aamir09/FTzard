FROM nvidia/cuda:11.7.1-base-ubi8


RUN yum install -y curl 
RUN curl -fsSL https://pixi.sh/install.sh | sh
RUN '/home/aamir/FTzard/.Trash-0'

EXPOSE 8080 8081 5000 8888

ENTRYPOINT ["bin/sh"]