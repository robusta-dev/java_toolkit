import subprocess
import typer

KNOWN_NSENTER_ERRORS=\
{
    "reassociate to namespace 'ns/mnt' failed",
    "reassociate to namespace 'ns/user' failed"
}
KNOWN_ERROR_MESSAGE ="Java-toolkit does not support the current cluster type.\n" \
                     " If the cluster type is not minikube or kind please contact the robusta team!"

def check_for_known_error(output: str):
    for known_error in KNOWN_NSENTER_ERRORS:
        if known_error in output:
            return KNOWN_ERROR_MESSAGE
    return output

def run_command(cmd: str, verbose: bool):
    if verbose:
        typer.echo(f"Running {cmd}")
    output = subprocess.check_output(
        cmd, shell=True, stdin=subprocess.PIPE, stderr=subprocess.STDOUT)
    if verbose:
        typer.echo(f"output recieved: \n{output.decode()}")
    return output.decode()

def run_cmd_in_proc_namespace(pid: int, command_to_run: str, verbose: bool):
    nsenter_cmd = f"nsenter -t {pid} -a {command_to_run}"
    output = run_command(nsenter_cmd, verbose)
    return check_for_known_error(output)