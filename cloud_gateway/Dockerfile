FROM ubuntu

WORKDIR /
ARG JAR_FILE=target/*.jar
#ARG CONFIG_FOLDER=config
#COPY $CONFIG_FOLDER .
COPY $JAR_FILE .

RUN apt-get update && apt-get install -y \
    openjdk-21-jdk \
    net-tools \
    iputils-ping \
    iproute2 \
    curl \
    telnet \
    keepalived \
    vim

CMD ["java", "-Xms128m", "-Xmx256m", "-jar", "cloud_gateway.jar"]
