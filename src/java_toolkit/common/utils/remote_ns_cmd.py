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
            return True
    return False

def run_command(cmd: str, verbose: bool):
    if verbose:
        typer.echo(f"Running {cmd}")
    result = subprocess.run(
        cmd, shell=True, capture_output=True)
    if verbose:
        typer.echo(f"output recieved: \n{result.stdout}")
    if result.stderr or result.returncode != 0:
        if check_for_known_error(result.stderr.decode()):
            return KNOWN_ERROR_MESSAGE
        raise subprocess.CalledProcessError(
            returncode=result.returncode,
            cmd=result.args,
            output=result.stderr
        )
    return result.stdout.decode()

def run_cmd_in_proc_namespace(pid: int, command_to_run: str, verbose: bool):
    nsenter_cmd = f"nsenter -t {pid} -a {command_to_run}"
    return run_command(nsenter_cmd, verbose)