How to support your specific jdk
\\\\
| In your docker image copy the jdk  to /app/openjdk in your dockerfile
| for example 'COPY --from=openjdk:11.0.14-jdk /usr/local/openjdk-11  /app/openjdk'

| If needed change the flags of the jdk commands in the config.py file.
| Sometimes jdk commands need to be run in a specific way or from a specific file
| for example ``jhsdb jmap --pid ...``

| example commands
| ``java-toolkit jmap PID_HERE``
| ``java-toolkit jstack PID_HERE``

| For building you can use skaffold
| For running on Google Cloud we have a faster build with skaffold
| ``skaffold run -p gcloud-build``
|
| For additional manual testing with the JDK there are additional bash commands added from additional_bash_commands.sh
| example usages:
| first assign environment variable of the pid you want to debug:
|           ``PID=1234``
| push the jdk onto the pod:
|            ``push_jdk``
| open a shell to the pod namespace and run whatever commands you want:
|           ``podns_shell``
| after you exit the interactive shell, remove the jdk from pod:
|           ``cleanup``