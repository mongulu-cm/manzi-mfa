FROM arm32v7/ubuntu:24.04

ENV TZ=Europe/Paris
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update -y && \
    apt-get install -y mysql-client postgresql-client curl  python3-pip && \
    pip install s4cmd --break-system-packages

CMD ["/bin/bash"]
