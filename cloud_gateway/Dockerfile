FROM openjdk:21-jdk

WORKDIR app/
ARG JAR_FILE=target/*.jar
#ARG CONFIG_FOLDER=config
#COPY $CONFIG_FOLDER .
COPY $JAR_FILE .

CMD ["java", "-Xms128m", "-Xmx256m", "-jar", "cloud_gateway.jar"]
