# Using an ARM32 Ubuntu base image
FROM arm32v7/ubuntu:20.04

ENV TZ=Europe/Minsk
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Set the working directory in the container
WORKDIR /usr/src/app

# Install dependencies required for building Python
RUN apt-get update -y && apt-get install -y \
    wget \
    build-essential \
    libffi-dev \
    libgdbm-dev \
    libc6-dev \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    libncursesw5-dev \
    xz-utils \
    tk-dev \
    libxml2-dev \
    libxmlsec1-dev \
    liblzma-dev \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Download and install Python 3.11
RUN wget --no-check-certificate https://www.python.org/ftp/python/3.11.0/Python-3.11.0.tar.xz 

RUN tar -xf Python-3.11.0.tar.xz \
    && cd Python-3.11.0 \
    && ./configure --enable-optimizations \
    && make -j 4 \
    && make altinstall
# Copy the current directory contents into the container at /usr/src/app
COPY . /usr/src/app

# Install pip for Python 3.11
RUN wget https://bootstrap.pypa.io/get-pip.py \
    && python3.11 get-pip.py

# Install any needed packages specified in requirements.txt
RUN pip3.11 install --no-cache-dir -r requirements.txt

# Set python3.11 as the default python
RUN update-alternatives --install /usr/bin/python python /usr/local/bin/python3.11 1 \
    && update-alternatives --install /usr/bin/pip pip /usr/local/bin/pip3.11 1

# Run script when the container launches
CMD ["python3.11", "your_script.py"]
