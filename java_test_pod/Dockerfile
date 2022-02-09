FROM adoptopenjdk/openjdk11-openj9:alpine
COPY ./for_docker /java_files
RUN ["javac","-d", "./", "/java_files/HelloWorld.java", "/java_files/EchoServer.java"]
RUN echo 'about to build jar'
RUN ["jar", "-cvfm", "HelloWorld.jar", "/java_files/manifest.MF", "/hello_world/HelloWorld.class", "/hello_world/EchoServer.class"]


FROM adoptopenjdk/openjdk11-openj9:alpine-jre
COPY --from=0 /HelloWorld.jar ./
ENTRYPOINT ["java", "-jar", "HelloWorld.jar", "1111"]

