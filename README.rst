How to support your specific jdk
\\\\
| In your docker image copy the jdk  to /app/openjdk in your dockerfile
| for example 'COPY --from=openjdk:11.0.14-jdk /usr/local/openjdk-11  /app/openjdk'

| If needed change the flags of the jdk commands in the config.py file.
| Sometimes jdk commands need to be run in a specific way or from a specific file
| for example 'jhsdb jmap --pid ...

| example commands
| 'java-toolkit jmap PID_HERE'
| 'java-toolkit jstack PID_HERE'