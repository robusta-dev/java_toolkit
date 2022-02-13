import subprocess
import typer


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
    return run_command(nsenter_cmd, verbose)