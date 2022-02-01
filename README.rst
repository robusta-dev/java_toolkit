How to support your specific jdk
\\\\
In your docker image copy the jdk  to /app in your dockerfile
////
update JDK_NAME, JDK_PATH and to your updated jdk folder name
/////
if needed change the flags JSTACK_CMD and JMAP_CMD - sometimes they need to be run in a specific way or from a specific file
like 'jhsdb jmap --pid ...'