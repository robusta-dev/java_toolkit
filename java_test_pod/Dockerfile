FROM openjdk:11.0.14-jdk
COPY ./for_docker /java_files
RUN ["javac","-d", "./", "/java_files/HelloWorld.java", "/java_files/EchoServer.java"]
RUN echo 'about to build jar'
RUN ["jar", "-cvfm", "HelloWorld.jar", "/java_files/manifest.MF", "/hello_world/HelloWorld.class", "/hello_world/EchoServer.class"]


FROM openjdk:11.0.14-jre
COPY --from=0 /HelloWorld.jar ./
ENTRYPOINT ["java", "-jar", "HelloWorld.jar", "1111"]

