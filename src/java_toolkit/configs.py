##### PATHS ####
"""
    JDK_PATH is the path our docker image stores the jdk. if you would like to change this you also will have to update
    your dockerfile. For multiple jdk versions you will need a different JDK_PATH for each one.

    LOCAL_MOUNT_PATH is the path the jdk will be temporary saved on to your pod
"""
JDK_PATH= "/app/openjdk"
LOCAL_MOUNT_PATH= "/mnt/robusta"

##### JDK COMMANDS####
"""
    they need the variable {jdk_path} in the command
    if it requires a pid add it in the {pid} field
    any flags the command needs add to the command itself
    
"""
JMAP_CMD= "{jdk_path}/bin/jmap -histo:live {pid}"
JSTACK_CMD= "{jdk_path}/bin/jstack -l {pid}"
