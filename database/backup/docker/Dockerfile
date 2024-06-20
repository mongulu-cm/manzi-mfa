FROM arm32v7/ubuntu:20.04

ENV TZ=Europe/Minsk
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update -y && \
    apt-get install -y mysql-client awscli

CMD ["/bin/bash"]
